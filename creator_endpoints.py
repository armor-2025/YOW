from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

from database import get_db, User
from creator_models import CreatorPost, PostProduct

router = APIRouter(prefix="/creators", tags=["creators"])

class PostProductResponse(BaseModel):
    id: int
    product_id: str
    product_name: str
    product_brand: Optional[str]
    product_image: str
    product_price: str
    affiliate_link: str
    commission_rate: float
    position_x: Optional[float]
    position_y: Optional[float]
    
    class Config:
        from_attributes = True

class CreatorPostResponse(BaseModel):
    id: str
    creator_id: Union[int, str]  # Accept both types
    image_url: str
    video_url: Optional[str]
    is_video: bool
    product_count: int
    caption: Optional[str]
    created_at: datetime
    likes_count: int
    views_count: int
    products: List[PostProductResponse] = []
    
    class Config:
        from_attributes = True

class PostsListResponse(BaseModel):
    posts: List[CreatorPostResponse]
    total_count: int
    has_more: bool

@router.get("/{creator_id}/posts", response_model=PostsListResponse)
def get_creator_posts(
    creator_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get posts for a specific creator"""
    total_count = db.query(CreatorPost).filter(
        CreatorPost.creator_id == creator_id
    ).count()
    
    posts = db.query(CreatorPost).filter(
        CreatorPost.creator_id == creator_id
    ).order_by(
        CreatorPost.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    has_more = (offset + limit) < total_count
    
    return {
        "posts": posts,
        "total_count": total_count,
        "has_more": has_more
    }
