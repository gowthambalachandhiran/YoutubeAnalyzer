# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:57:07 2025

@author: USER
"""
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
# YouTubeDataFetcher
class YouTubeDataFetcher:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable not set.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def search_channel(self, search_query: str) -> dict:
        request = self.youtube.search().list(
            part='snippet',
            q=search_query,
            type='channel',
            maxResults=1
        )
        response = request.execute()
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

        try:
            uploads_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            return self.get_playlist_videos(uploads_playlist_id, max_results)
        except KeyError:
            return []

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