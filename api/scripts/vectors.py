from model.transformer import get_transformer_model
import pandas as pd

def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding for the given text using the Transformer Model
    """
    model = get_transformer_model()
    return model.encode(text)

def create_vector_mappings(file_path: str, payloads: list[str], ids: list[str], output_path: str):
    """
    Create vector mappings for the database.
    """
    df = pd.read_csv(file_path)
    vector_mappings = []

    for _, row in df.iterrows():
        text = "\n".join([str(row[id]) for id in ids if id in row])
        embedding = generate_embedding(text)
        payload = {
            "embedding": embedding,
            "metadata": {
                key : row[key] for key in payloads if key in row
            }
        }
        vector_mappings.append(payload)

    # store vector mappings to a json file
    wdf = pd.DataFrame(vector_mappings)
    wdf.to_json(output_path, orient='records', lines=True)