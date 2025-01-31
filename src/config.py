import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for handling environment variables and settings."""
    
    @staticmethod
    def get_api_token() -> Optional[str]:
        """Retrieve the AIPROXY_TOKEN from environment variables."""
        token = os.getenv("AIPROXY_TOKEN")
        if not token:
            raise ValueError("AIPROXY_TOKEN is not set in the .env file.")
        return token

    @staticmethod
    def get_api_url() -> str:
        """Retrieve the API URL for OpenAI."""
        return "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

# Example usage
# if __name__ == "__main__":
#     try:
#         api_token = Config.get_api_token()
#         print(f"API Token: {api_token}")
#     except ValueError as e:
#         print(f"Error: {e}")