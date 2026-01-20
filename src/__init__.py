"""
Source package for Sentiment Analysis of Social Media Posts
Contains core modules: database, social_scraper, sentiment_analyzer
"""

__version__ = "1.0.0"
__author__ = "adityashm"

# Import main components for easier access
from .database import (
    create_database,
    insert_post,
    update_post_sentiment,
    get_all_posts,
    get_posts_by_platform,
    get_posts_by_sentiment,
    get_sentiment_statistics
)

from .sentiment_analyzer import SentimentAnalyzer, analyze_post
from .social_scraper import SocialMediaScraper

__all__ = [
    'create_database',
    'insert_post',
    'update_post_sentiment',
    'get_all_posts',
    'get_posts_by_platform',
    'get_posts_by_sentiment',
    'get_sentiment_statistics',
    'SentimentAnalyzer',
    'analyze_post',
    'SocialMediaScraper'
]
