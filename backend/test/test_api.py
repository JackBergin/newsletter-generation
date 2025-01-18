from fastapi.testclient import TestClient
from newsletter.api.app import app
import pytest
import os

client = TestClient(app)

# ------------------------
# Fixtures
# ------------------------
@pytest.fixture
def sample_video_url():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@pytest.fixture
def sample_subreddit():
    return "programming"

@pytest.fixture
def sample_date():
    return "2024-03-20"

# ------------------------
# YouTube API Tests
# ------------------------
def test_generate_youtube_summary_success(sample_video_url):
    response = client.post("/youtube/generate", params={"video_url": sample_video_url})
    assert response.status_code == 200
    assert "status" in response.json()

def test_generate_youtube_summary_invalid_url():
    response = client.post("/youtube/generate", params={"video_url": "invalid_url"})
    assert response.status_code == 400

def test_generate_youtube_summary_missing_url():
    response = client.post("/youtube/generate")
    assert response.status_code == 422

def test_download_youtube_summary_not_found():
    response = client.get("/youtube/download/nonexistent_id")
    assert response.status_code == 404

def test_download_youtube_summary_success(tmp_path):
    # Create a temporary summary file
    video_id = "test_video"
    test_content = "Test summary content"
    os.makedirs(tmp_path / "generated" / "youtube", exist_ok=True)
    with open(tmp_path / "generated" / "youtube" / f"youtube_summary_{video_id}.md", "w") as f:
        f.write(test_content)
    
    response = client.get(f"/youtube/download/{video_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"

# ------------------------
# Reddit API Tests
# ------------------------
def test_generate_reddit_summary_success(sample_subreddit):
    response = client.post("/reddit/generate", params={"subreddit_name": sample_subreddit})
    assert response.status_code == 200
    assert "status" in response.json()

def test_generate_reddit_summary_invalid_subreddit():
    response = client.post("/reddit/generate", params={"subreddit_name": ""})
    assert response.status_code == 400

def test_generate_reddit_summary_missing_subreddit():
    response = client.post("/reddit/generate")
    assert response.status_code == 422

def test_download_reddit_summary_not_found(sample_subreddit, sample_date):
    response = client.get("/reddit/download", params={
        "subreddit": sample_subreddit,
        "date": sample_date
    })
    assert response.status_code == 404

def test_download_reddit_summary_success(sample_subreddit, sample_date, tmp_path):
    # Create a temporary summary file
    test_content = "Test reddit summary content"
    os.makedirs(tmp_path / "generated" / sample_date, exist_ok=True)
    with open(tmp_path / "generated" / sample_date / f"reddit_summary_{sample_subreddit}.md", "w") as f:
        f.write(test_content)
    
    response = client.get("/reddit/download", params={
        "subreddit": sample_subreddit,
        "date": sample_date
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
