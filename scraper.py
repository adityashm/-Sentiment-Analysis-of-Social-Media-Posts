import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from database import create_database, insert_article, insert_job
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        create_database()
    
    def scrape_tech_news(self):
        """Scrape tech news from HackerNews-like sites"""
        logger.info("Starting tech news scrape...")
        try:
            # Example: Scrape from a public API or website
            url = "https://news.ycombinator.com"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            stories = soup.select('.athing')[:10]  # Get top 10
            
            count = 0
            for story in stories:
                try:
                    title_elem = story.select_one('.titleline > a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text()
                    url = title_elem.get('href', '')
                    
                    if insert_article(
                        title=title,
                        description="Tech news from HackerNews",
                        url=url,
                        author="HackerNews",
                        publish_date=datetime.now().isoformat(),
                        category="Technology"
                    ):
                        count += 1
                        logger.info(f"Inserted: {title}")
                except Exception as e:
                    logger.error(f"Error processing story: {e}")
                    continue
            
            logger.info(f"Successfully scraped {count} articles")
            return count
        except Exception as e:
            logger.error(f"Error scraping tech news: {e}")
            return 0
    
    def scrape_python_jobs(self):
        """Scrape Python job listings"""
        logger.info("Starting Python jobs scrape...")
        try:
            # Example structure for job scraping
            # In production, you would use actual job board APIs
            jobs_data = [
                {
                    'title': 'Senior Python Developer',
                    'company': 'TechCorp',
                    'location': 'Remote',
                    'job_type': 'Full-time',
                    'salary': '$120,000 - $150,000',
                    'description': 'Looking for experienced Python developer...',
                    'url': 'https://example.com/jobs/1'
                },
                {
                    'title': 'Python Backend Engineer',
                    'company': 'StartupXYZ',
                    'location': 'San Francisco, CA',
                    'job_type': 'Full-time',
                    'salary': '$100,000 - $130,000',
                    'description': 'Build scalable backend systems...',
                    'url': 'https://example.com/jobs/2'
                }
            ]
            
            count = 0
            for job in jobs_data:
                if insert_job(
                    title=job['title'],
                    company=job['company'],
                    location=job['location'],
                    job_type=job['job_type'],
                    salary=job['salary'],
                    description=job['description'],
                    url=job['url']
                ):
                    count += 1
                    logger.info(f"Inserted: {job['title']} at {job['company']}")
            
            logger.info(f"Successfully scraped {count} jobs")
            return count
        except Exception as e:
            logger.error(f"Error scraping jobs: {e}")
            return 0
    
    def scrape_all(self):
        """Run all scrapers"""
        logger.info("="*50)
        logger.info("Starting complete scrape cycle")
        logger.info("="*50)
        
        articles = self.scrape_tech_news()
        time.sleep(2)  # Respectful delay
        
        jobs = self.scrape_python_jobs()
        
        logger.info("="*50)
        logger.info(f"Scrape cycle complete. Articles: {articles}, Jobs: {jobs}")
        logger.info("="*50)

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape_all()
