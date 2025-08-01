"""
Tests for Value SERP Client

This module contains unit tests for the ValueSerpClient class.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from src.api_clients.valueserp_client import ValueSerpClient


class TestValueSerpClient:
    """Test cases for ValueSerpClient class."""
    
    @pytest.fixture
    def client(self):
        """Create a ValueSerpClient instance for testing."""
        return ValueSerpClient(api_key="test_api_key")
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock API response."""
        mock = Mock()
        mock.json.return_value = {
            "organic_results": [
                {
                    "title": "Test Result 1",
                    "link": "https://example.com/1",
                    "snippet": "This is a test result",
                    "position": 1,
                    "displayed_link": "example.com"
                },
                {
                    "title": "Test Result 2",
                    "link": "https://example.com/2",
                    "snippet": "This is another test result",
                    "position": 2,
                    "displayed_link": "example.com"
                }
            ]
        }
        mock.raise_for_status.return_value = None
        return mock
    
    def test_init(self, client):
        """Test client initialization."""
        assert client.api_key == "test_api_key"
        assert client.base_url == "https://api.valueserp.com"
        assert client.retries == 3
        assert client.timeout == 30
        assert client.backoff_factor == 2.0
    
    def test_init_with_custom_base_url(self):
        """Test client initialization with custom base URL."""
        client = ValueSerpClient(api_key="test_key", base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"
    
    @patch('requests.Session.get')
    def test_search_success(self, mock_get, client, mock_response):
        """Test successful search request."""
        mock_get.return_value = mock_response
        
        result = client.search("test query")
        
        assert result is not None
        assert "organic_results" in result
        assert len(result["organic_results"]) == 2
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "api_key" in call_args[1]["params"]
        assert call_args[1]["params"]["q"] == "test query"
    
    @patch('requests.Session.get')
    def test_search_with_parameters(self, mock_get, client, mock_response):
        """Test search request with additional parameters."""
        mock_get.return_value = mock_response
        
        result = client.search(
            query="test query",
            location="United States",
            gl="us",
            hl="en",
            num=5,
            start=10,
            safe="active"
        )
        
        assert result is not None
        
        # Verify parameters were passed correctly
        call_args = mock_get.call_args
        params = call_args[1]["params"]
        assert params["q"] == "test query"
        assert params["location"] == "United States"
        assert params["gl"] == "us"
        assert params["hl"] == "en"
        assert params["num"] == 5
        assert params["start"] == 10
        assert params["safe"] == "active"
    
    @patch('requests.Session.get')
    def test_search_api_error(self, mock_get, client):
        """Test search request with API error."""
        mock_response = Mock()
        mock_response.json.return_value = {"error": "API key invalid"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception, match="API Error: API key invalid"):
            client.search("test query")
    
    @patch('requests.Session.get')
    def test_search_http_error(self, mock_get, client):
        """Test search request with HTTP error."""
        mock_get.side_effect = Exception("Connection error")
        
        result = client.search("test query")
        assert result is None
    
    @patch('requests.Session.get')
    def test_places_success(self, mock_get, client):
        """Test successful places request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "places_results": [
                {
                    "title": "Test Place",
                    "address": "123 Test St",
                    "phone": "555-1234",
                    "rating": 4.5
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = client.places("restaurants")
        
        assert result is not None
        assert "places_results" in result
        assert len(result["places_results"]) == 1
    
    @patch('requests.Session.get')
    def test_news_success(self, mock_get, client):
        """Test successful news request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "news_results": [
                {
                    "title": "Test News",
                    "link": "https://news.com/test",
                    "source": "Test News",
                    "date": "2024-01-01"
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = client.news("tech news")
        
        assert result is not None
        assert "news_results" in result
        assert len(result["news_results"]) == 1
    
    @patch('requests.Session.get')
    def test_shopping_success(self, mock_get, client):
        """Test successful shopping request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "shopping_results": [
                {
                    "title": "Test Product",
                    "price": "$99.99",
                    "source": "Test Store",
                    "rating": 4.0
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = client.shopping("laptop")
        
        assert result is not None
        assert "shopping_results" in result
        assert len(result["shopping_results"]) == 1
    
    def test_extract_search_results(self, client):
        """Test search results extraction."""
        data = {
            "organic_results": [
                {
                    "title": "Test Result",
                    "link": "https://example.com",
                    "snippet": "Test snippet",
                    "position": 1,
                    "displayed_link": "example.com"
                }
            ]
        }
        
        results = client.extract_search_results(data)
        
        assert len(results) == 1
        assert results[0]["title"] == "Test Result"
        assert results[0]["link"] == "https://example.com"
        assert results[0]["position"] == 1
    
    def test_extract_search_results_empty(self, client):
        """Test search results extraction with empty data."""
        results = client.extract_search_results({})
        assert results == []
        
        results = client.extract_search_results(None)
        assert results == []
    
    def test_extract_places_results(self, client):
        """Test places results extraction."""
        data = {
            "places_results": [
                {
                    "title": "Test Place",
                    "address": "123 Test St",
                    "phone": "555-1234",
                    "rating": 4.5,
                    "reviews": 100
                }
            ]
        }
        
        results = client.extract_places_results(data)
        
        assert len(results) == 1
        assert results[0]["title"] == "Test Place"
        assert results[0]["address"] == "123 Test St"
        assert results[0]["rating"] == 4.5
    
    def test_extract_news_results(self, client):
        """Test news results extraction."""
        data = {
            "news_results": [
                {
                    "title": "Test News",
                    "link": "https://news.com/test",
                    "snippet": "Test news snippet",
                    "source": "Test News",
                    "date": "2024-01-01"
                }
            ]
        }
        
        results = client.extract_news_results(data)
        
        assert len(results) == 1
        assert results[0]["title"] == "Test News"
        assert results[0]["source"] == "Test News"
        assert results[0]["date"] == "2024-01-01"
    
    def test_extract_shopping_results(self, client):
        """Test shopping results extraction."""
        data = {
            "shopping_results": [
                {
                    "title": "Test Product",
                    "price": "$99.99",
                    "currency": "USD",
                    "rating": 4.0,
                    "reviews": 50,
                    "source": "Test Store"
                }
            ]
        }
        
        results = client.extract_shopping_results(data)
        
        assert len(results) == 1
        assert results[0]["title"] == "Test Product"
        assert results[0]["price"] == "$99.99"
        assert results[0]["rating"] == 4.0
    
    def test_to_dataframe(self, client):
        """Test DataFrame conversion."""
        results = [
            {"title": "Test 1", "value": 100},
            {"title": "Test 2", "value": 200}
        ]
        
        df = client.to_dataframe(results)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "title" in df.columns
        assert "value" in df.columns
    
    def test_to_dataframe_empty(self, client):
        """Test DataFrame conversion with empty results."""
        df = client.to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    @patch.object(ValueSerpClient, 'search')
    @patch.object(ValueSerpClient, 'places')
    @patch.object(ValueSerpClient, 'shopping')
    @patch.object(ValueSerpClient, 'news')
    def test_get_serp_insights(self, mock_news, mock_shopping, mock_places, mock_search, client):
        """Test comprehensive SERP insights."""
        # Mock responses
        mock_search.return_value = {"organic_results": [{"title": "Test Search"}]}
        mock_places.return_value = {"places_results": [{"title": "Test Place"}]}
        mock_shopping.return_value = {"shopping_results": [{"title": "Test Product"}]}
        mock_news.return_value = {"news_results": [{"title": "Test News"}]}
        
        insights = client.get_serp_insights("test query")
        
        assert insights["query"] == "test query"
        assert len(insights["search_results"]) == 1
        assert len(insights["places_results"]) == 1
        assert len(insights["shopping_results"]) == 1
        assert len(insights["news_results"]) == 1
        assert insights["summary"]["total_search_results"] == 1
        assert insights["summary"]["total_places_results"] == 1
        assert insights["summary"]["total_shopping_results"] == 1
        assert insights["summary"]["total_news_results"] == 1
    
    @patch.object(ValueSerpClient, 'search')
    @patch.object(ValueSerpClient, 'places')
    @patch.object(ValueSerpClient, 'shopping')
    @patch.object(ValueSerpClient, 'news')
    def test_get_serp_insights_with_errors(self, mock_news, mock_shopping, mock_places, mock_search, client):
        """Test SERP insights with some API errors."""
        # Mock some successful and some failed responses
        mock_search.return_value = {"organic_results": [{"title": "Test Search"}]}
        mock_places.return_value = None  # Simulate error
        mock_shopping.return_value = {"shopping_results": [{"title": "Test Product"}]}
        mock_news.return_value = None  # Simulate error
        
        insights = client.get_serp_insights("test query")
        
        assert insights["query"] == "test query"
        assert len(insights["search_results"]) == 1
        assert insights["places_results"] is None
        assert len(insights["shopping_results"]) == 1
        assert insights["news_results"] is None
        assert insights["summary"]["total_search_results"] == 1
        assert insights["summary"]["total_shopping_results"] == 1
        assert "total_places_results" not in insights["summary"]
        assert "total_news_results" not in insights["summary"]
    
    def test_retry_logic(self, client):
        """Test retry logic with exponential backoff."""
        # This test would require more complex mocking of the session
        # For now, we'll test that the retry parameters are set correctly
        assert client.retries == 3
        assert client.backoff_factor == 2.0
    
    def test_session_headers(self, client):
        """Test that session headers are set correctly."""
        assert client.session.headers["User-Agent"] == "ValueSerp-Python-Client/1.0"
        assert client.session.headers["Accept"] == "application/json"


if __name__ == "__main__":
    pytest.main([__file__]) 