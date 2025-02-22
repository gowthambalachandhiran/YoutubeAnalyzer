# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:58:42 2025

@author: USER
"""

class CrewAIAgent:
    def __init__(self):
        self.model = "gemini"
    
    def get_response(self, query, context):
        from google.generativeai import configure, generate_text
        configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        prompt = f"""
        Given the following context extracted from YouTube channel data:
        {context}
        Answer the following user query concisely:
        {query}
        """
        
        response = generate_text(prompt=prompt)
        return response.text if response else "I'm unable to generate a response."