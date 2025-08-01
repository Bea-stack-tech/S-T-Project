"""
Main Trends Analyzer for Google Search Trends API Project

This module provides the core functionality for analyzing Google Search Trends data,
including real-time trends, historical data, and geographic comparisons.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import pandas as pd
import numpy as np

from pytrends.request import TrendReq
from .api_clients.pytrends_client import PyTrendsClient
from .data_processors.trends_processor import TrendsDataProcessor
from .visualizations.trends_visualizer import TrendsVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendsAnalyzer:
    """
    Main class for analyzing Google Search Trends data.
    
    This class provides a high-level interface for fetching, processing,
    and analyzing Google Search Trends data using various API clients.
    """
    
    def __init__(self, 
                 api_client: str = "pytrends",
                 language: str = "en-US",
                 timezone: int = 360,
                 retries: int = 3,
                 timeout: int = 30):
        """
        Initialize the Trends Analyzer.
        
        Args:
            api_client (str): The API client to use ("pytrends", "google", "custom")
            language (str): Language for the API requests
            timezone (int): Timezone offset in minutes
            retries (int): Number of retries for failed requests
            timeout (int): Request timeout in seconds
        """
        self.api_client = api_client
        self.language = language
        self.timezone = timezone
        self.retries = retries
        self.timeout = timeout
        
        # Initialize API client
        self._init_api_client()
        
        # Initialize data processor and visualizer
        self.data_processor = TrendsDataProcessor()
        self.visualizer = TrendsVisualizer()
        
        logger.info(f"TrendsAnalyzer initialized with {api_client} client")
    
    def _init_api_client(self):
        """Initialize the appropriate API client."""
        if self.api_client == "pytrends":
            self.client = PyTrendsClient(
                language=self.language,
                timezone=self.timezone,
                retries=self.retries,
                timeout=self.timeout
            )
        else:
            raise ValueError(f"Unsupported API client: {self.api_client}")
    
    def get_trending_searches(self, 
                            geo: str = "US",
                            limit: int = 20) -> Dict[str, Any]:
        """
        Get current trending searches for a specific location.
        
        Args:
            geo (str): Geographic location (e.g., "US", "GB", "CA")
            limit (int): Maximum number of trends to return
            
        Returns:
            Dict containing trending searches data
        """
        try:
            logger.info(f"Fetching trending searches for {geo}")
            trends = self.client.get_trending_searches(geo=geo)
            
            if trends and len(trends) > limit:
                trends = trends[:limit]
            
            return {
                "geo": geo,
                "timestamp": datetime.now().isoformat(),
                "trends": trends,
                "count": len(trends) if trends else 0
            }
        except Exception as e:
            logger.error(f"Error fetching trending searches: {e}")
            return {"error": str(e)}
    
    def get_historical_trends(self,
                            keyword: str,
                            timeframe: str = "today 12-m",
                            geo: str = "US",
                            category: int = 0) -> Dict[str, Any]:
        """
        Get historical trend data for a specific keyword.
        
        Args:
            keyword (str): Search term to analyze
            timeframe (str): Time range (e.g., "today 12-m", "2023-01-01 2024-01-01")
            geo (str): Geographic location
            category (int): Search category (0 for all categories)
            
        Returns:
            Dict containing historical trends data
        """
        try:
            logger.info(f"Fetching historical trends for '{keyword}' in {geo}")
            
            # Build payload
            payload = {
                "kw_list": [keyword],
                "cat": category,
                "geo": geo,
                "timeframe": timeframe
            }
            
            # Get interest over time
            interest_data = self.client.get_interest_over_time(payload)
            
            # Get related topics and queries
            related_topics = self.client.get_related_topics(payload)
            related_queries = self.client.get_related_queries(payload)
            
            # Process the data
            processed_data = self.data_processor.process_historical_data(
                interest_data, related_topics, related_queries
            )
            
            return {
                "keyword": keyword,
                "geo": geo,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "data": processed_data
            }
        except Exception as e:
            logger.error(f"Error fetching historical trends: {e}")
            return {"error": str(e)}
    
    def compare_keywords(self,
                        keywords: List[str],
                        timeframe: str = "today 12-m",
                        geo: str = "US") -> Dict[str, Any]:
        """
        Compare trends between multiple keywords.
        
        Args:
            keywords (List[str]): List of keywords to compare
            timeframe (str): Time range for comparison
            geo (str): Geographic location
            
        Returns:
            Dict containing comparison data
        """
        try:
            logger.info(f"Comparing keywords: {keywords}")
            
            if len(keywords) > 5:
                logger.warning("Limiting to 5 keywords for comparison")
                keywords = keywords[:5]
            
            payload = {
                "kw_list": keywords,
                "geo": geo,
                "timeframe": timeframe
            }
            
            # Get interest over time for all keywords
            interest_data = self.client.get_interest_over_time(payload)
            
            # Process comparison data
            comparison_data = self.data_processor.process_comparison_data(
                interest_data, keywords
            )
            
            return {
                "keywords": keywords,
                "geo": geo,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "comparison": comparison_data
            }
        except Exception as e:
            logger.error(f"Error comparing keywords: {e}")
            return {"error": str(e)}
    
    def get_geographic_trends(self,
                            keyword: str,
                            timeframe: str = "today 12-m",
                            countries: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get geographic distribution of trends for a keyword.
        
        Args:
            keyword (str): Search term to analyze
            timeframe (str): Time range
            countries (List[str], optional): List of countries to compare
            
        Returns:
            Dict containing geographic trends data
        """
        try:
            logger.info(f"Fetching geographic trends for '{keyword}'")
            
            if not countries:
                countries = ["US", "GB", "CA", "AU", "DE", "FR", "JP", "IN", "BR", "MX"]
            
            geographic_data = {}
            
            for country in countries:
                payload = {
                    "kw_list": [keyword],
                    "geo": country,
                    "timeframe": timeframe
                }
                
                interest_data = self.client.get_interest_over_time(payload)
                if interest_data is not None and not interest_data.empty:
                    avg_interest = interest_data[keyword].mean()
                    geographic_data[country] = {
                        "average_interest": float(avg_interest),
                        "max_interest": float(interest_data[keyword].max()),
                        "min_interest": float(interest_data[keyword].min())
                    }
            
            return {
                "keyword": keyword,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "geographic_data": geographic_data
            }
        except Exception as e:
            logger.error(f"Error fetching geographic trends: {e}")
            return {"error": str(e)}
    
    def get_related_topics(self,
                          keyword: str,
                          timeframe: str = "today 12-m",
                          geo: str = "US") -> Dict[str, Any]:
        """
        Get related topics for a keyword.
        
        Args:
            keyword (str): Search term to analyze
            timeframe (str): Time range
            geo (str): Geographic location
            
        Returns:
            Dict containing related topics data
        """
        try:
            logger.info(f"Fetching related topics for '{keyword}'")
            
            payload = {
                "kw_list": [keyword],
                "geo": geo,
                "timeframe": timeframe
            }
            
            related_topics = self.client.get_related_topics(payload)
            
            return {
                "keyword": keyword,
                "geo": geo,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "related_topics": related_topics
            }
        except Exception as e:
            logger.error(f"Error fetching related topics: {e}")
            return {"error": str(e)}
    
    def get_related_queries(self,
                           keyword: str,
                           timeframe: str = "today 12-m",
                           geo: str = "US") -> Dict[str, Any]:
        """
        Get related queries for a keyword.
        
        Args:
            keyword (str): Search term to analyze
            timeframe (str): Time range
            geo (str): Geographic location
            
        Returns:
            Dict containing related queries data
        """
        try:
            logger.info(f"Fetching related queries for '{keyword}'")
            
            payload = {
                "kw_list": [keyword],
                "geo": geo,
                "timeframe": timeframe
            }
            
            related_queries = self.client.get_related_queries(payload)
            
            return {
                "keyword": keyword,
                "geo": geo,
                "timeframe": timeframe,
                "timestamp": datetime.now().isoformat(),
                "related_queries": related_queries
            }
        except Exception as e:
            logger.error(f"Error fetching related queries: {e}")
            return {"error": str(e)}
    
    def export_data(self,
                   data: Dict[str, Any],
                   format: str = "json",
                   filename: Optional[str] = None) -> str:
        """
        Export data to various formats.
        
        Args:
            data (Dict): Data to export
            format (str): Export format ("json", "csv", "excel")
            filename (str, optional): Custom filename
            
        Returns:
            str: Path to exported file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"trends_export_{timestamp}.{format}"
            
            export_path = f"data/exports/{filename}"
            
            if format == "json":
                self.data_processor.export_to_json(data, export_path)
            elif format == "csv":
                self.data_processor.export_to_csv(data, export_path)
            elif format == "excel":
                self.data_processor.export_to_excel(data, export_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Data exported to {export_path}")
            return export_path
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    def create_visualization(self,
                           data: Dict[str, Any],
                           chart_type: str = "line",
                           save_path: Optional[str] = None) -> str:
        """
        Create visualizations from trends data.
        
        Args:
            data (Dict): Data to visualize
            chart_type (str): Type of chart ("line", "bar", "heatmap", "wordcloud")
            save_path (str, optional): Path to save the visualization
            
        Returns:
            str: Path to saved visualization
        """
        try:
            if not save_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"data/exports/visualization_{chart_type}_{timestamp}.png"
            
            if chart_type == "line":
                self.visualizer.create_line_chart(data, save_path)
            elif chart_type == "bar":
                self.visualizer.create_bar_chart(data, save_path)
            elif chart_type == "heatmap":
                self.visualizer.create_heatmap(data, save_path)
            elif chart_type == "wordcloud":
                self.visualizer.create_wordcloud(data, save_path)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            logger.info(f"Visualization saved to {save_path}")
            return save_path
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            raise
    
    def get_summary_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics for trends data.
        
        Args:
            data (Dict): Trends data to analyze
            
        Returns:
            Dict containing summary statistics
        """
        try:
            return self.data_processor.generate_summary_statistics(data)
        except Exception as e:
            logger.error(f"Error generating summary statistics: {e}")
            return {"error": str(e)}
    
    async def get_realtime_trends(self, geo: str = "US") -> Dict[str, Any]:
        """
        Get real-time trending searches (async version).
        
        Args:
            geo (str): Geographic location
            
        Returns:
            Dict containing real-time trends
        """
        try:
            logger.info(f"Fetching real-time trends for {geo}")
            
            # Simulate async operation
            await asyncio.sleep(0.1)
            
            return self.get_trending_searches(geo=geo)
        except Exception as e:
            logger.error(f"Error fetching real-time trends: {e}")
            return {"error": str(e)} 