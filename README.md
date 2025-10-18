# PlotCortex
A place to search movies by there plot.

# Architecture
1. Database: Qdrant vector database to ingest movies data.
2. Backend: Fast API service to request search queries.
3. Vector Embeddings: Sentence Transformer for vector embeddings.

# Run Configurations
1. docker-compose up --build