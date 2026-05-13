# 📈 EquityAI Research Tool

A comprehensive AI-powered equity research platform that combines Natural Language Processing (NLP) and Generative AI to analyze financial text data and generate actionable investment insights.

## 🎯 Features

### Core Capabilities
- **📰 News Ingestion**: Fetch financial news from multiple sources (NewsAPI, RSS feeds)
- **🧠 NLP Analysis**: Sentiment analysis, named entity recognition, keyword extraction
- **🤖 AI Insights**: Generate summaries and investment recommendations using LLMs
- **📊 Interactive Dashboard**: Real-time visualization of market sentiment and trends
- **💬 AI Chatbot**: RAG-based financial assistant for answering queries
- **🔍 Advanced Search**: Filter news by company, sentiment, and time periods

### Technical Features
- **Backend**: FastAPI with async support
- **NLP Models**: Hugging Face Transformers, spaCy, NLTK
- **Database**: SQLAlchemy with PostgreSQL/MongoDB support
- **Frontend**: Streamlit with Plotly visualizations
- **AI Integration**: OpenAI GPT, Hugging Face models

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL or MongoDB (optional, defaults to SQLite)
- OpenAI API key (optional, for enhanced AI features)
- NewsAPI key (optional, for news fetching)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd EquityAI
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
# Backend dependencies
cd backend
pip install -r ../requirements.txt

# Frontend dependencies
cd ../frontend
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Download NLP models**
```bash
python -m spacy download en_core_web_sm
```

### Running the Application

1. **Start the backend API**
```bash
cd backend
python run.py
```
The API will be available at `http://localhost:8000`

2. **Start the frontend dashboard**
```bash
cd frontend
streamlit run app.py
```
The dashboard will be available at `http://localhost:8501`

3. **Access the application**
- Frontend Dashboard: http://localhost:8501
- API Documentation: http://localhost:8000/docs
- API Health Check: http://localhost:8000/api/v1/health

## 📁 Project Structure

```
EquityAI/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration
│   │   ├── database/      # Database models and connections
│   │   ├── models/        # SQLAlchemy models
│   │   ├── nlp/           # NLP processing modules
│   │   ├── services/      # Business logic services
│   │   └── utils/         # Utility functions
│   └── run.py             # Backend entry point
├── frontend/
│   ├── app.py             # Streamlit dashboard
│   └── requirements.txt   # Frontend dependencies
├── tests/
│   ├── test_api.py        # API tests
│   ├── test_nlp.py        # NLP component tests
│   └── sample_data.py     # Sample testing data
├── requirements.txt       # All dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# API Keys
NEWS_API_KEY=your_news_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/equity_ai
MONGODB_URL=mongodb://localhost:27017/equity_ai

# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:8500", "http://localhost:8000"]
```

### Database Setup

#### SQLite (Default)
No setup required - uses local file `equity_ai.db`

#### PostgreSQL
```bash
# Install PostgreSQL
# Create database
createdb equity_ai

# Update .env with connection string
DATABASE_URL=postgresql://username:password@localhost:5432/equity_ai
```

#### MongoDB
```bash
# Install MongoDB
# Update .env with connection string
MONGODB_URL=mongodb://localhost:27017/equity_ai
```

## 📊 API Documentation

### Core Endpoints

#### News Management
- `GET /api/v1/news` - Get news articles with filters
- `POST /api/v1/news/fetch` - Fetch news from external sources
- `POST /api/v1/news/manual` - Add manual article

#### Analysis
- `POST /api/v1/analyze/sentiment` - Analyze text sentiment
- `POST /api/v1/analyze/entities` - Extract entities from text
- `POST /api/v1/summarize` - Summarize text

#### AI Insights
- `POST /api/v1/insights/generate` - Generate investment insights
- `POST /api/v1/query` - Answer financial queries (RAG)
- `POST /api/v1/portfolio/insights` - Get portfolio analysis

#### Analytics
- `GET /api/v1/sentiment/summary` - Get sentiment summary
- `GET /api/v1/companies/trending` - Get trending companies
- `GET /api/v1/health` - Health check

