import uuid
from sqlalchemy import Column, String, BigInteger, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class AssetType(enum.Enum):
    SCREENSHOT = "screenshot"
    AVATAR = "avatar"
    NEWS_COVER = "news_cover"

class ArticleStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class MediaAsset(Base):
    __tablename__ = "media_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    s3_key = Column(String, nullable=False, unique=True)
    file_size_bytes = Column(BigInteger, nullable=False)
    mime_type = Column(String, nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    reference_id = Column(UUID(as_uuid=True), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(String, nullable=False)
    cover_image_id = Column(UUID(as_uuid=True), ForeignKey("media_assets.id"), nullable=True)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.DRAFT)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    cover_image = relationship("MediaAsset")
