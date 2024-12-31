import requests
import os
from .youtube_format_utils import FormatVideoSummaryUtils
from .reddit_format_utils import RedditFormatUtils
from .reddit_scraper_utils import RedditScraperUtils
import logging
import os
import threading
from datetime import datetime
import argparse
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler("app.log"),
                        logging.StreamHandler()])
logger = logging.getLogger(__name__)

class ApiUtils():

    def __init__ (self):
        # Create base directories if they don't exist
        self.base_path = "./generated"
        os.makedirs(os.path.join(self.base_path, "youtube"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, "reddit"), exist_ok=True)

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        raise ValueError("Invalid YouTube URL")

    def generate_video_summary(self, youtube_url):
        """Generate markdown summary from YouTube video"""
        try:
            video_id = self.extract_video_id(youtube_url)
            file_name = f"youtube_summary_{video_id}"
            base_path = os.path.join(self.base_path, "youtube")
            
            formatter = FormatVideoSummaryUtils(video_id, base_path, file_name)
            formatter.convert_data_to_text()
            formatter.summarize_text()
            formatter.write_response_to_text()
            
            return {
                "status": "success",
                "message": "Summary generated successfully",
                "video_id": video_id,
                "file_path": formatter.md_path
            }
        except Exception as e:
            logger.error(f"Error generating video summary: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def generate_reddit_summary(self, subreddit):
        """Generate markdown summary from Reddit subreddit"""
        try:
            reddit_scraper = RedditScraperUtils(subreddit)
            file_name = f"reddit_summary_{subreddit}"
            
            # Get posts from subreddit
            top_posts = reddit_scraper.get_top_posts(time_filter='day', limit=10)
            hot_posts = reddit_scraper.get_hot_posts(limit=10)
            all_posts = top_posts + hot_posts
            
            # Format and save summary
            reddit_formatter = RedditFormatUtils(all_posts, self.base_path, file_name)
            reddit_formatter.create_raw_digest()
            reddit_formatter.summarize_posts()
            reddit_formatter.save_files()
            
            return {
                "status": "success",
                "message": "Reddit summary generated successfully",
                "subreddit": subreddit,
                "file_path": reddit_formatter.md_path
            }
        except Exception as e:
            logger.error(f"Error processing Reddit content: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

