"""
PyTrends Client for Google Search Trends API Project

This module provides a wrapper around the pytrends library for accessing
Google Trends data with enhanced error handling and rate limiting.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from pytrends.request import TrendReq

logger = logging.getLogger(__name__)


class PyTrendsClient:
    """
    Enhanced PyTrends client with rate limiting and error handling.
    
    This class wraps the pytrends library to provide a more robust
    interface for accessing Google Trends data.
    """
    
    def __init__(self,
                 language: str = "en-US",
                 timezone: int = 360,
                 retries: int = 3,
                 timeout: int = 30,
                 backoff_factor: float = 2.0):
        """
        Initialize the PyTrends client.
        
        Args:
            language (str): Language for requests (e.g., "en-US")
            timezone (int): Timezone offset in minutes
            retries (int): Number of retries for failed requests
            timeout (int): Request timeout in seconds
            backoff_factor (float): Exponential backoff factor
        """
        self.language = language
        self.timezone = timezone
        self.retries = retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        
        # Initialize pytrends
        self.pytrends = TrendReq(
            hl=language,
            tz=timezone,
            timeout=timeout,
            retries=retries,
            backoff_factor=backoff_factor
        )
        
        logger.info(f"PyTrendsClient initialized with language={language}, timezone={timezone}")
    
    def _handle_rate_limit(self, delay: float = 1.0):
        """
        Handle rate limiting by adding delays between requests.
        
        Args:
            delay (float): Delay in seconds
        """
        time.sleep(delay)
    
    def _retry_request(self, func, *args, **kwargs):
        """
        Retry a request with exponential backoff.
        
        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Result of the function call
        """
        last_exception = None
        
        for attempt in range(self.retries + 1):
            try:
                result = func(*args, **kwargs)
                
                # Add delay between requests to respect rate limits
                self._handle_rate_limit()
                
                return result
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retries + 1}): {e}")
                
                if attempt < self.retries:
                    # Exponential backoff
                    delay = self.backoff_factor ** attempt
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Request failed after {self.retries + 1} attempts")
                    raise last_exception
    
    def get_trending_searches(self, geo: str = "US") -> List[str]:
        """
        Get current trending searches for a specific location.
        
        Args:
            geo (str): Geographic location (e.g., "US", "GB", "CA")
            
        Returns:
            List of trending search terms
        """
        try:
            logger.info(f"Fetching trending searches for {geo}")
            
            def _fetch_trends():
                return self.pytrends.trending_searches(pn=geo)
            
            trends = self._retry_request(_fetch_trends)
            
            if trends is not None and not trends.empty:
                return trends[0].tolist()
            else:
                logger.warning(f"No trending searches found for {geo}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching trending searches for {geo}: {e}")
            return []
    
    def get_interest_over_time(self, payload: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """
        Get interest over time data for keywords.
        
        Args:
            payload (Dict): Request payload with keywords and parameters
            
        Returns:
            DataFrame with interest over time data
        """
        try:
            logger.info(f"Fetching interest over time for {payload.get('kw_list', [])}")
            
            def _fetch_interest():
                return self.pytrends.interest_over_time(
                    kw_list=payload.get('kw_list', []),
                    cat=payload.get('cat', 0),
                    geo=payload.get('geo', ''),
                    timeframe=payload.get('timeframe', 'today 12-m'),
                    gprop=payload.get('gprop', '')
                )
            
            result = self._retry_request(_fetch_interest)
            
            if result is not None and not result.empty:
                # Remove the 'isPartial' column if it exists
                if 'isPartial' in result.columns:
                    result = result.drop('isPartial', axis=1)
                
                return result
            else:
                logger.warning("No interest over time data found")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching interest over time: {e}")
            return None
    
    def get_related_topics(self, payload: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Get related topics for keywords.
        
        Args:
            payload (Dict): Request payload with keywords and parameters
            
        Returns:
            Dictionary with related topics data for each keyword
        """
        try:
            logger.info(f"Fetching related topics for {payload.get('kw_list', [])}")
            
            def _fetch_topics():
                return self.pytrends.related_topics(
                    kw_list=payload.get('kw_list', []),
                    cat=payload.get('cat', 0),
                    geo=payload.get('geo', ''),
                    timeframe=payload.get('timeframe', 'today 12-m')
                )
            
            result = self._retry_request(_fetch_topics)
            
            if result:
                return result
            else:
                logger.warning("No related topics found")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching related topics: {e}")
            return {}
    
    def get_related_queries(self, payload: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """
        Get related queries for keywords.
        
        Args:
            payload (Dict): Request payload with keywords and parameters
            
        Returns:
            Dictionary with related queries data for each keyword
        """
        try:
            logger.info(f"Fetching related queries for {payload.get('kw_list', [])}")
            
            def _fetch_queries():
                return self.pytrends.related_queries(
                    kw_list=payload.get('kw_list', []),
                    cat=payload.get('cat', 0),
                    geo=payload.get('geo', ''),
                    timeframe=payload.get('timeframe', 'today 12-m')
                )
            
            result = self._retry_request(_fetch_queries)
            
            if result:
                return result
            else:
                logger.warning("No related queries found")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching related queries: {e}")
            return {}
    
    def get_interest_by_region(self, payload: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """
        Get interest by region data for keywords.
        
        Args:
            payload (Dict): Request payload with keywords and parameters
            
        Returns:
            DataFrame with interest by region data
        """
        try:
            logger.info(f"Fetching interest by region for {payload.get('kw_list', [])}")
            
            def _fetch_region_interest():
                return self.pytrends.interest_by_region(
                    kw_list=payload.get('kw_list', []),
                    cat=payload.get('cat', 0),
                    geo=payload.get('geo', ''),
                    timeframe=payload.get('timeframe', 'today 12-m'),
                    resolution=payload.get('resolution', 'COUNTRY')
                )
            
            result = self._retry_request(_fetch_region_interest)
            
            if result is not None and not result.empty:
                return result
            else:
                logger.warning("No interest by region data found")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching interest by region: {e}")
            return None
    
    def get_realtime_trending_searches(self, geo: str = "US") -> List[Dict[str, Any]]:
        """
        Get real-time trending searches for a specific location.
        
        Args:
            geo (str): Geographic location
            
        Returns:
            List of trending searches with metadata
        """
        try:
            logger.info(f"Fetching real-time trending searches for {geo}")
            
            def _fetch_realtime():
                return self.pytrends.realtime_trending_searches(pn=geo)
            
            result = self._retry_request(_fetch_realtime)
            
            if result is not None and not result.empty:
                # Convert to list of dictionaries
                trends = []
                for _, row in result.iterrows():
                    trend = {
                        'title': row.get('title', ''),
                        'traffic': row.get('traffic', ''),
                        'image_url': row.get('image', {}).get('newsUrl', ''),
                        'articles': row.get('articles', [])
                    }
                    trends.append(trend)
                
                return trends
            else:
                logger.warning(f"No real-time trending searches found for {geo}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching real-time trending searches: {e}")
            return []
    
    def get_top_charts(self, date: str = "20240101", geo: str = "US", cat: str = "all") -> List[Dict[str, Any]]:
        """
        Get top charts for a specific date and location.
        
        Args:
            date (str): Date in YYYYMMDD format
            geo (str): Geographic location
            cat (str): Category (e.g., "all", "entertainment", "sports")
            
        Returns:
            List of top charts data
        """
        try:
            logger.info(f"Fetching top charts for {date} in {geo}")
            
            def _fetch_charts():
                return self.pytrends.top_charts(date=date, hl=self.language, tz=self.timezone, geo=geo, cat=cat)
            
            result = self._retry_request(_fetch_charts)
            
            if result is not None and not result.empty:
                # Convert to list of dictionaries
                charts = []
                for _, row in result.iterrows():
                    chart = {
                        'title': row.get('title', ''),
                        'exploreQuery': row.get('exploreQuery', ''),
                        'rank': row.get('rank', 0),
                        'value': row.get('value', 0)
                    }
                    charts.append(chart)
                
                return charts
            else:
                logger.warning(f"No top charts found for {date} in {geo}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching top charts: {e}")
            return []
    
    def get_suggestions(self, keyword: str) -> List[str]:
        """
        Get search suggestions for a keyword.
        
        Args:
            keyword (str): Search term to get suggestions for
            
        Returns:
            List of suggested search terms
        """
        try:
            logger.info(f"Fetching suggestions for '{keyword}'")
            
            def _fetch_suggestions():
                return self.pytrends.suggestions(keyword)
            
            result = self._retry_request(_fetch_suggestions)
            
            if result:
                return [item.get('title', '') for item in result]
            else:
                logger.warning(f"No suggestions found for '{keyword}'")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching suggestions: {e}")
            return []
    
    def build_payload(self,
                     kw_list: List[str],
                     cat: int = 0,
                     geo: str = "",
                     timeframe: str = "today 12-m",
                     gprop: str = "") -> Dict[str, Any]:
        """
        Build a payload for API requests.
        
        Args:
            kw_list (List[str]): List of keywords
            cat (int): Category ID
            geo (str): Geographic location
            timeframe (str): Time range
            gprop (str): Google property (web, news, images, youtube, froogle)
            
        Returns:
            Dictionary with request payload
        """
        return {
            'kw_list': kw_list,
            'cat': cat,
            'geo': geo,
            'timeframe': timeframe,
            'gprop': gprop
        }
    
    def get_available_categories(self) -> Dict[int, str]:
        """
        Get available search categories.
        
        Returns:
            Dictionary mapping category IDs to names
        """
        # Common Google Trends categories
        categories = {
            0: "All categories",
            3: "Arts & Entertainment",
            12: "Autos & Vehicles",
            958: "Beauty & Fitness",
            5: "Books & Literature",
            958: "Business & Industrial",
            958: "Computers & Electronics",
            958: "Finance",
            958: "Food & Drink",
            958: "Games",
            958: "Health",
            958: "Hobbies & Leisure",
            958: "Home & Garden",
            958: "Internet & Telecom",
            958: "Jobs & Education",
            958: "Law & Government",
            958: "News",
            958: "Online Communities",
            958: "People & Society",
            958: "Pets & Animals",
            958: "Real Estate",
            958: "Reference",
            958: "Science",
            958: "Shopping",
            958: "Sports",
            958: "Travel"
        }
        
        return categories 