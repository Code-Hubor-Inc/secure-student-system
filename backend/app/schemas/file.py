from datetime import datetime

from pydantic import BaseModel


class FileOut(BaseModel):
    id: int
    original_filename: str
    file_size: int
    content_type: str | None = None
    expires_at: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True
