import io
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.models.file import File as FileModel
from app.models.user import User
from app.schemas.file import FileOut
from app.services.audit import log_action
from app.services.encryption import decrypt_file, encrypt_file
from app.services.storage import delete_object, download_object, upload_object

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileOut)
async def upload_file(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = await file.read()
    if len(data) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds maximum allowed size",
        )

    ciphertext, wrapped_dek, nonce = encrypt_file(data)
    storage_key = f"{current_user.id}/{uuid4()}"
    upload_object(storage_key, ciphertext)

    file_row = FileModel(
        user_id=current_user.id,
        original_filename=file.filename,
        storage_key=storage_key,
        encrypted_dek=wrapped_dek,
        nonce=nonce,
        file_size=len(data),
        content_type=file.content_type,
    )
    db.add(file_row)
    db.commit()
    db.refresh(file_row)

    log_action(
        db,
        user_id=current_user.id,
        action="file_upload",
        resource_type="file",
        resource_id=str(file_row.id),
    )

    return file_row


@router.get("/", response_model=list[FileOut])
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(FileModel)
        .filter(FileModel.user_id == current_user.id)
        .order_by(FileModel.created_at.desc())
        .all()
    )


def _get_owned_file(db: Session, file_id: int, current_user: User) -> FileModel:
    file_row = (
        db.query(FileModel)
        .filter(FileModel.id == file_id, FileModel.user_id == current_user.id)
        .first()
    )
    if file_row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return file_row


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_row = _get_owned_file(db, file_id, current_user)

    ciphertext = download_object(file_row.storage_key)
    plaintext = decrypt_file(ciphertext, file_row.encrypted_dek, file_row.nonce)

    log_action(
        db,
        user_id=current_user.id,
        action="file_download",
        resource_type="file",
        resource_id=str(file_row.id),
    )

    return StreamingResponse(
        io.BytesIO(plaintext),
        media_type=file_row.content_type or "application/octet-stream",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{file_row.original_filename}"'
            )
        },
    )


@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_row = _get_owned_file(db, file_id, current_user)

    delete_object(file_row.storage_key)
    db.delete(file_row)
    db.commit()

    log_action(
        db,
        user_id=current_user.id,
        action="file_delete",
        resource_type="file",
        resource_id=str(file_id),
    )

    return {"detail": "File deleted"}
