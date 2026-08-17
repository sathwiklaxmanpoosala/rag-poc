import ollama
from ingest import collection

def search_documents(query):
    response = ollama.embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    return results["documents"][0]