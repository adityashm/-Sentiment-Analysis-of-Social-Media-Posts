"""
Sentiment Analysis Module
Supports multiple sentiment analysis methods:
1. VADER (Valence Aware Dictionary and sEntiment Reasoner) - Best for social media
2. TextBlob - Simple and effective
3. Transformers (RoBERTa) - Advanced deep learning model
"""

import logging
from typing import Dict, Tuple
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Multi-model sentiment analyzer for social media posts"""
    
    def __init__(self, method='vader'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'vader', 'textblob', or 'transformers'
        """
        self.method = method
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the selected sentiment analysis method"""
        try:
            if self.method == 'vader':
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                self.analyzer = SentimentIntensityAnalyzer()
                logger.info("VADER sentiment analyzer initialized")
                
            elif self.method == 'textblob':
                from textblob import TextBlob
                self.analyzer = TextBlob
                logger.info("TextBlob sentiment analyzer initialized")
                
            elif self.method == 'transformers':
                from transformers import pipeline
                self.analyzer = pipeline("sentiment-analysis", 
                                       model="cardiffnlp/twitter-roberta-base-sentiment-latest")
                logger.info("Transformer sentiment analyzer initialized")
            else:
                raise ValueError(f"Unknown method: {self.method}")
        except ImportError as e:
            logger.error(f"Failed to import required library: {e}")
            raise
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove mentions (@username)
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags (keep the text, remove #)
        text = re.sub(r'#', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with 'score', 'label', and method-specific details
        """
        if not text or not text.strip():
            return {'score': 0.0, 'label': 'neutral', 'confidence': 0.0}
        
        # Preprocess text
        clean_text = self.preprocess_text(text)
        
        if not clean_text:
            return {'score': 0.0, 'label': 'neutral', 'confidence': 0.0}
        
        if self.method == 'vader':
            return self._analyze_vader(clean_text)
        elif self.method == 'textblob':
            return self._analyze_textblob(clean_text)
        elif self.method == 'transformers':
            return self._analyze_transformers(clean_text)
    
    def _analyze_vader(self, text: str) -> Dict[str, any]:
        """Analyze using VADER"""
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Classify sentiment based on compound score
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'score': compound,
            'label': label,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'method': 'vader'
        }
    
    def _analyze_textblob(self, text: str) -> Dict[str, any]:
        """Analyze using TextBlob"""
        blob = self.analyzer(text)
        polarity = blob.sentiment.polarity  # Range: -1 to 1
        subjectivity = blob.sentiment.subjectivity  # Range: 0 to 1
        
        # Classify sentiment
        if polarity > 0.1:
            label = 'positive'
        elif polarity < -0.1:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'score': polarity,
            'label': label,
            'subjectivity': subjectivity,
            'method': 'textblob'
        }
    
    def _analyze_transformers(self, text: str) -> Dict[str, any]:
        """Analyze using Transformer model"""
        # Truncate text if too long (max 512 tokens for most models)
        max_length = 500
        if len(text) > max_length:
            text = text[:max_length]
        
        result = self.analyzer(text)[0]
        label_map = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive',
            'negative': 'negative',
            'neutral': 'neutral',
            'positive': 'positive'
        }
        
        raw_label = result['label']
        label = label_map.get(raw_label, raw_label.lower())
        confidence = result['score']
        
        # Convert to score (-1 to 1 scale)
        score_map = {'negative': -confidence, 'neutral': 0, 'positive': confidence}
        score = score_map.get(label, 0)
        
        return {
            'score': score,
            'label': label,
            'confidence': confidence,
            'method': 'transformers'
        }
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze multiple texts at once
        
        Args:
            texts: List of text strings
            
        Returns:
            List of sentiment results
        """
        results = []
        for text in texts:
            try:
                result = self.analyze(text)
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing text: {e}")
                results.append({'score': 0.0, 'label': 'neutral', 'error': str(e)})
        
        return results


def analyze_post(content: str, method='vader') -> Tuple[float, str]:
    """
    Quick function to analyze a single post
    
    Args:
        content: Post content
        method: Analysis method ('vader', 'textblob', 'transformers')
        
    Returns:
        Tuple of (score, label)
    """
    analyzer = SentimentAnalyzer(method=method)
    result = analyzer.analyze(content)
    return result['score'], result['label']


if __name__ == "__main__":
    # Test the analyzer
    test_texts = [
        "I absolutely love this product! Best purchase ever! 😊",
        "This is terrible. Worst experience of my life.",
        "It's okay, nothing special.",
        "OMG this is amazing!!! Can't believe how good this is! 🔥🔥🔥",
        "Disappointed and frustrated. Would not recommend."
    ]
    
    print("=" * 60)
    print("TESTING SENTIMENT ANALYZERS")
    print("=" * 60)
    
    for method in ['vader', 'textblob']:
        print(f"\n{method.upper()} Analysis:")
        print("-" * 60)
        
        try:
            analyzer = SentimentAnalyzer(method=method)
            for text in test_texts:
                result = analyzer.analyze(text)
                print(f"Text: {text[:50]}...")
                print(f"Score: {result['score']:.3f} | Label: {result['label']}")
                print()
        except Exception as e:
            print(f"Error with {method}: {e}\n")
