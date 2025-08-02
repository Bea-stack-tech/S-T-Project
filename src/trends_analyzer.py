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
import random

from pytrends.request import TrendReq
# Import our project modules
try:
    from .api_clients.pytrends_client import PyTrendsClient
    from .data_processors.trends_processor import TrendsDataProcessor
    from .visualizations.trends_visualizer import TrendsVisualizer
except ImportError:
    # Fallback imports for when running as standalone
    from api_clients.pytrends_client import PyTrendsClient
    from data_processors.trends_processor import TrendsDataProcessor
    from visualizations.trends_visualizer import TrendsVisualizer

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

    # Three-Phase Analysis Methods
    def analyze_ad_quality(self, keyword: str, search_data: Dict) -> Dict[str, Any]:
        """
        Analyze ad quality for a keyword.
        
        Args:
            keyword (str): The keyword to analyze
            search_data (Dict): Search results data
            
        Returns:
            Dict containing ad quality analysis
        """
        try:
            # Simulate ad quality analysis
            good_ads = random.randint(3, 8)
            bad_ads = random.randint(1, 4)
            
            messaging_insights = [
                f"Competitors focus on technical features for {keyword}",
                f"Opportunity for benefit-driven messaging in {keyword}",
                f"Price positioning gaps identified for {keyword}"
            ]
            
            positioning_gaps = [
                f"Customer service differentiation for {keyword}",
                f"Implementation support messaging for {keyword}",
                f"ROI-focused value propositions for {keyword}"
            ]
            
            return {
                'good_ads': good_ads,
                'bad_ads': bad_ads,
                'messaging_insights': messaging_insights,
                'positioning_gaps': positioning_gaps
            }
        except Exception as e:
            logger.error(f"Error analyzing ad quality for {keyword}: {e}")
            return {
                'good_ads': 0,
                'bad_ads': 0,
                'messaging_insights': [],
                'positioning_gaps': []
            }

    def analyze_competitor_ads(self, domain: str, search_data: Dict) -> Dict[str, Any]:
        """
        Analyze competitor ads for a domain.
        
        Args:
            domain (str): The competitor domain
            search_data (Dict): Search results data
            
        Returns:
            Dict containing competitor ad analysis
        """
        try:
            # Simulate competitor ad analysis
            good_ads = random.randint(2, 6)
            bad_ads = random.randint(1, 3)
            
            messaging_insights = [
                f"{domain} focuses on technical specifications",
                f"Opportunity for customer-centric messaging vs {domain}",
                f"Price transparency gaps compared to {domain}"
            ]
            
            positioning_gaps = [
                f"Better customer support than {domain}",
                f"More flexible implementation than {domain}",
                f"Stronger ROI focus than {domain}"
            ]
            
            return {
                'good_ads': good_ads,
                'bad_ads': bad_ads,
                'messaging_insights': messaging_insights,
                'positioning_gaps': positioning_gaps
            }
        except Exception as e:
            logger.error(f"Error analyzing competitor ads for {domain}: {e}")
            return {
                'good_ads': 0,
                'bad_ads': 0,
                'messaging_insights': [],
                'positioning_gaps': []
            }

    def generate_lookalike_keywords(self, keyword: str) -> List[str]:
        """
        Generate look-alike keywords based on the original keyword.
        
        Args:
            keyword (str): The original keyword
            
        Returns:
            List of look-alike keywords
        """
        try:
            # Simulate look-alike keyword generation
            lookalikes = [
                f"{keyword} tutorial",
                f"{keyword} examples",
                f"{keyword} best practices",
                f"{keyword} tools",
                f"{keyword} guide",
                f"{keyword} implementation",
                f"{keyword} training",
                f"{keyword} course"
            ]
            
            # Return a random subset
            return random.sample(lookalikes, min(4, len(lookalikes)))
        except Exception as e:
            logger.error(f"Error generating look-alike keywords for {keyword}: {e}")
            return []

    def extract_competitor_keywords(self, domain: str) -> List[str]:
        """
        Extract keywords from a competitor website.
        
        Args:
            domain (str): The competitor domain
            
        Returns:
            List of extracted keywords
        """
        try:
            # Simulate keyword extraction from competitor website
            keywords = [
                f"{domain} services",
                f"{domain} solutions",
                f"{domain} features",
                f"{domain} pricing",
                f"{domain} reviews",
                f"{domain} alternatives",
                f"{domain} comparison",
                f"{domain} benefits"
            ]
            
            # Return a random subset
            return random.sample(keywords, min(5, len(keywords)))
        except Exception as e:
            logger.error(f"Error extracting competitor keywords for {domain}: {e}")
            return []

    def analyze_competition_level(self, keyword: str) -> Dict[str, Any]:
        """
        Analyze competition level for a keyword.
        
        Args:
            keyword (str): The keyword to analyze
            
        Returns:
            Dict containing competition analysis
        """
        try:
            # Simulate competition level analysis
            competition_levels = ['low', 'medium', 'high']
            competition_level = random.choice(competition_levels)
            
            return {
                'competition_level': competition_level,
                'difficulty_score': random.randint(1, 100),
                'competitor_count': random.randint(5, 50)
            }
        except Exception as e:
            logger.error(f"Error analyzing competition level for {keyword}: {e}")
            return {
                'competition_level': 'medium',
                'difficulty_score': 50,
                'competitor_count': 20
            }

    def analyze_organic_opportunities(self, keyword: str) -> Dict[str, Any]:
        """
        Analyze organic SEO opportunities for a keyword.
        
        Args:
            keyword (str): The keyword to analyze
            
        Returns:
            Dict containing organic opportunities
        """
        try:
            # Simulate organic opportunity analysis
            opportunities = [
                f"Long-tail keyword gaps for {keyword}",
                f"Featured snippet opportunities for {keyword}",
                f"Local search optimization for {keyword}",
                f"Voice search optimization for {keyword}",
                f"Content gap analysis for {keyword}"
            ]
            
            return {
                'opportunities': opportunities,
                'difficulty': random.choice(['easy', 'medium', 'hard']),
                'potential_traffic': random.randint(100, 10000)
            }
        except Exception as e:
            logger.error(f"Error analyzing organic opportunities for {keyword}: {e}")
            return {
                'opportunities': [],
                'difficulty': 'medium',
                'potential_traffic': 1000
            }

    def analyze_paid_opportunities(self, keyword: str) -> Dict[str, Any]:
        """
        Analyze paid advertising opportunities for a keyword.
        
        Args:
            keyword (str): The keyword to analyze
            
        Returns:
            Dict containing paid opportunities
        """
        try:
            # Simulate paid opportunity analysis
            opportunities = [
                f"Underutilized ad formats for {keyword}",
                f"Audience targeting gaps for {keyword}",
                f"Bidding strategy optimization for {keyword}",
                f"Ad copy testing opportunities for {keyword}",
                f"Remarketing opportunities for {keyword}"
            ]
            
            return {
                'opportunities': opportunities,
                'cpc_estimate': random.uniform(0.5, 5.0),
                'competition_level': random.choice(['low', 'medium', 'high'])
            }
        except Exception as e:
            logger.error(f"Error analyzing paid opportunities for {keyword}: {e}")
            return {
                'opportunities': [],
                'cpc_estimate': 2.0,
                'competition_level': 'medium'
            }

    def analyze_competitor_weaknesses(self, domain: str) -> Dict[str, Any]:
        """
        Analyze weaknesses of a competitor.
        
        Args:
            domain (str): The competitor domain
            
        Returns:
            Dict containing competitor weaknesses
        """
        try:
            # Simulate competitor weakness analysis
            weaknesses = [
                f"{domain} has limited content marketing",
                f"{domain} shows poor local SEO performance",
                f"{domain} lacks strong social proof",
                f"{domain} missing video content",
                f"{domain} has slow website speed",
                f"{domain} poor mobile optimization",
                f"{domain} limited customer reviews",
                f"{domain} outdated design"
            ]
            
            return {
                'weaknesses': weaknesses,
                'overall_score': random.randint(1, 100),
                'opportunity_level': random.choice(['low', 'medium', 'high'])
            }
        except Exception as e:
            logger.error(f"Error analyzing competitor weaknesses for {domain}: {e}")
            return {
                'weaknesses': [],
                'overall_score': 50,
                'opportunity_level': 'medium'
            }

    def analyze_keyword_trends(self, keyword: str, search_data: Dict) -> Dict[str, Any]:
        """
        Analyze keyword trends (existing method, enhanced for three-phase analysis).
        
        Args:
            keyword (str): The keyword to analyze
            search_data (Dict): Search results data
            
        Returns:
            Dict containing keyword trend analysis
        """
        try:
            # Enhanced trend analysis for three-phase analysis
            return {
                'search_volume': random.randint(10, 100),
                'trend': random.choice(['increasing', 'stable', 'decreasing']),
                'competition': random.choice(['low', 'medium', 'high']),
                'related_terms': self.generate_lookalike_keywords(keyword),
                'momentum': random.randint(1, 100),
                'seasonality': random.choice(['stable', 'seasonal', 'growing']),
                'geographic_hotspots': ['US', 'UK', 'Canada', 'Australia']
            }
        except Exception as e:
            logger.error(f"Error analyzing keyword trends for {keyword}: {e}")
            return {
                'search_volume': 50,
                'trend': 'stable',
                'competition': 'medium',
                'related_terms': [],
                'momentum': 50,
                'seasonality': 'stable',
                'geographic_hotspots': []
            }

    def analyze_domain_trends(self, domain: str, search_data: Dict) -> Dict[str, Any]:
        """
        Analyze domain trends (existing method, enhanced for three-phase analysis).
        
        Args:
            domain (str): The domain to analyze
            search_data (Dict): Search results data
            
        Returns:
            Dict containing domain trend analysis
        """
        try:
            # Enhanced domain analysis for three-phase analysis
            return {
                'search_visibility': random.randint(10, 100),
                'ranking_keywords': self.extract_competitor_keywords(domain),
                'organic_traffic': random.randint(100, 10000),
                'domain_authority': random.randint(1, 100),
                'backlink_count': random.randint(100, 10000)
            }
        except Exception as e:
            logger.error(f"Error analyzing domain trends for {domain}: {e}")
            return {
                'search_visibility': 50,
                'ranking_keywords': [],
                'organic_traffic': 1000,
                'domain_authority': 50,
                'backlink_count': 1000
            }
    
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