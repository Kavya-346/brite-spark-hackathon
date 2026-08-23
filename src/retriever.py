import json
import re
from datetime import date
from pathlib import Path

import faiss
import numpy as np

from embeddings import EmbeddingModel


INDEX_PATH = Path("storage/policy.index")
METADATA_PATH = Path("storage/metadata.json")

TOP_K = 5

AMENDMENT_EFFECTIVE_DATE = date(2026, 3, 1)


class PolicyRetriever:

    def __init__(self):
        self.index = faiss.read_index(str(INDEX_PATH))

        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

        self.embedding_model = EmbeddingModel()

    def get_policy_version(self, relevant_date: date) -> str:
        if relevant_date < AMENDMENT_EFFECTIVE_DATE:
            return "Original manual"

        return "Amendment No. 2026-01"

    def search(self, question: str, top_k: int = TOP_K):
        question_embedding = self.embedding_model.encode([question])

        question_embedding = np.asarray(
            question_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            question_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            clause = self.metadata[index].copy()
            clause["score"] = float(score)

            results.append(clause)

        existing_ids = {
            clause["clause_id"]
            for clause in results
        }

        referenced_ids = []

        for clause in results:
            references = re.findall(
                r"§\d+\.\d+\.\d+",
                clause["text"]
            )

            for reference in references:
                if reference not in existing_ids:
                    referenced_ids.append(reference)

        for reference in referenced_ids:
            for clause in self.metadata:
                if clause["clause_id"] == reference:
                    clause_copy = clause.copy()
                    clause_copy["score"] = 0.0
                    results.append(clause_copy)
                    break

        return results