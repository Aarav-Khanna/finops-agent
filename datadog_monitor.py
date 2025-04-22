from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatadogMonitor:
    def __init__(self):
        if not Config.DATADOG_API_KEY or not Config.DATADOG_APP_KEY:
            raise ValueError("Datadog API key or App key is missing. Please check your .env file.")
            
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = Config.DATADOG_API_KEY
        configuration.api_key["appKeyAuth"] = Config.DATADOG_APP_KEY
        
        # Set the host to the correct Datadog API endpoint
        configuration.host = "https://api.us5.datadoghq.com"
        
        self.api_client = ApiClient(configuration)
        self.monitors_api = MonitorsApi(self.api_client)
        self.events_api = EventsApi(self.api_client)
        
        # Test the connection
        self._test_connection()

    def _test_connection(self):
        """Test the Datadog API connection"""
        try:
            # Try to get a list of monitors to test the connection
            self.monitors_api.list_monitors()
            logger.info("Successfully connected to Datadog API")
        except Exception as e:
            logger.error(f"Failed to connect to Datadog API: {str(e)}")
            if "403" in str(e):
                logger.error("Authentication failed. Please check your API and App keys.")
            raise

    def get_active_alerts(self):
        """Get all active alerts from Datadog"""
        try:
            monitors = self.monitors_api.list_monitors()
            active_alerts = []
            
            for monitor in monitors:
                if str(monitor.overall_state) != "OK":
                    alert_details = {
                        "id": monitor.id,
                        "name": monitor.name,
                        "message": monitor.message,
                        "state": monitor.overall_state,
                        "query": monitor.query,
                        "tags": monitor.tags
                    }
                    logger.info(f"Found active alert: {alert_details['name']} (ID: {alert_details['id']})")
                    logger.info(f"Alert message: {alert_details['message']}")
                    logger.info(f"Alert query: {alert_details['query']}")
                    logger.info(f"Alert state: {alert_details['state']}")
                    active_alerts.append(alert_details)
            
            logger.info(f"Found {len(active_alerts)} active alerts")
            return active_alerts
        except Exception as e:
            logger.error(f"Error fetching Datadog alerts: {str(e)}")
            if "403" in str(e):
                logger.error("Authentication failed. Please check your API and App keys.")
            return []

    def get_alert_details(self, alert_id):
        """Get detailed information about a specific alert"""
        try:
            monitor = self.monitors_api.get_monitor(alert_id)
            details = {
                "id": monitor.id,
                "name": monitor.name,
                "message": monitor.message,
                "state": monitor.overall_state,
                "query": monitor.query,
                "tags": monitor.tags,
                "options": monitor.options
            }
            logger.info(f"Retrieved detailed information for alert {alert_id}")
            logger.info(f"Full alert details: {details}")
            return details
        except Exception as e:
            logger.error(f"Error fetching alert details: {str(e)}")
            return None 