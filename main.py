import streamlit as st
import pandas as pd

from utils.data_generator import generate_mock_data
from utils.sentiment_analyzer import analyze_sentiment, get_sentiment_metrics
from components.filters import create_filters
from components.visualizations import (
    create_sentiment_trend,
    create_show_sentiment,
    create_demographic_insights,
    create_region_sentiment
)

# Page configuration
st.set_page_config(
    page_title="Netflix Content Sentiment Analysis",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main content styling */
    .stApp {
        background-color: #141414;
    }

    /* Card-like container styling */
    div[data-testid="stMetric"] {
        background-color: #1F1F1F;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Enhance text visibility */
    .metric-label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1F1F1F;
    }

    /* Header styling */
    h1 {
        color: #E50914 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 2rem !important;
    }

    /* Subheader styling */
    h2 {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with animation
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>📺 Netflix Content Sentiment Analysis</h1>
            <p style='color: #CCCCCC; font-size: 1.2rem; max-width: 800px; margin: 0 auto;'>
                Real-time analysis of audience reactions to Netflix original content through social media data.
                Discover trends, insights, and audience sentiments across demographics and regions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Generate and analyze data
    with st.spinner('Processing data...'):
        try:
            # Generate mock data
            df = generate_mock_data(n_samples=1000)

            # Perform sentiment analysis
            df = analyze_sentiment(df)

            # Apply filters
            filtered_df = create_filters(df)

            if filtered_df.empty:
                st.warning("No data available for the selected filters.")
                return

            # Calculate metrics
            metrics = get_sentiment_metrics(filtered_df)

            # Display metrics with enhanced styling
            st.markdown("<h2>Key Metrics</h2>", unsafe_allow_html=True)
            metrics_container = st.container()
            with metrics_container:
                col1, col2, col3, col4 = st.columns(4)

                metric_style = """
                    <div style='background-color: #1F1F1F; padding: 20px; border-radius: 10px; 
                    text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);'>
                        <h3 style='color: #E50914; margin: 0;'>{value}</h3>
                        <p style='color: #CCCCCC; margin: 5px 0 0 0;'>{label}</p>
                    </div>
                """

                with col1:
                    st.markdown(metric_style.format(
                        value=f"{metrics['total_comments']:,}",
                        label="Total Comments"
                    ), unsafe_allow_html=True)
                with col2:
                    st.markdown(metric_style.format(
                        value=f"{metrics['positive_percentage']:.1f}%",
                        label="Positive Sentiment"
                    ), unsafe_allow_html=True)
                with col3:
                    st.markdown(metric_style.format(
                        value=f"{metrics['neutral_percentage']:.1f}%",
                        label="Neutral Sentiment"
                    ), unsafe_allow_html=True)
                with col4:
                    st.markdown(metric_style.format(
                        value=f"{metrics['negative_percentage']:.1f}%",
                        label="Negative Sentiment"
                    ), unsafe_allow_html=True)

            # Create visualizations with enhanced styling
            st.markdown("<h2>Sentiment Analysis Insights</h2>", unsafe_allow_html=True)

            # Sentiment trend with improved styling
            st.plotly_chart(
                create_sentiment_trend(filtered_df),
                use_container_width=True,
                config={'displayModeBar': False}
            )

            # Show-wise sentiment and demographics
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(
                    create_show_sentiment(filtered_df),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            with col2:
                st.plotly_chart(
                    create_demographic_insights(filtered_df),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            # Regional distribution
            st.plotly_chart(
                create_region_sentiment(filtered_df),
                use_container_width=True,
                config={'displayModeBar': False}
            )

            # Sample comments with enhanced styling
            st.markdown("<h2>Recent Audience Reactions</h2>", unsafe_allow_html=True)
            comment_sample = filtered_df.sort_values(
                'timestamp', ascending=False
            )[['timestamp', 'show', 'comment', 'sentiment']].head(5)

            for _, row in comment_sample.iterrows():
                sentiment_color = {
                    'Positive': '#1DB954',  # Spotify green
                    'Neutral': '#FFB13B',   # Warm yellow
                    'Negative': '#E50914'    # Netflix red
                }[row['sentiment']]

                st.markdown(f"""
                <div style='
                    background-color: #1F1F1F;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    border-left: 5px solid {sentiment_color};
                    animation: fadeIn 0.5s ease-in;
                '>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: #E50914; font-weight: bold;'>{row['show']}</span>
                        <span style='color: #666666;'>{row['timestamp'].strftime('%Y-%m-%d %H:%M')}</span>
                    </div>
                    <p style='color: #FFFFFF; margin: 0;'>{row['comment']}</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()