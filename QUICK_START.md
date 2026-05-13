# 🚀 Quick Start Guide

## Step 1: Setup Environment

### Option A: Automated Setup (Recommended)
```bash
# Run the automated setup script
python scripts/setup_environment.py
```

### Option B: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLP models
python -m spacy download en_core_web_sm

# 5. Create environment file
copy .env.example .env
```

## Step 2: Configure API Keys (Optional)

Edit the `.env` file to add your API keys:
```bash
# Open .env file and add:
NEWS_API_KEY=your_news_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Step 3: Start the Applications

### Start Backend API
```bash
cd backend
python run.py
```
The API will be available at: http://localhost:8000

### Start Frontend Dashboard
```bash
# Open a NEW terminal window
cd frontend
streamlit run app.py
```
The dashboard will be available at: http://localhost:8501

## Step 4: Access the Application

1. **Main Dashboard**: http://localhost:8501
2. **API Documentation**: http://localhost:8000/docs
3. **Health Check**: http://localhost:8000/api/v1/health

## Step 5: Test the System

1. Open the dashboard at http://localhost:8501
2. Click "🔄 Refresh Data" to fetch sample news
3. Try adding a manual article in the sidebar
4. Test the AI chat with financial questions

## Troubleshooting

### If you get import errors:
```bash
# Make sure you're in the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### If models don't download:
```bash
# Download spaCy model manually
python -m spacy download en_core_web_sm
```

### If API doesn't start:
```bash
# Check if port 8000 is available
# Try a different port in backend/run.py
```

## First Time Setup Notes

- **Model Downloads**: First run may take 5-10 minutes to download AI models
- **Sample Data**: The system includes sample financial news for testing
- **No API Keys Required**: The system works without API keys (with limited features)
