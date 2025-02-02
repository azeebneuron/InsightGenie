import httpx
import json
from typing import Dict, Any, Optional
from .config import Config

class AIAnalyzer:
    """Handles AI-powered analysis using the OpenAI API."""
    @staticmethod
    def generate_insights(data_summary: Dict[str, Any]) -> Optional[str]:
        """
        Generate insights using the OpenAI API.
        
        Args:
            data_summary (Dict[str, Any]): A summary of the dataset statistics.
        
        Returns:
            Optional[str]: Generated insights or None if the API call fails.
        """
        try:
            # Prepare the API request payload
            prompt = f"Analyze the following dataset summary and provide key insights:\n{json.dumps(data_summary, indent=2)}"
            payload = {
                "model": "gpt-4o-mini",  # Use the correct model name
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
            }

            # Debugging: Print the payload
            print("Payload:", json.dumps(payload, indent=2))

            # Make the API request with an increased timeout
            headers = {
                "Authorization": f"Bearer {Config.get_api_token()}",
                "Content-Type": "application/json",
            }
            timeout = httpx.Timeout(30.0)  # Set timeout to 30 seconds
            response = httpx.post(Config.get_api_url(), headers=headers, json=payload, timeout=timeout)
            
            # Debugging: Print the response status and content
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)

            response.raise_for_status()

            # Extract and return the generated insights
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Response content: {e.response.text}")
        except httpx.ReadTimeout as e:
            print(f"Read operation timed out: {e}")
        except Exception as e:
            print(f"Error generating insights: {e}")
        return None
# Example usage
