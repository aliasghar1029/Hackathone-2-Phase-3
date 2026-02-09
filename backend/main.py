import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="TODO AI Chatbot API", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to TODO AI Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-ai-chatbot-api"}

# Import and register routes
try:
    from routes import auth, tasks, chat
    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(chat.router)
except ImportError as e:
    print(f"Routes not yet implemented: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)