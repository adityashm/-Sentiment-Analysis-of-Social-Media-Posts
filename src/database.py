import sqlite3
from pathlib import Path

DATABASE_FILE = Path(__file__).parent / 'scraped_data.db'

def create_database():
    """Create database and tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Social Media Posts table with sentiment analysis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            username TEXT,
            content TEXT NOT NULL,
            url TEXT UNIQUE,
            likes INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            post_date TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentiment_score REAL,
            sentiment_label TEXT,
            analyzed_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT UNIQUE NOT NULL,
            author TEXT,
            publish_date TEXT,
            category TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            salary TEXT,
            description TEXT,
            url TEXT UNIQUE NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_article(title, description, url, author, publish_date, category):
    """Insert article into database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO articles (title, description, url, author, publish_date, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, url, author, publish_date, category))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # URL already exists
        return False
    finally:
        conn.close()

def insert_job(title, company, location, job_type, salary, description, url):
    """Insert job into database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO jobs (title, company, location, job_type, salary, description, url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, company, location, job_type, salary, description, url))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_articles(limit=50):
    """Retrieve all articles from database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY scraped_at DESC LIMIT ?', (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_articles_by_category(category, limit=50):
    """Get articles by category"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM articles WHERE category = ? ORDER BY scraped_at DESC LIMIT ?',
        (category, limit)
    )
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_all_jobs(limit=50):
    """Retrieve all jobs from database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY scraped_at DESC LIMIT ?', (limit,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_jobs_by_type(job_type, limit=50):
    """Get jobs by type"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM jobs WHERE job_type = ? ORDER BY scraped_at DESC LIMIT ?',
        (job_type, limit)
    )
    jobs = cursor.fetchall()
    conn.close()
    return jobs

# ==================== SOCIAL MEDIA POST FUNCTIONS ====================

def insert_post(platform, username, content, url, likes=0, shares=0, comments=0, post_date=None):
    """Insert social media post into database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO posts (platform, username, content, url, likes, shares, comments, post_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (platform, username, content, url, likes, shares, comments, post_date))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_post_sentiment(post_id, sentiment_score, sentiment_label):
    """Update sentiment analysis results for a post"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE posts 
        SET sentiment_score = ?, sentiment_label = ?, analyzed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (sentiment_score, sentiment_label, post_id))
    
    conn.commit()
    conn.close()

def get_all_posts(limit=100):
    """Retrieve all posts from database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY scraped_at DESC LIMIT ?', (limit,))
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_posts_by_platform(platform, limit=100):
    """Get posts by platform"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM posts WHERE platform = ? ORDER BY scraped_at DESC LIMIT ?',
        (platform, limit)
    )
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_posts_by_sentiment(sentiment_label, limit=100):
    """Get posts by sentiment label (positive, negative, neutral)"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM posts WHERE sentiment_label = ? ORDER BY scraped_at DESC LIMIT ?',
        (sentiment_label, limit)
    )
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_sentiment_statistics():
    """Get sentiment statistics across all posts"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_posts,
            AVG(sentiment_score) as avg_sentiment,
            COUNT(CASE WHEN sentiment_label = 'positive' THEN 1 END) as positive_count,
            COUNT(CASE WHEN sentiment_label = 'negative' THEN 1 END) as negative_count,
            COUNT(CASE WHEN sentiment_label = 'neutral' THEN 1 END) as neutral_count
        FROM posts
        WHERE sentiment_label IS NOT NULL
    ''')
    
    stats = cursor.fetchone()
    conn.close()
    return stats

    jobs = cursor.fetchall()
    conn.close()
    return jobs

def delete_old_data(days=30):
    """Delete data older than specified days"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM articles 
        WHERE datetime(scraped_at) < datetime('now', '-' || ? || ' days')
    ''', (days,))
    cursor.execute('''
        DELETE FROM jobs 
        WHERE datetime(scraped_at) < datetime('now', '-' || ? || ' days')
    ''', (days,))
    conn.commit()
    conn.close()
