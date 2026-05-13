import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from newspaper import Article
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.rss_feeds = settings.RSS_FEEDS
        
    async def fetch_news_from_api(self, query: str = "finance", 
                                 from_date: Optional[str] = None,
                                 to_date: Optional[str] = None) -> List[Dict]:
        """Fetch news from NewsAPI"""
        if not self.news_api_key:
            logger.warning("NewsAPI key not provided")
            return []
            
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "apiKey": self.news_api_key,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title", ""),
                    "content": article.get("content", article.get("description", "")),
                    "source": article.get("source", {}).get("name", ""),
                    "author": article.get("author", ""),
                    "published_date": article.get("publishedAt", ""),
                    "url": article.get("url", "")
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching news from API: {e}")
            return []
    
    async def fetch_news_from_rss(self) -> List[Dict]:
        """Fetch news from RSS feeds"""
        articles = []
        
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Get full article content
                    content = self._extract_article_content(entry.link)
                    
                    articles.append({
                        "title": entry.get("title", ""),
                        "content": content or entry.get("description", ""),
                        "source": feed.feed.get("title", ""),
                        "author": entry.get("author", ""),
                        "published_date": entry.get("published", ""),
                        "url": entry.get("link", "")
                    })
                    
            except Exception as e:
                logger.error(f"Error fetching from RSS feed {feed_url}: {e}")
                
        return articles
    
    def _extract_article_content(self, url: str) -> Optional[str]:
        """Extract full article content using newspaper3k"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            logger.error(f"Error extracting article content from {url}: {e}")
            return None
    
    async def add_manual_article(self, title: str, content: str, 
                                 source: str = "manual", author: str = "") -> Dict:
        """Add manually entered article"""
        return {
            "title": title,
            "content": content,
            "source": source,
            "author": author,
            "published_date": datetime.now().isoformat(),
            "url": f"manual_{datetime.now().timestamp()}"
        }
    
    async def get_recent_news(self, days: int = 7) -> List[Dict]:
        """Get news from the last N days"""
        all_articles = []
        
        # Fetch from RSS feeds
        rss_articles = await self.fetch_news_from_rss()
        all_articles.extend(rss_articles)
        
        # Fetch from API if key is available
        if self.news_api_key:
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            api_articles = await self.fetch_news_from_api(from_date=from_date)
            all_articles.extend(api_articles)
        
        # Filter by date and remove duplicates
        unique_articles = {}
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for article in all_articles:
            try:
                pub_date = datetime.fromisoformat(
                    article["published_date"].replace("Z", "+00:00")
                ).replace(tzinfo=None)
                
                if pub_date >= cutoff_date:
                    url = article["url"]
                    if url not in unique_articles:
                        unique_articles[url] = article
            except:
                continue
                
        return list(unique_articles.values())
