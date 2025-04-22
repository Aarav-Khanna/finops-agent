import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import Config
import asyncio
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self):
        self.app = App(token=Config.SLACK_BOT_TOKEN)
        self.handler = SocketModeHandler(self.app, Config.SLACK_APP_TOKEN)
        
        # Register event handlers
        self.app.event("app_mention")(self.handle_mention)
        
    def start(self):
        """Start the Slack bot in a separate thread"""
        def run_handler():
            logger.info("Starting Slack bot handler...")
            self.handler.start()
        
        # Start the handler in a separate thread
        self.handler_thread = threading.Thread(target=run_handler)
        self.handler_thread.daemon = True  # This ensures the thread will exit when the main program exits
        self.handler_thread.start()
        logger.info("Slack bot handler thread started")

    async def handle_mention(self, event, say):
        """Handle mentions of the bot"""
        text = event.get("text", "")
        user = event.get("user", "")
        
        # Respond to the mention
        await say(f"Hello <@{user}>! I'm your FinOps assistant. How can I help you today?")

    async def send_alert(self, alert_data, analysis, solution):
        """Send an alert message to the configured Slack channel"""
        try:
            message = {
                "channel": Config.SLACK_CHANNEL_ID,
                "text": f"🚨 Alert: {alert_data['name']}",  # Fallback text for notifications
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 Alert: {alert_data['name']}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Alert Details:*\n{alert_data['message']}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Root Cause Analysis:*\n{analysis}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Proposed Solution:*\n{solution}"
                        }
                    }
                ]
            }
            
            # Use the WebClient directly instead of the async say method
            response = self.app.client.chat_postMessage(**message)
            logger.info(f"Successfully sent alert to Slack: {alert_data['name']}")
            return response
        except Exception as e:
            logger.error(f"Error sending Slack message: {str(e)}")
            raise 