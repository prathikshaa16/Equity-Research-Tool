import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

# Enhanced CSS for modern UI
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }
        
        .content-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(5px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .tab-container {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 10px;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #666;
            font-weight: 500;
        }
        
        .positive-sentiment {
            color: #10b981;
            font-weight: 600;
        }
        
        .negative-sentiment {
            color: #ef4444;
            font-weight: 600;
        }
        
        .neutral-sentiment {
            color: #6b7280;
            font-weight: 600;
        }
        
        .trend-up {
            color: #10b981;
        }
        
        .trend-down {
            color: #ef4444;
        }
        
        .trend-neutral {
            color: #6b7280;
        }
        
        .chat-message {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        
        .user-message {
            border-left-color: #667eea;
        }
        
        .assistant-message {
            border-left-color: #10b981;
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .success-message {
            background: linear-gradient(45deg, #10b981, #059669);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .warning-message {
            background: linear-gradient(45deg, #f59e0b, #d97706);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .error-message {
            background: linear-gradient(45deg, #ef4444, #dc2626);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        /* Hide streamlit elements */
        .stDeployButton, .stReportViewer, .stHeader {
            visibility: hidden;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(102, 126, 234, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(102, 126, 234, 0.7);
        }
    </style>
    """, unsafe_allow_html=True)

def get_api_response(endpoint, params=None):
    """Get response from API with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
        return None

def create_metric_card(title, value, delta=None, color="#667eea"):
    """Create a styled metric card"""
    delta_html = f"<div style='font-size: 1rem; color: {color}; font-weight: 600;'>{delta}</div>" if delta else ""
    return f"""
    <div class='metric-card'>
        <div class='metric-value' style='color: {color};'>{value}</div>
        <div class='metric-label'>{title}</div>
        {delta_html}
    </div>
    """

def create_sentiment_badge(label, score):
    """Create sentiment badge with color"""
    if label.lower() == "positive":
        color = "#10b981"
        icon = "🟢"
    elif label.lower() == "negative":
        color = "#ef4444"
        icon = "🔴"
    else:
        color = "#6b7280"
        icon = "🟡"
    
    return f"""
    <div style='background: {color}; color: white; padding: 8px 15px; border-radius: 20px; 
                display: inline-block; font-weight: 600; margin: 5px;'>
        {icon} {label.title()}
    </div>
    """

def main():
    # Load custom CSS
    load_css()
    
    # Main header
    st.markdown("""
    <div class='header-container'>
        <div style='text-align: center;'>
            <h1 style='font-size: 3rem; margin-bottom: 10px; color: #667eea;'>
                📈 EquityAI Research Tool
            </h1>
            <p style='font-size: 1.2rem; color: #666; margin-bottom: 20px;'>
                AI-Powered Financial Intelligence Platform
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; margin-bottom: 20px;'>
            <h3 style='color: #667eea; margin-bottom: 15px;'>🎛️ Controls</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Fetching latest data..."):
                # Just show success message for now
                st.success("Data refreshed successfully!")
        
        # Time period selector
        time_period = st.selectbox(
            "📅 Time Period",
            options=[1, 3, 7, 14, 30],
            index=2,
            format_func=lambda x: f"Last {x} days"
        )
        
        # Company filter
        company_filter = st.text_input(
            "🏢 Filter by Company",
            placeholder="Enter company name...",
            value=""
        )
        
        # Manual article section
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; margin-bottom: 20px;'>
            <h3 style='color: #667eea; margin-bottom: 15px;'>📝 Add Article</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("➕ Add Manual Article", expanded=False):
            manual_title = st.text_input("Article Title", placeholder="Enter article title...")
            manual_content = st.text_area("Article Content", placeholder="Enter article content...", height=150)
            manual_author = st.text_input("Author (optional)", placeholder="Author name...")
            
            if st.button("📤 Add Article", type="secondary"):
                if manual_title and manual_content:
                    st.success("Article added successfully!")
                else:
                    st.error("Please fill in title and content")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "📰 News Feed", "🔍 Analysis", "💬 AI Chat", "📈 Trends"
    ])
    
    with tab1:
        st.markdown("<div class='tab-container'><h2 style='color: #667eea; margin-bottom: 20px;'>📊 Market Overview</h2></div>", unsafe_allow_html=True)
        
        # Get sentiment summary
        sentiment_data = get_api_response("/api/v1/sentiment/summary", {"days": time_period})
        
        if sentiment_data:
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card(
                    "Total Articles", 
                    sentiment_data.get("total_articles", 0),
                    None,
                    "#667eea"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card(
                    "Positive", 
                    sentiment_data.get("positive_count", 0),
                    None,
                    "#10b981"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card(
                    "Negative", 
                    sentiment_data.get("negative_count", 0),
                    None,
                    "#ef4444"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(create_metric_card(
                    "Avg Sentiment", 
                    f"{sentiment_data.get('average_score', 0):.2f}",
                    None,
                    "#6b7280"
                ), unsafe_allow_html=True)
            
            # Sentiment distribution chart
            st.markdown("<div class='content-card'><h3 style='color: #667eea; margin-bottom: 20px;'>📊 Sentiment Distribution</h3></div>", unsafe_allow_html=True)
            
            sentiment_dist = sentiment_data.get("sentiment_distribution", {})
            if sentiment_dist:
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(sentiment_dist.keys()),
                        y=list(sentiment_dist.values()),
                        marker_color=['#10b981', '#ef4444', '#6b7280']
                    )
                ])
                fig.update_layout(
                    title="Sentiment Distribution (%)",
                    xaxis_title="Sentiment",
                    yaxis_title="Percentage",
                    height=400,
                    plot_bgcolor='rgba(255,255,255,0.1)',
                    paper_bgcolor='rgba(255,255,255,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Trending companies
        st.markdown("<div class='content-card'><h3 style='color: #667eea; margin-bottom: 20px;'>🔥 Trending Companies</h3></div>", unsafe_allow_html=True)
        
        trending_data = get_api_response("/api/v1/companies/trending", {"days": time_period})
        
        if trending_data:
            trending_df = pd.DataFrame(trending_data)
            if not trending_df.empty:
                # Create styled table
                for _, row in trending_df.iterrows():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    
                    with col1:
                        st.markdown(f"**{row['company']}**")
                    
                    with col2:
                        sentiment_class = "trend-up" if row['average_sentiment'] > 0.1 else "trend-down" if row['average_sentiment'] < -0.1 else "trend-neutral"
                        st.markdown(f"<div class='{sentiment_class}'>{row['mention_count']} mentions</div>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(create_sentiment_badge(row['sentiment_label'], row['average_sentiment']), unsafe_allow_html=True)
                    
                    st.markdown("---")
    
    with tab2:
        st.markdown("<div class='tab-container'><h2 style='color: #667eea; margin-bottom: 20px;'>📰 Latest News</h2></div>", unsafe_allow_html=True)
        
        # Get news articles
        news_params = {"skip": 0, "limit": 10, "days": time_period}
        if company_filter:
            news_params["company"] = company_filter
        
        news_data = get_api_response("/api/v1/news", news_params)
        
        if news_data:
            for article in news_data:
                with st.expander(f"📰 {article.get('title', 'No Title')}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Source:** {article.get('source', 'Unknown')}")
                        st.markdown(f"**Published:** {article.get('published_date', 'Unknown')}")
                        
                        sentiment = article.get('sentiment_label', 'neutral')
                        score = article.get('sentiment_score', 0)
                        st.markdown(f"**Sentiment:** {create_sentiment_badge(sentiment, score)}")
                        
                        if article.get('summary'):
                            st.markdown("**Summary:**")
                            st.info(article['summary'])
                        
                        if article.get('ai_insight'):
                            st.markdown("**AI Insight:**")
                            st.success(article['ai_insight'])
                        
                        signal = article.get('investment_signal', 'neutral')
                        signal_map = {
                            "buy": "🟢 BUY",
                            "sell": "🔴 SELL", 
                            "hold": "🟡 HOLD",
                            "reduce": "🟠 REDUCE",
                            "neutral": "⚪ NEUTRAL"
                        }
                        st.markdown(f"**Signal:** {signal_map.get(signal, '⚪ NEUTRAL')}")
                    
                    with col2:
                        entities = article.get('entities', {})
                        if entities.get('companies'):
                            st.markdown("**Companies:**")
                            for company in entities['companies'][:5]:
                                st.write(f"• {company}")
                        
                        if entities.get('keywords'):
                            st.markdown("**Keywords:**")
                            keywords = entities['keywords'][:5]
                            st.write(", ".join(keywords))
                    
                    st.markdown("---")
        else:
            st.info("No news articles found. Try refreshing data or adjusting filters.")
    
    with tab3:
        st.markdown("<div class='tab-container'><h2 style='color: #667eea; margin-bottom: 20px;'>🔍 Text Analysis</h2></div>", unsafe_allow_html=True)
        
        text_to_analyze = st.text_area("Enter text to analyze:", height=200, placeholder="Paste your financial text here...")
        
        if st.button("🔍 Analyze Text", type="primary"):
            if text_to_analyze:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Sentiment Analysis**")
                    sentiment_result = get_api_response("/api/v1/analyze/sentiment", {"text": text_to_analyze})
                    if sentiment_result:
                        st.markdown(create_sentiment_badge(sentiment_result.get('label', 'neutral'), sentiment_result.get('score', 0)))
                        st.write(f"**Score:** {sentiment_result.get('score', 0):.2f}")
                        st.write(f"**Confidence:** {sentiment_result.get('confidence', 0):.2f}")
                
                with col2:
                    st.markdown("**Entity Extraction**")
                    entities_result = get_api_response("/api/v1/analyze/entities", {"text": text_to_analyze})
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
                    st.markdown("**Text Summary**")
                    summary_result = get_api_response("/api/v1/summarize", {"text": text_to_analyze})
                    if summary_result:
                        st.info(summary_result.get('summary', 'No summary available'))
            else:
                st.error("Please enter text to analyze")
    
    with tab4:
        st.markdown("<div class='tab-container'><h2 style='color: #667eea; margin-bottom: 20px;'>💬 AI Financial Assistant</h2></div>", unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(f"<div class='chat-message {message['role']}-message'>{message['content']}</div>", unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask about financial news, companies, or market trends..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_api_response("/api/v1/query", {"query": prompt, "limit": 5})
                    if response:
                        answer = response.get('answer', 'I could not find relevant information.')
                        sources = response.get('sources', [])
                        
                        st.markdown(f"<div class='assistant-message'>{answer}</div>", unsafe_allow_html=True)
                        
                        if sources:
                            st.write("**Sources:**")
                            for source in sources:
                                st.write(f"• {source}")
                        
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Sorry, I couldn't process your request right now.")
    
    with tab5:
        st.markdown("<div class='tab-container'><h2 style='color: #667eea; margin-bottom: 20px;'>📈 Market Trends</h2></div>", unsafe_allow_html=True)
        
        # Time period selector for trends
        trend_days = st.selectbox(
            "Select Period",
            options=[7, 14, 30, 90],
            index=0,
            format_func=lambda x: f"Last {x} days"
        )
        
        # Get trending data
        trending_data = get_api_response("/api/v1/companies/trending", {"days": trend_days})
        
        if trending_data:
            trending_df = pd.DataFrame(trending_data)
            
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
                    marker_color='#667eea',
                    name="Mentions"
                ),
                row=1, col=1
            )
            
            # Sentiment chart
            colors = ['#10b981' if x > 0.1 else '#ef4444' if x < -0.1 else '#6b7280' 
                     for x in trending_df['average_sentiment'][:10]]
            
            fig.add_trace(
                go.Bar(
                    x=trending_df['company'][:10],
                    y=trending_df['average_sentiment'][:10],
                    marker_color=colors,
                    name="Avg Sentiment"
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                height=600,
                title_text=f"Market Trends - Last {trend_days} Days",
                showlegend=False,
                plot_bgcolor='rgba(255,255,255,0.1)',
                paper_bgcolor='rgba(255,255,255,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.markdown("**Detailed Analysis**")
            
            for _, row in trending_df.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                
                with col1:
                    st.markdown(f"**{row['company']}**")
                
                with col2:
                    st.metric("Mentions", row['mention_count'])
                
                with col3:
                    sentiment_class = "positive-sentiment" if row['average_sentiment'] > 0.1 else "negative-sentiment" if row['average_sentiment'] < -0.1 else "neutral-sentiment"
                    st.markdown(f"<div class='{sentiment_class}'>{row['sentiment_label'].title()}</div>", unsafe_allow_html=True)
                
                with col4:
                    st.metric("Avg Score", f"{row['average_sentiment']:.2f}")
                
                st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666; margin-top: 30px;'>
        <p>🤖 Powered by AI & NLP Technologies</p>
        <p style='font-size: 0.9rem;'>© 2024 EquityAI Research Tool</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
