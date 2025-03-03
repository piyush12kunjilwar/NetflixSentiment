import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(n_samples=1000):
    """Generate mock social media data for Netflix content analysis."""
    
    # Netflix shows and their genres
    shows = {
        'Stranger Things': 'Sci-Fi',
        'The Crown': 'Drama',
        'Bridgerton': 'Romance',
        'Squid Game': 'Thriller',
        'Wednesday': 'Fantasy'
    }
    
    # Sample comments
    positive_comments = [
        "Absolutely loved this show!",
        "Best series I've watched this year!",
        "Can't wait for the next season!",
        "Outstanding performance by the cast!",
        "This is a masterpiece!"
    ]
    
    negative_comments = [
        "Disappointed with the ending",
        "Not worth the hype",
        "Could have been better",
        "Lost interest halfway through",
        "Poor character development"
    ]
    
    neutral_comments = [
        "It was okay",
        "Might watch the next season",
        "Has its moments",
        "Pretty standard stuff",
        "Nothing special but watchable"
    ]
    
    # Generate random data
    data = {
        'timestamp': [],
        'show': [],
        'genre': [],
        'comment': [],
        'user_age': [],
        'user_gender': [],
        'user_region': [],
        'platform': []
    }
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for _ in range(n_samples):
        show = np.random.choice(list(shows.keys()))
        sentiment_type = np.random.choice(['positive', 'negative', 'neutral'], 
                                        p=[0.6, 0.2, 0.2])
        
        if sentiment_type == 'positive':
            comment = np.random.choice(positive_comments)
        elif sentiment_type == 'negative':
            comment = np.random.choice(negative_comments)
        else:
            comment = np.random.choice(neutral_comments)
            
        data['timestamp'].append(start_date + timedelta(
            days=np.random.randint(0, 31),
            hours=np.random.randint(0, 24)
        ))
        data['show'].append(show)
        data['genre'].append(shows[show])
        data['comment'].append(comment)
        data['user_age'].append(np.random.randint(18, 65))
        data['user_gender'].append(np.random.choice(['Male', 'Female', 'Other']))
        data['user_region'].append(np.random.choice(
            ['North America', 'Europe', 'Asia', 'South America', 'Oceania']))
        data['platform'].append(np.random.choice(
            ['Twitter', 'Instagram', 'Facebook']))
    
    return pd.DataFrame(data)
