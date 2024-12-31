import praw
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class RedditScraperUtils:
    def __init__(self, subreddits):
        # Initialize Reddit client
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        # Subreddits to monitor
        self.subreddits = [subreddits]

    def get_top_posts(self, time_filter='day', limit=10):
        """Get top posts from each subreddit"""
        all_posts = []
        
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                top_posts = subreddit.top(time_filter=time_filter, limit=limit)
                
                for post in top_posts:
                    post_data = {
                        'subreddit': subreddit_name,
                        'title': post.title,
                        'score': post.score,
                        'url': f"https://reddit.com{post.permalink}",
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author),
                        'num_comments': post.num_comments,
                        'selftext': post.selftext,
                        'is_self': post.is_self,
                        'upvote_ratio': post.upvote_ratio
                    }
                    all_posts.append(post_data)
            except Exception as e:
                print(f"Error fetching from r/{subreddit_name}: {e}")
                
        return all_posts

    def get_hot_posts(self, limit=10):
        """Get hot posts from each subreddit"""
        all_posts = []
        
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                hot_posts = subreddit.hot(limit=limit)
                
                for post in hot_posts:
                    if post.stickied:  # Skip stickied posts
                        continue
                    
                    post_data = {
                        'subreddit': subreddit_name,
                        'title': post.title,
                        'score': post.score,
                        'url': f"https://reddit.com{post.permalink}",
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'author': str(post.author),
                        'num_comments': post.num_comments,
                        'selftext': post.selftext,
                        'is_self': post.is_self,
                        'upvote_ratio': post.upvote_ratio
                    }
                    all_posts.append(post_data)
            except Exception as e:
                print(f"Error fetching from r/{subreddit_name}: {e}")
                
        return all_posts 