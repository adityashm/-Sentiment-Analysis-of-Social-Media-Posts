"""
Social Media Scraper for Sentiment Analysis
Scrapes posts from various social media platforms and stores them for analysis
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
try:
    from .database import create_database, insert_post
except ImportError:
    from database import create_database, insert_post
import logging
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SocialMediaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        create_database()
    
    def scrape_reddit_posts(self, subreddit='python', limit=50):
        """
        Scrape posts from Reddit (using public JSON API)
        
        Args:
            subreddit: Subreddit name
            limit: Number of posts to fetch
        """
        logger.info(f"Scraping r/{subreddit}...")
        
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data['data']['children']
            
            count = 0
            for post_data in posts:
                try:
                    post = post_data['data']
                    
                    # Extract post information
                    title = post.get('title', '')
                    selftext = post.get('selftext', '')
                    content = f"{title}. {selftext}" if selftext else title
                    
                    post_id = insert_post(
                        platform='reddit',
                        username=post.get('author', 'unknown'),
                        content=content,
                        url=f"https://reddit.com{post.get('permalink', '')}",
                        likes=post.get('score', 0),
                        comments=post.get('num_comments', 0),
                        post_date=datetime.fromtimestamp(post.get('created_utc', 0)).isoformat()
                    )
                    
                    if post_id:
                        count += 1
                        logger.info(f"Inserted post: {title[:50]}...")
                    
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error processing post: {e}")
                    continue
            
            logger.info(f"Successfully scraped {count} posts from r/{subreddit}")
            return count
            
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
            return 0
    
    def scrape_hacker_news(self, limit=30):
        """
        Scrape posts from Hacker News
        
        Args:
            limit: Number of posts to fetch
        """
        logger.info("Scraping Hacker News...")
        
        try:
            url = "https://news.ycombinator.com"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            stories = soup.select('.athing')[:limit]
            
            count = 0
            for story in stories:
                try:
                    title_elem = story.select_one('.titleline > a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text()
                    story_url = title_elem.get('href', '')
                    
                    # Get the comment thread if available
                    story_id = story.get('id')
                    
                    post_id = insert_post(
                        platform='hackernews',
                        username='HN User',
                        content=title,
                        url=story_url if story_url.startswith('http') else f"https://news.ycombinator.com/{story_url}",
                        likes=0,
                        comments=0,
                        post_date=datetime.now().isoformat()
                    )
                    
                    if post_id:
                        count += 1
                        logger.info(f"Inserted: {title[:50]}...")
                    
                except Exception as e:
                    logger.error(f"Error processing story: {e}")
                    continue
            
            logger.info(f"Successfully scraped {count} posts from Hacker News")
            return count
            
        except Exception as e:
            logger.error(f"Error scraping Hacker News: {e}")
            return 0
    
    def load_sample_twitter_data(self):
        """
        Load sample Twitter-like data for demonstration
        (Real Twitter scraping requires API access)
        """
        logger.info("Loading sample Twitter-like data...")
        
        sample_tweets = [
            {
                'username': 'tech_enthusiast',
                'content': 'Just tried the new AI model and it\'s absolutely incredible! The performance is mind-blowing! 🚀',
                'likes': 245,
                'shares': 42,
                'comments': 18
            },
            {
                'username': 'frustrated_user',
                'content': 'This service is terrible. Customer support hasn\'t responded in 3 days. Extremely disappointed.',
                'likes': 89,
                'shares': 15,
                'comments': 34
            },
            {
                'username': 'neutral_observer',
                'content': 'The new update is out. Some features added, some removed. Mixed feelings about it.',
                'likes': 56,
                'shares': 8,
                'comments': 12
            },
            {
                'username': 'happy_customer',
                'content': 'Best purchase I\'ve made this year! Highly recommend to everyone! Worth every penny! ⭐⭐⭐⭐⭐',
                'likes': 312,
                'shares': 67,
                'comments': 45
            },
            {
                'username': 'angry_reviewer',
                'content': 'Worst experience ever. Product broke after 2 days. Don\'t waste your money!!!',
                'likes': 134,
                'shares': 28,
                'comments': 56
            },
            {
                'username': 'product_lover',
                'content': 'I love how smooth and efficient this is. Makes my work so much easier! Great job team! 👏',
                'likes': 198,
                'shares': 34,
                'comments': 22
            },
            {
                'username': 'disappointed_buyer',
                'content': 'Expected more for the price. Quality is mediocre at best. Not impressed.',
                'likes': 78,
                'shares': 12,
                'comments': 19
            },
            {
                'username': 'excited_fan',
                'content': 'OMG! This is AMAZING!!! Can\'t believe how good this is! Exceeded all expectations! 🔥🔥🔥',
                'likes': 467,
                'shares': 89,
                'comments': 76
            },
            {
                'username': 'casual_user',
                'content': 'It\'s okay. Does what it says on the box. Nothing extraordinary but gets the job done.',
                'likes': 45,
                'shares': 5,
                'comments': 8
            },
            {
                'username': 'tech_critic',
                'content': 'Buggy software, poor documentation, terrible user interface. Needs major improvements.',
                'likes': 167,
                'shares': 43,
                'comments': 91
            },
            {
                'username': 'satisfied_customer',
                'content': 'Really happy with this purchase. Quality is excellent and delivery was fast. 5 stars!',
                'likes': 234,
                'shares': 38,
                'comments': 29
            },
            {
                'username': 'skeptical_user',
                'content': 'Not sure if this lives up to the hype. Seems overrated to me. Time will tell.',
                'likes': 92,
                'shares': 14,
                'comments': 27
            },
            {
                'username': 'enthusiastic_reviewer',
                'content': 'Absolutely fantastic! This has changed my life! Everyone needs to try this! 🎉🎉',
                'likes': 389,
                'shares': 72,
                'comments': 54
            },
            {
                'username': 'unhappy_customer',
                'content': 'Save your money. This is a scam. Poor quality and terrible customer service.',
                'likes': 156,
                'shares': 34,
                'comments': 67
            },
            {
                'username': 'average_joe',
                'content': 'Meh. It\'s fine I guess. Nothing special but not terrible either.',
                'likes': 34,
                'shares': 3,
                'comments': 6
            }
        ]
        
        count = 0
        for tweet in sample_tweets:
            try:
                post_id = insert_post(
                    platform='twitter',
                    username=tweet['username'],
                    content=tweet['content'],
                    url=f"https://twitter.com/{tweet['username']}/status/sample",
                    likes=tweet.get('likes', 0),
                    shares=tweet.get('shares', 0),
                    comments=tweet.get('comments', 0),
                    post_date=datetime.now().isoformat()
                )
                
                if post_id:
                    count += 1
                    logger.info(f"Inserted sample tweet from @{tweet['username']}")
                    
            except Exception as e:
                logger.error(f"Error inserting sample data: {e}")
        
        logger.info(f"Successfully loaded {count} sample tweets")
        return count
    
    def scrape_all(self):
        """Scrape from all available sources"""
        logger.info("Starting comprehensive scraping...")
        
        total = 0
        
        # Load sample data
        total += self.load_sample_twitter_data()
        
        # Scrape Reddit
        total += self.scrape_reddit_posts('technology', limit=25)
        total += self.scrape_reddit_posts('python', limit=25)
        
        # Scrape Hacker News
        total += self.scrape_hacker_news(limit=20)
        
        logger.info(f"Total posts scraped: {total}")
        return total


if __name__ == "__main__":
    scraper = SocialMediaScraper()
    scraper.scrape_all()
