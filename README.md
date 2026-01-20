# 📊 Sentiment Analysis of Social Media Posts

A comprehensive Python-based sentiment analysis system that scrapes social media posts, analyzes their sentiment using multiple NLP models, and visualizes results through an interactive dashboard.

## ✨ Features

### 🎯 **NEW! User-Driven Topic Search**
- 🔎 **Search ANY topic** - Enter any subreddit directly in the dashboard
- 🚀 **One-click buttons** - Quick access to science, AI, geopolitics, crypto
- 📊 **Real-time progress** - Visual feedback during scraping and analysis
- 🎛️ **Adjustable limits** - Control number of posts (10-100)
- 💾 **Database stats** - See what topics are currently stored

### 🤖 **Core Features**
- 🌐 **Multi-Platform Scraping** - Collect posts from Reddit, Twitter (sample data), Hacker News
- 🤖 **Multiple AI Models** - VADER, TextBlob, and Transformer-based sentiment analysis
- 💾 **SQLite Database** - Persistent storage with efficient querying
- 📊 **Interactive Dashboard** - Beautiful Streamlit web interface with charts and word clouds
- 📈 **Real-time Analytics** - Sentiment trends, platform comparisons, engagement metrics
- ⚡ **CLI Tools** - Flexible command-line options for power users
- 🔄 **Automated Pipeline** - Scrape → Analyze → Visualize workflow

## 🛠️ Tech Stack

- **Scraping**: BeautifulSoup4, Requests
- **Sentiment Analysis**: VADER, TextBlob, Transformers (RoBERTa)
- **Database**: SQLite3
- **Visualization**: Streamlit, Plotly, Matplotlib, WordCloud
- **Data Processing**: Pandas, NumPy

## 📋 Requirements

- Python 3.8+
- 2GB RAM minimum
- Internet connection (for scraping and downloading models)

## 🚀 Installation

### 1. Clone or Navigate to Project
```bash
cd "D:\downloads\Sentiment Analysis of Social Media Posts"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Installing transformers and torch may take several minutes and requires ~2GB download.

## 📖 Usage Guide

### 🚀 Quick Start (Recommended)

**Option 1: Dashboard (Easiest - No Code!)**
```bash
streamlit run dashboard.py
```
Then in the sidebar:
1. Enter any subreddit (e.g., "geopolitics", "AI", "science")
2. Click "🚀 Scrape & Analyze"
3. Watch real-time progress
4. View results instantly!

**Option 2: Command Line (Power Users)**
```bash
# Default (r/technology, 25 posts)
python scripts/quick_start.py

# Custom topic
python scripts/quick_start.py --subreddit geopolitics

# More posts, different AI model
python scripts/quick_start.py --subreddit AI --limit 100 --method transformers

# Just scrape and analyze (no dashboard)
python scripts/quick_start.py --subreddit science --no-dashboard
```

### 📝 Step-by-Step (Manual Control)

#### Step 1: Scrape Social Media Posts

```bash
python src/social_scraper.py
```

This will:
- Load 15 sample Twitter posts
- Scrape 25 posts from r/technology
- Scrape 25 posts from r/python  
- Scrape 20 posts from Hacker News

**Total**: ~85 posts stored in `src/scraped_data.db`

#### Step 2: Analyze Sentiment

```bash
# Using VADER (recommended for social media)
python scripts/analyze_sentiment.py --method vader

# Using TextBlob
python scripts/analyze_sentiment.py --method textblob

# Using Transformers (slower but more accurate)
python scripts/analyze_sentiment.py --method transformers

# Show sample results
python scripts/analyze_sentiment.py --sample
```

#### Step 3: View Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501` and display:
- 📈 Sentiment distribution charts
- 📊 Platform comparison analytics
- ☁️ Word clouds for each sentiment
- 🔝 Top posts by engagement
- 📋 Raw data export

## 🎯 Quick Start (All-in-One)

Run the complete pipeline:

```bash
# Method 1: Using main.py
python main.py

# Method 2: Using quick start script
python scripts/quick_start.py

# Or step by step:
# 1. Scrape posts
python src/social_scraper.py

# 2. Analyze sentiment
python scripts/analyze_sentiment.py --method vader --sample

# 3. View dashboard
streamlit run dashboard.py
```

## 📊 Project Structure

```
Sentiment-Analysis-of-Social-Media-Posts/
│
├── src/                         # Core source code
│   ├── __init__.py             # Package initialization
│   ├── database.py             # Database operations (SQLite)
│   ├── social_scraper.py       # Social media scraping module
│   └── sentiment_analyzer.py   # Multi-model sentiment analysis
│
├── scripts/                     # Executable scripts
│   ├── __init__.py             # Scripts package init
│   ├── analyze_sentiment.py    # Main analysis script
│   ├── quick_start.py          # One-command pipeline
│   └── examples.py             # Usage examples and tests
│
├── docs/                        # Documentation
│   ├── GETTING_STARTED.md      # Quick start guide
│   └── PROJECT_SUMMARY.md      # Project overview
│
├── main.py                      # Main entry point
├── dashboard.py                 # Streamlit visualization dashboard
├── setup.py                     # Package setup configuration
├── pyproject.toml              # Modern Python packaging
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                  # Git ignore patterns
└── scraped_data.db             # SQLite database (created after first run)
```

