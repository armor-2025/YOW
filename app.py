from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from creator_endpoints import router as creator_router

app = FastAPI(title="Wardrobe Creator API")

# CORS
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
