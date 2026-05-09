# 📈 EquityLens: Intelligent Equity Research Tool

EquityLens is an advanced AI-powered platform that combines **Natural Language Processing (NLP)** and **Generative AI** to analyze financial text data (news, reports, earnings) and generate actionable investment insights.

## 🎯 Project Overview
In fast-paced financial markets, processing massive volumes of unstructured text is a major challenge. EquityLens automates this by:
- **Sentiment Analysis**: Determining bullish/bearish market impact.
- **Entity Extraction**: Identifying company names, organizations, and key persons.
- **Generative Summarization**: Condensing long articles into concise, info-rich summaries using Transformer models.
- **AI Chatbot**: Providing a RAG-based assistant to answer specific financial queries.

## 🧠 Generative AI & NLP Models
- **Summarization**: `facebook/bart-large-cnn` (Primary) or `t5-small` (Fallback).
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`.
- **Entity Recognition**: `dbmdz/bert-large-cased-finetuned-conll03-english` and spaCy `en_core_web_sm`.
- **Insight Generation**: OpenAI GPT-3.5/4 (Optional) for natural language investment recommendations.

### Prerequisites
- Python 3.8+
- [Optional] OpenAI API Key (for enhanced insights)
- [Optional] NewsAPI Key (for live news fetching)
