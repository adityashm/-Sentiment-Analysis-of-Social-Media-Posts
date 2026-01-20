"""
Main Sentiment Analysis Script
Analyzes sentiment for all posts in the database
"""

import logging
import sys
from pathlib import Path
import argparse
from tqdm import tqdm

# Add project root and src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Now import from src
try:
    from src.database import get_all_posts, update_post_sentiment
    from src.sentiment_analyzer import SentimentAnalyzer
except ImportError:
    # Fallback for direct imports
    from database import get_all_posts, update_post_sentiment
    from sentiment_analyzer import SentimentAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def analyze_all_posts(method='vader', reanalyze=False):
    """
    Analyze sentiment for all posts in the database
    
    Args:
        method: Sentiment analysis method ('vader', 'textblob', 'transformers')
        reanalyze: If True, reanalyze posts that already have sentiment scores
    """
    logger.info(f"Starting sentiment analysis using {method.upper()} method...")
    
    # Initialize analyzer
    try:
        analyzer = SentimentAnalyzer(method=method)
    except Exception as e:
        logger.error(f"Failed to initialize analyzer: {e}")
        logger.info("Please install required libraries: pip install -r requirements.txt")
        return
    
    # Get all posts
    posts = get_all_posts(limit=10000)
    
    if not posts:
        logger.warning("No posts found in database. Please run the scraper first.")
        logger.info("Run: python social_scraper.py")
        return
    
    logger.info(f"Found {len(posts)} posts in database")
    
    # Analyze each post
    analyzed_count = 0
    skipped_count = 0
    error_count = 0
    
    for post in tqdm(posts, desc="Analyzing posts"):
        post_id = post[0]
        content = post[3]
        existing_sentiment = post[10]  # sentiment_score column
        
        # Skip if already analyzed (unless reanalyze flag is set)
        if existing_sentiment is not None and not reanalyze:
            skipped_count += 1
            continue
        
        try:
            # Analyze sentiment
            result = analyzer.analyze(content)
            score = result['score']
            label = result['label']
            
            # Update database
            update_post_sentiment(post_id, score, label)
            analyzed_count += 1
            
        except Exception as e:
            logger.error(f"Error analyzing post {post_id}: {e}")
            error_count += 1
            continue
    
    logger.info("=" * 60)
    logger.info("SENTIMENT ANALYSIS COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Total posts: {len(posts)}")
    logger.info(f"Analyzed: {analyzed_count}")
    logger.info(f"Skipped (already analyzed): {skipped_count}")
    logger.info(f"Errors: {error_count}")
    logger.info("=" * 60)
    
    if analyzed_count > 0:
        logger.info("\n✅ Analysis complete! View results:")
        logger.info("   1. Run dashboard: streamlit run dashboard.py")
        logger.info("   2. Query database: python -c \"from database import get_sentiment_statistics; print(get_sentiment_statistics())\"")


def display_sample_results(limit=10):
    """Display sample sentiment analysis results"""
    import sqlite3
    from src.database import DATABASE_FILE
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT platform, username, content, sentiment_label, sentiment_score
        FROM posts
        WHERE sentiment_label IS NOT NULL
        ORDER BY ABS(sentiment_score) DESC
        LIMIT ?
    ''', (limit,))
    
    posts = cursor.fetchall()
    conn.close()
    
    if not posts:
        logger.warning("No analyzed posts found.")
        return
    
    print("\n" + "=" * 80)
    print(f"SAMPLE SENTIMENT ANALYSIS RESULTS (Top {limit} by absolute score)")
    print("=" * 80)
    
    for i, post in enumerate(posts, 1):
        platform, username, content, label, score = post
        
        # Emoji indicator
        emoji = "😊" if label == 'positive' else "😢" if label == 'negative' else "😐"
        
        print(f"\n{i}. [{platform}] @{username}")
        print(f"   {emoji} Sentiment: {label.upper()} (Score: {score:.3f})")
        print(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze sentiment of social media posts")
    parser.add_argument(
        '--method',
        choices=['vader', 'textblob', 'transformers'],
        default='vader',
        help='Sentiment analysis method (default: vader)'
    )
    parser.add_argument(
        '--reanalyze',
        action='store_true',
        help='Reanalyze posts that already have sentiment scores'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Display sample results after analysis'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    analyze_all_posts(method=args.method, reanalyze=args.reanalyze)
    
    # Show sample results
    if args.sample:
        display_sample_results(limit=10)
