import http

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from scripts.ingestion import ingest_movies_to_vdb

router = APIRouter()

class IngestRequest(BaseModel):
    csv_file_path: str
    batch_size: int
    collection_name: str

@router.post("/ingest-movies/")
async def ingest_movies(
    request: IngestRequest,
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(
            ingest_movies_to_vdb,
            request.csv_file_path,
            request.batch_size,
            request.collection_name
        )
        return {
            "status": http.HTTPStatus.ACCEPTED,
            "message": "Ingestion started in the background."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))