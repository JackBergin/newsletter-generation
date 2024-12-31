from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ..utils.api_utils import ApiUtils
import os
from dotenv import load_dotenv

app = FastAPI()

# Add CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://sandbox01.ddns.net:3000",
        "https://sandbox01.ddns.net:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_utils = ApiUtils()

@app.post("/youtube/generate")
async def generate_youtube_summary(video_url: str):
    """Generate a summary for a YouTube video"""
    try:
        result = api_utils.generate_video_summary(video_url)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/youtube/download/{video_id}")
async def download_youtube_summary(video_id: str):
    """Download the generated YouTube summary"""
    file_path = f"./generated/youtube/youtube_summary_{video_id}.md"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Summary not found")
    return FileResponse(file_path, filename=f"youtube_summary_{video_id}.md")

@app.post("/reddit/generate")
async def generate_reddit_summary(subreddit: str):
    """Generate a summary for a subreddit"""
    try:
        result = api_utils.generate_reddit_summary(subreddit)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reddit/download")
async def download_reddit_summary(subreddit: str, date: str):
    """Download the generated Reddit summary"""
    file_path = f"./generated/{date}/reddit_summary_{subreddit}.md"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Summary not found")
    return FileResponse(file_path, filename=f"reddit_summary_{subreddit}.md")