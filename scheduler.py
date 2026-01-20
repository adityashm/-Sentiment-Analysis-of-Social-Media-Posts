import schedule
import time
from scraper import WebScraper
from database import delete_old_data
import logging

logger = logging.getLogger(__name__)

def scheduled_scrape():
    """Run scrape task"""
    scraper = WebScraper()
    scraper.scrape_all()

def cleanup_old_data():
    """Delete data older than 30 days"""
    logger.info("Running cleanup task...")
    delete_old_data(days=30)
    logger.info("Cleanup complete")

def main():
    """Setup and run scheduler"""
    scraper = WebScraper()
    
    # Schedule tasks
    schedule.every().day.at("10:00").do(scheduled_scrape)
    schedule.every().day.at("02:00").do(cleanup_old_data)
    
    logger.info("Scheduler started. Waiting for scheduled tasks...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    main()
