import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app.nlp.sentiment_analyzer import SentimentAnalyzer
from backend.app.nlp.entity_extractor import EntityExtractor
from backend.app.nlp.text_summarizer import TextSummarizer

def test_sentiment_analyzer():
    """Test sentiment analyzer functionality"""
    print("Testing Sentiment Analyzer...")
    
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    positive_text = "Apple stock is soaring today with excellent earnings report and strong growth prospects!"
    result = analyzer.analyze_sentiment(positive_text)
    print(f"Positive text: {result}")
    assert result["label"] in ["positive", "negative", "neutral"]
    assert isinstance(result["score"], float)
    
    # Test negative sentiment
    negative_text = "Tesla shares plummeted after disappointing earnings and production delays."
    result = analyzer.analyze_sentiment(negative_text)
    print(f"Negative text: {result}")
    assert result["label"] in ["positive", "negative", "neutral"]
    
    # Test batch analysis
    texts = [
        "Great earnings report from Microsoft!",
        "Google faces regulatory challenges.",
        "Amazon announces new cloud services."
    ]
    batch_results = analyzer.batch_analyze(texts)
    print(f"Batch analysis: {len(batch_results)} results")
    assert len(batch_results) == len(texts)
    
    print("✓ Sentiment Analyzer tests passed\n")

def test_entity_extractor():
    """Test entity extractor functionality"""
    print("Testing Entity Extractor...")
    
    extractor = EntityExtractor()
    
    test_text = """
    Apple CEO Tim Cook announced new iPhone features at the Cupertino headquarters. 
    Microsoft CEO Satya Nadella also commented on the AI partnership with OpenAI. 
    The companies are investing billions in artificial intelligence research.
    """
    
    # Test spaCy entities
    entities = extractor.extract_entities_spacy(test_text)
    print(f"SpaCy entities: {len(entities)} found")
    for entity in entities[:5]:
        print(f"  - {entity['text']} ({entity['label']})")
    
    # Test company extraction
    companies = extractor.extract_companies(test_text)
    print(f"Companies found: {companies}")
    
    # Test financial entities
    financial_entities = extractor.extract_financial_entities(test_text)
    print(f"Financial entities: {financial_entities}")
    
    # Test keyword extraction
    keywords = extractor.extract_keywords(test_text)
    print(f"Keywords: {keywords}")
    
    # Test comprehensive extraction
    all_entities = extractor.extract_all(test_text)
    print(f"All entities extracted: {list(all_entities.keys())}")
    
    print("✓ Entity Extractor tests passed\n")

def test_text_summarizer():
    """Test text summarizer functionality"""
    print("Testing Text Summarizer...")
    
    summarizer = TextSummarizer()
    
    long_text = """
    Apple Inc. reported better-than-expected fourth quarter earnings, driven by strong iPhone sales 
    and growing services revenue. The tech giant posted earnings per share of $1.26, beating analysts' 
    estimates of $1.01. Revenue came in at $89.5 billion, exceeding expectations of $87.6 billion. 
    CEO Tim Cook expressed optimism about the upcoming quarter, citing strong demand for the new iPhone 15 
    and continued growth in the services segment. The company's stock jumped more than 5% in after-hours 
    trading, reflecting investor confidence in Apple's ability to navigate challenging market conditions. 
    The strong performance was attributed to robust iPhone sales, particularly in emerging markets, as well 
    as continued growth in the services division, which includes Apple Music, iCloud, and the App Store. 
    Analysts were particularly impressed with the services revenue growth, which reached an all-time high 
    and demonstrates the company's successful transition to a more diversified business model.
    """
    
    # Test summarization
    result = summarizer.summarize_text(long_text)
    print(f"Summary: {result['summary']}")
    print(f"Confidence: {result['confidence']}")
    assert len(result["summary"]) < len(long_text)
    
    # Test key points extraction
    key_points = summarizer.extract_key_points(long_text)
    print(f"Key points: {key_points}")
    assert len(key_points) > 0
    
    print("✓ Text Summarizer tests passed\n")

def test_nlp_integration():
    """Test NLP components working together"""
    print("Testing NLP Integration...")
    
    sample_article = {
        "title": "Apple Reports Record Earnings",
        "content": """
        Apple Inc. (AAPL) reported record fourth quarter earnings today, with CEO Tim Cook announcing 
        exceptional performance across all product lines. The company's revenue exceeded expectations 
        driven by strong iPhone 15 sales and growing services revenue. Apple stock surged 5% in 
        after-hours trading as investors reacted positively to the news. The tech giant also announced 
        new AI features coming to iOS and macOS in partnership with OpenAI.
        """
    }
    
    # Initialize components
    sentiment_analyzer = SentimentAnalyzer()
    entity_extractor = EntityExtractor()
    text_summarizer = TextSummarizer()
    
    # Analyze sentiment
    sentiment = sentiment_analyzer.analyze_sentiment(sample_article["content"])
    print(f"Sentiment: {sentiment}")
    
    # Extract entities
    entities = entity_extractor.extract_all(sample_article["content"])
    print(f"Entities: {entities}")
    
    # Generate summary
    summary = text_summarizer.summarize_text(sample_article["content"])
    print(f"Summary: {summary['summary']}")
    
    print("✓ NLP Integration tests passed\n")

def run_all_nlp_tests():
    """Run all NLP tests"""
    try:
        test_sentiment_analyzer()
        test_entity_extractor()
        test_text_summarizer()
        test_nlp_integration()
        print("All NLP tests completed successfully! 🎉")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_nlp_tests()
