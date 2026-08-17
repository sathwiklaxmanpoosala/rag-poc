# Data Ingestion and Similarity Search POC

This project is to understand how document ingestion and similarity search work using embeddings and a vector database.

The POC takes a text file, breaks it into smaller chunks, converts the chunks into embeddings using Ollama, stores them in ChromaDB, and then searches for the most relevant chunks based on a user query.

## What this POC does

The flow is:

Text File
↓
Load Document
↓
Split into Chunks
↓
Generate Embeddings
↓
Store in ChromaDB
↓
User Query
↓
Generate Query Embedding
↓
Similarity Search
↓
Return Relevant Results

## Technologies Used

- Python
- LangChain
- Ollama
- ChromaDB
- nomic-embed-text

## Project Structure

rag-poc/
│
├── data/
│   └── sample.txt
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore

## How it works

### 1. Loading the document

The `sample.txt` file is loaded using LangChain's `TextLoader`.

The loaded document contains the actual text along with basic metadata such as the source file.

### 2. Chunking

The document is split into smaller pieces using `CharacterTextSplitter`.

For this POC, the chunk size is set to 300 characters with an overlap of 50 characters.

Chunking is useful because searching smaller sections of a document allows the system to retrieve more specific information.

### 3. Creating embeddings

Each chunk is sent to the Ollama `nomic-embed-text` model.

The model converts the text into a numerical vector representation.

For example:
Text
 ↓
nomic-embed-text
 ↓
[0.02, -0.11, 0.43, ...]

The vectors generated in this POC have 768 dimensions.

### 4. Storing data in ChromaDB

The generated embeddings are stored in a ChromaDB collection along
with the original document content and metadata.

Each stored record contains:

* ID
* Document content
* Embedding
* Metadata

### 5. Searching

When a user enters a query, the query is also converted into an
embedding using the same `nomic-embed-text` model.

The query embedding is then sent to ChromaDB.

ChromaDB compares the query with the stored embeddings and returns the
most relevant chunks.

The current POC retrieves the top 3 results.

## What is similarity search?

Similarity search is used to find content that is related to a query
based on its meaning.

For example, if the document contains information aboutPostgreSQL and
the user asks:

What database is used for structured data?

the system can retrieve the PostgreSQL-related chunk even if the exact
words from the query are not present in the document.

The basic process is:

User Query
    ↓
Query Embedding
    ↓
Compare with Document Embeddings
    ↓
Rank Similar Results
    ↓
Top-K Results

## Current Scope

This POC currently focuses only on the ingestion and retrieval part.

It includes:

* Loading a text file
* Text chunking
* Embedding generation
* ChromaDB storage
* Query embedding
* Similarity search
* Top-K retrieval

It does not currently use an LLM to generate a final answer.

## Future Improvements

Some possible improvements are:

* Add an LLM such as Llama 3.2 to generate answers
* Convert this into a complete RAG pipeline
* Add similarity/distance scores
* Separate ingestion and retrieval into different files
* Add FastAPI
* Support PDF and other document formats
* Add persistent vector storage
* Add a simple UI