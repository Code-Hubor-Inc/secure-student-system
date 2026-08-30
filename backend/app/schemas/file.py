from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    file_size: int
    content_type: Optional[str] = None
    created_at: datetime
