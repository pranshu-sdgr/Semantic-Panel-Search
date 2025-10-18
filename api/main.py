import http
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from routes import search
from sentence_transformers import SentenceTransformer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("INFO:     Starting up application...")

    yield
    # --- Shutdown Logic ---
    print("INFO:     Shutting down application...")


app = FastAPI(
    title="PlotCortex API",
    description="API for searching movies by their plot using embeddings and vector search.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


@app.get("/")
async def root():
    return {
        "status": http.HTTPStatus.OK,
        "message": "Welcome to the PlotCortex API"
    }
