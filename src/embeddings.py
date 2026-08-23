from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def encode(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )