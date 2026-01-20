"""
Setup script for Sentiment Analysis of Social Media Posts
Allows installation as a package: pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="sentiment-analysis-social-media",
    version="1.0.0",
    author="adityashm",
    description="Sentiment Analysis of Social Media Posts using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityashm/-Sentiment-Analysis-of-Social-Media-Posts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "lxml>=4.9.3",
        "pandas>=2.1.4",
        "vaderSentiment>=3.3.2",
        "textblob>=0.17.1",
        "transformers>=4.35.2",
        "torch>=2.1.0",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        "streamlit>=1.29.0",
        "wordcloud>=1.9.3",
        "python-dotenv>=1.0.0",
        "schedule>=1.2.0",
        "numpy>=1.26.2",
        "tqdm>=4.66.1",
    ],
    entry_points={
        'console_scripts': [
            'sentiment-scrape=src.social_scraper:main',
            'sentiment-analyze=scripts.analyze_sentiment:main',
            'sentiment-dashboard=dashboard:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
