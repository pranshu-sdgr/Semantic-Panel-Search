import http
from typing import Any, List

from fastapi import HTTPException
from qdrant_client import QdrantClient, models

COLLECTION_NAME = "movies"

client = None

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client.
    """
    global client
    if client is None:
        client = QdrantClient(host="qdrant", port=6333)
    return client

def get_top_k_similar_movies(embedding: List[float], top_k: int) -> List[models.ScoredPoint]:
    """
    Searches for similar movies in the Qdrant collection based on the provided embedding.
    """
    try:
        client = get_qdrant_client()
        response = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding,
            limit=top_k,
            with_payload=True
        )
    except Exception as e:
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return response
