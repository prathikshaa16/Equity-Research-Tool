"""
Robust backend runner that works reliably
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import time

# Create a robust FastAPI app
app = FastAPI(
    title="EquityAI Research Tool",
    version="1.0.0",
    description="AI-powered Equity Research Tool API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EquityAI Research Tool API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/v1/health")
async def api_health():
    """API health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

# Mock endpoints for frontend testing
@app.get("/api/v1/sentiment/summary")
async def sentiment_summary(days: int = 7):
    """Mock sentiment summary"""
    return {
        "total_articles": 15,
        "positive_count": 8,
        "negative_count": 3,
        "neutral_count": 4,
        "average_score": 0.25,
        "sentiment_distribution": {
            "positive": 53.3,
            "negative": 20.0,
            "neutral": 26.7
        }
    }

@app.get("/api/v1/companies/trending")
async def trending_companies(days: int = 7):
    """Mock trending companies"""
    return [
        {"company": "Apple", "mention_count": 12, "average_sentiment": 0.3, "sentiment_label": "positive"},
        {"company": "Microsoft", "mention_count": 8, "average_sentiment": 0.2, "sentiment_label": "positive"},
        {"company": "Tesla", "mention_count": 6, "average_sentiment": -0.1, "sentiment_label": "neutral"},
        {"company": "Amazon", "mention_count": 5, "average_sentiment": 0.4, "sentiment_label": "positive"},
        {"company": "Google", "mention_count": 4, "average_sentiment": 0.1, "sentiment_label": "neutral"}
    ]

@app.get("/api/v1/news")
async def get_news(skip: int = 0, limit: int = 20):
    """Mock news articles"""
    return [
        {
            "id": 1,
            "title": "Apple Reports Strong Q4 Earnings",
            "content": "Apple Inc. reported better-than-expected quarterly earnings...",
            "source": "Reuters",
            "author": "Tech Reporter",
            "published_date": "2024-01-15T10:00:00Z",
            "url": "https://example.com/apple-earnings",
            "sentiment_score": 0.3,
            "sentiment_label": "positive",
            "entities": {"companies": ["Apple"], "keywords": ["earnings", "growth"]},
            "ai_insight": "Strong earnings indicate positive momentum for Apple stock.",
            "investment_signal": "buy"
        },
        {
            "id": 2,
            "title": "Tesla Faces Production Challenges",
            "content": "Tesla Inc. is experiencing production delays at key facilities...",
            "source": "Bloomberg",
            "author": "Auto Analyst",
            "published_date": "2024-01-14T15:30:00Z",
            "url": "https://example.com/tesla-production",
            "sentiment_score": -0.2,
            "sentiment_label": "negative",
            "entities": {"companies": ["Tesla"], "keywords": ["production", "delays"]},
            "ai_insight": "Production challenges may impact short-term performance.",
            "investment_signal": "hold"
        }
    ]

def run_server():
    """Run the server"""
    print("🚀 Starting EquityAI Backend Server...")
    print("📊 Frontend: http://localhost:8501")
    print("📚 API Docs: http://localhost:8000/docs")
    print("❤️  Health: http://localhost:8000/api/v1/health")
    print("🔗 Server running at: http://localhost:8000")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
