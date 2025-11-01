from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from creator_endpoints import router as creator_router
from database import Base, engine
from creator_models import CreatorPost, PostProduct

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
