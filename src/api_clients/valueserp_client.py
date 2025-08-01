"""
Value SERP Client for Google Search Trends API Project

This module provides a wrapper around the Value SERP API from Traject Data
for accessing comprehensive SERP (Search Engine Results Page) data including
Google Search, Maps, Shopping, News, Products, and Reviews.
"""

import time
import logging
import requests
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class ValueSerpClient:
    """
    Value SERP API client for accessing comprehensive Google SERP data.
    
    This class provides access to various Google data endpoints including:
    - Google Search results
    - Google Maps results
    - Google Shopping results
    - Google News results
    - Google Product results
    - Google Reviews
    """
    
    def __init__(self,
                 api_key: str,
                 base_url: str = "https://api.valueserp.com",
                 retries: int = 3,
                 timeout: int = 30,
                 backoff_factor: float = 2.0):
        """
        Initialize the Value SERP client.
        
        Args:
            api_key (str): Your Value SERP API key
            base_url (str): Base URL for the API
            retries (int): Number of retries for failed requests
            timeout (int): Request timeout in seconds
            backoff_factor (float): Exponential backoff factor
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.retries = retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ValueSerp-Python-Client/1.0',
            'Accept': 'application/json'
        })
        
        logger.info(f"ValueSerpClient initialized with base_url={base_url}")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make a request to the Value SERP API with retry logic.
        
        Args:
            endpoint (str): API endpoint
            params (Dict): Request parameters
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        # Add API key to parameters
        params['api_key'] = self.api_key
        
        last_exception = None
        
        for attempt in range(self.retries + 1):
            try:
                logger.debug(f"Making request to {url} (attempt {attempt + 1})")
                
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                
                data = response.json()
                
                # Check for API errors
                if 'error' in data:
                    raise Exception(f"API Error: {data['error']}")
                
                return data
                
            except requests.exceptions.RequestException as e:
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
    
    def search(self,
               query: str,
               location: str = "United States",
               gl: str = "us",
               hl: str = "en",
               num: int = 10,
               start: int = 0,
               safe: str = "active",
               **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google search results for a query.
        
        Args:
            query (str): Search query
            location (str): Location for search
            gl (str): Country code (e.g., "us", "uk")
            hl (str): Language code (e.g., "en", "es")
            num (int): Number of results to return
            start (int): Starting position for results
            safe (str): Safe search setting
            **kwargs: Additional parameters
            
        Returns:
            Search results data
        """
        try:
            logger.info(f"Fetching search results for query: '{query}'")
            
            params = {
                'q': query,
                'location': location,
                'gl': gl,
                'hl': hl,
                'num': num,
                'start': start,
                'safe': safe,
                **kwargs
            }
            
            return self._make_request('/search', params)
            
        except Exception as e:
            logger.error(f"Error fetching search results: {e}")
            return None
    
    def places(self,
               query: str,
               location: str = "United States",
               gl: str = "us",
               hl: str = "en",
               num: int = 10,
               **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google Maps results for a query.
        
        Args:
            query (str): Search query
            location (str): Location for search
            gl (str): Country code
            hl (str): Language code
            num (int): Number of results to return
            **kwargs: Additional parameters
            
        Returns:
            Places results data
        """
        try:
            logger.info(f"Fetching places results for query: '{query}'")
            
            params = {
                'q': query,
                'location': location,
                'gl': gl,
                'hl': hl,
                'num': num,
                **kwargs
            }
            
            return self._make_request('/places', params)
            
        except Exception as e:
            logger.error(f"Error fetching places results: {e}")
            return None
    
    def shopping(self,
                query: str,
                location: str = "United States",
                gl: str = "us",
                hl: str = "en",
                num: int = 10,
                **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google Shopping results for a query.
        
        Args:
            query (str): Search query
            location (str): Location for search
            gl (str): Country code
            hl (str): Language code
            num (int): Number of results to return
            **kwargs: Additional parameters
            
        Returns:
            Shopping results data
        """
        try:
            logger.info(f"Fetching shopping results for query: '{query}'")
            
            params = {
                'q': query,
                'location': location,
                'gl': gl,
                'hl': hl,
                'num': num,
                **kwargs
            }
            
            return self._make_request('/shopping', params)
            
        except Exception as e:
            logger.error(f"Error fetching shopping results: {e}")
            return None
    
    def news(self,
             query: str,
             location: str = "United States",
             gl: str = "us",
             hl: str = "en",
             num: int = 10,
             **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google News results for a query.
        
        Args:
            query (str): Search query
            location (str): Location for search
            gl (str): Country code
            hl (str): Language code
            num (int): Number of results to return
            **kwargs: Additional parameters
            
        Returns:
            News results data
        """
        try:
            logger.info(f"Fetching news results for query: '{query}'")
            
            params = {
                'q': query,
                'location': location,
                'gl': gl,
                'hl': hl,
                'num': num,
                **kwargs
            }
            
            return self._make_request('/news', params)
            
        except Exception as e:
            logger.error(f"Error fetching news results: {e}")
            return None
    
    def product(self,
                product_id: str,
                location: str = "United States",
                gl: str = "us",
                hl: str = "en",
                **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google Product results for a product ID.
        
        Args:
            product_id (str): Product ID
            location (str): Location for search
            gl (str): Country code
            hl (str): Language code
            **kwargs: Additional parameters
            
        Returns:
            Product results data
        """
        try:
            logger.info(f"Fetching product results for ID: '{product_id}'")
            
            params = {
                'product_id': product_id,
                'location': location,
                'gl': gl,
                'hl': hl,
                **kwargs
            }
            
            return self._make_request('/product', params)
            
        except Exception as e:
            logger.error(f"Error fetching product results: {e}")
            return None
    
    def place_reviews(self,
                     place_id: str,
                     location: str = "United States",
                     gl: str = "us",
                     hl: str = "en",
                     num: int = 10,
                     **kwargs) -> Optional[Dict[str, Any]]:
        """
        Get Google Reviews for a place.
        
        Args:
            place_id (str): Place ID
            location (str): Location for search
            gl (str): Country code
            hl (str): Language code
            num (int): Number of reviews to return
            **kwargs: Additional parameters
            
        Returns:
            Place reviews data
        """
        try:
            logger.info(f"Fetching place reviews for ID: '{place_id}'")
            
            params = {
                'place_id': place_id,
                'location': location,
                'gl': gl,
                'hl': hl,
                'num': num,
                **kwargs
            }
            
            return self._make_request('/place_reviews', params)
            
        except Exception as e:
            logger.error(f"Error fetching place reviews: {e}")
            return None
    
    def extract_search_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format search results from API response.
        
        Args:
            data (Dict): API response data
            
        Returns:
            List of formatted search results
        """
        results = []
        
        if not data or 'organic_results' not in data:
            return results
        
        for result in data['organic_results']:
            formatted_result = {
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'position': result.get('position', 0),
                'displayed_link': result.get('displayed_link', ''),
                'date': result.get('date', ''),
                'rich_snippet': result.get('rich_snippet', {}),
                'sitelinks': result.get('sitelinks', [])
            }
            results.append(formatted_result)
        
        return results
    
    def extract_places_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format places results from API response.
        
        Args:
            data (Dict): API response data
            
        Returns:
            List of formatted places results
        """
        results = []
        
        if not data or 'places_results' not in data:
            return results
        
        for result in data['places_results']:
            formatted_result = {
                'title': result.get('title', ''),
                'address': result.get('address', ''),
                'phone': result.get('phone', ''),
                'website': result.get('website', ''),
                'rating': result.get('rating', 0),
                'reviews': result.get('reviews', 0),
                'type': result.get('type', ''),
                'hours': result.get('hours', ''),
                'latitude': result.get('latitude', 0),
                'longitude': result.get('longitude', 0)
            }
            results.append(formatted_result)
        
        return results
    
    def extract_shopping_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format shopping results from API response.
        
        Args:
            data (Dict): API response data
            
        Returns:
            List of formatted shopping results
        """
        results = []
        
        if not data or 'shopping_results' not in data:
            return results
        
        for result in data['shopping_results']:
            formatted_result = {
                'title': result.get('title', ''),
                'price': result.get('price', ''),
                'currency': result.get('currency', ''),
                'rating': result.get('rating', 0),
                'reviews': result.get('reviews', 0),
                'source': result.get('source', ''),
                'link': result.get('link', ''),
                'image': result.get('image', ''),
                'shipping': result.get('shipping', ''),
                'condition': result.get('condition', '')
            }
            results.append(formatted_result)
        
        return results
    
    def extract_news_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract and format news results from API response.
        
        Args:
            data (Dict): API response data
            
        Returns:
            List of formatted news results
        """
        results = []
        
        if not data or 'news_results' not in data:
            return results
        
        for result in data['news_results']:
            formatted_result = {
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'source': result.get('source', ''),
                'date': result.get('date', ''),
                'thumbnail': result.get('thumbnail', ''),
                'position': result.get('position', 0)
            }
            results.append(formatted_result)
        
        return results
    
    def to_dataframe(self, results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert results to pandas DataFrame.
        
        Args:
            results (List): List of result dictionaries
            
        Returns:
            DataFrame with results
        """
        if not results:
            return pd.DataFrame()
        
        return pd.DataFrame(results)
    
    def get_serp_insights(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive SERP insights for a query.
        
        Args:
            query (str): Search query
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with comprehensive SERP insights
        """
        insights = {
            'query': query,
            'search_results': None,
            'places_results': None,
            'shopping_results': None,
            'news_results': None,
            'summary': {}
        }
        
        try:
            # Get search results
            search_data = self.search(query, **kwargs)
            if search_data:
                insights['search_results'] = self.extract_search_results(search_data)
                insights['summary']['total_search_results'] = len(insights['search_results'])
            
            # Get places results
            places_data = self.places(query, **kwargs)
            if places_data:
                insights['places_results'] = self.extract_places_results(places_data)
                insights['summary']['total_places_results'] = len(insights['places_results'])
            
            # Get shopping results
            shopping_data = self.shopping(query, **kwargs)
            if shopping_data:
                insights['shopping_results'] = self.extract_shopping_results(shopping_data)
                insights['summary']['total_shopping_results'] = len(insights['shopping_results'])
            
            # Get news results
            news_data = self.news(query, **kwargs)
            if news_data:
                insights['news_results'] = self.extract_news_results(news_data)
                insights['summary']['total_news_results'] = len(insights['news_results'])
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting SERP insights: {e}")
            return insights 