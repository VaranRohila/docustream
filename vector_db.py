
import os
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict

class VectorDBClient:
    def __init__(self, collection_name="docustream_index"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embeddings = OpenAIEmbeddings()

    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """
        Embeds and indexes documents in batches.
        """
        # Generate embeddings
        embeddings = self.embeddings.embed_documents(documents)
        
        # Add to Chroma
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Index Stats: {self.collection.count()} documents indexed.")

    def query(self, query_text: str, n_results: int = 3):
        """
        Semantic search against the index.
        """
        query_embedding = self.embeddings.embed_query(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
