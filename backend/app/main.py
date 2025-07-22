from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
from datetime import datetime
from .config.database import influxdb_conn

app = FastAPI(title="InfluxDB AI Analytics Agent")

# Add CORS middleware - IMPORTANT: This must be added BEFORE other routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str
    timestamp: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Test InfluxDB connection
@app.get("/api/v1/test-connection")
async def test_connection():
    try:
        # Use your existing connection class
        is_connected = influxdb_conn.test_connection()
        
        if is_connected:
            return {
                "status": "connected",
                "database": influxdb_conn.config.database if not influxdb_conn.use_mock else "mock_mode",
                "mock_mode": influxdb_conn.use_mock,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Query endpoint for chat messages
@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # For now, return a placeholder response
        # Later, this will integrate with LLM and query InfluxDB
        response_text = f'I received your message: "{request.message}". The natural language processing feature is coming soon!'
        
        return QueryResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process the message (placeholder for now)
            response = {
                "response": f"WebSocket received: {message_data.get('message', 'No message')}",
                "timestamp": datetime.now().isoformat()
            }
            
            # Send response back to client
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    