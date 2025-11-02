from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from creator_endpoints import router as creator_router
from database import Base, engine, SessionLocal, User, get_db
from creator_models import CreatorPost, PostProduct
import uuid
from datetime import datetime, timedelta
import hashlib

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wardrobe Creator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(creator_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Wardrobe Creator API"}

@app.get("/seed-data")
def seed_data(db = Depends(get_db)):
    """Create test user and posts"""
    
    # Check if data already exists
    existing_user = db.query(User).first()
    if existing_user:
        return {"message": "Data already exists", "creator_id": existing_user.id}
    
    # Create test user
    user = User(
        email="test@example.com",
        password_hash=hashlib.sha256("test123".encode()).hexdigest()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    creator_id = user.id
    
    # Sample products
    sample_products = [
        {"name": "Zara Blazer", "brand": "Zara", "price": "$89.99", "image": "https://via.placeholder.com/300x400?text=Blazer"},
        {"name": "Levi's Jeans", "brand": "Levi's", "price": "$98.00", "image": "https://via.placeholder.com/300x400?text=Jeans"},
        {"name": "Nike Sneakers", "brand": "Nike", "price": "$110.00", "image": "https://via.placeholder.com/300x400?text=Sneakers"},
        {"name": "H&M Tee", "brand": "H&M", "price": "$12.99", "image": "https://via.placeholder.com/300x400?text=Tee"},
        {"name": "Mango Bag", "brand": "Mango", "price": "$45.99", "image": "https://via.placeholder.com/300x400?text=Bag"},
    ]
    
    # Create 15 posts
    for i in range(15):
        post_id = str(uuid.uuid4())
        
        product_count = (i % 5) + 3
        
        post = CreatorPost(
            id=post_id,
            creator_id=creator_id,
            image_url=f"https://via.placeholder.com/600x800?text=Post+{i+1}",
            video_url=None if i % 3 != 0 else f"https://via.placeholder.com/video{i+1}.mp4",
            is_video=(i % 3 == 0),
            product_count=product_count,
            caption=f"Fall outfit inspo #{i+1} 🍂✨",
            created_at=datetime.utcnow() - timedelta(days=i),
            likes_count=150 + (i * 20),
            views_count=1000 + (i * 50)
        )
        db.add(post)
        # Add products
        for j in range(product_count):
            product_data = sample_products[j % len(sample_products)]
            product = PostProduct(
                post_id=post_id,
                product_id=str(uuid.uuid4()),
                product_name=product_data["name"],
                product_brand=product_data["brand"],
                product_image=product_data["image"],
                product_price=product_data["price"],
                affiliate_link=f"https://example.com/product/{j}",
                commission_rate=0.10,
                position_x=0.2 + (j * 0.15),
                position_y=0.3 + (j * 0.1)
            )
            db.add(product)
    
    db.commit()
    
    return {
        "message": "Successfully created 15 posts!",
        "creator_id": creator_id,
        "test_url": f"https://wardrobe-api-w0vo.onrender.com/creators/{creator_id}/posts"
    }
