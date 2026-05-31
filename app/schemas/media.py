from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class MediaAssetBase(BaseModel):
    user_id: UUID4
    original_name: str
    file_size_bytes: int
    mime_type: str
    asset_type: str
    reference_id: Optional[UUID4] = None

class MediaAssetResponse(MediaAssetBase):
    id: UUID4
    s3_key: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
