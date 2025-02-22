# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:57:57 2025

@author: USER
"""
import faiss
import json
import os
import pickle
from sentence_transformers import SentenceTransformer

class VectorDBHandler:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_file = "vector_db.index"
        self.data_file = "vector_db.pkl"
        self.index = faiss.IndexFlatL2(384)
        self.data_store = []
        self.load_index()
    
    def replace_data(self, json_data):
        self.index = faiss.IndexFlatL2(384)
        text_data = json.dumps(json_data)
        embedding = self.model.encode([text_data])
        self.index.add(embedding)
        self.data_store = [text_data]
        self.save_index()
    
    def query_context(self, query):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k=3)
        results = [self.data_store[idx] for idx in indices[0] if idx != -1 and idx < len(self.data_store)]
        return results if results else "No relevant context found."
    
    def save_index(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.data_file, "wb") as f:
            pickle.dump(self.data_store, f)
    
    def load_index(self):
        if os.path.exists(self.index_file) and os.path.exists(self.data_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.data_file, "rb") as f:
                self.data_store = pickle.load(f)