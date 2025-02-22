# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 15:04:00 2025

@author: USER
"""

import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
dotenv_path = os.path.join("..", ".env")

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

class YouTubeDataFetcher:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable not set.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_channels(self, topic: str, max_results: int = 3) -> list:
        request = self.youtube.search().list(
            part='snippet',
            q=topic,
            type='channel',
            maxResults=max_results
        )
        response = request.execute()
        return response

    def search_channel(self, search_query: str) -> dict:
        request = self.youtube.search().list(
            part='snippet',
            q=search_query,
            type='channel',
            maxResults=1
        )
        response = request.execute()
        return response

    def get_channels_details(self, channel_ids: list) -> list:
        channels_data = []
        for i in range(0, len(channel_ids), 50):
            batch = channel_ids[i:i + 50]
            request = self.youtube.channels().list(
                part='snippet,statistics,contentDetails,brandingSettings',
                id=','.join(batch)
            )
            response = request.execute()
            if 'error' in response:
                print(f"Error in get_channel_details: {response['error']}")
                return {}  # Return empty dict to indicate failure
            return response

    def get_channel_details(self, channel_id: str) -> dict:
        request = self.youtube.channels().list(
            part='snippet,statistics,contentDetails,brandingSettings',
            id=channel_id
        )
        response = request.execute()
        return response

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> list:
        channel_details = self.get_channel_details(channel_id)
        if not channel_details or not channel_details.get('items'):
            return []

        print(json.dumps(channel_details, indent=2))  # Print for debugging

        try:
            uploads_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            print(f"Uploads Playlist ID: {uploads_playlist_id}")  # Print for debugging
            return self.get_playlist_videos(uploads_playlist_id, max_results)
        except KeyError as e:
            print(f"KeyError: {e}.  'relatedPlaylists' or 'uploads' key might be missing.")
            return [] # Or handle the error as appropriate

    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> list:
        video_items = []
        next_page_token = None
        results_count = 0

        while results_count < max_results:
            request = self.youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=min(50, max_results - results_count),
                pageToken=next_page_token
            )
            response = request.execute()

            if not response.get('items'):
                break

            video_ids = [item['contentDetails']['videoId'] for item in response['items']]
            video_details = self.get_videos_details(video_ids)
            video_items.extend(video_details)
            results_count += len(response['items'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        return video_items

    def get_videos_details(self, video_ids: list) -> list:
        all_videos = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(batch)
            )
            response = request.execute()
            if response.get('items'):
                all_videos.extend(response['items'])
        return all_videos

    def get_average_video_duration(self, uploads_playlist_id: str) -> dict:
        request = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=50
        )
        response = request.execute()
        return response

    def get_merchandise_info(self, channel_id: str) -> dict:
        request = self.youtube.channels().list(
            part='brandingSettings',
            id=channel_id
        )
        response = request.execute()
        return response


if __name__ == "__main__":
    fetcher = YouTubeDataFetcher()

    search_term = "F1"
    search_response = fetcher.search_channels(search_term)

    if search_response and search_response.get('items'):
        print(f"Top 3 channels for '{search_term}':")
        for i, item in enumerate(search_response['items']):
            channel_title = item['snippet']['title']
            channel_id = item['id']['channelId']
            print(f"{i+1}. {channel_title} (ID: {channel_id})")

            channel_details_response = fetcher.get_channel_details(channel_id)
            print(f"\nDetails for {channel_title}:")
            print(json.dumps(channel_details_response, indent=2))

            videos_response = fetcher.get_channel_videos(channel_id)
            print(f"\nVideos for {channel_title}:")
            print(json.dumps(videos_response, indent=2))

            merch_response = fetcher.get_merchandise_info(channel_id)
            print(f"\nMerchandise Info for {channel_title}:")
            print(json.dumps(merch_response, indent=2))

            if channel_details_response and channel_details_response.get('items'):
                uploads_playlist_id = channel_details_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                average_duration_response = fetcher.get_average_video_duration(uploads_playlist_id)
                print(f"\nAverage Duration Response for {channel_title}:")
                print(json.dumps(average_duration_response, indent=2))

            print("-" * 20)

    else:
        print(f"No channels found for '{search_term}'.")