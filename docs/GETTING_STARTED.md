# 🚀 Getting Started - Quick Reference

## Complete Setup (5 minutes)

### 1️⃣ Install Dependencies
```bash
# Activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install all packages
pip install -r requirements.txt
```

### 2️⃣ Run the Project (Easy Way)
```bash
# One command to run everything (default: r/technology)
python scripts/quick_start.py

# Scrape a specific topic
python scripts/quick_start.py --subreddit geopolitics

# Scrape more posts
python scripts/quick_start.py --subreddit AI --limit 100

# Use different AI model
python scripts/quick_start.py --method transformers --sample

# Skip dashboard (just scrape and analyze)
python scripts/quick_start.py --subreddit science --no-dashboard
```

### 3️⃣ Run the Project (Step by Step)
```bash
# Step 1: Scrape social media posts
python src/social_scraper.py

# Step 2: Analyze sentiment
python scripts/analyze_sentiment.py --method vader

# Step 3: View dashboard
streamlit run dashboard.py
```

### 4️⃣ Use the Dashboard (NEW! 🔥)
**You can now scrape ANY topic directly from the dashboard!**

1. Open dashboard: `streamlit run dashboard.py`
2. In the sidebar, enter a subreddit/topic (e.g., "geopolitics", "crypto")
3. Click "Scrape & Analyze"
4. Watch real-time progress
5. View results instantly!

**Quick topic buttons:** science, AI, geopolitics, crypto

## 📚 What Each File Does

| File | Purpose |
|------|---------|
| `src/database.py` | Database operations (create, insert, query) |
| `src/social_scraper.py` | Scrape Reddit, Twitter, Hacker News |
| `src/sentiment_analyzer.py` | 3 AI models for sentiment analysis |
| `scripts/analyze_sentiment.py` | Main script to analyze all posts |
| `scripts/quick_start.py` | Run everything with CLI options |
| `scripts/examples.py` | Code examples and testing |
| `dashboard.py` | Interactive Streamlit web dashboard with topic search |

## 🎯 Common Commands

```bash
# Quick start with options (NEW!)
python scripts/quick_start.py --subreddit geopolitics --limit 50

# See examples and test the system
python scripts/examples.py

# Analyze with different AI models
python scripts/analyze_sentiment.py --method vader      # Fast, good for social media
python scripts/analyze_sentiment.py --method textblob   # Simple, general purpose
python scripts/analyze_sentiment.py --method transformers # Slow, most accurate

# Show sample results after analysis
python scripts/analyze_sentiment.py --sample

# Re-analyze all posts (overwrite existing analysis)
python scripts/analyze_sentiment.py --reanalyze
```

## 🔍 Verify Everything Works

```bash
# Test the sentiment analyzers
python sentiment_analyzer.py

# Check database functions
python -c "from database import get_sentiment_statistics; print(get_sentiment_statistics())"

# Run examples
python examples.py
```

## 📊 Dashboard Features

Once you run `streamlit run dashboard.py`, you'll see:

- **🔎 Topic Search**: Enter any subreddit and scrape instantly (NEW!)
- **Quick Buttons**: One-click access to science, AI, geopolitics, crypto
- **📊 Database Stats**: See what topics are in your database
- **Key Metrics**: Total posts, sentiment percentages
- **Charts**: Pie charts, bar charts, timelines
- **Word Clouds**: Visual representation of common words
- **Filters**: Filter by platform or sentiment
- **Export**: Download data as CSV
- **Real-time Progress**: Visual feedback during scraping

## ⚡ Quick Tips

1. **First time setup**: Run `python scripts/quick_start.py` - it does everything!
2. **Search any topic**: Use the dashboard sidebar - no code editing needed!
3. **Want more data**: Use `--limit` flag: `python scripts/quick_start.py --limit 100`
4. **Different topics**: Try geopolitics, AI, science, crypto, or any subreddit
5. **Transformers slow**: First run downloads ~500MB model, then it's faster
6. **Dashboard not updating**: Click "Scrape & Analyze" button or restart streamlit

## ❓ Troubleshooting

**Problem**: "No module named X"
**Solution**: `pip install -r requirements.txt`

**Problem**: "No posts found"
**Solution**: Run `python social_scraper.py` first

**Problem**: Dashboard empty
**Solution**: Run `python analyze_sentiment.py` after scraping

**Problem**: Transformers error
**Solution**: Install CPU version: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

## 🎓 Learn More

- Read full documentation: [README.md](README.md)
- See code examples: `python examples.py`
- Check individual file docstrings for detailed API

---
**You're all set! Run `python quick_start.py` to begin! 🎉**
