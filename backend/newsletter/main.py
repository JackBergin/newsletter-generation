import uvicorn
from .api.app import app
import os

if __name__ == "__main__":
    uvicorn.run(
        "backend.newsletter.api.app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False  # Set to True for development
    )