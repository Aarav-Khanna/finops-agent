import asyncio
import time
from datadog_monitor import DatadogMonitor
from slack_bot import SlackBot
from ai_analyzer import AIAnalyzer
from config import Config

class FinOpsAgent:
    def __init__(self):
        self.datadog = DatadogMonitor()
        self.slack = SlackBot()
        self.ai = AIAnalyzer()
        self.processed_alerts = set()

    async def start(self):
        """Start the FinOps agent"""
        # Start the Slack bot in the background
        self.slack.start()  # Note: This is now synchronous since it handles threading internally
        
        # Start monitoring Datadog alerts
        while True:
            await self.check_alerts()
            await asyncio.sleep(60)  # Check every minute

    async def check_alerts(self):
        """Check for new alerts and process them"""
        try:
            alerts = self.datadog.get_active_alerts()
            print(f"Found {len(alerts)} active alerts")
            
            for alert in alerts:
                alert_id = alert['id']
                
                # Skip if we've already processed this alert
                if alert_id in self.processed_alerts:
                    print(f"Skipping already processed alert: {alert_id}")
                    continue
                
                print(f"Processing new alert: {alert_id}")
                
                # Get detailed alert information
                alert_details = self.datadog.get_alert_details(alert_id)
                if not alert_details:
                    print(f"Could not get details for alert: {alert_id}")
                    continue
                
                # Analyze the alert
                print(f"Analyzing alert: {alert_id}")
                root_cause, solution = await self.ai.analyze_alert(alert_details)
                
                # Send the alert to Slack
                print(f"Sending alert to Slack: {alert_id}")
                await self.slack.send_alert(alert_details, root_cause, solution)
                
                # Mark the alert as processed
                self.processed_alerts.add(alert_id)
                print(f"Completed processing alert: {alert_id}")
                
        except Exception as e:
            print(f"Error in alert checking: {str(e)}")

if __name__ == "__main__":
    # Validate configuration
    Config.validate_config()
    
    # Create and start the agent
    agent = FinOpsAgent()
    asyncio.run(agent.start()) 