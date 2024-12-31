import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# YouTube Data API key
API_KEY = os.getenv('YOUTUBE_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3/'

logger = logging.getLogger(__name__)

class YoutubeScraperUtils():
    def __init__(self):
        self.today = datetime.now().strftime('%Y%m%d')
        self.base_path = "./generated/youtube"
        self.daily_path = os.path.join(self.base_path, self.today)
        
        # Create directories if they don't exist
        os.makedirs(self.daily_path, exist_ok=True)
    
    def get_latest_videos(self, channel_id):
        """Get latest videos from a channel"""
        if not channel_id:
            return []

        # Calculate the current time and 24 hours ago
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        yesterday_rfc3339 = yesterday.isoformat("T") + "Z"

        # First get video IDs and basic info
        search_endpoint = f"{BASE_URL}search"
        search_params = {
            'part': 'snippet',
            'channelId': channel_id,
            'order': 'date',
            'maxResults': 5,
            'type': 'video',
            'publishedAfter': yesterday_rfc3339,
            'key': API_KEY
        }

        try:
            response = requests.get(search_endpoint, search_params)
            data = response.json()

            if 'items' not in data:
                logger.warning(f"No videos found for channel {channel_id}")
                return []

            videos = []
            for item in data['items']:
                # Check if video has captions
                if self.has_captions(item['id']['videoId']):
                    video_info = {
                        'video_name': item['snippet']['title'],
                        'video_id': item['id']['videoId'],
                        'published_at': datetime.strptime(
                            item['snippet']['publishedAt'], 
                            '%Y-%m-%dT%H:%M:%SZ'
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        'description': item['snippet']['description']
                    }
                    videos.append(video_info)
                    logger.info(f"Found video with captions: {video_info['video_name']}")
                else:
                    logger.info(f"Skipping video without captions: {item['snippet']['title']}")

            return videos

        except Exception as e:
            logger.error(f"Error fetching videos for channel {channel_id}: {e}")
            return []

    def has_captions(self, video_id):
        """Check if a video has captions available"""
        captions_endpoint = f"{BASE_URL}captions"
        params = {
            'part': 'snippet',
            'videoId': video_id,
            'key': API_KEY
        }
        
        try:
            response = requests.get(captions_endpoint, params=params)
            data = response.json()
            has_captions = 'items' in data and len(data['items']) > 0
            return has_captions
        except Exception as e:
            logger.error(f"Error checking captions for video {video_id}: {e}")
            return False

    def get_channel_id(self, username):
        """Get channel ID from username/handle"""
        # Remove @ symbol if present
        # clean_username = username.replace('@', '')
        
        # First try getting channel by handle
        endpoint = f"{BASE_URL}channels"
        params = {
            'part': 'id,snippet',
            'forHandle': username,
            'key': API_KEY
        }

        try:
            response = requests.get(endpoint, params=params)
            data = response.json()

            if 'items' in data and len(data['items']) > 0:
                channel_id = data['items'][0]['id']
                logger.info(f"Found channel ID for {username}: {channel_id}")
                return channel_id

            # If handle search fails, try searching by username
            endpoint = f"{BASE_URL}search"
            params = {
                'part': 'snippet',
                'q': username,
                'type': 'channel',
                'maxResults': 1,
                'key': API_KEY
            }

            response = requests.get(endpoint, params=params)
            data = response.json()

            if 'items' in data and len(data['items']) > 0:
                channel_id = data['items'][0]['snippet']['channelId']
                logger.info(f"Found channel ID for {username}: {channel_id}")
                return channel_id
            else:
                logger.warning(f"No channel found for {username}")
                return None

        except Exception as e:
            logger.error(f"Error finding channel ID for {username}: {e}")
            return None