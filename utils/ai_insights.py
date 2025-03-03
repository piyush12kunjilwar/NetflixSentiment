import os
from anthropic import Anthropic
from typing import Dict, List
import json

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

        Format your response exactly as a JSON object with these three keys:
        {
          "analysis": "your trend analysis here",
          "recommendations": "your marketing recommendations here",
          "actions": "your suggested actions here"
        }
        """

        # Call Claude API for insights
        # Note: the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract and validate the response
        response = message.content[0].text.strip()

        # Ensure valid JSON response
        try:
            data = json.loads(response)
            required_keys = ['analysis', 'recommendations', 'actions']
            if not all(key in data for key in required_keys):
                raise ValueError("Missing required keys in response")
            return {
                'success': True,
                'insights': json.dumps(data),
                'error': None
            }
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback formatting if response isn't valid JSON
            formatted_response = {
                'analysis': "Unable to analyze trends at this time.",
                'recommendations': "Please try again later for recommendations.",
                'actions': "System is currently processing the data."
            }
            return {
                'success': True,
                'insights': json.dumps(formatted_response),
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
        prompt = f"""Analyze this comment about Netflix content and provide recommendations.
        Format your response exactly as shown in the example:

        Comment: "{text}"

        Example Response Format:
        {{
            "emotion": "excitement",
            "recommendations": [
                "Stranger Things - For high-energy supernatural drama",
                "Wednesday - For darkly entertaining adventures"
            ]
        }}
        """

        # Note: the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract and validate the response
        response = message.content[0].text.strip()

        try:
            data = json.loads(response)
            if not all(key in data for key in ['emotion', 'recommendations']):
                raise ValueError("Missing required keys in response")
            return {
                'success': True,
                'recommendations': json.dumps(data),
                'error': None
            }
        except (json.JSONDecodeError, ValueError):
            # Fallback formatting if response isn't valid JSON
            fallback = {
                'emotion': 'neutral',
                'recommendations': [
                    'Popular shows based on your viewing history',
                    'Trending content in your region'
                ]
            }
            return {
                'success': True,
                'recommendations': json.dumps(fallback),
                'error': None
            }

    except Exception as e:
        return {
            'success': False,
            'recommendations': None,
            'error': str(e)
        }