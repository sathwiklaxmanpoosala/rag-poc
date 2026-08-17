from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import ollama
import chromadb


client = chromadb.Client()

collection = client.get_or_create_collection(
    name="Document"
)


def ingest_documents():

    loader = TextLoader(
        "data/sample.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    for i, doc in enumerate(docs):

        response = ollama.embed(
            model="nomic-embed-text",
            input=doc.page_content
        )

        embedding = response["embeddings"][0]

        collection.add(
            ids=[f"doc_{i}"],
            documents=[doc.page_content],
            embeddings=[embedding],
            metadatas=[doc.metadata]
        )

    print("Documents successfully indexed.")