import openai
import logging
from typing import Dict, List, Optional
from ..core.config import settings
from ..nlp.sentiment_analyzer import SentimentAnalyzer
from ..nlp.entity_extractor import EntityExtractor
from ..nlp.text_summarizer import TextSummarizer

logger = logging.getLogger(__name__)


class AIInsightsService:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_extractor = EntityExtractor()
        self.text_summarizer = TextSummarizer()
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_investment_insight(self, article: Dict) -> Dict:
        """Generate investment insight for a news article"""
        try:
            title = article.get("title", "")
            content = article.get("content", "")
            
            # Extract key information
            sentiment = self.sentiment_analyzer.analyze_sentiment(content)
            entities = self.entity_extractor.extract_financial_entities(content)
            summary_result = self.text_summarizer.summarize_text(content)
            
            # Generate insight using OpenAI if available, otherwise use rule-based approach
            if self.openai_api_key:
                insight = self._generate_ai_insight(title, content, sentiment, entities)
            else:
                insight = self._generate_rule_based_insight(sentiment, entities)
            
            # Determine investment signal
            signal = self._determine_investment_signal(sentiment, entities)
            
            return {
                "summary": summary_result.get("summary", ""),
                "sentiment": sentiment,
                "entities": entities,
                "insight": insight,
                "investment_signal": signal,
                "confidence": sentiment.get("confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"Error generating investment insight: {e}")
            return {
                "summary": "",
                "sentiment": {"label": "neutral", "score": 0.0},
                "entities": {},
                "insight": "Unable to generate insight due to an error.",
                "investment_signal": "neutral",
                "confidence": 0.0
            }
    
    def _generate_ai_insight(self, title: str, content: str, 
                           sentiment: Dict, entities: Dict) -> str:
        """Generate insight using OpenAI GPT"""
        try:
            prompt = f"""
            As a financial analyst, analyze this news article and provide investment insight:
            
            Title: {title}
            Content: {content[:1000]}...
            
            Sentiment: {sentiment['label']} (score: {sentiment['score']:.2f})
            Key Companies: {', '.join(entities.get('companies', []))}
            Key People: {', '.join(entities.get('people', []))}
            
            Provide a concise investment insight (2-3 sentences) focusing on:
            1. Potential market impact
            2. Investment implications
            3. Risk factors
            
            Insight:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing investment insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI insight: {e}")
            return self._generate_rule_based_insight(sentiment, entities)
    
    def _generate_rule_based_insight(self, sentiment: Dict, entities: Dict) -> str:
        """Generate insight using rule-based approach"""
        sentiment_label = sentiment.get("label", "neutral")
        companies = entities.get("companies", [])
        
        if sentiment_label == "positive" and companies:
            return f"Positive news coverage for {', '.join(companies[:2])} suggests potential upside. Market sentiment appears favorable."
        elif sentiment_label == "negative" and companies:
            return f"Negative sentiment around {', '.join(companies[:2])} indicates potential risks. Caution advised for short-term positions."
        else:
            return "Neutral market sentiment detected. Monitor for additional news and market indicators."
    
    def _determine_investment_signal(self, sentiment: Dict, entities: Dict) -> str:
        """Determine investment signal based on sentiment and entities"""
        sentiment_score = sentiment.get("score", 0.0)
        confidence = sentiment.get("confidence", 0.0)
        
        # High confidence positive sentiment
        if sentiment_score > 0.3 and confidence > 0.7:
            return "buy"
        # High confidence negative sentiment
        elif sentiment_score < -0.3 and confidence > 0.7:
            return "sell"
        # Moderate sentiment
        elif abs(sentiment_score) > 0.1 and confidence > 0.5:
            return "hold" if sentiment_score > 0 else "reduce"
        else:
            return "neutral"
    
    def generate_portfolio_insights(self, articles: List[Dict], 
                                  portfolio_companies: List[str]) -> Dict:
        """Generate insights for a portfolio of companies"""
        relevant_articles = []
        
        for article in articles:
            entities = self.entity_extractor.extract_companies(article.get("content", ""))
            if any(company in entities for company in portfolio_companies):
                relevant_articles.append(article)
        
        if not relevant_articles:
            return {
                "total_articles": 0,
                "insights": "No relevant news found for your portfolio companies.",
                "sentiment_summary": {"label": "neutral", "score": 0.0},
                "recommendations": []
            }
        
        # Analyze sentiment for relevant articles
        sentiments = []
        for article in relevant_articles:
            sentiment = self.sentiment_analyzer.analyze_sentiment(article.get("content", ""))
            sentiments.append(sentiment)
        
        # Calculate overall sentiment
        avg_score = sum(s.get("score", 0) for s in sentiments) / len(sentiments)
        overall_sentiment = "positive" if avg_score > 0.1 else "negative" if avg_score < -0.1 else "neutral"
        
        # Generate recommendations
        recommendations = []
        if overall_sentiment == "positive":
            recommendations.append("Consider increasing exposure to positively mentioned companies")
        elif overall_sentiment == "negative":
            recommendations.append("Monitor risk for negatively mentioned companies")
        
        return {
            "total_articles": len(relevant_articles),
            "insights": f"Found {len(relevant_articles)} relevant articles with {overall_sentiment} sentiment",
            "sentiment_summary": {"label": overall_sentiment, "score": avg_score},
            "recommendations": recommendations
        }
    
    def answer_financial_query(self, query: str, articles: List[Dict]) -> Dict:
        """Answer user query using RAG approach"""
        try:
            # Find relevant articles
            relevant_articles = self._find_relevant_articles(query, articles)
            
            if not relevant_articles:
                return {
                    "answer": "I couldn't find relevant information to answer your query.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Generate answer using OpenAI if available
            if self.openai_api_key:
                answer = self._generate_rag_answer(query, relevant_articles)
            else:
                answer = self._generate_simple_answer(query, relevant_articles)
            
            return {
                "answer": answer,
                "sources": [article.get("title", "") for article in relevant_articles[:3]],
                "confidence": 0.7
            }
            
        except Exception as e:
            logger.error(f"Error answering query: {e}")
            return {
                "answer": "I encountered an error while processing your query.",
                "sources": [],
                "confidence": 0.0
            }
    
    def _find_relevant_articles(self, query: str, articles: List[Dict]) -> List[Dict]:
        """Find articles relevant to the query"""
        query_terms = query.lower().split()
        relevant_articles = []
        
        for article in articles:
            content = (article.get("title", "") + " " + article.get("content", "")).lower()
            
            # Simple relevance scoring based on term overlap
            score = sum(1 for term in query_terms if term in content)
            if score > 0:
                relevant_articles.append({"score": score, **article})
        
        # Sort by relevance and return top articles
        relevant_articles.sort(key=lambda x: x["score"], reverse=True)
        return [article for article in relevant_articles[:3]]
    
    def _generate_rag_answer(self, query: str, relevant_articles: List[Dict]) -> str:
        """Generate answer using RAG with OpenAI"""
        context = "\n\n".join([
            f"Article: {article.get('title', '')}\n{article.get('content', '')[:500]}..."
            for article in relevant_articles
        ])
        
        prompt = f"""
        Based on the following news articles, answer this question: {query}
        
        Context:
        {context}
        
        Provide a concise and accurate answer based on the given information.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial assistant answering questions based on news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating RAG answer: {e}")
            return self._generate_simple_answer(query, relevant_articles)
    
    def _generate_simple_answer(self, query: str, relevant_articles: List[Dict]) -> str:
        """Generate simple answer without AI"""
        if not relevant_articles:
            return "I don't have enough information to answer your question."
        
        top_article = relevant_articles[0]
        summary = self.text_summarizer.summarize_text(top_article.get("content", ""))
        
        return f"Based on recent news: {summary.get('summary', 'No summary available')}"
