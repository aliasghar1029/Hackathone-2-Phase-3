import os
import sys

# Temporarily override the DATABASE_URL to use SQLite for local development
os.environ['DATABASE_URL'] = 'sqlite:///./local_test.db'

# Now run the main application
if __name__ == "__main__":
    from main import app
    import uvicorn
    
    # Run the application
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)