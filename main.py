from ingest import ingest_documents
from search import search_documents

ingest_documents()

query = input("Enter your search query: ")

results = search_documents(query)

print("\nRelevant results:\n")

for i, result in enumerate(results, start=1):
    print(f"Result {i}:")
    print(result)
    print()