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
# One command to run everything
python quick_start.py
```

### 3️⃣ Run the Project (Step by Step)
```bash
# Step 1: Scrape social media posts
python social_scraper.py

# Step 2: Analyze sentiment
python analyze_sentiment.py --method vader

# Step 3: View dashboard
streamlit run dashboard.py
```

## 📚 What Each File Does

| File | Purpose |
|------|---------|
| `database.py` | Database operations (create, insert, query) |
| `social_scraper.py` | Scrape Reddit, Twitter, Hacker News |
| `sentiment_analyzer.py` | 3 AI models for sentiment analysis |
| `analyze_sentiment.py` | Main script to analyze all posts |
| `dashboard.py` | Interactive Streamlit web dashboard |
| `quick_start.py` | Run everything with one command |
| `examples.py` | Code examples and testing |
| `scheduler.py` | Optional: Schedule automatic scraping |

## 🎯 Common Commands

```bash
# See examples and test the system
python examples.py

# Analyze with different AI models
python analyze_sentiment.py --method vader      # Fast, good for social media
python analyze_sentiment.py --method textblob   # Simple, general purpose
python analyze_sentiment.py --method transformers # Slow, most accurate

# Show sample results after analysis
python analyze_sentiment.py --sample

# Re-analyze all posts (overwrite existing analysis)
python analyze_sentiment.py --reanalyze
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

- **Key Metrics**: Total posts, sentiment percentages
- **Charts**: Pie charts, bar charts, timelines
- **Word Clouds**: Visual representation of common words
- **Filters**: Filter by platform or sentiment
- **Export**: Download data as CSV

## ⚡ Quick Tips

1. **First time setup**: Run `python quick_start.py` - it does everything!
2. **Want more data**: Edit `social_scraper.py` to increase `limit` parameters
3. **Different subreddits**: Change `'technology'` and `'python'` in social_scraper.py
4. **Transformers slow**: First run downloads ~500MB model, then it's faster
5. **Dashboard not updating**: Refresh browser or restart streamlit

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
