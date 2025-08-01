"""
Tests for TrendsAnalyzer

This module contains unit tests for the TrendsAnalyzer class.
"""

import pytest
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from trends_analyzer import TrendsAnalyzer


class TestTrendsAnalyzer:
    """Test cases for TrendsAnalyzer class."""
    
    def test_initialization(self):
        """Test TrendsAnalyzer initialization."""
        analyzer = TrendsAnalyzer()
        assert analyzer is not None
        assert analyzer.api_client == "pytrends"
        assert analyzer.language == "en-US"
        assert analyzer.timezone == 360
    
    def test_initialization_with_custom_params(self):
        """Test TrendsAnalyzer initialization with custom parameters."""
        analyzer = TrendsAnalyzer(
            api_client="pytrends",
            language="en-GB",
            timezone=0,
            retries=5,
            timeout=60
        )
        assert analyzer.language == "en-GB"
        assert analyzer.timezone == 0
        assert analyzer.retries == 5
        assert analyzer.timeout == 60
    
    def test_invalid_api_client(self):
        """Test initialization with invalid API client."""
        with pytest.raises(ValueError):
            TrendsAnalyzer(api_client="invalid_client")
    
    def test_get_summary_statistics_empty_data(self):
        """Test get_summary_statistics with empty data."""
        analyzer = TrendsAnalyzer()
        empty_data = {}
        summary = analyzer.get_summary_statistics(empty_data)
        assert "timestamp" in summary
        assert summary["data_type"] == "unknown"
    
    def test_export_data_invalid_format(self):
        """Test export_data with invalid format."""
        analyzer = TrendsAnalyzer()
        test_data = {"test": "data"}
        
        with pytest.raises(ValueError):
            analyzer.export_data(test_data, format="invalid_format")
    
    def test_create_visualization_invalid_chart_type(self):
        """Test create_visualization with invalid chart type."""
        analyzer = TrendsAnalyzer()
        test_data = {"test": "data"}
        
        with pytest.raises(ValueError):
            analyzer.create_visualization(test_data, chart_type="invalid_type")


if __name__ == "__main__":
    pytest.main([__file__]) 