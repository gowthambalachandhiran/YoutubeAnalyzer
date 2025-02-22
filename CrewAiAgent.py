# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:58:42 2025

@author: USER
"""
import os
import google.generativeai as genai

class CrewAIAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_response(self, query, context):
        prompt = f"""
        Given the following context extracted from YouTube channel data:
        {context}
        Answer the following user query concisely:
        {query}
        """
        
        response = self.model.generate_content(prompt)
        return response.text if response else "I'm unable to generate a response."
