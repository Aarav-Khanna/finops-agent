# FinOps Agent

A Slack bot that monitors Datadog alerts, analyzes them using AI, and provides root cause analysis and solutions.

## Features

- Monitors Datadog alerts in real-time
- Uses AI to analyze alerts and provide root cause analysis
- Sends detailed alerts to Slack with proposed solutions
- Handles alert deduplication to avoid spam
- Detailed logging for monitoring and debugging
- Robust error handling and authentication validation

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and fill in your API keys:
   - Slack Bot Token
   - Slack App Token
   - Slack Channel ID
   - Datadog API Key
   - Datadog App Key
   - OpenAI API Key

4. Set up your Slack app:
   - Create a new Slack app at https://api.slack.com/apps
   - Enable Socket Mode
   - Add the following bot token scopes:
     - `chat:write`
     - `app_mentions:read`
   - Install the app to your workspace
   - Copy the Bot User OAuth Token and App-Level Token to your `.env` file

5. Set up your Datadog account:
   - Create API and App keys in your Datadog account
   - Ensure you have the necessary permissions to read monitors
   - Note: The application uses the US5 Datadog endpoint by default
   - Copy the API and App keys to your `.env` file

6. Set up OpenAI:
   - Get your API key from https://platform.openai.com/api-keys
   - Copy the API key to your `.env` file

## Usage

Run the agent:
```bash
python main.py
```

The agent will:
1. Start monitoring Datadog alerts
2. When an alert is detected, it will:
   - Analyze the alert using AI
   - Generate a root cause analysis
   - Propose a solution
   - Send a formatted message to your Slack channel

## Logging

The application provides detailed logging at the INFO level:
- Alert detection and details
- AI analysis results
- Slack message status
- Error conditions and authentication issues

## Architecture

- `main.py`: Main application orchestrator
- `config.py`: Configuration management and environment variable handling
- `datadog_monitor.py`: Datadog API integration with robust error handling
- `slack_bot.py`: Slack bot implementation with async support
- `ai_analyzer.py`: AI-powered alert analysis using OpenAI

## Error Handling

The application includes comprehensive error handling for:
- Datadog API authentication
- Slack message sending
- AI analysis failures
- Configuration validation

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use different API keys for development and production
- Regularly rotate your API keys
- Monitor your API usage and set up alerts for unusual activity

## Future Enhancements

- Automatic GitHub PR creation for solutions
- More sophisticated alert analysis
- Customizable alert thresholds
- Integration with other monitoring tools
- Support for multiple Datadog regions
- Enhanced logging and monitoring capabilities 