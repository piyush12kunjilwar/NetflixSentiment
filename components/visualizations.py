import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_sentiment_trend(df):
    """Create sentiment trend over time visualization."""
    
    daily_sentiment = df.groupby(
        [df['timestamp'].dt.date, 'sentiment']
    ).size().unstack(fill_value=0)
    
    daily_sentiment_pct = daily_sentiment.div(
        daily_sentiment.sum(axis=1), axis=0
    ) * 100
    
    fig = go.Figure()
    
    for sentiment in ['Positive', 'Neutral', 'Negative']:
        if sentiment in daily_sentiment_pct.columns:
            fig.add_trace(go.Scatter(
                x=daily_sentiment_pct.index,
                y=daily_sentiment_pct[sentiment],
                name=sentiment,
                mode='lines',
                stackgroup='one'
            ))
    
    fig.update_layout(
        title='Sentiment Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Percentage',
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def create_show_sentiment(df):
    """Create show-wise sentiment distribution."""
    
    show_sentiment = df.groupby(['show', 'sentiment']).size().unstack(fill_value=0)
    show_sentiment_pct = show_sentiment.div(show_sentiment.sum(axis=1), axis=0) * 100
    
    fig = px.bar(
        show_sentiment_pct,
        barmode='stack',
        title='Sentiment Distribution by Show',
        labels={'value': 'Percentage', 'show': 'Show'}
    )
    
    fig.update_layout(
        xaxis_title='Show',
        yaxis_title='Percentage',
        showlegend=True
    )
    
    return fig

def create_demographic_insights(df):
    """Create demographic insights visualization."""
    
    age_bins = [0, 25, 35, 45, 55, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '55+']
    
    df['age_group'] = pd.cut(
        df['user_age'],
        bins=age_bins,
        labels=age_labels,
        right=False
    )
    
    demo_sentiment = df.groupby(['age_group', 'sentiment']).size().unstack(fill_value=0)
    demo_sentiment_pct = demo_sentiment.div(demo_sentiment.sum(axis=1), axis=0) * 100
    
    fig = px.bar(
        demo_sentiment_pct,
        barmode='group',
        title='Sentiment Distribution by Age Group',
        labels={'value': 'Percentage', 'age_group': 'Age Group'}
    )
    
    fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Percentage',
        showlegend=True
    )
    
    return fig

def create_region_sentiment(df):
    """Create region-wise sentiment visualization."""
    
    region_sentiment = df.groupby(['user_region', 'sentiment']).size().unstack(fill_value=0)
    
    fig = px.pie(
        values=region_sentiment.sum(axis=1),
        names=region_sentiment.index,
        title='Regional Distribution of Comments'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig
