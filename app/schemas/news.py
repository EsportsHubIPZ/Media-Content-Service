from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class NewsArticleCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    cover_image_id: Optional[UUID4] = None
    status: str = "draft"

class NewsArticleResponse(NewsArticleCreate):
    id: UUID4
    author_id: UUID4
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
