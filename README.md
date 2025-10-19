# PlotCortex
A place to search movies by there plot.

# Architecture
1. Database: Qdrant vector database to ingest movies data.
2. Backend: Fast API service to request search queries.
3. Vector Embeddings: Sentence Transformer for vector embeddings.

# Run Configurations
1. `docker-compose up --build` -> http://0.0.0.0:8000/docs
2. Run the ingest/ingest-movies with /app/data/movies.csv file path to ingest data in Qdrant VDB
3. Once the background tasks finish, user the /search/query endpoint to look for the data.