from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import ollama
import chromadb


# Load the document
loader = TextLoader(
    "data/sample.txt",
    encoding="utf-8"
)

documents = loader.load()

# Splitting the document into chunks
splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=300,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# Creating the embeddings
embeddings = []

for i, doc in enumerate(docs):

    response = ollama.embed(
        model="nomic-embed-text",
        input=doc.page_content
    )

    embedding = response["embeddings"][0]

    embeddings.append(
        (
            f"doc_{i}",
            doc.page_content,
            embedding,
            doc.metadata
        )
    )

# Creating an ChromaDB client
client = chromadb.Client()

collection = client.get_or_create_collection(
    name="Document"
)

# Storing the documents and embeddings
for doc_id, content, embedding, metadata in embeddings:

    collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata]
    )

# Asking the user for a query
query = input("Enter your search query: ")

# Converts the query into an embedding
query_embedding = ollama.embed(
    model="nomic-embed-text",
    input=query
)["embeddings"][0]


# Performing the similarity search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)


# Displaying the top relevant results
print("\nRelevant results:\n")

for i, result in enumerate(results["documents"][0], start=1):

    print(f"Result {i}:")
    print(result)
    print()