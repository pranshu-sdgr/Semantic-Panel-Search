import http
from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import ingest, search

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("INFO:     Starting up application...")

    yield
    # --- Shutdown Logic ---
    print("INFO:     Shutting down application...")


app = FastAPI(
    title="Semantic Panel Search API",
    description="API for searching panels using vector search techniques.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["ingest"])


@app.get("/")
async def root():
    return {
        "status": http.HTTPStatus.OK,
        "message": "Welcome to the Semantic Panel Search API!"
    }
