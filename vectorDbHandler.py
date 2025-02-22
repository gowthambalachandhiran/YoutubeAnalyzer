# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:57:57 2025

@author: USER
"""
import faiss
import json
from sentence_transformers import SentenceTransformer

class VectorDBHandler:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # FAISS index for embeddings
        self.text_data = []  # List to store corresponding JSON text

    def store_data(self, json_data):
        """Clears the old index and stores new embeddings with text data."""
        self.index = faiss.IndexFlatL2(384)  # Reset index
        self.text_data = []  # Reset stored text data

        text_data = json.dumps(json_data)
        embedding = self.model.encode([text_data])
        self.index.add(embedding)
        self.text_data.append(text_data)  # Store the actual JSON

    def query_context(self, query):
        """Retrieve relevant context from stored embeddings."""
        if not self.text_data:
            return "No data available in VectorDB."

        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k=1)  # Get best match
        
        best_match = self.text_data[indices[0][0]] if indices[0][0] < len(self.text_data) else "No relevant data found."
        return json.loads(best_match)  # Convert back to dictionary
