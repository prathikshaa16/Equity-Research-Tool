import pytest
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"

class TestEquityAIAPI:
    """Test suite for EquityAI API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis endpoint"""
        test_text = "Apple stock is performing very well today with great earnings report."
        response = requests.post(f"{API_BASE_URL}/analyze/sentiment", 
                               json={"text": test_text})
        assert response.status_code == 200
        data = response.json()
        assert "label" in data
        assert "score" in data
        assert "confidence" in data
        assert data["label"] in ["positive", "negative", "neutral"]
        assert -1 <= data["score"] <= 1
    
    def test_entity_extraction(self):
        """Test entity extraction endpoint"""
        test_text = "Apple CEO Tim Cook announced new iPhone features at the Cupertino headquarters."
        response = requests.post(f"{API_BASE_URL}/analyze/entities", 
                               json={"text": test_text})
        assert response.status_code == 200
        data = response.json()
        assert "entities" in data
        assert "companies" in data
        assert "financial_entities" in data
    
    def test_text_summarization(self):
        """Test text summarization endpoint"""
        test_text = """
        Apple Inc. reported better-than-expected fourth quarter earnings, driven by strong iPhone sales 
        and growing services revenue. The tech giant posted earnings per share of $1.26, beating analysts' 
        estimates of $1.01. Revenue came in at $89.5 billion, exceeding expectations of $87.6 billion. 
        CEO Tim Cook expressed optimism about the upcoming quarter, citing strong demand for the new iPhone 15 
        and continued growth in the services segment. The company's stock jumped more than 5% in after-hours 
        trading, reflecting investor confidence in Apple's ability to navigate challenging market conditions.
        """
        response = requests.post(f"{API_BASE_URL}/summarize", 
                               json={"text": test_text})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert len(data["summary"]) < len(test_text)
    
    def test_manual_article_addition(self):
        """Test adding manual article"""
        article_data = {
            "title": "Test Article",
            "content": "This is a test article for testing the API.",
            "author": "Test Author"
        }
        response = requests.post(f"{API_BASE_URL}/news/manual", 
                               json=article_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "id" in data
    
    def test_news_retrieval(self):
        """Test news retrieval endpoint"""
        response = requests.get(f"{API_BASE_URL}/news")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_sentiment_summary(self):
        """Test sentiment summary endpoint"""
        response = requests.get(f"{API_BASE_URL}/sentiment/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_articles" in data
        assert "positive_count" in data
        assert "negative_count" in data
        assert "neutral_count" in data
        assert "average_score" in data
    
    def test_trending_companies(self):
        """Test trending companies endpoint"""
        response = requests.get(f"{API_BASE_URL}/companies/trending")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:  # If there are trending companies
            assert "company" in data[0]
            assert "mention_count" in data[0]
            assert "average_sentiment" in data[0]
    
    def test_financial_query(self):
        """Test financial query endpoint"""
        query_data = {
            "query": "What are the latest earnings reports for tech companies?",
            "limit": 5
        }
        response = requests.post(f"{API_BASE_URL}/query", 
                               json=query_data)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data
    
    def test_portfolio_insights(self):
        """Test portfolio insights endpoint"""
        portfolio_data = {
            "companies": ["Apple", "Microsoft", "Google"]
        }
        response = requests.post(f"{API_BASE_URL}/portfolio/insights", 
                               json=portfolio_data)
        assert response.status_code == 200
        data = response.json()
        assert "total_articles" in data
        assert "insights" in data
        assert "sentiment_summary" in data
        assert "recommendations" in data

def run_tests():
    """Run all API tests"""
    test_instance = TestEquityAIAPI()
    test_methods = [
        test_instance.test_health_check,
        test_instance.test_sentiment_analysis,
        test_instance.test_entity_extraction,
        test_instance.test_text_summarization,
        test_instance.test_manual_article_addition,
        test_instance.test_news_retrieval,
        test_instance.test_sentiment_summary,
        test_instance.test_trending_companies,
        test_instance.test_financial_query,
        test_instance.test_portfolio_insights
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            print(f"Running {test_method.__name__}...")
            test_method()
            print(f"✓ {test_method.__name__} PASSED")
            passed += 1
        except Exception as e:
            print(f"✗ {test_method.__name__} FAILED: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return passed, failed

if __name__ == "__main__":
    run_tests()