### Example API Usage

```python
import requests

# Analyze sentiment
response = requests.post("http://localhost:8000/api/v1/analyze/sentiment", 
                        json={"text": "Apple stock is performing well today!"})
print(response.json())

# Get news
response = requests.get("http://localhost:8000/api/v1/news", 
                       params={"days": 7, "company": "Apple"})
print(response.json())

# Generate insights
article = {
    "title": "Apple Reports Record Earnings",
    "content": "Apple Inc. reported better-than-expected earnings..."
}
response = requests.post("http://localhost:8000/api/v1/insights/generate", 
                        json=article)
print(response.json())
```

## 🧪 Testing

### Run API Tests
```bash
cd tests
python test_api.py
```

### Run NLP Tests
```bash
cd tests
python test_nlp.py
```

### Generate Sample Data
```bash
cd tests
python sample_data.py
```

## 🎨 Dashboard Features

### Main Dashboard
- **Overview**: Real-time sentiment metrics and trending companies
- **News Feed**: Filtered news with AI-generated insights
- **Analysis**: Text analysis tools for custom content
- **AI Chat**: Interactive financial assistant
- **Trends**: Market sentiment visualizations

### Key Visualizations
- Sentiment distribution charts
- Company mention trends
- Sentiment score heatmaps
- Time-series sentiment analysis

## 🤖 AI Models Used

### Sentiment Analysis
- Primary: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Fallback: `distilbert-base-uncased-finetuned-sst-2-english`

### Named Entity Recognition
- Primary: `dbmdz/bert-large-cased-finetuned-conll03-english`
- Secondary: spaCy `en_core_web_sm`

### Text Summarization
- Primary: `facebook/bart-large-cnn`
- Fallback: `t5-small`

### Generative AI
- OpenAI GPT-3.5-turbo (for insights and chat)
- Rule-based fallback (when API unavailable)

## 🔍 Advanced Features

### Portfolio Analysis
```python
# Analyze portfolio companies
portfolio_data = {
    "companies": ["Apple", "Microsoft", "Google"]
}
response = requests.post("http://localhost:8000/api/v1/portfolio/insights", 
                        json=portfolio_data)
```

### Custom News Sources
Add RSS feeds in `.env`:
```bash
RSS_FEEDS=["https://feeds.finance.yahoo.com/rss/2.0/headline", 
          "https://www.cnbc.com/id/100003114/device/rss/rss.html",
          "https://your-custom-feed.com/rss"]
```

### Batch Processing
```python
# Process multiple articles
articles = [
    {"title": "Article 1", "content": "Content 1..."},
    {"title": "Article 2", "content": "Content 2..."}
]
for article in articles:
    response = requests.post("http://localhost:8000/api/v1/news/manual", 
                            json=article)
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Download Errors**
   ```bash
   # Ensure internet connection for first-time model downloads
   python -c "from transformers import AutoModel; AutoModel.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest')"
   ```

2. **Database Connection Issues**
   ```bash
   # Check database URL in .env
   # For SQLite: DATABASE_URL=sqlite:///./equity_ai.db
   ```

3. **API Key Errors**
   ```bash
   # Verify API keys in .env file
   # Test NewsAPI: curl "https://newsapi.org/v2/everything?q=bitcoin&apiKey=YOUR_KEY"
   ```

4. **Memory Issues**
   ```bash
   # Reduce model size or use CPU instead of GPU
   # Update config to use smaller models
   ```

### Performance Optimization

1. **Caching**: Enable Redis for API response caching
2. **Batch Processing**: Use batch endpoints for multiple analyses
3. **Model Quantization**: Use quantized models for faster inference
4. **Database Indexing**: Ensure proper indexes on frequently queried fields

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for NLP models
- OpenAI for GPT API
- Streamlit for frontend framework
- FastAPI for backend framework
- Financial news sources and APIs

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section

---

**Built with ❤️ using AI and NLP technologies**
