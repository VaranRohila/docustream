
# 📄 DocuStream-RAG-Pipeline

**High-Throughput Asynchronous Document Ingestion Engine**

## 🚀 Overview
DocuStream is a resilient Data Engineering pipeline designed for Enterprise RAG (Retrieval-Augmented Generation) systems. It solves the "bottleneck problem" of ingesting thousands of documents by decoupling the upload process from the heavy lifting of chunking and embedding. Using an async background worker pattern, it ensures the API remains responsive even under heavy load.

### Business Value
-   **Scalability**: Handles concurrent uploads without blocking the main API thread.
-   **Observability**: Trackable ingestion status for every document.
-   **Modularity**: Vector abstraction layer allows swapping Chroma for Pinecone/Qdrant without code changes.

## 🏗️ Architecture
The system follows a modern Event-Driven/Async architecture:

1.  **FastAPI Gateway**:
    -   Exposes REST endpoints for file upload (`/ingest`) and query (`/query`).
    -   Validates input and saves files to temporary staging.

2.  **Ingestion Worker (Background Task)**:
    -   *Triggered by*: File Upload.
    -   *Step 1*: **Text Splitting**: Recursive chunking (1000 chars) to maintain context.
    -   *Step 2*: **Embedding**: Generates vectors using OpenAI `text-embedding-3-small`.
    -   *Step 3*: **Indexing**: Writes vectors + metadata to ChromaDB.

3.  **Storage Layer**:
    -   **Vector DB**: Chroma (persistent on disk).
    -   **Metadata**: Source filename and chunk index preserved for citation.

## 🛠️ Technical Stack
-   **Framework**: FastAPI (Python)
-   **Async Runtime**: Uvicorn / asyncio
-   **Vector DB**: ChromaDB
-   **Orchestration**: LangChain
-   **Embeddings**: OpenAI

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/DocuStream-RAG-Pipeline.git
    cd DocuStream-RAG-Pipeline
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

4.  **Run the Server**
    ```bash
    uvicorn app:app --reload
    ```
    API will be available at `http://localhost:8000`.

## 🧪 Usage Examples

### 1. Ingest a Document
```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/company_policy.txt"
```
**Response**: `{"message": "Document received...", "filename": "company_policy.txt"}`

### 2. Semantic Search
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the remote work policy?", "top_k": 2}'
```

## 🔮 Future Enhancements
-   Replace local BackgroundTasks with **Celery + Redis** for distributed processing.
-   Add **Dead Letter Queue (DLQ)** for failed ingestion retries.
-   Implement **OCR** (Tesseract/Textract) for PDF/Image support.
