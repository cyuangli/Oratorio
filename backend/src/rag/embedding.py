from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.logger import logging

class EmbeddingPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logging.info("Initializing embedding pipeline.")
        self.model = SentenceTransformer(model_name)
        logging.info("Initialized embedding pipeline.")

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        logging.info(f"Generating embeddings for {len(texts)} texts.")
        embeddings = self.model.encode(texts, show_progress_bar=False)
        logging.info(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings
    
