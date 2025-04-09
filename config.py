import os
from dotenv import load_dotenv

# Load .env file if it exists (useful for development)
load_dotenv()

# Configuration variables from environment variables
API_KEY = os.getenv("PAGERTREE_API_KEY", "your-default-api-key-here")
BASE_URL = os.getenv("PAGERTREE_BASE_URL", "https://api.pagertree.com/api/v4")