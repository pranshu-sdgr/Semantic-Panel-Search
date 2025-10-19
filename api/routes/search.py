import http
from datetime import datetime

from database import vdao
from fastapi import APIRouter, HTTPException, Query
from model.transformer import get_transformer_model
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = Query(5, description="Number of top similar movies to return")
    collection_name: str = Query("movies", description="Name of the Qdrant collection to search in")

router = APIRouter()

@router.post("/query")
async def search_movies(request: SearchRequest):
    # Placeholder implementation
    start = datetime.now()
    # Here you would add the logic to perform the search using embeddings and vector search
    try:
        transformer = get_transformer_model()
        query_vector = transformer.encode(request.query)
        search_result = vdao.get_top_k_similar_movies(query_vector, top_k=request.top_k, collection_name=request.collection_name)
    except Exception as e:
        raise HTTPException(status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    end = datetime.now()
    response_time = (end - start).total_seconds()
    results = [
            {
                "id": hit.id,
                "score": hit.score,
                "title": hit.payload.get("title"),
                "year": hit.payload.get("year"),
                "genre": hit.payload.get("genre"),
                "actors": hit.payload.get("actors"),
                "description": hit.payload.get("description"),
            }
            for hit in search_result
        ]
    return {
        "results": results,
        "response_time": response_time
    }

@router.post("/custom-query")
async def search_custom_dataset(request: SearchRequest):
    # Placeholder implementation for custom dataset search
    start = datetime.now()
    try:
        transformer = get_transformer_model()
        query_vector = transformer.encode(request.query)
        search_result = vdao.get_top_k_similar_movies(query_vector, top_k=request.top_k, collection_name=request.collection_name)
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