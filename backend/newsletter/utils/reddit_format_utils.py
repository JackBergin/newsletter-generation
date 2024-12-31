import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RedditFormatUtils:
    def __init__(self, posts, base_path="./generated/reddit", file_name="reddit_summary"):
        self.posts = posts
        self.today = datetime.now().strftime('%Y%m%d')
        self.daily_path = os.path.join(base_path, self.today)
        self.md_path = os.path.join(self.daily_path, f"{file_name}.md")
        
        # Create directories if they don't exist
        os.makedirs(self.daily_path, exist_ok=True)
        
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def summarize_posts(self):
        """Generate a summary of the Reddit posts using GPT"""
        # Prepare posts for summarization
        posts_text = "\n\n".join([
            f"Subreddit: r/{post['subreddit']}\n"
            f"Title: {post['title']}\n"
            f"Score: {post['score']}\n"
            f"Comments: {post['num_comments']}\n"
            f"Content: {post['selftext'][:500]}..."
            for post in self.posts
        ])

        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"""As a crypto analyst, create a summary of these Reddit posts:

{posts_text}

Format the report in markdown:

# Reddit Crypto Pulse - {datetime.now().strftime('%Y-%m-%d')}

## Community Sentiment Overview
[Analyze overall community sentiment and main topics of discussion]

## Top Discussions by Subreddit
[Break down key discussions by subreddit]

## Trending Topics
- [Topic 1]
- [Topic 2]
- [Topic 3]

## Notable Insights
[Key insights from the discussions]

## Market Sentiment
- Overall Sentiment: [Positive/Neutral/Negative]
- Key Concerns:
- Bullish Signals:
- Bearish Signals:

---
*This is a summary of community discussions and should not be considered as financial advice.*
"""
            }],
            temperature=0.7,
            model="gpt-3.5-turbo-16k",
        )
        
        self.summary = response.choices[0].message.content

    def create_raw_digest(self):
        """Create a raw digest of all posts"""
        content = f"# Reddit Crypto Posts - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for post in sorted(self.posts, key=lambda x: x['score'], reverse=True):
            content += f"## {post['title']}\n\n"
            content += f"- Subreddit: r/{post['subreddit']}\n"
            content += f"- Score: {post['score']}\n"
            content += f"- Comments: {post['num_comments']}\n"
            content += f"- Posted by: u/{post['author']}\n"
            content += f"- URL: {post['url']}\n"
            if post['selftext']:
                content += f"\n{post['selftext'][:500]}...\n"
            content += "\n---\n\n"
            
        self.raw_digest = content

    def save_files(self):
        """Save both the summary and raw digest"""
        # Save the AI summary
        with open(self.md_path, 'w', encoding='utf-8') as f:
            f.write(self.summary)
            
        # Save the raw digest
        raw_digest_path = os.path.join(self.daily_path, "reddit_raw_digest.md")
        with open(raw_digest_path, 'w', encoding='utf-8') as f:
            f.write(self.raw_digest)