"""
Sentiment Analysis Dashboard using Streamlit
Interactive web interface for visualizing sentiment analysis results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import datetime
import sqlite3

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

# Import from src
try:
    from src.database import (
        get_all_posts, 
        get_posts_by_platform, 
        get_posts_by_sentiment,
        get_sentiment_statistics,
        DATABASE_FILE
    )
except ImportError:
    # Fallback for direct imports
    from database import (
        get_all_posts, 
        get_posts_by_platform, 
        get_posts_by_sentiment,
        get_sentiment_statistics,
        DATABASE_FILE
    )


# Page configuration
st.set_page_config(
    page_title="Social Media Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- USER SCRAPING SECTION ---
st.sidebar.header("🔎 Scrape New Topic")

# Topic input with suggestions
st.sidebar.markdown("**Popular Topics:**")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔬 science", use_container_width=True):
        st.session_state['subreddit'] = 'science'
    if st.button("🤖 AI", use_container_width=True):
        st.session_state['subreddit'] = 'artificial'
with col2:
    if st.button("🌍 geopolitics", use_container_width=True):
        st.session_state['subreddit'] = 'geopolitics'
    if st.button("💰 crypto", use_container_width=True):
        st.session_state['subreddit'] = 'cryptocurrency'

subreddit = st.sidebar.text_input(
    "Or enter any subreddit:", 
    value=st.session_state.get('subreddit', 'technology'),
    key='subreddit_input'
)
scrape_limit = st.sidebar.slider("Number of posts to scrape:", 10, 100, 25)
scrape_btn = st.sidebar.button("🚀 Scrape & Analyze", help="Scrape latest posts and analyze sentiment.", type="primary")

if scrape_btn and subreddit:
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    try:
        import subprocess
        
        # Step 1: Scrape
        status_text.text(f"Scraping r/{subreddit}...")
        progress_bar.progress(33)
        result1 = subprocess.run([
            sys.executable, "-c",
            f"from src.social_scraper import SocialMediaScraper; SocialMediaScraper().scrape_reddit_posts('{subreddit}', limit={scrape_limit})"
        ], capture_output=True, text=True)
        
        if result1.returncode != 0:
            st.sidebar.error(f"Scraping failed: {result1.stderr}")
        else:
            # Step 2: Analyze
            status_text.text("Analyzing sentiment...")
            progress_bar.progress(66)
            result2 = subprocess.run([
                sys.executable, str(project_root / "scripts" / "analyze_sentiment.py"), 
                "--method", "vader"
            ], capture_output=True, text=True)
            
            if result2.returncode != 0:
                st.sidebar.error(f"Analysis failed: {result2.stderr}")
            else:
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                st.sidebar.success(f"Scraped {scrape_limit} posts from r/{subreddit}!")
                st.cache_data.clear()
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")


@st.cache_data(ttl=60)
def load_posts_data():
    """Load posts data from database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        query = """
            SELECT id, platform, username, content, url, likes, shares, comments,
                   post_date, scraped_at, sentiment_score, sentiment_label, analyzed_at
            FROM posts
            WHERE sentiment_label IS NOT NULL
            ORDER BY scraped_at DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def create_sentiment_distribution_chart(df):
    """Create pie chart for sentiment distribution"""
    sentiment_counts = df['sentiment_label'].value_counts()
    
    colors = {
        'positive': '#2ecc71',
        'neutral': '#95a5a6',
        'negative': '#e74c3c'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        marker=dict(colors=[colors.get(label, '#3498db') for label in sentiment_counts.index]),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        height=400
    )
    
    return fig


def create_platform_sentiment_chart(df):
    """Create grouped bar chart for sentiment by platform"""
    platform_sentiment = df.groupby(['platform', 'sentiment_label']).size().reset_index(name='count')
    
    fig = px.bar(
        platform_sentiment,
        x='platform',
        y='count',
        color='sentiment_label',
        barmode='group',
        color_discrete_map={
            'positive': '#2ecc71',
            'neutral': '#95a5a6',
            'negative': '#e74c3c'
        },
        title="Sentiment Distribution by Platform"
    )
    
    fig.update_layout(height=400)
    return fig


def create_sentiment_timeline(df):
    """Create timeline chart showing sentiment over time"""
    df['scraped_date'] = pd.to_datetime(df['scraped_at']).dt.date
    timeline = df.groupby(['scraped_date', 'sentiment_label']).size().reset_index(name='count')
    
    fig = px.line(
        timeline,
        x='scraped_date',
        y='count',
        color='sentiment_label',
        color_discrete_map={
            'positive': '#2ecc71',
            'neutral': '#95a5a6',
            'negative': '#e74c3c'
        },
        title="Sentiment Trends Over Time"
    )
    
    fig.update_layout(height=400)
    return fig


def create_wordcloud(df, sentiment=None):
    """Create word cloud from post content"""
    if sentiment:
        texts = ' '.join(df[df['sentiment_label'] == sentiment]['content'].astype(str))
    else:
        texts = ' '.join(df['content'].astype(str))
    
    if not texts.strip():
        return None
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(texts)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig


def main():
    # Header
    st.title("📊 Social Media Sentiment Analysis Dashboard")
    st.markdown("---")
    
    # Load data
    df = load_posts_data()
    
    if df.empty:
        st.warning("⚠️ No analyzed posts found in the database.")
        st.info("**Use the sidebar** to scrape a topic (e.g., 'technology', 'geopolitics') and analyze sentiment!")
        return
    
    # Database Overview (show what's in the database)
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Database Stats")
    
    # Get unique topics from content
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT url FROM posts WHERE url LIKE '%reddit.com/r/%'")
        urls = [row[0] for row in cursor.fetchall() if row[0]]
        
        # Extract subreddit names
        subreddits = set()
        for url in urls:
            if '/r/' in url:
                subreddit = url.split('/r/')[1].split('/')[0]
                subreddits.add(subreddit)
        
        if subreddits:
            st.sidebar.markdown(f"**Topics in database:** {', '.join(sorted(subreddits)[:5])}")
        
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        st.sidebar.metric("Total Posts in DB", total_posts)
        
        cursor.execute("SELECT COUNT(*) FROM posts WHERE sentiment_label IS NOT NULL")
        analyzed_posts = cursor.fetchone()[0]
        st.sidebar.metric("Analyzed Posts", analyzed_posts)
        
        conn.close()
    except Exception as e:
        pass
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")
    
    platforms = ['All'] + list(df['platform'].unique())
    selected_platform = st.sidebar.selectbox("Platform", platforms)
    
    sentiments = ['All'] + list(df['sentiment_label'].unique())
    selected_sentiment = st.sidebar.selectbox("Sentiment", sentiments)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_platform != 'All':
        filtered_df = filtered_df[filtered_df['platform'] == selected_platform]
    if selected_sentiment != 'All':
        filtered_df = filtered_df[filtered_df['sentiment_label'] == selected_sentiment]
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", len(filtered_df))
    
    with col2:
        positive_pct = (filtered_df['sentiment_label'] == 'positive').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("Positive", f"{positive_pct:.1f}%")
    
    with col3:
        negative_pct = (filtered_df['sentiment_label'] == 'negative').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.metric("Negative", f"{negative_pct:.1f}%")
    
    with col4:
        avg_score = filtered_df['sentiment_score'].mean() if len(filtered_df) > 0 else 0
        st.metric("Avg Sentiment Score", f"{avg_score:.3f}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_sentiment_distribution_chart(filtered_df), use_container_width=True)
    
    with col2:
        if selected_platform == 'All':
            st.plotly_chart(create_platform_sentiment_chart(filtered_df), use_container_width=True)
        else:
            # Show engagement metrics for selected platform
            st.subheader(f"{selected_platform.title()} Engagement")
            avg_likes = filtered_df['likes'].mean()
            avg_comments = filtered_df['comments'].mean()
            avg_shares = filtered_df['shares'].mean()
            
            metrics_df = pd.DataFrame({
                'Metric': ['Likes', 'Comments', 'Shares'],
                'Average': [avg_likes, avg_comments, avg_shares]
            })
            
            fig = px.bar(metrics_df, x='Metric', y='Average', color='Metric')
            st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.plotly_chart(create_sentiment_timeline(filtered_df), use_container_width=True)
    
    # Word Clouds
    st.header("☁️ Word Clouds")
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Posts", "Positive", "Negative", "Neutral"])
    
    with tab1:
        fig = create_wordcloud(filtered_df)
        if fig:
            st.pyplot(fig)
    
    with tab2:
        fig = create_wordcloud(filtered_df, 'positive')
        if fig:
            st.pyplot(fig)
        else:
            st.info("No positive posts to display")
    
    with tab3:
        fig = create_wordcloud(filtered_df, 'negative')
        if fig:
            st.pyplot(fig)
        else:
            st.info("No negative posts to display")
    
    with tab4:
        fig = create_wordcloud(filtered_df, 'neutral')
        if fig:
            st.pyplot(fig)
        else:
            st.info("No neutral posts to display")
    
    # Top Posts
    st.header("🔝 Top Posts by Engagement")
    
    top_posts = filtered_df.nlargest(10, 'likes')[['platform', 'username', 'content', 'likes', 'comments', 'sentiment_label', 'sentiment_score']]
    
    for idx, row in top_posts.iterrows():
        with st.expander(f"[{row['platform']}] @{row['username']} - {row['sentiment_label'].upper()} ({row['likes']} likes)"):
            st.write(row['content'])
            col1, col2, col3 = st.columns(3)
            col1.metric("Likes", row['likes'])
            col2.metric("Comments", row['comments'])
            col3.metric("Sentiment Score", f"{row['sentiment_score']:.3f}")
    
    # Raw Data
    st.header("📋 Raw Data")
    
    if st.checkbox("Show raw data"):
        st.dataframe(
            filtered_df[['platform', 'username', 'content', 'sentiment_label', 'sentiment_score', 'likes', 'comments']],
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
