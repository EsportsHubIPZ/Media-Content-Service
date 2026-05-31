from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.news import NewsArticleCreate, NewsArticleResponse
import uuid

router = APIRouter()

@router.get("", response_model=List[NewsArticleResponse])
async def list_news(limit: int = 10, offset: int = 0):
    return []

@router.post("", response_model=NewsArticleResponse, status_code=201)
async def create_news(article: NewsArticleCreate):
    return {
        "id": uuid.uuid4(),
        "author_id": uuid.uuid4(),
        "title": article.title,
        "summary": article.summary,
        "content": article.content,
        "cover_image_id": article.cover_image_id,
        "status": article.status,
        "created_at": "2026-05-31T12:00:00Z"
    }
