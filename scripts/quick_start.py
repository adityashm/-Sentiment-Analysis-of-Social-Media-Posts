"""
Quick Start Guide
Run this script to execute the complete sentiment analysis pipeline
"""

import subprocess
import sys
import logging
import argparse
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"\n{'='*60}")
    logger.info(f"STEP: {description}")
    logger.info(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        logger.info(f"✅ {description} - COMPLETED\n")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} - FAILED")
        logger.error(f"Error: {e}")
        return False

def parse_args():
    parser = argparse.ArgumentParser(description="Run scraping, sentiment analysis, and dashboard")
    parser.add_argument("--subreddit", default="technology", help="Subreddit/topic to scrape (default: technology)")
    parser.add_argument("--limit", type=int, default=25, help="Number of Reddit posts to fetch (default: 25)")
    parser.add_argument("--method", choices=["vader", "textblob", "transformers"], default="vader", help="Sentiment model to use")
    parser.add_argument("--sample", action="store_true", help="Show sample results after analysis")
    parser.add_argument("--no-dashboard", action="store_true", help="Skip launching the Streamlit dashboard")
    return parser.parse_args()


def main():
    args = parse_args()
    logger.info("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     SENTIMENT ANALYSIS OF SOCIAL MEDIA POSTS - QUICK START    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Scrape data
    scrape_cmd = (
        f'"{sys.executable}" -c '
        f'"from src.social_scraper import SocialMediaScraper; '
        f'SocialMediaScraper().scrape_reddit_posts(\"{args.subreddit}\", limit={args.limit})"'
    )
    if not run_command(scrape_cmd, 
                       f"Scraping r/{args.subreddit} (limit={args.limit})"):
        logger.error("Scraping failed. Exiting...")
        return
    
    # Step 2: Analyze sentiment
    analyze_cmd = f'"{sys.executable}" "{project_root / "scripts" / "analyze_sentiment.py"}" --method {args.method}'
    if args.sample:
        analyze_cmd += " --sample"
    if not run_command(analyze_cmd, 
                      f"Analyzing Sentiment ({args.method.upper()})"):
        logger.error("Analysis failed. Exiting...")
        return
    
    # Step 3: Launch dashboard (optional)
    if args.no_dashboard:
        logger.info("Dashboard launch skipped (--no-dashboard)")
        return

    logger.info(f"\n{'='*60}")
    logger.info("LAUNCHING DASHBOARD")
    logger.info(f"{'='*60}\n")
    logger.info("🚀 Starting Streamlit dashboard...")
    logger.info("📊 Dashboard will open at: http://localhost:8501")
    logger.info("⚠️  Press Ctrl+C to stop the dashboard\n")
    
    run_command(f'"{sys.executable}" -m streamlit run "{project_root / "dashboard.py"}"', "Dashboard")

if __name__ == "__main__":
    main()
