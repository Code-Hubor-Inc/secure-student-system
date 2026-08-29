import os
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File as FastAPIFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.models.audit_log import AuditAction
from app.models.file import File
from app.models.user import User
from app.schemas.file import FileOut
from app.services.audit import log_action
from app.services.encryption import decrypt_file, encrypt_file

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/", response_model=FileOut, status_code=status.HTTP_201_CREATED)
def upload_file(
    request: Request,
    upload: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = upload.file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    ciphertext, encrypted_dek, nonce = encrypt_file(content)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    stored_filename = f"{uuid.uuid4().hex}.enc"
    stored_path = os.path.join(settings.UPLOAD_DIR, stored_filename)
    with open(stored_path, "wb") as f:
        f.write(ciphertext)

    file_record = File(
        user_id=current_user.id,
        institution_id=current_user.institution_id,
        original_filename=upload.filename,
        stored_filename=stored_filename,
        encrypted_dek=encrypted_dek,
        nonce=nonce,
        file_size=len(content),
        content_type=upload.content_type,
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    log_action(
        db,
        user_id=current_user.id,
        action=AuditAction.upload,
        resource_type="file",
        resource_id=file_record.id,
        ip_address=request.client.host if request.client else None,
    )

    return file_record


@router.get("/", response_model=list[FileOut])
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(File).filter(File.user_id == current_user.id).all()


@router.get("/{file_id}")
def download_file(
    file_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_record = db.query(File).filter(File.id == file_id, File.user_id == current_user.id).first()
    if not file_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    if file_record.expires_at and file_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="File has expired")

    stored_path = os.path.join(settings.UPLOAD_DIR, file_record.stored_filename)
    with open(stored_path, "rb") as f:
        ciphertext = f.read()

    plaintext = decrypt_file(ciphertext, file_record.encrypted_dek, file_record.nonce)

    log_action(
        db,
        user_id=current_user.id,
        action=AuditAction.download,
        resource_type="file",
        resource_id=file_record.id,
        ip_address=request.client.host if request.client else None,
    )

    return Response(
        content=plaintext,
        media_type=file_record.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_record.original_filename}"'},
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_record = db.query(File).filter(File.id == file_id, File.user_id == current_user.id).first()
    if not file_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    stored_path = os.path.join(settings.UPLOAD_DIR, file_record.stored_filename)
    if os.path.exists(stored_path):
        os.remove(stored_path)

    db.delete(file_record)
    db.commit()

    log_action(
        db,
        user_id=current_user.id,
        action=AuditAction.delete,
        resource_type="file",
        resource_id=file_id,
        ip_address=request.client.host if request.client else None,
    )
    return None