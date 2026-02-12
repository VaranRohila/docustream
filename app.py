
import uvicorn
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import asyncio
from pipeline import IngestionPipeline
from vector_db import VectorDBClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DocuStream-RAG-Pipeline", version="1.0.0")
pipeline = IngestionPipeline()
vector_db = VectorDBClient()

# Schemas
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class HealthCheck(BaseModel):
    status: str

# Background Task Wrapper
async def run_ingestion(file_path: str, original_filename: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        print(f"Background: Processing {original_filename}...")
        result = await pipeline.process_document(original_filename, content)
        print(f"Background: Ingestion Complete: {result}")
        
        # Cleanup temp file
        os.remove(file_path)
    except Exception as e:
        print(f"Background Error: {e}")

@app.get("/", response_model=HealthCheck)
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Async endpoint to accept documents for ingestion.
    Offloads processing to a background worker.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files supported for demo.")
        
    temp_file_path = f"temp_{file.filename}"
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Kick off background task
    background_tasks.add_task(run_ingestion, temp_file_path, file.filename)
    
    return {"message": "Document received. Ingestion started in background.", "filename": file.filename}

@app.post("/query")
def query_index(request: QueryRequest):
    """
    Semantic search over the ingested index.
    """
    try:
        results = vector_db.query(request.query, n_results=request.top_k)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
