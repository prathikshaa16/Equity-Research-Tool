from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch
import logging
from typing import Dict, List
from ..core.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        self.model_name = settings.SENTIMENT_MODEL
        self.device = 0 if torch.cuda.is_available() else -1
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the sentiment analysis model"""
        try:
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=self.device
            )
            logger.info(f"Loaded sentiment model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading sentiment model: {e}")
            # Fallback to a simpler model
            try:
                self.pipeline = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=self.device
                )
                logger.info("Loaded fallback sentiment model")
            except Exception as e2:
                logger.error(f"Error loading fallback model: {e2}")
                self.pipeline = None
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of given text"""
        if not self.pipeline:
            return {
                "label": "neutral",
                "score": 0.5,
                "confidence": 0.0
            }
        
        try:
            # Truncate text if too long
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            result = self.pipeline(text)[0]
            
            # Normalize score to -1 to 1 range
            label = result["label"].lower()
            score = result["score"]
            
            if label in ["positive", "pos", "label_2"]:
                normalized_score = score
            elif label in ["negative", "neg", "label_0"]:
                normalized_score = -score
            else:  # neutral
                normalized_score = 0
            
            return {
                "label": "positive" if normalized_score > 0.1 else "negative" if normalized_score < -0.1 else "neutral",
                "score": normalized_score,
                "confidence": score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "label": "neutral",
                "score": 0.0,
                "confidence": 0.0
            }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        results = []
        for text in texts:
            result = self.analyze_sentiment(text)
            results.append(result)
        return results
    
    def get_sentiment_summary(self, articles: List[Dict]) -> Dict:
        """Get sentiment summary for multiple articles"""
        if not articles:
            return {
                "total_articles": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "average_score": 0.0
            }
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0.0
        
        for article in articles:
            sentiment = self.analyze_sentiment(article.get("content", ""))
            sentiments.append(sentiment)
            
            label = sentiment["label"]
            score = sentiment["score"]
            
            if label == "positive":
                positive_count += 1
            elif label == "negative":
                negative_count += 1
            else:
                neutral_count += 1
            
            total_score += score
        
        return {
            "total_articles": len(articles),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "average_score": total_score / len(articles) if articles else 0.0,
            "sentiment_distribution": {
                "positive": positive_count / len(articles) * 100 if articles else 0,
                "negative": negative_count / len(articles) * 100 if articles else 0,
                "neutral": neutral_count / len(articles) * 100 if articles else 0
            }
        }
