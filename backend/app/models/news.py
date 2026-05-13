from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from ..database.database import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    source = Column(String, index=True)
    author = Column(String)
    published_date = Column(DateTime, index=True)
    url = Column(String, unique=True, index=True)
    
    # NLP Analysis Results
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String)  # positive, negative, neutral
    entities = Column(JSON)  # List of extracted entities
    keywords = Column(JSON)  # List of keywords
    category = Column(String, index=True)
    
    # Generated Insights
    ai_insight = Column(Text)
    investment_signal = Column(String)  # buy, sell, hold, neutral
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, index=True)
    article_id = Column(Integer, nullable=False)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    confidence = Column(Float)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())


class EntityExtraction(Base):
    __tablename__ = "entity_extraction"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, nullable=False)
    entity_text = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)  # PERSON, ORG, GPE, etc.
    confidence = Column(Float)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())
