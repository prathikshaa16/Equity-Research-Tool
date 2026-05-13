import json
from datetime import datetime, timedelta

# Sample financial news articles for testing
SAMPLE_ARTICLES = [
    {
        "title": "Apple Reports Record Q4 Earnings, Stock Surges 5%",
        "content": "Apple Inc. (AAPL) reported better-than-expected fourth quarter earnings, driven by strong iPhone sales and growing services revenue. The tech giant posted earnings per share of $1.26, beating analysts' estimates of $1.01. Revenue came in at $89.5 billion, exceeding expectations of $87.6 billion. CEO Tim Cook expressed optimism about the upcoming quarter, citing strong demand for the new iPhone 15 and continued growth in the services segment. The company's stock jumped more than 5% in after-hours trading, reflecting investor confidence in Apple's ability to navigate challenging market conditions.",
        "source": "Financial Times",
        "author": "Sarah Johnson",
        "published_date": (datetime.now() - timedelta(days=1)).isoformat(),
        "url": "https://example.com/apple-earnings"
    },
    {
        "title": "Tesla Faces Production Challenges, Stock Declines",
        "content": "Tesla Inc. (TSLA) is facing production challenges at its Gigafactory in Berlin, leading to concerns about meeting delivery targets for the current quarter. The electric vehicle manufacturer announced that production has been temporarily slowed due to supply chain disruptions and regulatory hurdles. CEO Elon Musk addressed the issues on social media, stating that the company is working diligently to resolve the problems and expects to be back at full capacity within weeks. The news caused Tesla's stock to decline by 3% in pre-market trading, as investors worry about the potential impact on quarterly earnings.",
        "source": "Reuters",
        "author": "Michael Chen",
        "published_date": (datetime.now() - timedelta(days=2)).isoformat(),
        "url": "https://example.com/tesla-production"
    },
    {
        "title": "Microsoft Announces Major AI Partnership with OpenAI",
        "content": "Microsoft Corporation (MSFT) announced a landmark multi-year partnership with OpenAI, significantly expanding their collaboration on artificial intelligence research and development. The deal, valued at over $10 billion, will give Microsoft exclusive access to OpenAI's cutting-edge technology and will integrate advanced AI capabilities across Microsoft's product suite, including Office 365, Azure, and Bing. CEO Satya Nadella described the partnership as a 'game-changer' for the industry and emphasized Microsoft's commitment to responsible AI development. The announcement was met with enthusiasm from investors, with Microsoft shares rising 2% in early trading.",
        "source": "TechCrunch",
        "author": "Emily Rodriguez",
        "published_date": (datetime.now() - timedelta(days=3)).isoformat(),
        "url": "https://example.com/microsoft-openai"
    },
    {
        "title": "Amazon Expands Healthcare Division with New Acquisition",
        "content": "Amazon.com Inc. (AMZN) announced the acquisition of healthcare technology startup HealthTech Solutions for $3.9 billion, marking the e-commerce giant's latest move into the healthcare sector. The acquisition will strengthen Amazon's position in the digital health market and complement its existing healthcare services, including Amazon Pharmacy and Amazon Care. The deal is expected to close in the second quarter of next year, subject to regulatory approval. Amazon CEO Andy Jassy stated that healthcare represents a significant opportunity for innovation and that the company is committed to making healthcare more accessible and affordable for customers.",
        "source": "Bloomberg",
        "author": "David Kim",
        "published_date": (datetime.now() - timedelta(days=4)).isoformat(),
        "url": "https://example.com/amazon-healthcare"
    },
    {
        "title": "Federal Reserve Signals Potential Rate Cuts in 2024",
        "content": "The Federal Reserve indicated that it may begin cutting interest rates in 2024, citing easing inflation pressures and a cooling labor market. Fed Chair Jerome Powell stated that while the central bank remains committed to bringing inflation down to its 2% target, recent economic data suggests that the current monetary policy stance may be sufficient to achieve this goal. Markets reacted positively to the news, with major stock indices reaching new highs. Treasury yields declined, and the dollar weakened against major currencies as investors priced in the possibility of lower rates in the coming year.",
        "source": "Wall Street Journal",
        "author": "Robert Thompson",
        "published_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "url": "https://example.com/fed-rates"
    },
    {
        "title": "Google Parent Alphabet Faces Antitrust Lawsuit",
        "content": "Alphabet Inc. (GOOGL) is facing a new antitrust lawsuit from the Department of Justice, alleging that the company has abused its dominant position in the digital advertising market. The lawsuit claims that Google's ad tech practices have harmed competition and led to higher prices for advertisers and publishers. The company has denied the allegations and stated that it will vigorously defend its business practices. Legal experts suggest that this could be one of the most significant antitrust cases in recent years, with potential implications for the broader tech industry. Alphabet's stock remained relatively stable, as investors had largely priced in the possibility of regulatory action.",
        "source": "New York Times",
        "author": "Lisa Anderson",
        "published_date": (datetime.now() - timedelta(days=6)).isoformat(),
        "url": "https://example.com/google-antitrust"
    }
]

def get_sample_articles():
    """Return sample articles for testing"""
    return SAMPLE_ARTICLES

def save_sample_data(filename="sample_articles.json"):
    """Save sample data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(SAMPLE_ARTICLES, f, indent=2, default=str)
    print(f"Sample data saved to {filename}")

if __name__ == "__main__":
    save_sample_data()
