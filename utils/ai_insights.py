import os
from anthropic import Anthropic
from typing import Dict, List

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

def generate_content_insights(sentiment_data: Dict) -> Dict:
    """Generate AI-powered content insights and recommendations."""
    try:
        # Prepare the prompt
        prompt = f"""Based on the following Netflix content sentiment data:
        - Positive Sentiment: {sentiment_data['positive_percentage']:.1f}%
        - Neutral Sentiment: {sentiment_data['neutral_percentage']:.1f}%
        - Negative Sentiment: {sentiment_data['negative_percentage']:.1f}%
        - Total Comments: {sentiment_data['total_comments']}

        Please analyze this data and provide:
        1. A brief analysis of the overall sentiment trends
        2. Three specific content marketing recommendations
        3. Two actionable steps to improve audience engagement

        Format your response as a dictionary with three keys:
        {{"analysis": "your trend analysis", 
          "recommendations": "your marketing recommendations",
          "actions": "your suggested actions"}}
        """

        # Call Claude API for insights
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract and clean the response
        response = message.content[0].text
        # Ensure the response is properly formatted as a JSON string
        if not response.startswith('{'):
            response = '{"analysis": "' + response + '"}'

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
        prompt = f"""Analyze this comment about Netflix content and provide recommendations:

        Comment: "{text}"

        Please provide:
        1. The primary emotion expressed
        2. Two Netflix show recommendations based on this emotion

        Format your response as a dictionary:
        {{"emotion": "primary emotion", 
          "recommendations": ["show 1", "show 2"]}}
        """

        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Clean and format the response
        response = message.content[0].text
        if not response.startswith('{'):
            response = '{"emotion": "Unknown", "recommendations": []}'

        return {
            'success': True,
            'recommendations': response,
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'recommendations': None,
            'error': str(e)
        }