"""
Main FastAPI application for InfluxDB AI Analytics Agent
"""
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="InfluxDB AI Analytics Agent",
    description="AI-powered time-series analytics with natural language querying",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "healthy", "service": "influxdb-ai-agent"}

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to InfluxDB AI Analytics Agent API",
        "docs": "/docs",
        "health": "/health"
    }

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat interface"""
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Echo back for now - will be replaced with AI agent logic
            await websocket.send_text(f"Echo: {data}")
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """Get API information"""
    return {
        "name": "InfluxDB AI Analytics Agent",
        "version": "1.0.0",
        "features": [
            "Natural Language Queries",
            "Real-time Analytics",
            "AI-powered Insights",
            "Time-series Visualization"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("APP_DEBUG", "True").lower() == "true"
    )
