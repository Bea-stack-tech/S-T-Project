#!/usr/bin/env python3
"""
Trend Monitor Script

This script continuously monitors Google Search Trends for specified keywords
and sends alerts when significant changes are detected.

Features:
- Real-time trend monitoring
- Configurable alert thresholds
- Multiple notification methods (email, Slack, webhook)
- Historical trend comparison
- Automated reporting
"""

import os
import time
import json
import logging
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# Add parent directory to path to import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_clients.pytrends_client import PyTrendsClient
from src.api_clients.valueserp_client import ValueSerpClient
from src.trends_analyzer import TrendsAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trend_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TrendMonitor:
    """
    Trend monitoring class for continuous keyword tracking.
    """
    
    def __init__(self, config_file: str = "config/monitor_config.json"):
        """
        Initialize the trend monitor.
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config = self.load_config(config_file)
        self.analyzer = TrendsAnalyzer()
        self.pytrends_client = PyTrendsClient()
        
        # Initialize Value SERP client if API key is available
        self.valueserp_client = None
        if os.getenv('VALUE_SERP_API_KEY'):
            self.valueserp_client = ValueSerpClient(api_key=os.getenv('VALUE_SERP_API_KEY'))
        
        # Store historical data
        self.historical_data = {}
        self.alert_history = []
        
        logger.info("Trend Monitor initialized")
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            config_file (str): Path to configuration file
            
        Returns:
            Dict containing configuration
        """
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "keywords": ["artificial intelligence", "machine learning", "python"],
            "monitoring_interval": 3600,  # 1 hour
            "alert_threshold": 20,  # 20% change triggers alert
            "geographic_locations": ["US", "GB", "CA"],
            "timeframe": "today 7-d",
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender_email": "",
                    "sender_password": "",
                    "recipient_emails": []
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": "",
                    "channel": "#trends"
                },
                "webhook": {
                    "enabled": False,
                    "url": "",
                    "headers": {}
                }
            },
            "data_storage": {
                "save_to_file": True,
                "file_path": "data/monitoring/",
                "save_to_database": False,
                "database_url": ""
            }
        }
    
    def get_current_trends(self, keywords: List[str], geo: str = "US") -> Dict[str, Any]:
        """
        Get current trend data for keywords.
        
        Args:
            keywords (List[str]): List of keywords to monitor
            geo (str): Geographic location
            
        Returns:
            Dictionary with current trend data
        """
        try:
            # Get interest over time data
            payload = {
                'kw_list': keywords,
                'geo': geo,
                'timeframe': self.config['timeframe']
            }
            
            data = self.pytrends_client.get_interest_over_time(payload)
            
            if data is not None and not data.empty:
                # Get the latest values
                latest_data = {}
                for keyword in keywords:
                    if keyword in data.columns:
                        latest_value = data[keyword].iloc[-1]
                        latest_data[keyword] = {
                            'current_value': latest_value,
                            'timestamp': datetime.now().isoformat(),
                            'location': geo
                        }
                
                return latest_data
            else:
                logger.warning(f"No trend data available for keywords: {keywords}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting current trends: {e}")
            return {}
    
    def calculate_trend_change(self, keyword: str, current_value: int, geo: str = "US") -> float:
        """
        Calculate the percentage change in trend value.
        
        Args:
            keyword (str): Keyword to analyze
            current_value (int): Current trend value
            geo (str): Geographic location
            
        Returns:
            Percentage change (positive or negative)
        """
        if keyword not in self.historical_data:
            # First time seeing this keyword, store baseline
            self.historical_data[keyword] = {
                'baseline_value': current_value,
                'last_value': current_value,
                'last_update': datetime.now()
            }
            return 0.0
        
        historical = self.historical_data[keyword]
        baseline_value = historical['baseline_value']
        
        if baseline_value == 0:
            return 0.0
        
        # Calculate percentage change from baseline
        change_percentage = ((current_value - baseline_value) / baseline_value) * 100
        
        # Update historical data
        historical['last_value'] = current_value
        historical['last_update'] = datetime.now()
        
        return change_percentage
    
    def check_alert_conditions(self, keyword: str, change_percentage: float) -> bool:
        """
        Check if alert conditions are met.
        
        Args:
            keyword (str): Keyword being monitored
            change_percentage (float): Percentage change in trend
            
        Returns:
            True if alert should be triggered
        """
        threshold = self.config['alert_threshold']
        
        # Check if change exceeds threshold
        if abs(change_percentage) >= threshold:
            # Check if we've already alerted recently for this keyword
            recent_alerts = [
                alert for alert in self.alert_history
                if alert['keyword'] == keyword and 
                (datetime.now() - alert['timestamp']).total_seconds() < 3600  # 1 hour
            ]
            
            if not recent_alerts:
                return True
        
        return False
    
    def send_email_alert(self, keyword: str, change_percentage: float, current_value: int):
        """
        Send email alert for trend change.
        
        Args:
            keyword (str): Keyword that triggered alert
            change_percentage (float): Percentage change
            current_value (int): Current trend value
        """
        email_config = self.config['notifications']['email']
        
        if not email_config['enabled']:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = ', '.join(email_config['recipient_emails'])
            msg['Subject'] = f"Trend Alert: {keyword}"
            
            body = f"""
            Trend Alert Detected!
            
            Keyword: {keyword}
            Current Value: {current_value}
            Change: {change_percentage:.2f}%
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            This alert was triggered because the trend change exceeded the threshold of {self.config['alert_threshold']}%.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
    
    def send_slack_alert(self, keyword: str, change_percentage: float, current_value: int):
        """
        Send Slack alert for trend change.
        
        Args:
            keyword (str): Keyword that triggered alert
            change_percentage (float): Percentage change
            current_value (int): Current trend value
        """
        slack_config = self.config['notifications']['slack']
        
        if not slack_config['enabled']:
            return
        
        try:
            message = {
                "channel": slack_config['channel'],
                "text": f"🚨 Trend Alert: {keyword}",
                "attachments": [
                    {
                        "fields": [
                            {
                                "title": "Keyword",
                                "value": keyword,
                                "short": True
                            },
                            {
                                "title": "Current Value",
                                "value": str(current_value),
                                "short": True
                            },
                            {
                                "title": "Change",
                                "value": f"{change_percentage:.2f}%",
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "short": True
                            }
                        ],
                        "color": "danger" if change_percentage < 0 else "good"
                    }
                ]
            }
            
            response = requests.post(slack_config['webhook_url'], json=message)
            response.raise_for_status()
            
            logger.info(f"Slack alert sent for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")
    
    def send_webhook_alert(self, keyword: str, change_percentage: float, current_value: int):
        """
        Send webhook alert for trend change.
        
        Args:
            keyword (str): Keyword that triggered alert
            change_percentage (float): Percentage change
            current_value (int): Current trend value
        """
        webhook_config = self.config['notifications']['webhook']
        
        if not webhook_config['enabled']:
            return
        
        try:
            payload = {
                "keyword": keyword,
                "current_value": current_value,
                "change_percentage": change_percentage,
                "timestamp": datetime.now().isoformat(),
                "alert_type": "trend_change"
            }
            
            response = requests.post(
                webhook_config['url'],
                json=payload,
                headers=webhook_config['headers']
            )
            response.raise_for_status()
            
            logger.info(f"Webhook alert sent for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"Error sending webhook alert: {e}")
    
    def save_monitoring_data(self, data: Dict[str, Any]):
        """
        Save monitoring data to file or database.
        
        Args:
            data (Dict): Monitoring data to save
        """
        storage_config = self.config['data_storage']
        
        if storage_config['save_to_file']:
            try:
                # Ensure directory exists
                os.makedirs(storage_config['file_path'], exist_ok=True)
                
                # Save to JSON file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{storage_config['file_path']}trends_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                
                logger.debug(f"Monitoring data saved to {filename}")
                
            except Exception as e:
                logger.error(f"Error saving monitoring data: {e}")
    
    def run_monitoring_cycle(self):
        """
        Run one complete monitoring cycle.
        """
        logger.info("Starting monitoring cycle")
        
        for geo in self.config['geographic_locations']:
            logger.info(f"Monitoring keywords in {geo}")
            
            # Get current trends
            current_trends = self.get_current_trends(self.config['keywords'], geo)
            
            for keyword, trend_data in current_trends.items():
                current_value = trend_data['current_value']
                
                # Calculate trend change
                change_percentage = self.calculate_trend_change(keyword, current_value, geo)
                
                logger.info(f"{keyword} ({geo}): {current_value} (change: {change_percentage:.2f}%)")
                
                # Check for alerts
                if self.check_alert_conditions(keyword, change_percentage):
                    logger.warning(f"Alert triggered for {keyword}: {change_percentage:.2f}% change")
                    
                    # Send notifications
                    self.send_email_alert(keyword, change_percentage, current_value)
                    self.send_slack_alert(keyword, change_percentage, current_value)
                    self.send_webhook_alert(keyword, change_percentage, current_value)
                    
                    # Record alert
                    self.alert_history.append({
                        'keyword': keyword,
                        'change_percentage': change_percentage,
                        'current_value': current_value,
                        'location': geo,
                        'timestamp': datetime.now()
                    })
            
            # Save monitoring data
            self.save_monitoring_data({
                'timestamp': datetime.now().isoformat(),
                'location': geo,
                'trends': current_trends
            })
    
    def start_monitoring(self):
        """
        Start continuous monitoring.
        """
        logger.info("Starting trend monitoring service")
        
        try:
            while True:
                self.run_monitoring_cycle()
                
                # Wait for next cycle
                interval = self.config['monitoring_interval']
                logger.info(f"Monitoring cycle completed. Waiting {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            raise


def main():
    """Main function to run the trend monitor."""
    print("🚀 Starting Google Search Trends Monitor")
    print("=" * 50)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Initialize and start monitor
    monitor = TrendMonitor()
    monitor.start_monitoring()


if __name__ == "__main__":
    main() 