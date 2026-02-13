import os
import sys
from dotenv import load_dotenv

# Load environment variables but temporarily override DATABASE_URL for local testing
load_dotenv()

# Override DATABASE_URL to use SQLite for local development
os.environ['DATABASE_URL'] = 'sqlite:///./test_local.db'

# Now import and run the main application
from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8001)