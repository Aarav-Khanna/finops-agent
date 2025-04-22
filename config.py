import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Slack Configuration
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
    SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')
    
    # Datadog Configuration
    DATADOG_API_KEY = os.getenv('DATADOG_API_KEY')
    DATADOG_APP_KEY = os.getenv('DATADOG_APP_KEY')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Application Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    @classmethod
    def validate_config(cls):
        required_vars = [
            'SLACK_BOT_TOKEN',
            'SLACK_APP_TOKEN',
            'SLACK_CHANNEL_ID',
            'DATADOG_API_KEY',
            'DATADOG_APP_KEY',
            'OPENAI_API_KEY'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 