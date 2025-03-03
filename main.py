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
    layout="wide"
)

def main():
    # Header
    st.title("📺 Netflix Content Sentiment Analysis Dashboard")
    st.markdown("""
    Analyze audience reactions to Netflix original content using social media data.
    Filter by demographics, region, and genre to gain valuable insights.
    """)
    
    # Generate and analyze data
    with st.spinner('Loading and analyzing data...'):
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
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Comments", f"{metrics['total_comments']:,}")
            with col2:
                st.metric("Positive", f"{metrics['positive_percentage']:.1f}%")
            with col3:
                st.metric("Neutral", f"{metrics['neutral_percentage']:.1f}%")
            with col4:
                st.metric("Negative", f"{metrics['negative_percentage']:.1f}%")
            
            # Create visualizations
            st.subheader("Sentiment Analysis Insights")
            
            # Sentiment trend
            st.plotly_chart(
                create_sentiment_trend(filtered_df),
                use_container_width=True
            )
            
            # Show-wise sentiment and demographics
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    create_show_sentiment(filtered_df),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    create_demographic_insights(filtered_df),
                    use_container_width=True
                )
            
            # Regional distribution
            st.plotly_chart(
                create_region_sentiment(filtered_df),
                use_container_width=True
            )
            
            # Sample comments
            st.subheader("Recent Comments")
            comment_sample = filtered_df.sort_values(
                'timestamp', ascending=False
            )[['timestamp', 'show', 'comment', 'sentiment']].head(5)
            
            for _, row in comment_sample.iterrows():
                sentiment_color = {
                    'Positive': 'green',
                    'Neutral': 'gray',
                    'Negative': 'red'
                }[row['sentiment']]
                
                st.markdown(f"""
                <div style='padding: 10px; border-left: 5px solid {sentiment_color}; margin: 10px 0;'>
                    <p><strong>{row['show']}</strong> - {row['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
                    <p>{row['comment']}</p>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()
