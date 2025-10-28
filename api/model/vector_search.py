import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from model.transformer import get_transformer_model

def search_local_vector_mapping(
    query: str,
    local_vectors_path: str,
    top_k: int = 5,
):
    """
    Search local vector mappings from a JSON file.
    """
    # Load local vector mappings
    df = pd.read_json(local_vectors_path, lines=True)
    embeddings = np.array(df['embedding'].tolist())

    # Generate embedding for the query
    transformer = get_transformer_model()
    query_vector = np.array(transformer.encode(query)).reshape(1, -1)

    # Compute cosine similarities
    similarities = cosine_similarity(query_vector, embeddings).flatten()

    # Get top_k results
    top_k_indices = similarities.argsort()[-top_k:][::-1]
    results = []
    for idx in top_k_indices:
        results.append({
            "id": int(idx),
            "score": float(similarities[idx]),
            "payload": df.iloc[idx]['metadata']
        })

    return {
        "results": results
    }