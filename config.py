import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file (works regardless of cwd)
load_dotenv(Path(__file__).parent / ".env")

# Facebook Graph API setup
GRAPH_API_VERSION = "v22.0"
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
