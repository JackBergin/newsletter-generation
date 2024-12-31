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
            timestamp = str(datetime.fromtimestamp(dp['start'], datetime.UTC).strftime('%H:%M:%S'))
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