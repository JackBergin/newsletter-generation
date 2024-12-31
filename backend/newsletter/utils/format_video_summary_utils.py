import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import markdown
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class FormatVideoSummaryUtils():
    def __init__(self, video_id, base_path, file_name):
        self.video_id = video_id
        self.file_name = file_name
        
        # Set up paths - don't add date to base_path as it's already included
        self.daily_path = base_path  # Remove the date append since it's already in base_path
        self.md_path = os.path.join(self.daily_path, f"{file_name}.md")
        self.html_path = os.path.join(self.daily_path, f"{file_name}.html")
        self.transcript_path = os.path.join(self.daily_path, f"{file_name}_transcript.md")
        
        # Get transcript
        self.transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
    def convert_data_to_text(self):
        """Convert transcript to clean text and save raw transcript"""
        clean_text = ""
        raw_transcript = "# Raw Transcript\n\n"
        
        for dp in self.transcript:
            clean_text += str(dp['text']) + ' '
            timestamp = str(datetime.utcfromtimestamp(dp['start']).strftime('%H:%M:%S'))
            raw_transcript += f"[{timestamp}] {dp['text']}\n"
        
        # Save raw transcript
        with open(self.transcript_path, 'w', encoding='utf-8') as f:
            f.write(raw_transcript)
        
        self.text = clean_text

    def summarize_text(self):
        """Generate summary using OpenAI"""
        client = OpenAI(api_key=OPENAI_API_KEY)

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"""As Jordan, a seasoned crypto journalist and market analyst, create a comprehensive newsletter section from this video summary:

{self.text}

Format the report in markdown with the following sections:

# {self.file_name}

## Key Takeaways
- [Bullet points of 3-4 main points from the video]

## Market Analysis
### Current Market Conditions
[Analyze the current market state, including:]
- Overall market sentiment
- Key price levels discussed
- Technical analysis insights
- Macro factors affecting the market

### Cryptocurrency Deep Dive
[For each cryptocurrency mentioned:]
- Current price analysis
- Support/resistance levels
- Short-term and long-term predictions
- Risk factors

## Trading Opportunities
### Potential Setups
- Entry points
- Stop loss levels
- Take profit targets
- Risk/reward ratios

## Risk Assessment
- Market risks
- Technical warnings
- Regulatory concerns
- Other potential headwinds

## Expert Opinion
[Your professional analysis including:]
- Market direction probability
- Confidence level in predictions
- Alternative scenarios to consider
- Time horizon for predictions

## Actionable Steps
1. [Specific action items for traders/investors]
2. [Key levels to watch]
3. [Risk management suggestions]

## Market Sentiment Gauge
**Short Term (1-4 weeks):**
- Bullish/Bearish Rating: [1-10]
- Key Catalysts:
  - [List main factors]

**Medium Term (1-6 months):**
- Bullish/Bearish Rating: [1-10]
- Key Catalysts:
  - [List main factors]

---
*Disclaimer: This summary is for informational purposes only and should not be considered as financial advice.*"""
            }],
            temperature=0.7,
            model="gpt-3.5-turbo-16k",
        )

        self.summary = chat_completion.choices[0].message.content

    def write_response_to_text(self):
        """Save summary to markdown file"""
        with open(self.md_path, 'w', encoding='utf-8') as file:
            file.write(self.summary)

    def md_to_html(self):
        """Convert markdown to HTML with navigation"""
        with open(self.md_path, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
            
        html_content = markdown.markdown(md_content)
        
        # Create daily index if it doesn't exist
        self.create_daily_index()
        
        html_template = f'''
        <html>
        <head>
            <title>{self.file_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; max-width: 1200px; margin: 0 auto; }}
                nav {{ margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; }}
                nav a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
                nav a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <nav>
                <a href="/index.html">Home</a>
                <a href="index.html">Today's Summaries</a>
                <a href="{os.path.basename(self.transcript_path)}">View Transcript</a>
            </nav>
            {html_content}
        </body>
        </html>
        '''
        
        with open(self.html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)

    def create_daily_index(self):
        """Create index.html for daily summaries"""
        index_path = os.path.join(self.daily_path, 'index.html')
        
        # Get all HTML files except transcripts and index
        html_files = [f for f in os.listdir(self.daily_path) 
                     if f.endswith('.html') and not f.endswith('_transcript.html') 
                     and f != 'index.html']
        
        content = f'''
        <html>
        <head>
            <title>YouTube Summaries - {datetime.now().strftime('%Y-%m-%d')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; max-width: 1200px; margin: 0 auto; }}
                nav {{ margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; }}
                nav a {{ margin-right: 15px; text-decoration: none; color: #007bff; }}
                nav a:hover {{ text-decoration: underline; }}
                .summary-list {{ list-style: none; padding: 0; }}
                .summary-list li {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            <nav>
                <a href="/index.html">Home</a>
            </nav>
            <h1>YouTube Summaries - {datetime.now().strftime('%Y-%m-%d')}</h1>
            <ul class="summary-list">
        '''
        
        for html_file in sorted(html_files):
            content += f'<li><a href="{html_file}">{html_file[:-5]}</a></li>\n'
        
        content += '''
            </ul>
        </body>
        </html>
        '''
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)