## 🎓 Sentiment Analysis Methods

### 1. VADER (Recommended)
- **Best for**: Social media text with emojis, slang
- **Speed**: Very fast
- **Accuracy**: Good for informal text
- **Use when**: Analyzing tweets, Reddit posts, casual content

### 2. TextBlob
- **Best for**: General purpose sentiment
- **Speed**: Fast
- **Accuracy**: Good for formal text
- **Use when**: Analyzing news, articles, reviews

### 3. Transformers (RoBERTa)
- **Best for**: High accuracy requirements
- **Speed**: Slower (requires model download on first run)
- **Accuracy**: Excellent
- **Use when**: Research, production systems, maximum accuracy needed

## 📚 Database Schema

### Posts Table
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL,              -- reddit, twitter, hackernews
    username TEXT,                        -- Post author
    content TEXT NOT NULL,                -- Post text
    url TEXT UNIQUE,                      -- Post URL
    likes INTEGER DEFAULT 0,              -- Likes/upvotes
    shares INTEGER DEFAULT 0,             -- Shares/retweets
    comments INTEGER DEFAULT 0,           -- Comment count
    post_date TEXT,                       -- Original post date
    scraped_at TIMESTAMP,                 -- When scraped
    sentiment_score REAL,                 -- -1 to 1 scale
    sentiment_label TEXT,                 -- positive/negative/neutral
    analyzed_at TIMESTAMP                 -- When analyzed
);
```

## 🔧 Advanced Usage

### Query Database Programmatically

```python
from database import (
    get_all_posts,
    get_posts_by_platform,
    get_posts_by_sentiment,
    get_sentiment_statistics
)

# Get all posts
posts = get_all_posts(limit=100)

# Get Reddit posts only
reddit_posts = get_posts_by_platform('reddit', limit=50)

# Get positive posts
positive_posts = get_posts_by_sentiment('positive')

# Get statistics
stats = get_sentiment_statistics()
print(f"Total posts: {stats[0]}")
print(f"Average sentiment: {stats[1]:.3f}")
print(f"Positive: {stats[2]}, Negative: {stats[3]}, Neutral: {stats[4]}")
```

### Custom Sentiment Analysis

```python
import sys
from pathlib import Path
sys.path.insert(0, 'src')

from sentiment_analyzer import SentimentAnalyzer

# Initialize analyzer
analyzer = SentimentAnalyzer(method='vader')

# Analyze single text
result = analyzer.analyze("This product is amazing! I love it! 😊")
print(f"Sentiment: {result['label']} (Score: {result['score']:.3f})")

# Batch analysis
texts = ["Great!", "Terrible!", "It's okay"]
results = analyzer.batch_analyze(texts)
```

## 📈 Dashboard Features

### 1. Key Metrics
- Total posts analyzed
- Positive/Negative/Neutral percentages
- Average sentiment score

### 2. Visualizations
- Sentiment distribution pie chart
- Platform comparison bar chart
- Sentiment timeline
- Word clouds by sentiment

### 3. Filters
- Filter by platform
- Filter by sentiment
- Date range filtering (if available)

### 4. Data Export
- Download filtered results as CSV
- View raw data table

## 🤝 API Integration Examples

### Reddit API (Official)
```python
# Install: pip install praw
import praw

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='sentiment-analyzer'
)

for submission in reddit.subreddit('python').hot(limit=10):
    print(submission.title)
```

### Twitter API (Sample)

### Twitter API (Sample)
Currently uses sample data. For real Twitter scraping, use:
```python
# Install: pip install tweepy
import tweepy

client = tweepy.Client(bearer_token='YOUR_BEARER_TOKEN')
tweets = client.search_recent_tweets(query='python', max_results=10)
```

## 🐛 Troubleshooting

### Installation Issues

**Issue**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

**Issue**: Torch/Transformers installation fails
```bash
# Solution: Install CPU-only version
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers
```

### Runtime Issues

**Issue**: "No posts found in database"
```bash
# Solution: Run scraper first
python social_scraper.py
```

**Issue**: Dashboard shows empty charts
```bash
# Solution: Run sentiment analysis
python analyze_sentiment.py --method vader
```

## 🔮 Future Enhancements

- [ ] Real-time Twitter API integration
- [ ] Multi-language sentiment analysis
- [ ] Aspect-based sentiment analysis
- [ ] Export reports to PDF
- [ ] Email alerts for negative sentiment spikes
- [ ] Custom trained models for specific domains

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built for learning and demonstration purposes.

## 🙏 Acknowledgments

- **VADER Sentiment**: [vaderSentiment](https://github.com/cjhutto/vaderSentiment)
- **TextBlob**: [textblob](https://textblob.readthedocs.io/)
- **Transformers**: [Hugging Face](https://huggingface.co/)
- **Streamlit**: [streamlit.io](https://streamlit.io/)

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review code comments in individual files
3. Ensure all dependencies are installed

---

**Happy Analyzing! 📊😊**
