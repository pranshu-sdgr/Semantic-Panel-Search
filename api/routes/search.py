import http
from datetime import datetime

from database import vdao
from fastapi import APIRouter, HTTPException, Query
from model.transformer import get_transformer_model
from model.vector_search import search_local_vector_mapping
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = Query(5, description="Number of top similar results to return")
    collection_name: str = Query("panel_dataset", description="Name of the Qdrant collection to search in")

router = APIRouter()

@router.post("/custom-query")
async def search_custom_dataset(request: SearchRequest):
    # Placeholder implementation for custom dataset search
    start = datetime.now()
    try:
        transformer = get_transformer_model()
        query_vector = transformer.encode(request.query)
        search_result = vdao.get_top_k_similar_vectors(query_vector, top_k=request.top_k, collection_name=request.collection_name)
    except Exception as e:
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    end = datetime.now()
    response_time = (end - start).total_seconds()
    results = [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in search_result
        ]
    return {
        "results": results,
        "response_time": response_time
    }

@router.post("/local-vector-mapping/search/")
async def search_local_mapping(
    query: str = Query(..., description="The search query string"),
    local_vectors_path: str = Query('/app/data/vectors/mappings.json', description="Path to the local vector mappings JSON file"),
    top_k: int = Query(5, description="Number of top similar results to return")
):
    """
    Search local vector mappings from a JSON file.
    """
    start = datetime.now()
    try:
        results = search_local_vector_mapping(
            query=query,
            local_vectors_path=local_vectors_path,
            top_k=top_k
        )
    except Exception as e:
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    end = datetime.now()
    response_time = (end - start).total_seconds()
    results['response_time'] = response_time
    return results
