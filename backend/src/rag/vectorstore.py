import os
import sys
import shutil
import faiss
import numpy as np
import pickle
from typing import List, Any
from sentence_transformers import SentenceTransformer
from rag.embedding import EmbeddingPipeline
from rag.chunking import TextChunker
from src.logger import logging
from src.exception import CustomException

class VectorStore:
    def __init__(self, persist_dir: str = "../data/faiss_store", embedding_model: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200):
        logging.info("Initializing vector store.")
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.index = None
        self.metadata = []
        self.faiss_path = os.path.join(self.persist_dir, "faiss.index")
        self.metadata_path = os.path.join(self.persist_dir, "metadata.pkl")
        self.embedding_model = embedding_model
        self.model = SentenceTransformer(self.embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logging.info("Finished loading vector store.")

    def build(self, documents: List[Any]):

        logging.info("Building vector store.")
        embedding_pipeline = EmbeddingPipeline(model_name=self.embedding_model)
        text_chunker = TextChunker(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        texts = text_chunker.generate_chunks(documents=documents)
        embeddings = embedding_pipeline.generate_embeddings(texts=texts)

        self.add(np.array(embeddings).astype("float32"), texts)
        self.save()
        logging.info("Vector store built and saved.")

    
    def add(self, embeddings: np.ndarray, metadatas: List[Any] = None):
        logging.info(f"Adding {embeddings.shape[0]} vectors to Faiss index.")
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings) 
        if metadatas:
            self.metadata.extend(metadatas)
        logging.info(f"Added {embeddings.shape[0]} vectors to Faiss index.")

    def save(self):
        try:
            logging.info("Saving Faiss index and metadata.")
            faiss.write_index(self.index, self.faiss_path)
            with open(self.metadata_path, "wb") as file:
                pickle.dump(self.metadata, file)
            logging.info("Saved Faiss index and metadata.")
        except Exception as e:
            raise CustomException(e,sys)
        
    def delete(self):
        logging.info("Deleting vector store directory.")
        if os.path.exists(self.persist_dir):
            try:
                shutil.rmtree(self.persist_dir)
                logging.info("Deleted vector store directory.")
            except Exception as e:
                raise CustomException(e, sys)
        else:
            logging.info("This vector store's directory has not been initialized.")

    def load(self):
        try:
            logging.info(f"Loading Faiss index and metadata.")
            self.index = faiss.read_index(self.faiss_path)
            with open(self.metadata_path, "rb") as file:
                self.metadata = pickle.load(file)
            logging.info(f"Loaded Faiss index and metadata.")
        except Exception as e:
            raise CustomException(e, sys)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Any]:
        logging.info("Initiating search.")
        if not self.metadata or self.index is None:
            logging.info("Faiss index and metadata are not loaded.")
            return None
        
        D, I = self.index.search(query_embedding, k)
        results = []

        for idx, dist in zip(I[0], D[0]):
            metadata = self.metadata[idx] if idx < len(self.metadata) else None
            results.append({"index" : idx, "distance" : dist, "metadata" : metadata})
        logging.info("Search successful.")
        return results

    
    
    def query(self, query_text: str, k: int = 5) -> List[Any]:
        logging.info(f"Querying vector store for '{query_text}'")
        query_embeddings = self.model.encode([query_text]).astype("float32")
        logging.info(f"Successfully queried vector store for '{query_text}'")
        return self.search(query_embeddings, k)