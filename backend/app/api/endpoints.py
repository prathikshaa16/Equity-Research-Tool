from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from ..database.database import get_db
from ..models.news import NewsArticle, SentimentAnalysis, EntityExtraction
from ..services.news_service import NewsService
from ..services.ai_insights_service import AIInsightsService
from ..core.config import settings

router = APIRouter()

# Pydantic models for API
class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str]
    source: str
    author: Optional[str]
    published_date: datetime
    url: str
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    entities: Optional[Dict]
    keywords: Optional[List[str]]
    category: Optional[str]
    ai_insight: Optional[str]
    investment_signal: Optional[str]

class ManualArticleRequest(BaseModel):
    title: str
    content: str
    source: str = "manual"
    author: Optional[str] = ""

class SentimentAnalysisRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str
    limit: int = 10

class PortfolioInsightsRequest(BaseModel):
    companies: List[str]

# Initialize services
news_service = NewsService()
ai_insights_service = AIInsightsService()

@router.get("/news", response_model=List[ArticleResponse])
async def get_news(
    skip: int = 0,
    limit: int = 50,
    company: Optional[str] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get news articles with optional filtering"""
    query = db.query(NewsArticle)
    
    if company:
        query = query.filter(NewsArticle.title.contains(company) | 
                           NewsArticle.content.contains(company))
    
    # Filter by recent dates
    cutoff_date = datetime.now() - timedelta(days=days)
    query = query.filter(NewsArticle.published_date >= cutoff_date)
    
    articles = query.order_by(NewsArticle.published_date.desc()).offset(skip).limit(limit).all()
    return articles

@router.post("/news/fetch")
async def fetch_news(background_tasks: BackgroundTasks, days: int = 7):
    """Fetch news from external sources"""
    background_tasks.add_task(fetch_and_process_news, days)
    return {"message": f"News fetching started for the last {days} days"}

async def fetch_and_process_news(days: int):
    """Background task to fetch and process news"""
    try:
        # Fetch news from various sources
        articles = await news_service.get_recent_news(days)
        
        # Process each article
        for article_data in articles:
            # Generate insights
            insights = ai_insights_service.generate_investment_insight(article_data)
            
            # Create database record (simplified - in production you'd use proper ORM)
            print(f"Processed article: {article_data.get('title', '')[:50]}...")
            
    except Exception as e:
        print(f"Error in background task: {e}")

@router.post("/news/manual")
async def add_manual_article(
    article: ManualArticleRequest,
    db: Session = Depends(get_db)
):
    """Add a manually entered article"""
    try:
        # Generate insights for the manual article
        article_data = article.dict()
        insights = ai_insights_service.generate_investment_insight(article_data)
        
        # Create database record
        db_article = NewsArticle(
            title=article.title,
            content=article.content,
            source=article.source,
            author=article.author,
            published_date=datetime.now(),
            url=f"manual_{datetime.now().timestamp()}",
            summary=insights.get("summary"),
            sentiment_score=insights.get("sentiment", {}).get("score"),
            sentiment_label=insights.get("sentiment", {}).get("label"),
            entities=insights.get("entities"),
            keywords=insights.get("entities", {}).get("keywords", []),
            category="manual",
            ai_insight=insights.get("insight"),
            investment_signal=insights.get("investment_signal")
        )
        
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        return {"message": "Article added successfully", "id": db_article.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/sentiment")
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """Analyze sentiment of given text"""
    try:
        sentiment = ai_insights_service.sentiment_analyzer.analyze_sentiment(request.text)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/entities")
async def extract_entities(request: SentimentAnalysisRequest):
    """Extract entities from given text"""
    try:
        entities = ai_insights_service.entity_extractor.extract_all(request.text)
        return entities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_text(request: SentimentAnalysisRequest):
    """Summarize given text"""
    try:
        summary = ai_insights_service.text_summarizer.summarize_text(request.text)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insights/generate")
async def generate_insights(article: Dict):
    """Generate AI insights for an article"""
    try:
        insights = ai_insights_service.generate_investment_insight(article)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def answer_query(request: QueryRequest, db: Session = Depends(get_db)):
    """Answer financial query using RAG"""
    try:
        # Get recent articles for context
        articles = db.query(NewsArticle).order_by(NewsArticle.published_date.desc()).limit(100).all()
        article_dicts = [
            {
                "title": article.title,
                "content": article.content,
                "url": article.url
            }
            for article in articles
        ]
        
        answer = ai_insights_service.answer_financial_query(request.query, article_dicts)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portfolio/insights")
async def get_portfolio_insights(request: PortfolioInsightsRequest, db: Session = Depends(get_db)):
    """Get insights for portfolio companies"""
    try:
        # Get recent articles
        articles = db.query(NewsArticle).order_by(NewsArticle.published_date.desc()).limit(200).all()
        article_dicts = [
            {
                "title": article.title,
                "content": article.content,
                "url": article.url
            }
            for article in articles
        ]
        
        insights = ai_insights_service.generate_portfolio_insights(article_dicts, request.companies)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sentiment/summary")
async def get_sentiment_summary(
    company: Optional[str] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get sentiment summary for recent news"""
    try:
        query = db.query(NewsArticle)
        
        if company:
            query = query.filter(NewsArticle.title.contains(company) | 
                               NewsArticle.content.contains(company))
        
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(NewsArticle.published_date >= cutoff_date)
        
        articles = query.all()
        article_dicts = [
            {
                "title": article.title,
                "content": article.content
            }
            for article in articles
        ]
        
        summary = ai_insights_service.sentiment_analyzer.get_sentiment_summary(article_dicts)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/companies/trending")
async def get_trending_companies(days: int = 7, db: Session = Depends(get_db)):
    """Get trending companies based on news mentions"""
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        articles = db.query(NewsArticle).filter(NewsArticle.published_date >= cutoff_date).all()
        
        company_mentions = {}
        for article in articles:
            if article.entities and "companies" in article.entities:
                for company in article.entities["companies"]:
                    if company not in company_mentions:
                        company_mentions[company] = {
                            "count": 0,
                            "sentiment_scores": [],
                            "latest_article": article.published_date
                        }
                    company_mentions[company]["count"] += 1
                    if article.sentiment_score:
                        company_mentions[company]["sentiment_scores"].append(article.sentiment_score)
        
        # Calculate average sentiment and sort by mention count
        trending = []
        for company, data in company_mentions.items():
            avg_sentiment = sum(data["sentiment_scores"]) / len(data["sentiment_scores"]) if data["sentiment_scores"] else 0
            trending.append({
                "company": company,
                "mention_count": data["count"],
                "average_sentiment": avg_sentiment,
                "sentiment_label": "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
            })
        
        trending.sort(key=lambda x: x["mention_count"], reverse=True)
        return trending[:10]  # Return top 10
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}
