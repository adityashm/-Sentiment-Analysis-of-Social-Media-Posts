"""
Example usage and testing script
Demonstrates all major features of the sentiment analysis system
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from database import (
    get_all_posts,
    get_posts_by_platform,
    get_posts_by_sentiment,
    get_sentiment_statistics
)
from sentiment_analyzer import SentimentAnalyzer, analyze_post

def test_sentiment_analyzers():
    """Test different sentiment analysis methods"""
    print("\n" + "="*70)
    print("TESTING SENTIMENT ANALYZERS")
    print("="*70)
    
    test_texts = [
        "I absolutely love this product! Best purchase ever! 😊",
        "This is terrible. Worst experience of my life.",
        "It's okay, nothing special.",
        "OMG this is amazing!!! 🔥🔥🔥",
        "Disappointed and frustrated. Would not recommend."
    ]
    
    for method in ['vader', 'textblob']:
        print(f"\n{method.upper()} Method:")
        print("-" * 70)
        
        try:
            analyzer = SentimentAnalyzer(method=method)
            
            for text in test_texts:
                result = analyzer.analyze(text)
                emoji = "😊" if result['label'] == 'positive' else "😢" if result['label'] == 'negative' else "😐"
                print(f"{emoji} {result['label']:8} ({result['score']:+.3f}) | {text[:40]}...")
                
        except ImportError as e:
            print(f"⚠️  {method} not available. Install with: pip install -r requirements.txt")
        except Exception as e:
            print(f"❌ Error: {e}")

def show_database_stats():
    """Show statistics from the database"""
    print("\n" + "="*70)
    print("DATABASE STATISTICS")
    print("="*70)
    
    try:
        stats = get_sentiment_statistics()
        
        if stats and stats[0] > 0:
            total, avg_sentiment, positive, negative, neutral = stats
            
            print(f"\n📊 Total Posts Analyzed: {total}")
            print(f"📈 Average Sentiment Score: {avg_sentiment:.3f}")
            print(f"\n   😊 Positive: {positive} ({positive/total*100:.1f}%)")
            print(f"   😐 Neutral:  {neutral} ({neutral/total*100:.1f}%)")
            print(f"   😢 Negative: {negative} ({negative/total*100:.1f}%)")
        else:
            print("\n⚠️  No analyzed posts found in database.")
            print("   Run: python analyze_sentiment.py")
            
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

def show_sample_posts():
    """Show sample posts from each sentiment category"""
    print("\n" + "="*70)
    print("SAMPLE POSTS BY SENTIMENT")
    print("="*70)
    
    for sentiment in ['positive', 'negative', 'neutral']:
        posts = get_posts_by_sentiment(sentiment, limit=3)
        
        emoji = "😊" if sentiment == 'positive' else "😢" if sentiment == 'negative' else "😐"
        print(f"\n{emoji} {sentiment.upper()} Posts:")
        print("-" * 70)
        
        if posts:
            for post in posts:
                platform = post[1]
                username = post[2]
                content = post[3]
                score = post[10]
                
                print(f"[{platform}] @{username}")
                print(f"Score: {score:.3f}")
                print(f"Content: {content[:100]}...")
                print()
        else:
            print(f"No {sentiment} posts found.\n")

def show_platform_breakdown():
    """Show posts count by platform"""
    print("\n" + "="*70)
    print("POSTS BY PLATFORM")
    print("="*70)
    
    platforms = ['twitter', 'reddit', 'hackernews']
    
    for platform in platforms:
        posts = get_posts_by_platform(platform, limit=1000)
        print(f"{platform.title():15} : {len(posts)} posts")

def main():
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║       SENTIMENT ANALYSIS SYSTEM - EXAMPLES & TESTING           ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Test sentiment analyzers
    test_sentiment_analyzers()
    
    # Show database statistics
    show_database_stats()
    
    # Show platform breakdown
    show_platform_breakdown()
    
    # Show sample posts
    show_sample_posts()
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
    1. View the interactive dashboard:
       streamlit run dashboard.py
    
    2. Scrape more posts:
       python social_scraper.py
    
    3. Analyze with different methods:
       python analyze_sentiment.py --method textblob
       python analyze_sentiment.py --method transformers
    
    4. Query specific data:
       python -c "from database import get_posts_by_sentiment; \\
                  posts = get_posts_by_sentiment('positive', 10); \\
                  print(posts)"
    """)

if __name__ == "__main__":
    main()
