import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def analyze_sentiment(df):
    """Analyze sentiment of comments using NLTK's VADER."""
    
    sia = SentimentIntensityAnalyzer()
    
    # Calculate sentiment scores
    df['sentiment_scores'] = df['comment'].apply(lambda x: sia.polarity_scores(x))
    df['compound_score'] = df['sentiment_scores'].apply(lambda x: x['compound'])
    
    # Classify sentiment
    df['sentiment'] = df['compound_score'].apply(
        lambda x: 'Positive' if x > 0.2 
        else 'Negative' if x < -0.2 
        else 'Neutral'
    )
    
    return df

def get_sentiment_metrics(df):
    """Calculate overall sentiment metrics."""
    
    total_comments = len(df)
    sentiment_counts = df['sentiment'].value_counts()
    
    metrics = {
        'total_comments': total_comments,
        'positive_percentage': (sentiment_counts.get('Positive', 0) / total_comments) * 100,
        'neutral_percentage': (sentiment_counts.get('Neutral', 0) / total_comments) * 100,
        'negative_percentage': (sentiment_counts.get('Negative', 0) / total_comments) * 100
    }
    
    return metrics
