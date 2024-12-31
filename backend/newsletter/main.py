from .utils.format_video_summary_utils import FormatVideoSummaryUtils
from .utils.youtube_scraper_utils import YoutubeScraperUtils
from .utils.reddit_scraper_utils import RedditScraperUtils
from .utils.reddit_format_utils import RedditFormatUtils
from .utils.html_utils import HTMLUtils
import logging
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from datetime import datetime
import argparse

logging.basicConfig(level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler("app.log"),
                        logging.StreamHandler()])
logger = logging.getLogger(__name__)

class HTMLHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="./generated", **kwargs)
    
    def do_GET(self):
        # Serve root index.html for the root path
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        return super().do_GET()

def start_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTMLHandler)
    logger.info(f"Server started at http://localhost:{port}")
    httpd.serve_forever()

def generate_video_summary(video_id, base_path, file_name):
    try:
        format_video_summary_obj = FormatVideoSummaryUtils(video_id, base_path, file_name)
        format_video_summary_obj.convert_data_to_text()
        format_video_summary_obj.summarize_text()
        format_video_summary_obj.write_response_to_text()
        format_video_summary_obj.md_to_html()
        logger.info(f"Video summary generated successfully for {file_name}")
    except Exception as e:
        if "Could not retrieve a transcript" in str(e):
            logger.info(f"Skipping video {file_name} - No transcript available")
        else:
            logger.error(f"Error generating video summary: {e}")

def process_reddit_content():
    try:
        logger.info("Starting Reddit content processing")
        reddit_scraper = RedditScraperUtils()
        
        top_posts = reddit_scraper.get_top_posts(time_filter='day', limit=10)
        hot_posts = reddit_scraper.get_hot_posts(limit=10)
        all_posts = top_posts + hot_posts
        
        reddit_formatter = RedditFormatUtils(all_posts)
        reddit_formatter.create_raw_digest()
        reddit_formatter.summarize_posts()
        reddit_formatter.save_files()
        logger.info("Reddit content processed successfully")
    except Exception as e:
        logger.error(f"Error processing Reddit content: {e}")

def serve_existing_content(port=8000):
    """Just serve existing HTML content without generating new summaries"""
    if not os.path.exists("./generated"):
        logger.error("No content found in ./generated directory")
        return
    
    HTMLUtils.create_root_index()
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    logger.info("HTTP server started in background")
    
    try:
        while True:
            input("Press Ctrl+C to stop the server...\n")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")

def process_and_serve(port=8000):
    """Full process: generate summaries and serve content"""
    # Create required directories
    os.makedirs("./generated", exist_ok=True)
    os.makedirs("./generated/youtube", exist_ok=True)
    os.makedirs("./generated/reddit", exist_ok=True)
    logger.info("Ensured required directories exist")
    
    try:
        # Process Reddit content
        process_reddit_content()
        
        # Process YouTube content
        youtube_channel_list = ['@AndreiJikh', '@CryptoBanterGroup', '@CoinBureau', '@CryptoCrewUniversity', '@CryptoDaily', '@DataDash', '@IvanOnTech', '@MitchRayTA']  

        
        scraper_obj = YoutubeScraperUtils()
        for channel in youtube_channel_list:
            channel_id = scraper_obj.get_channel_id(channel)
            latest_videos = scraper_obj.get_latest_videos(channel_id)
            if not latest_videos:
                logger.info(f"No new videos with captions from {channel}")
            else:
                logger.info(f"Latest videos with captions from {channel}:")
                for video in latest_videos:
                    file_name = f'({channel})_{video["video_name"]}_{video["published_at"]}'
                    generate_video_summary(video['video_id'], scraper_obj.daily_path, file_name)
        
        # Start the HTTP server in a separate thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        logger.info("HTTP server started in background")    

        # Create/update root index
        HTMLUtils.create_root_index()
        logger.info("Updated root index.html")
        logger.info("All content generated successfully")
        
        # Keep the main thread running
        while True:
            try:
                input("Press Ctrl+C to stop the server...\n")
            except KeyboardInterrupt:
                logger.info("Shutting down server...")
                break
            
    except Exception as e:
        logger.error(f"Error in main process: {e}")

def main():
    parser = argparse.ArgumentParser(description='Crypto Market Intelligence Generator and Server')
    parser.add_argument('--serve-only', action='store_true', 
                       help='Only serve existing content without generating new summaries')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port to run the HTTP server on (default: 8000)')
    args = parser.parse_args()
    
    md_path = "./generated/md"
    html_path = "./generated/html"
    
    if args.serve_only:
        logger.info("Starting in serve-only mode")
        serve_existing_content(args.port)
    else:
        logger.info("Starting full process mode")
        process_and_serve(args.port)

if __name__ == "__main__":
    main()


