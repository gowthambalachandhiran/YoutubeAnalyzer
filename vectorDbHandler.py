# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:57:57 2025

@author: USER
"""
import faiss
from sentence_transformers import SentenceTransformer
# VectorDBHandler
class VectorDBHandler:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # 384 is the embedding dimension
    
    def store_data(self, json_data):
        text_data = json.dumps(json_data)
        embedding = self.model.encode([text_data])
        self.index.add(embedding)
    
    def query_context(self, query):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k=5)
        return indices.tolist()