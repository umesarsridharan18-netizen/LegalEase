from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import CORS_ORIGINS
from backend.routes.routes import router

app = FastAPI(
    title="LegalEase API",
    description="AI-assisted legal document drafting API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "LegalEase",
        "status": "running",
        "message": "LegalEase FastAPI backend is running.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
