import http
import tempfile

from fastapi import (APIRouter, BackgroundTasks, File, Form, UploadFile)
from scripts.ingestion import (ingest_custom_dataset_to_vdb)
from scripts.vectors import create_vector_mappings

router = APIRouter()

@router.post("/custom-dataset/")
async def ingest_custom_dataset(
    background_tasks: BackgroundTasks,
    csv_file: UploadFile = File(..., description="CSV file containing the dataset to ingest"),
    collection_name: str = Form(..., description="Name of the collection to store the ingested data"),
    payload_column_str: str = Form(..., description="Name of the column containing the text payloads"),
    embedding_column_str: str = Form(..., description="Name of the column containing the embeddings"),
    batch_size: int = Form(256, description="Batch size for ingestion")
):
    """
    Ingest a custom dataset from an uploaded CSV file into the vector database.
    """

    embedding_columns = [col.strip() for col in embedding_column_str.split(",")]
    payload_column = [col.strip() for col in payload_column_str.split(",")]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="/app/data") as temp_f:
        temp_f.write(await csv_file.read())
        temp_file_path = temp_f.name
    
    background_tasks.add_task(
        ingest_custom_dataset_to_vdb,
        temp_file_path,
        batch_size,
        collection_name,
        payload_column,
        embedding_columns
    )

    return {
        "status": http.HTTPStatus.ACCEPTED,
        "message": "Ingestion started in the background."
    }

@router.post("/local-vector-mapping/create/")
async def create_local_vector_mapping(
    background_tasks: BackgroundTasks,
    source_path: str = Form('/app/data/conversions/dataset.csv', description="Path to the source CSV file"),
    payload_columns: str = Form(..., description="Comma-separated names of the payload columns"),
    embedding_columns: str = Form(..., description="Comma-separated names of the embedding columns"),
    output_path: str = Form('/app/data/vectors/mappings.json', description="Path to save the output vector mappings JSON file")
):
    """
    Create local vector mappings from a CSV file and save to a JSON file.
    """
    payload_cols = [col.strip() for col in payload_columns.split(",")]
    embedding_cols = [col.strip() for col in embedding_columns.split(",")]

    background_tasks.add_task(
        create_vector_mappings,
        source_path,
        payload_cols,
        embedding_cols,
        output_path
    )

    return {
        "status": http.HTTPStatus.ACCEPTED,
        "message": "Vector mapping creation started in the background."
    }