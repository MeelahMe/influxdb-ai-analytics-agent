"""
Main FastAPI application for InfluxDB AI Analytics Agent
"""
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from app.config.database import influxdb_conn
from app.utils.sample_data import SampleDataGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
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

# Test InfluxDB connection endpoint
@app.get("/api/v1/test-connection")
async def test_influxdb_connection():
    """Test InfluxDB connection"""
    try:
        # Test connection
        if influxdb_conn.test_connection():
            return {
                "status": "connected",
                "message": "InfluxDB 3 Core connection successful",
                "database": influxdb_conn.config.database if not influxdb_conn.use_mock else "mock",
                "mode": "mock" if influxdb_conn.use_mock else "live"
            }
        else:
            raise HTTPException(status_code=503, detail="Connection test failed")
    except Exception as e:
        logger.error(f"InfluxDB connection failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Generate sample data endpoint
@app.post("/api/v1/generate-sample-data")
async def generate_sample_data():
    """Generate sample data for testing"""
    try:
        SampleDataGenerator.populate_sample_data()
        return {
            "status": "success",
            "message": "Sample data generated successfully"
        }
    except Exception as e:
        logger.error(f"Failed to generate sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate sample data: {str(e)}")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("APP_DEBUG", "True").lower() == "true"
    )
