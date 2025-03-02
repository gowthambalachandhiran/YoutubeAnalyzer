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
import io  # Add this import at the top with other imports
import plotly.graph_objects as go

# New agent classes
class AnalysisAgent:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")
        
    
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
        4. Monetization tips
        """
        
        response = self.model.generate_content(prompt)
        return response.text if response else "I'm unable to generate an analysis response."

class BIAgent:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")
        
    
    def generate_visualizations(self, query, context, data_json):
        """Generate visualizations based on the data"""
        # Process the data for visualization
        df_videos = self.extract_video_data(data_json)
        
        # Create visualizations based on the query
        figures = []
        
        
        
        # Default visualizations if data is available
        if not df_videos.empty:
            try:
                # 1. Views distribution
                if "viewCount" in df_videos.columns and "title" in df_videos.columns:
                    df_sorted = df_videos.sort_values("viewCount", ascending=False)
                    show_count = min(10, len(df_sorted))  # Show at most 10 videos
                    
                    fig1 = px.bar(
                        df_sorted.head(show_count),
                        x="title", y="viewCount",
                        title=f"Top {show_count} Videos by View Count",
                        labels={"viewCount": "Views", "title": "Video Title"}
                    )
                    fig1.update_layout(xaxis_tickangle=-45)
                    figures.append(fig1)
                    
                    
                # 2. Engagement metrics comparison
                if all(col in df_videos.columns for col in ["viewCount", "likeCount"]):
                    if "commentCount" in df_videos.columns:
                        fig2 = px.scatter(
                            df_videos, x="viewCount", y="likeCount", size="commentCount",
                            hover_data=["title"],
                            title="Engagement Metrics Comparison",
                            labels={"viewCount": "Views", "likeCount": "Likes", "commentCount": "Comments"}
                        )
                    else:
                        # Alternative if commentCount is not available
                        fig2 = px.scatter(
                            df_videos, x="viewCount", y="likeCount",
                            hover_data=["title"],
                            title="Views vs. Likes",
                            labels={"viewCount": "Views", "likeCount": "Likes"}
                        )
                    figures.append(fig2)
                    
                    
                # 3. Timeline of video performance
                if "publishedAt" in df_videos.columns and "viewCount" in df_videos.columns:
                    # Make sure publishedAt is datetime
                    if not pd.api.types.is_datetime64_any_dtype(df_videos["publishedAt"]):
                        df_videos["publishedAt"] = pd.to_datetime(df_videos["publishedAt"])
                    
                    df_time = df_videos.sort_values("publishedAt")
                    fig3 = px.line(
                        df_time, 
                        x="publishedAt", y="viewCount", 
                        markers=True,
                        title="Video Performance Over Time",
                        labels={"publishedAt": "Publication Date", "viewCount": "Views"}
                    )
                    figures.append(fig3)
                    
                    
                # 4. Like/View Ratio (NEW)
                if "viewCount" in df_videos.columns and "likeCount" in df_videos.columns:
                    # Calculate like/view ratio
                    df_videos["likeViewRatio"] = (df_videos["likeCount"] / df_videos["viewCount"] * 100).round(2)
                    df_ratio = df_videos.sort_values("likeViewRatio", ascending=False)
                    
                    show_count = min(10, len(df_ratio))
                    fig4 = px.bar(
                        df_ratio.head(show_count),
                        x="title", y="likeViewRatio",
                        title=f"Top {show_count} Videos by Like/View Ratio (%)",
                        labels={"likeViewRatio": "Like/View Ratio (%)", "title": "Video Title"}
                    )
                    fig4.update_layout(xaxis_tickangle=-45)
                    figures.append(fig4)
                    
                    
                # 5. Comment Engagement (NEW)
                if "viewCount" in df_videos.columns and "commentCount" in df_videos.columns:
                    # Calculate comments per view (in percentage)
                    df_videos["commentRate"] = (df_videos["commentCount"] / df_videos["viewCount"] * 100).round(2)
                    df_comments = df_videos.sort_values("commentRate", ascending=False)
                    
                    show_count = min(10, len(df_comments))
                    fig5 = px.bar(
                        df_comments.head(show_count),
                        x="title", y="commentRate",
                        title=f"Top {show_count} Videos by Comment Rate (%)",
                        labels={"commentRate": "Comments per 100 Views", "title": "Video Title"}
                    )
                    fig5.update_layout(xaxis_tickangle=-45)
                    figures.append(fig5)
                    
                    
            except Exception as e:
                st.error(f"Error creating visualizations: {e}")
                st.exception(e)
        
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
        4. Colorful visualization
        5.Eye catching trends
        Focus on extracting actionable business intelligence insights.
        """
        
        response = self.model.generate_content(prompt)
        return response.text if response else "Unable to generate a summary."
    
    def extract_video_data(self, data_json):
        """Extract and process video data for visualization"""
        try:
            videos = []
            
            # Debug: Print data structure
            #st.write("Data keys:", list(data_json.keys()) if isinstance(data_json, dict) else "Not a dictionary")
            
            if isinstance(data_json, dict) and "channel_videos" in data_json:
                channel_videos = data_json["channel_videos"]
                
                # Extra debug to see the actual type and structure
                
                
                # If channel_videos is directly a list
                if isinstance(channel_videos, list):
                    # Process each video in the list
                    for video_item in channel_videos:
                        video = {}
                        # Extract available fields - adjust these paths based on the actual structure
                        if isinstance(video_item, dict):
                            # Extract title and publishedAt if available
                            if "snippet" in video_item:
                                video["title"] = video_item["snippet"].get("title", "Unknown")
                                video["publishedAt"] = video_item["snippet"].get("publishedAt", "")
                            
                            # Extract statistics if available
                            if "statistics" in video_item:
                                video["viewCount"] = int(video_item["statistics"].get("viewCount", 0))
                                video["likeCount"] = int(video_item["statistics"].get("likeCount", 0))
                                video["commentCount"] = int(video_item["statistics"].get("commentCount", 0))
                            
                            videos.append(video)
                # If it's a dictionary with items
                elif isinstance(channel_videos, dict) and "items" in channel_videos:
                    for item in channel_videos["items"]:
                        video = {
                            "title": item.get("snippet", {}).get("title", "Unknown"),
                            "publishedAt": item.get("snippet", {}).get("publishedAt", ""),
                        }
                        
                        # Add statistics if available
                        if "statistics" in item:
                            video["viewCount"] = int(item["statistics"].get("viewCount", 0))
                            video["likeCount"] = int(item["statistics"].get("likeCount", 0))
                            video["commentCount"] = int(item["statistics"].get("commentCount", 0))
                        
                        videos.append(video)
                
                # # Add debug output to show what we've extracted
                # st.write(f"Extracted {len(videos)} video records")
                # if videos:
                #     st.write("Sample video structure:", videos[0])
            
            # Convert to DataFrame
            df = pd.DataFrame(videos)
            
            # if not df.empty:
            #     st.write("DataFrame info:")
            #     buffer = io.StringIO()
            #     df.info(buf=buffer)
            #     st.text(buffer.getvalue())
                
                
            
            
            
            # Convert date strings to datetime objects
            if "publishedAt" in df.columns and not df.empty:
                df["publishedAt"] = pd.to_datetime(df["publishedAt"])
            
            return df
        except Exception as e:
            st.error(f"Error preprocessing data: {e}")
            st.exception(e)
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
            # st.subheader("Summary Insights")
            # st.markdown(summary)
            
            # Get visualizations from BI agent
            st.subheader("Visualizations")
            figures = bi_agent.generate_visualizations(query, context, st.session_state.channel_data)
            for fig in figures:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.write("### Retrieved Context:")
        st.json(context)  # Show retrieved context for debugging