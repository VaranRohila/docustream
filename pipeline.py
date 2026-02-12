
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vector_db import VectorDBClient

class IngestionPipeline:
    def __init__(self):
        self.vector_db = VectorDBClient()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_document(self, filename: str, content: str):
        """
        Async task to chunk, embed, and index a document.
        Simulates a heavy background job.
        """
        print(f"Starting ingestion for: {filename}")
        
        # 1. Chunking
        chunks = self.splitter.split_text(content)
        print(f"Split {filename} into {len(chunks)} chunks.")

        # 2. Prepare for Vector DB
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

        # 3. Indexing (Blocking call wrapped in async)
        # In a real Celery worker, this would be the primary task.
        try:
            self.vector_db.add_documents(chunks, metadatas, ids)
            print(f"Successfully indexed {filename}")
            return {"status": "success", "chunks_processed": len(chunks)}
        except Exception as e:
            print(f"Error indexing {filename}: {e}")
            return {"status": "failed", "error": str(e)}
