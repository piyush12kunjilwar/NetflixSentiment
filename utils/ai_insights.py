import os
from anthropic import Anthropic
from typing import Dict, List

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

def generate_content_insights(sentiment_data: Dict) -> Dict:
    """Generate AI-powered content insights and recommendations."""
    
    # Prepare the prompt with sentiment data
    prompt = f"""Based on the following Netflix content sentiment data:
    - Positive Sentiment: {sentiment_data['positive_percentage']:.1f}%
    - Neutral Sentiment: {sentiment_data['neutral_percentage']:.1f}%
    - Negative Sentiment: {sentiment_data['negative_percentage']:.1f}%
    - Total Comments: {sentiment_data['total_comments']}

    Please provide:
    1. A brief analysis of the overall sentiment trends
    2. Content marketing recommendations
    3. Suggested actions to improve audience engagement
    
    Format the response as a JSON with keys: 'analysis', 'recommendations', 'actions'
    """
    
    try:
        # Call Claude API for insights
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",  # Latest model as of March 2025
            max_tokens=1000,
            temperature=0.7,
            system="You are an expert content strategy analyst specializing in streaming media. Provide concise, actionable insights.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract and format the response
        response = message.content[0].text
        
        return {
            'success': True,
            'insights': response,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'insights': None,
            'error': str(e)
        }

def get_emotion_recommendations(text: str) -> Dict:
    """Generate emotion-based content recommendations."""
    
    try:
        prompt = f"""Analyze the following comment and suggest Netflix content recommendations:
        
        Comment: "{text}"
        
        Provide:
        1. The primary emotion expressed
        2. Three Netflix show recommendations based on this emotion
        3. A brief explanation for each recommendation
        
        Format as JSON with keys: 'emotion', 'recommendations'
        """
        
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            system="You are an expert in emotion analysis and content recommendation.",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return {
            'success': True,
            'recommendations': message.content[0].text,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'recommendations': None,
            'error': str(e)
        }
