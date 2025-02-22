# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:55:59 2025

@author: USER
"""

import streamlit as st
from YouTubeFetcher import YouTubeDataFetcher
from vectorDbHandler import VectorDBHandler
from CrewAiAgent import CrewAIAgent
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json

# Load environment variables
dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path=dotenv_path)

# Initialize handlers
yt_fetcher = YouTubeDataFetcher()
vector_db = VectorDBHandler()
crew_agent = CrewAIAgent()

# Streamlit UI
st.title("YouTube Channel Insights Agent")

# Step 1: User inputs channel name
channel_name = st.text_input("Enter YouTube Channel Name:")

if st.button("Fetch Data"):
    with st.spinner("Fetching channel data..."):
        search_results = yt_fetcher.search_channel(channel_name)
        if search_results and search_results.get('items'):
            channel_id = search_results['items'][0]['id']['channelId']
            
            channel_details = yt_fetcher.get_channel_details(channel_id)
            channel_videos = yt_fetcher.get_channel_videos(channel_id, max_results=10)
            
            all_data = {
                "channel_details": channel_details,
                "channel_videos": channel_videos
            }
            
            st.success("Data fetched successfully!")
            st.json(all_data)  # Show fetched JSON data
            
            # Step 2: Store in VectorDB
            with st.spinner("Storing data in VectorDB..."):
                vector_db.replace_data(all_data)
                st.success("Data stored in VectorDB!")

# Step 3: User inputs query
query = st.text_input("Ask a question about this channel:")
if query:
    with st.spinner("Fetching insights..."):
        context = vector_db.query_context(query)
        st.write("### Retrieved Context:")
        st.json(context)  # Show retrieved context for debugging

        response = crew_agent.get_response(query, context)
        st.write("### Agent Response:")
        st.write(response)
