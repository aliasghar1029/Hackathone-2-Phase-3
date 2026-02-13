from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from db import engine
from routes import auth, tasks, chat
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize the database on startup."""
    logger.info("Initializing database...")
    # Create all tables if they don't exist
    from models import User, Task, Conversation, Message  # Import here to ensure models are registered
    async with engine.begin() as conn:
        # Try to create tables, ignoring if they already exist
        try:
            await conn.run_sync(SQLModel.metadata.create_all)
        except Exception as e:
            logger.warning(f"Could not create tables (they might already exist): {e}")
    logger.info("Database initialized successfully!")
    yield
    # Shutdown logic can go here if needed


# Create FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    description="A FastAPI backend for a Todo application with authentication",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        "https://*.hf.space",     # Hugging Face Spaces
        # Add your production domain here if needed
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    # expose_headers=["Access-Control-Allow-Origin"]
)


# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(tasks.router, prefix="/api")
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "Todo API is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Todo API"}


# Error handlers
@app.exception_handler(404)
async def custom_http_exception_handler(request, exc):
    from starlette.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    from starlette.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)}
    )