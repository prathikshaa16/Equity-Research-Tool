import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Set page config
st.set_page_config(
    page_title="EquityAI Research Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive-sentiment {
        color: #2e8b57;
        font-weight: bold;
    }
    .negative-sentiment {
        color: #dc143c;
        font-weight: bold;
    }
    .neutral-sentiment {
        color: #708090;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_api_response(endpoint, params=None):
    """Get response from API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def post_api_response(endpoint, data=None):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def format_sentiment_score(score):
    """Format sentiment score with color"""
    if score > 0.1:
        return f"<span class='positive-sentiment'>{score:.2f}</span>"
    elif score < -0.1:
        return f"<span class='negative-sentiment'>{score:.2f}</span>"
    else:
        return f"<span class='neutral-sentiment'>{score:.2f}</span>"

def format_sentiment_label(label):
    """Format sentiment label with emoji"""
    label_map = {
        "positive": "🟢 Positive",
        "negative": "🔴 Negative", 
        "neutral": "🟡 Neutral"
    }
    return label_map.get(label.lower(), "🟡 Neutral")

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">📈 EquityAI Research Tool</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Refresh data button
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Fetching latest news..."):
                result = post_api_response("/news/fetch", {"days": 7})
                if result:
                    st.success("News fetching started!")
                    st.rerun()
        
        # Time period selector
        time_period = st.selectbox(
            "Time Period",
            options=[1, 3, 7, 14, 30],
            index=2,
            format_func=lambda x: f"Last {x} days"
        )
        
        # Company filter
        company_filter = st.text_input("Filter by Company", placeholder="Enter company name...")
        
        # Manual article section
        st.markdown("---")
        st.subheader("📝 Add Manual Article")
        with st.expander("Add Article"):
            manual_title = st.text_input("Article Title")
            manual_content = st.text_area("Article Content", height=150)
            manual_author = st.text_input("Author (optional)")
            
            if st.button("Add Article"):
                if manual_title and manual_content:
                    article_data = {
                        "title": manual_title,
                        "content": manual_content,
                        "author": manual_author
                    }
                    result = post_api_response("/news/manual", article_data)
                    if result:
                        st.success("Article added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in title and content")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "📰 News Feed", "🔍 Analysis", "💬 AI Chat", "📈 Trends"
    ])
    
    with tab1:
        st.header("📊 Dashboard Overview")
        
        # Get sentiment summary
        sentiment_params = {"days": time_period}
        if company_filter:
            sentiment_params["company"] = company_filter
            
        sentiment_summary = get_api_response("/sentiment/summary", sentiment_params)
        
        if sentiment_summary:
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Articles", sentiment_summary.get("total_articles", 0))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Positive", sentiment_summary.get("positive_count", 0), delta=None)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Negative", sentiment_summary.get("negative_count", 0), delta=None)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                avg_score = sentiment_summary.get("average_score", 0)
                st.metric("Avg Sentiment", f"{avg_score:.2f}", delta=None)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Sentiment distribution chart
            st.subheader("Sentiment Distribution")
            sentiment_dist = sentiment_summary.get("sentiment_distribution", {})
            
            if sentiment_dist:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(sentiment_dist.keys()),
                        y=list(sentiment_dist.values()),
                        marker_color=['#2e8b57', '#dc143c', '#708090']
                    )
                ])
                fig.update_layout(
                    title="Sentiment Distribution (%)",
                    xaxis_title="Sentiment",
                    yaxis_title="Percentage",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Trending companies
        st.subheader("🔥 Trending Companies")
        trending = get_api_response("/companies/trending", {"days": time_period})
        
        if trending:
            trending_df = pd.DataFrame(trending)
            if not trending_df.empty:
                # Display as table with sentiment colors
                display_df = trending_df.copy()
                display_df['Sentiment'] = display_df['sentiment_label'].apply(format_sentiment_label)
                display_df['Mentions'] = display_df['mention_count']
                display_df['Avg Score'] = display_df['average_sentiment'].apply(lambda x: f"{x:.2f}")
                
                st.dataframe(
                    display_df[['company', 'Mentions', 'Sentiment', 'Avg Score']],
                    column_config={
                        "company": "Company",
                        "Mentions": "News Mentions",
                        "Sentiment": "Overall Sentiment",
                        "Avg Score": "Avg Sentiment Score"
                    },
                    hide_index=True
                )
    
    with tab2:
        st.header("📰 News Feed")
        
        # Get news articles
        news_params = {"skip": 0, "limit": 20, "days": time_period}
        if company_filter:
            news_params["company"] = company_filter
            
        articles = get_api_response("/news", news_params)
        
        if articles:
            for i, article in enumerate(articles):
                with st.expander(f"📰 {article.get('title', 'No Title')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Source:** {article.get('source', 'Unknown')}")
                        st.write(f"**Published:** {article.get('published_date', 'Unknown')}")
                        st.write(f"**Author:** {article.get('author', 'Unknown')}")
                        
                        # Sentiment
                        sentiment = article.get('sentiment_label', 'neutral')
                        score = article.get('sentiment_score', 0)
                        st.write(f"**Sentiment:** {format_sentiment_label(sentiment)} ({format_sentiment_score(score)})")
                        
                        # Summary
                        if article.get('summary'):
                            st.write("**Summary:**")
                            st.write(article['summary'])
                        
                        # AI Insight
                        if article.get('ai_insight'):
                            st.write("**AI Insight:**")
                            st.info(article['ai_insight'])
                        
                        # Investment Signal
                        signal = article.get('investment_signal', 'neutral')
                        signal_map = {
                            "buy": "🟢 BUY",
                            "sell": "🔴 SELL", 
                            "hold": "🟡 HOLD",
                            "reduce": "🟠 REDUCE",
                            "neutral": "⚪ NEUTRAL"
                        }
                        st.write(f"**Signal:** {signal_map.get(signal, '⚪ NEUTRAL')}")
                    
                    with col2:
                        # Entities
                        entities = article.get('entities', {})
                        if entities.get('companies'):
                            st.write("**Companies:**")
                            for company in entities['companies'][:5]:
                                st.write(f"• {company}")
                        
                        if entities.get('keywords'):
                            st.write("**Keywords:**")
                            keywords = entities['keywords'][:5]
                            st.write(", ".join(keywords))
                    
                    st.markdown("---")
        else:
            st.info("No articles found. Try fetching news or adjusting filters.")
    
    with tab3:
        st.header("🔍 Text Analysis")
        
        # Text input for analysis
        text_to_analyze = st.text_area("Enter text to analyze:", height=200)
        
        if st.button("Analyze Text") and text_to_analyze:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Sentiment Analysis")
                sentiment_result = post_api_response("/analyze/sentiment", {"text": text_to_analyze})
                if sentiment_result:
                    label = sentiment_result.get('label', 'neutral')
                    score = sentiment_result.get('score', 0)
                    confidence = sentiment_result.get('confidence', 0)
                    
                    st.write(f"**Label:** {format_sentiment_label(label)}")
                    st.write(f"**Score:** {format_sentiment_score(score)}")
                    st.write(f"**Confidence:** {confidence:.2f}")
            
            with col2:
                st.subheader("Entity Extraction")
                entities_result = post_api_response("/analyze/entities", {"text": text_to_analyze})
                if entities_result:
                    entities = entities_result.get('entities', [])
                    if entities:
                        for entity in entities[:5]:
                            st.write(f"• **{entity.get('text', '')}** ({entity.get('label', '')})")
                    
                    companies = entities_result.get('companies', [])
                    if companies:
                        st.write("**Companies:**")
                        for company in companies[:5]:
                            st.write(f"• {company}")
            
            with col3:
                st.subheader("Text Summary")
                summary_result = post_api_response("/summarize", {"text": text_to_analyze})
                if summary_result:
                    summary = summary_result.get('summary', '')
                    if summary:
                        st.write(summary)
    
    with tab4:
        st.header("💬 AI Financial Assistant")
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about financial news, companies, or market trends..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = post_api_response("/query", {"query": prompt, "limit": 10})
                    if response:
                        answer = response.get('answer', 'I could not find relevant information.')
                        sources = response.get('sources', [])
                        
                        st.markdown(answer)
                        
                        if sources:
                            st.write("**Sources:**")
                            for source in sources:
                                st.write(f"• {source}")
                        
                        # Add assistant message to session state
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Sorry, I couldn't process your query right now.")
    
    with tab5:
        st.header("📈 Market Trends")
        
        # Time period selector for trends
        trend_days = st.selectbox(
            "Select Period",
            options=[7, 14, 30, 90],
            index=0,
            format_func=lambda x: f"Last {x} days"
        )
        
        # Get trending companies
        trending = get_api_response("/companies/trending", {"days": trend_days})
        
        if trending:
            trending_df = pd.DataFrame(trending)
            
            if not trending_df.empty:
                # Create subplots
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Company Mentions", "Sentiment Analysis"),
                    specs=[[{"type": "bar"}, {"type": "bar"}]]
                )
                
                # Mentions chart
                fig.add_trace(
                    go.Bar(
                        x=trending_df['company'][:10],
                        y=trending_df['mention_count'][:10],
                        name="Mentions",
                        marker_color='lightblue'
                    ),
                    row=1, col=1
                )
                
                # Sentiment chart
                colors = ['#2e8b57' if x > 0.1 else '#dc143c' if x < -0.1 else '#708090' 
                         for x in trending_df['average_sentiment'][:10]]
                
                fig.add_trace(
                    go.Bar(
                        x=trending_df['company'][:10],
                        y=trending_df['average_sentiment'][:10],
                        name="Avg Sentiment",
                        marker_color=colors
                    ),
                    row=1, col=2
                )
                
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    title_text=f"Market Trends - Last {trend_days} Days"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                st.subheader("Detailed Analysis")
                display_df = trending_df.copy()
                display_df['Sentiment'] = display_df['sentiment_label'].apply(format_sentiment_label)
                display_df['Sentiment Score'] = display_df['average_sentiment'].apply(format_sentiment_score)
                
                st.dataframe(
                    display_df[['company', 'mention_count', 'Sentiment', 'Sentiment Score']],
                    column_config={
                        "company": "Company",
                        "mention_count": "News Mentions",
                        "Sentiment": "Overall Sentiment",
                        "Sentiment Score": "Avg Sentiment Score"
                    },
                    hide_index=True
                )
        else:
            st.info("No trending data available. Make sure news has been fetched.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "EquityAI Research Tool - Powered by NLP and Generative AI"
    "</div>",
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()
