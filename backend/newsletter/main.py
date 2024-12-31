import os
import uvicorn
from dotenv import load_dotenv

app = "newsletter.api.app:app"

load_dotenv()
SERVE_URL = os.getenv("SERVE_URL")

def server():
    uvicorn.run(app, host=SERVE_URL, port=8080)

if __name__ == "__main__":
    server()