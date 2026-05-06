from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.logger import logging
class TextChunker():

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        logging.info("Initializing text chunker.")
        self.text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap,
                            length_function=len,
                            separators=["\n\n", "\n", " ", ""])
        logging.info("Initialized text chunker.")

    def generate_chunks(self, documents: List[str]):
        logging.info("Splitting documents.")
        docs = [Document(page_content=doc) for doc in documents]
        split_docs = self.text_splitter.split_documents(docs)

        texts = [split_doc.page_content for split_doc in split_docs]
        logging.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")
        return texts
        