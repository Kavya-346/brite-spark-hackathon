import json
from pathlib import Path

import faiss
import numpy as np

from embeddings import EmbeddingModel
from loader import load_policy, extract_clauses


DATA_PATH = "data/policy-manual.md"
STORAGE_DIR = Path("storage")

INDEX_PATH = STORAGE_DIR / "policy.index"
METADATA_PATH = STORAGE_DIR / "metadata.json"


def build_vector_store():
    text = load_policy(DATA_PATH)
    clauses = extract_clauses(text)

    embedding_model = EmbeddingModel()

    texts = [clause["text"] for clause in clauses]

    embeddings = embedding_model.encode(texts)

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    STORAGE_DIR.mkdir(exist_ok=True)

    faiss.write_index(index, str(INDEX_PATH))

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(clauses, file, ensure_ascii=False, indent=2)

    print("Vector store created successfully.")
    print("Clauses indexed:", len(clauses))
    print("Embedding dimensions:", dimension)
    print("Index:", INDEX_PATH)
    print("Metadata:", METADATA_PATH)


if __name__ == "__main__":
    build_vector_store()