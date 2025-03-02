# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:55:59 2025
@author: USER
"""
import streamlit as st
from YouTubeFetcher import YouTubeDataFetcher
from vectorDbHandler import VectorDBHandler
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# New agent classes
class AnalysisAgent:
    def __init__(self):
        import google.generativeai as genai
        self.model = genai.GenerativeModel("gemini-pro")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def analyze_data(self, query, context):
        prompt = f"""
        Given the following context extracted from YouTube channel data:
        {context}
        
        Provide a detailed analysis that answers the following user query:
        {query}
        
        Structure your response with:
        1. Direct answer to the query
        2. Key insights and patterns
        3. Actionable recommendations based on the data
        """
        
        response = self.model.generate_content(prompt)
        return response.text if response else "I'm unable to generate an analysis response."

class BIAgent:
    def __init__(self):
        import google.generativeai as genai
        self.model = genai.GenerativeModel("gemini-pro")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def generate_visualizations(self, query, context, data_json):
        # Process the data for visualization
        df_videos = self.extract_video_data(data_json)
        
        # Create visualizations based on the query
        figures = []
        
        # Default visualizations if data is available
        if not df_videos.empty:
            # 1. Views distribution
            fig1 = px.bar(
                df_videos.sort_values("viewCount", ascending=False).head(10),
                x="title", y="viewCount",
                title="Top 10 Videos by View Count",
                labels={"viewCount": "Views", "title": "Video Title"}
            )
            fig1.update_layout(xaxis_tickangle=-45)
            figures.append(fig1)
            
            # 2. Engagement metrics comparison
            if all(col in df_videos.columns for col in ["likeCount", "commentCount"]):
                fig2 = px.scatter(
                    df_videos, x="viewCount", y="likeCount", size="commentCount",
                    hover_data=["title"],
                    title="Engagement Metrics Comparison",
                    labels={"viewCount": "Views", "likeCount": "Likes", "commentCount": "Comments"}
                )
                figures.append(fig2)
                
            # 3. Timeline of video performance
            if "publishedAt" in df_videos.columns:
                fig3 = px.line(
                    df_videos.sort_values("publishedAt"), 
                    x="publishedAt", y="viewCount", 
                    markers=True,
                    title="Video Performance Over Time",
                    labels={"publishedAt": "Publication Date", "viewCount": "Views"}
                )
                figures.append(fig3)
                
            # Generate query-specific visualization prompt
            viz_prompt = f"""
            Given this YouTube analytics query: "{query}"
            
            What specific visualization would be most helpful to answer this? 
            
            Return ONLY executable Python code using Plotly that creates a relevant 
            visualization for this specific query. The code should work with this 
            DataFrame structure: {df_videos.columns.tolist()}
            """
            
            try:
                # Try to generate custom visualization based on query
                response = self.model.generate_content(viz_prompt)
                if response:
                    custom_viz_code = response.text
                    # Create a local namespace for execution
                    local_vars = {
                        "pd": pd, 
                        "px": px, 
                        "go": go,
                        "df": df_videos
                    }
                    # Execute the visualization code
                    exec(custom_viz_code, globals(), local_vars)
                    # If a figure was created, add it
                    if 'fig' in local_vars:
                        figures.append(local_vars['fig'])
            except Exception as e:
                # If custom viz fails, continue with default visualizations
                pass
                
        return figures
    
    def generate_summary(self, query, context):
        prompt = f"""
        Given the following context extracted from YouTube channel data:
        {context}
        
        And the user query:
        {query}
        
        Provide a concise summary highlighting:
        1. Key metrics and trends
        2. Notable patterns
        3. Brief recommendations
        
        Focus on extracting actionable business intelligence insights.
        """
        
        response = self.model.generate_content(prompt)
        return response.text if response else "Unable to generate a summary."
    
    def extract_video_data(self, data_json):
        """Extract and process video data for visualization"""
        try:
            videos = []
            if "channel_videos" in data_json and "items" in data_json["channel_videos"]:
                for item in data_json["channel_videos"]["items"]:
                    video = {
                        "title": item.get("snippet", {}).get("title", "Unknown"),
                        "publishedAt": item.get("snippet", {}).get("publishedAt", ""),
                        "viewCount": int(item.get("statistics", {}).get("viewCount", 0)),
                        "likeCount": int(item.get("statistics", {}).get("likeCount", 0)),
                        "commentCount": int(item.get("statistics", {}).get("commentCount", 0))
                    }
                    videos.append(video)
            
            # Convert to DataFrame
            df = pd.DataFrame(videos)
            
            # Convert date strings to datetime objects
            if "publishedAt" in df.columns and not df.empty:
                df["publishedAt"] = pd.to_datetime(df["publishedAt"])
            
            return df
        except Exception as e:
            st.error(f"Error preprocessing data: {e}")
            return pd.DataFrame()


# Load environment variables
dotenv_path = os.path.join("..", ".env")
load_dotenv(dotenv_path=dotenv_path)

# Initialize handlers
yt_fetcher = YouTubeDataFetcher()
vector_db = VectorDBHandler()
analysis_agent = AnalysisAgent()  # New analysis agent
bi_agent = BIAgent()  # New BI agent

# Session state initialization
if 'channel_data' not in st.session_state:
    st.session_state.channel_data = None

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
            
            # Store data in session state
            st.session_state.channel_data = all_data
            
            # Display basic channel info
            if "items" in channel_details and channel_details["items"]:
                channel_info = channel_details["items"][0]
                st.subheader(channel_info.get("snippet", {}).get("title", "Channel"))
                
                # Display metrics
                stats = channel_info.get("statistics", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Subscribers", f"{int(stats.get('subscriberCount', 0)):,}")
                with col2:
                    st.metric("Videos", f"{int(stats.get('videoCount', 0)):,}")
                with col3:
                    st.metric("Total Views", f"{int(stats.get('viewCount', 0)):,}")
            
            st.success("Data fetched successfully!")
            
            # Step 2: Store in VectorDB
            with st.spinner("Storing data in VectorDB..."):
                vector_db.replace_data(all_data)
                st.success("Data stored in VectorDB!")
        else:
            st.error("No channel found or API error occurred.")

# Step 3: User inputs query
query = st.text_input("Ask a question about this channel:")
if query and st.session_state.channel_data:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Text Analysis", "Visualizations", "Raw Context"])
    
    # Get context from VectorDB
    context = vector_db.query_context(query)
    
    with tab1:
        with st.spinner("Generating analysis..."):
            # Get analysis from the analysis agent
            analysis = analysis_agent.analyze_data(query, context)
            st.markdown(analysis)
    
    with tab2:
        with st.spinner("Creating visualizations..."):
            # Get summary from BI agent
            summary = bi_agent.generate_summary(query, context)
            st.subheader("Summary Insights")
            st.markdown(summary)
            
            # Get visualizations from BI agent
            st.subheader("Visualizations")
            figures = bi_agent.generate_visualizations(query, context, st.session_state.channel_data)
            for fig in figures:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.write("### Retrieved Context:")
        st.json(context)  # Show retrieved context for debugging