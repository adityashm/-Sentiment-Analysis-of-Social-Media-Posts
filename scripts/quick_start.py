"""
Quick Start Guide
Run this script to execute the complete sentiment analysis pipeline
"""

import subprocess
import sys
import logging
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
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

def main():
    logger.info("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     SENTIMENT ANALYSIS OF SOCIAL MEDIA POSTS - QUICK START    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Scrape data
    if not run_command(f"{sys.executable} {project_root / 'src' / 'social_scraper.py'}", 
                       "Scraping Social Media Posts"):
        logger.error("Scraping failed. Exiting...")
        return
    
    # Step 2: Analyze sentiment
    if not run_command(f"{sys.executable} {project_root / 'scripts' / 'analyze_sentiment.py'} --method vader --sample", 
                      "Analyzing Sentiment (VADER)"):
        logger.error("Analysis failed. Exiting...")
        return
    
    # Step 3: Launch dashboard
    logger.info(f"\n{'='*60}")
    logger.info("LAUNCHING DASHBOARD")
    logger.info(f"{'='*60}\n")
    logger.info("🚀 Starting Streamlit dashboard...")
    logger.info("📊 Dashboard will open at: http://localhost:8501")
    logger.info("⚠️  Press Ctrl+C to stop the dashboard\n")
    
    run_command(f"{sys.executable} -m streamlit run {project_root / 'dashboard.py'}", "Dashboard")

if __name__ == "__main__":
    main()
