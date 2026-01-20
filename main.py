"""
Main entry point for the Sentiment Analysis application
Imports from the organized src/ structure
"""

# Add src directory to path
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Now import from src
try:
    from src.social_scraper import SocialMediaScraper
    from src.sentiment_analyzer import SentimentAnalyzer
    from src.database import get_sentiment_statistics
except ImportError:
    # Fallback for direct imports
    from social_scraper import SocialMediaScraper
    from sentiment_analyzer import SentimentAnalyzer
    from database import get_sentiment_statistics

def main():
    """Main application entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     SENTIMENT ANALYSIS OF SOCIAL MEDIA POSTS                  ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Choose an option:
    1. Scrape social media posts
    2. Analyze sentiment
    3. View statistics
    4. Run dashboard
    5. Run complete pipeline
    
    """)
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == '1':
        print("\n🌐 Starting social media scraper...")
        scraper = SocialMediaScraper()
        scraper.scrape_all()
        
    elif choice == '2':
        print("\n🤖 Running sentiment analysis...")
        import subprocess
        subprocess.run([sys.executable, 'scripts/analyze_sentiment.py', '--method', 'vader', '--sample'])
        
    elif choice == '3':
        print("\n📊 Sentiment Statistics:")
        stats = get_sentiment_statistics()
        if stats and stats[0] > 0:
            print(f"Total Posts: {stats[0]}")
            print(f"Average Sentiment: {stats[1]:.3f}")
            print(f"Positive: {stats[2]}, Negative: {stats[3]}, Neutral: {stats[4]}")
        else:
            print("No analyzed posts found. Run analysis first.")
            
    elif choice == '4':
        print("\n📊 Launching dashboard...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'dashboard.py'])
        
    elif choice == '5':
        print("\n🚀 Running complete pipeline...")
        import subprocess
        subprocess.run([sys.executable, 'scripts/quick_start.py'])
        
    else:
        print("Invalid choice. Please run again and select 1-5.")

if __name__ == "__main__":
    main()
