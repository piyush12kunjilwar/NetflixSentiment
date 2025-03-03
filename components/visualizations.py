import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Dark theme template for all visualizations
DARK_TEMPLATE = {
    'layout': {
        'plot_bgcolor': '#141414',
        'paper_bgcolor': '#141414',
        'font': {'color': '#FFFFFF'},
        'title': {'font': {'color': '#FFFFFF', 'size': 24}},
        'xaxis': {
            'gridcolor': '#1F1F1F',
            'linecolor': '#1F1F1F',
            'title': {'font': {'color': '#FFFFFF'}}
        },
        'yaxis': {
            'gridcolor': '#1F1F1F',
            'linecolor': '#1F1F1F',
            'title': {'font': {'color': '#FFFFFF'}}
        },
        'legend': {'font': {'color': '#FFFFFF'}}
    }
}

def create_sentiment_trend(df):
    """Create enhanced sentiment trend visualization."""

    daily_sentiment = df.groupby(
        [df['timestamp'].dt.date, 'sentiment']
    ).size().unstack(fill_value=0)

    daily_sentiment_pct = daily_sentiment.div(
        daily_sentiment.sum(axis=1), axis=0
    ) * 100

    fig = go.Figure()

    colors = {
        'Positive': '#1DB954',  # Spotify green
        'Neutral': '#FFB13B',   # Warm yellow
        'Negative': '#E50914'    # Netflix red
    }

    for sentiment in ['Positive', 'Neutral', 'Negative']:
        if sentiment in daily_sentiment_pct.columns:
            fig.add_trace(go.Scatter(
                x=daily_sentiment_pct.index,
                y=daily_sentiment_pct[sentiment],
                name=sentiment,
                mode='lines',
                line=dict(width=3, color=colors[sentiment]),
                stackgroup='one',
                groupnorm='percent',
                hovertemplate="%{y:.1f}%<extra></extra>"
            ))

    fig.update_layout(
        title='Sentiment Trends Over Time',
        xaxis_title='Date',
        yaxis_title='Percentage',
        hovermode='x unified',
        showlegend=True,
        **DARK_TEMPLATE['layout']
    )

    return fig

def create_show_sentiment(df):
    """Create enhanced show-wise sentiment distribution."""

    show_sentiment = df.groupby(['show', 'sentiment']).size().unstack(fill_value=0)
    show_sentiment_pct = show_sentiment.div(show_sentiment.sum(axis=1), axis=0) * 100

    fig = go.Figure()

    colors = ['#1DB954', '#FFB13B', '#E50914']

    for i, sentiment in enumerate(['Positive', 'Neutral', 'Negative']):
        fig.add_trace(go.Bar(
            name=sentiment,
            x=show_sentiment_pct.index,
            y=show_sentiment_pct[sentiment],
            marker_color=colors[i],
            hovertemplate="%{y:.1f}%<extra></extra>"
        ))

    fig.update_layout(
        title='Sentiment Distribution by Show',
        barmode='stack',
        xaxis_title='Show',
        yaxis_title='Percentage',
        showlegend=True,
        **DARK_TEMPLATE['layout']
    )

    return fig

def create_demographic_insights(df):
    """Create enhanced demographic insights visualization."""

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

    fig = go.Figure()

    colors = ['#1DB954', '#FFB13B', '#E50914']

    for i, sentiment in enumerate(['Positive', 'Neutral', 'Negative']):
        fig.add_trace(go.Bar(
            name=sentiment,
            x=demo_sentiment_pct.index,
            y=demo_sentiment_pct[sentiment],
            marker_color=colors[i],
            hovertemplate="%{y:.1f}%<extra></extra>"
        ))

    fig.update_layout(
        title='Sentiment Distribution by Age Group',
        barmode='group',
        xaxis_title='Age Group',
        yaxis_title='Percentage',
        showlegend=True,
        **DARK_TEMPLATE['layout']
    )

    return fig

def create_region_sentiment(df):
    """Create enhanced region-wise sentiment visualization."""

    region_sentiment = df.groupby(['user_region', 'sentiment']).size().unstack(fill_value=0)
    region_total = region_sentiment.sum(axis=1)

    fig = go.Figure(data=[go.Pie(
        labels=region_sentiment.index,
        values=region_total,
        hole=0.4,
        marker=dict(
            colors=['#E50914', '#1DB954', '#FFB13B', '#564D4D', '#831010'],
            line=dict(color='#141414', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(color='#FFFFFF', size=14),
        hovertemplate="<b>%{label}</b><br>" +
                      "Comments: %{value}<br>" +
                      "Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title='Regional Distribution of Comments',
        annotations=[dict(text='Global<br>Reach', x=0.5, y=0.5, font_size=20, showarrow=False)],
        **DARK_TEMPLATE['layout']
    )

    return fig