from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Keys
    NEWS_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./equity_ai.db"
    MONGODB_URL: str = "mongodb://localhost:27017/equity_ai"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Application Settings
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-here"
    CORS_ORIGINS: List[str] = ["http://localhost:8500", "http://localhost:8000"]
    
    # News Sources
    RSS_FEEDS: List[str] = [
        "https://feeds.finance.yahoo.com/rss/2.0/headline",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    ]
    NEWS_CATEGORIES: List[str] = ["business", "technology", "finance"]
    
    # NLP Model Settings
    SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    NER_MODEL: str = "dbmdz/bert-large-cased-finetuned-conll03-english"
    SUMMARIZATION_MODEL: str = "facebook/bart-large-cnn"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EquityAI Research Tool"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
