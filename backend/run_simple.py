"""
Simple backend runner that works without heavy model downloads
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a simple FastAPI app for testing
app = FastAPI(
    title="EquityAI Research Tool - Simple Mode",
    version="1.0.0",
    description="AI-powered Equity Research Tool API (Simple Mode)"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8500", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EquityAI Research Tool API - Simple Mode",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "mode": "simple"}

@app.get("/api/v1/health")
async def api_health():
    """API health check endpoint"""
    return {"status": "healthy", "mode": "simple"}

if __name__ == "__main__":
    print("🚀 Starting EquityAI Backend in Simple Mode...")
    print("📊 Dashboard: http://localhost:8501")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/api/v1/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
