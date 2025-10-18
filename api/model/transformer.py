from sentence_transformers import SentenceTransformer


class TransformerModel:
    """
    Transformer model wrapper for sentence embeddings.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the TransformerModel with a specified model name.
        """
        self.model = SentenceTransformer(model_name, device='cpu')

    def encode(self, text: str) -> list[float]:
        """
        Encode a text into its corresponding embedding.
        """
        return self.model.encode(text).tolist()

model = None

def get_transformer_model() -> TransformerModel:
    """
    Singleton pattern to get the TransformerModel instance.
    """
    global model
    if model is None:
        model = TransformerModel()
    return model