import os
import uuid

import pandas as pd
from database import vdao
from model.transformer import get_transformer_model
from qdrant_client import models

def ingest_custom_dataset_to_vdb(csv_file_path, batch_size, collection_name, payload_columns, embedding_columns):
    """
    Ingests a custom dataset from a CSV file into the Qdrant vector database and processes specified columns for embeddings and payloads.
    """
    print("Initializing model and client...")
    transformer = get_transformer_model()
    client = vdao.get_qdrant_client()

    print(f"Creating collection {collection_name} in Qdrant...")
    vector_size = transformer.getModel().get_sentence_embedding_dimension()
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        )
    )

    print(f"Loading data from {csv_file_path}...")
    df = pd.read_csv(csv_file_path)

    print(f"Starting ingestion of {len(df)} records...")
    for i in range(0, len(df), batch_size):
        batch_size_df = df.iloc[i:i + batch_size]
        # Combine embedding columns into a single text for embedding generation
        # If column is null, convert to empty string
        combined_texts = batch_size_df[embedding_columns].fillna('').agg(' '.join, axis=1).tolist()
        embeddings = transformer.getModel().encode(combined_texts, show_progress_bar=False).tolist()
        payloads = batch_size_df[payload_columns].to_dict('records')
        points = [
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload,
            ) for vector, payload in zip(embeddings, payloads)
        ]
        client.upsert(
            collection_name=collection_name,
            points=points,
            wait=False
        )
        print(f"Ingested batch {i // batch_size + 1} / {(len(df) + batch_size - 1) // batch_size}")

    print("Ingestion completed!")
    os.remove(csv_file_path)  # Clean up temporary file
    print(f"Temporary file {csv_file_path} removed.")