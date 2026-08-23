from embeddings import EmbeddingModel


model = EmbeddingModel()

texts = [
    "A recipient must report a change of circumstances.",
    "The monthly award is calculated using countable income."
]

embeddings = model.encode(texts)

print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", embeddings.shape[1])
print("First embedding length:", len(embeddings[0]))