"""
Trends Data Processor for Google Search Trends API Project

This module provides data processing utilities for cleaning, transforming,
and analyzing Google Search Trends data.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class TrendsDataProcessor:
    """
    Data processor for Google Search Trends data.
    
    This class provides utilities for processing, cleaning, and analyzing
    trends data from various sources.
    """
    
    def __init__(self):
        """Initialize the Trends Data Processor."""
        logger.info("TrendsDataProcessor initialized")
    
    def process_historical_data(self,
                               interest_data: pd.DataFrame,
                               related_topics: Dict[str, pd.DataFrame],
                               related_queries: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Process historical trends data.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            related_topics (Dict): Related topics data
            related_queries (Dict): Related queries data
            
        Returns:
            Dict containing processed historical data
        """
        try:
            processed_data = {
                "interest_over_time": {},
                "related_topics": {},
                "related_queries": {},
                "summary_stats": {}
            }
            
            # Process interest over time data
            if interest_data is not None and not interest_data.empty:
                processed_data["interest_over_time"] = self._process_interest_data(interest_data)
            
            # Process related topics
            if related_topics:
                processed_data["related_topics"] = self._process_related_topics(related_topics)
            
            # Process related queries
            if related_queries:
                processed_data["related_queries"] = self._process_related_queries(related_queries)
            
            # Generate summary statistics
            processed_data["summary_stats"] = self._generate_interest_summary(interest_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing historical data: {e}")
            return {"error": str(e)}
    
    def process_comparison_data(self,
                               interest_data: pd.DataFrame,
                               keywords: List[str]) -> Dict[str, Any]:
        """
        Process comparison data for multiple keywords.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data for multiple keywords
            keywords (List[str]): List of keywords being compared
            
        Returns:
            Dict containing processed comparison data
        """
        try:
            comparison_data = {
                "keywords": keywords,
                "interest_data": {},
                "correlation_matrix": {},
                "summary_stats": {}
            }
            
            if interest_data is not None and not interest_data.empty:
                # Process interest data for each keyword
                for keyword in keywords:
                    if keyword in interest_data.columns:
                        comparison_data["interest_data"][keyword] = self._process_interest_data(
                            interest_data[[keyword]]
                        )
                
                # Calculate correlation matrix
                comparison_data["correlation_matrix"] = self._calculate_correlation_matrix(interest_data)
                
                # Generate summary statistics
                comparison_data["summary_stats"] = self._generate_comparison_summary(interest_data, keywords)
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"Error processing comparison data: {e}")
            return {"error": str(e)}
    
    def _process_interest_data(self, interest_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Process interest over time data.
        
        Args:
            interest_data (pd.DataFrame): Raw interest data
            
        Returns:
            Dict containing processed interest data
        """
        try:
            processed = {
                "timeline": [],
                "statistics": {},
                "peaks": [],
                "trends": {}
            }
            
            if interest_data is None or interest_data.empty:
                return processed
            
            # Convert to timeline format
            for date, row in interest_data.iterrows():
                for column in interest_data.columns:
                    if column != 'isPartial':
                        processed["timeline"].append({
                            "date": date.isoformat(),
                            "keyword": column,
                            "interest": int(row[column]) if pd.notna(row[column]) else 0
                        })
            
            # Calculate statistics for each keyword
            for column in interest_data.columns:
                if column != 'isPartial':
                    values = interest_data[column].dropna()
                    if not values.empty:
                        processed["statistics"][column] = {
                            "mean": float(values.mean()),
                            "max": float(values.max()),
                            "min": float(values.min()),
                            "std": float(values.std()),
                            "median": float(values.median())
                        }
            
            # Find peaks (local maxima)
            processed["peaks"] = self._find_peaks(interest_data)
            
            # Analyze trends
            processed["trends"] = self._analyze_trends(interest_data)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing interest data: {e}")
            return {"error": str(e)}
    
    def _process_related_topics(self, related_topics: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Process related topics data.
        
        Args:
            related_topics (Dict): Raw related topics data
            
        Returns:
            Dict containing processed related topics data
        """
        try:
            processed = {}
            
            for keyword, topics_data in related_topics.items():
                if topics_data is not None and not topics_data.empty:
                    processed[keyword] = {
                        "top": topics_data.get('top', pd.DataFrame()).to_dict('records') if 'top' in topics_data else [],
                        "rising": topics_data.get('rising', pd.DataFrame()).to_dict('records') if 'rising' in topics_data else []
                    }
                else:
                    processed[keyword] = {"top": [], "rising": []}
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing related topics: {e}")
            return {"error": str(e)}
    
    def _process_related_queries(self, related_queries: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Process related queries data.
        
        Args:
            related_queries (Dict): Raw related queries data
            
        Returns:
            Dict containing processed related queries data
        """
        try:
            processed = {}
            
            for keyword, queries_data in related_queries.items():
                if queries_data is not None and not queries_data.empty:
                    processed[keyword] = {
                        "top": queries_data.get('top', pd.DataFrame()).to_dict('records') if 'top' in queries_data else [],
                        "rising": queries_data.get('rising', pd.DataFrame()).to_dict('records') if 'rising' in queries_data else []
                    }
                else:
                    processed[keyword] = {"top": [], "rising": []}
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing related queries: {e}")
            return {"error": str(e)}
    
    def _find_peaks(self, interest_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Find peaks (local maxima) in interest data.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            
        Returns:
            List of peak data
        """
        try:
            peaks = []
            
            for column in interest_data.columns:
                if column != 'isPartial':
                    values = interest_data[column].dropna()
                    if len(values) > 2:
                        # Find local maxima
                        for i in range(1, len(values) - 1):
                            if values.iloc[i] > values.iloc[i-1] and values.iloc[i] > values.iloc[i+1]:
                                peaks.append({
                                    "keyword": column,
                                    "date": values.index[i].isoformat(),
                                    "value": int(values.iloc[i]),
                                    "position": i
                                })
            
            # Sort by value (descending)
            peaks.sort(key=lambda x: x["value"], reverse=True)
            
            return peaks[:10]  # Return top 10 peaks
            
        except Exception as e:
            logger.error(f"Error finding peaks: {e}")
            return []
    
    def _analyze_trends(self, interest_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in interest data.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            
        Returns:
            Dict containing trend analysis
        """
        try:
            trends = {}
            
            for column in interest_data.columns:
                if column != 'isPartial':
                    values = interest_data[column].dropna()
                    if len(values) > 1:
                        # Calculate trend direction
                        first_half = values[:len(values)//2]
                        second_half = values[len(values)//2:]
                        
                        first_avg = first_half.mean()
                        second_avg = second_half.mean()
                        
                        if second_avg > first_avg * 1.1:
                            direction = "increasing"
                        elif second_avg < first_avg * 0.9:
                            direction = "decreasing"
                        else:
                            direction = "stable"
                        
                        # Calculate volatility
                        volatility = values.std() / values.mean() if values.mean() > 0 else 0
                        
                        trends[column] = {
                            "direction": direction,
                            "volatility": float(volatility),
                            "trend_strength": float(abs(second_avg - first_avg) / first_avg) if first_avg > 0 else 0
                        }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {}
    
    def _calculate_correlation_matrix(self, interest_data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calculate correlation matrix for multiple keywords.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            
        Returns:
            Dict containing correlation matrix
        """
        try:
            # Remove non-numeric columns
            numeric_data = interest_data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                return {}
            
            # Calculate correlation matrix
            corr_matrix = numeric_data.corr()
            
            # Convert to dictionary format
            correlation_dict = {}
            for col1 in corr_matrix.columns:
                correlation_dict[col1] = {}
                for col2 in corr_matrix.columns:
                    correlation_dict[col1][col2] = float(corr_matrix.loc[col1, col2])
            
            return correlation_dict
            
        except Exception as e:
            logger.error(f"Error calculating correlation matrix: {e}")
            return {}
    
    def _generate_interest_summary(self, interest_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for interest data.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            
        Returns:
            Dict containing summary statistics
        """
        try:
            summary = {
                "total_keywords": 0,
                "total_data_points": 0,
                "date_range": {},
                "overall_stats": {}
            }
            
            if interest_data is not None and not interest_data.empty:
                # Remove non-numeric columns
                numeric_data = interest_data.select_dtypes(include=[np.number])
                
                summary["total_keywords"] = len(numeric_data.columns)
                summary["total_data_points"] = len(numeric_data)
                
                # Date range
                if not numeric_data.empty:
                    summary["date_range"] = {
                        "start": numeric_data.index.min().isoformat(),
                        "end": numeric_data.index.max().isoformat(),
                        "duration_days": (numeric_data.index.max() - numeric_data.index.min()).days
                    }
                
                # Overall statistics
                if not numeric_data.empty:
                    all_values = numeric_data.values.flatten()
                    all_values = all_values[~np.isnan(all_values)]
                    
                    if len(all_values) > 0:
                        summary["overall_stats"] = {
                            "mean": float(np.mean(all_values)),
                            "median": float(np.median(all_values)),
                            "std": float(np.std(all_values)),
                            "min": float(np.min(all_values)),
                            "max": float(np.max(all_values))
                        }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating interest summary: {e}")
            return {"error": str(e)}
    
    def _generate_comparison_summary(self, interest_data: pd.DataFrame, keywords: List[str]) -> Dict[str, Any]:
        """
        Generate summary statistics for keyword comparison.
        
        Args:
            interest_data (pd.DataFrame): Interest over time data
            keywords (List[str]): List of keywords
            
        Returns:
            Dict containing comparison summary
        """
        try:
            summary = {
                "keywords": keywords,
                "keyword_stats": {},
                "comparison_metrics": {}
            }
            
            if interest_data is not None and not interest_data.empty:
                # Statistics for each keyword
                for keyword in keywords:
                    if keyword in interest_data.columns:
                        values = interest_data[keyword].dropna()
                        if not values.empty:
                            summary["keyword_stats"][keyword] = {
                                "mean": float(values.mean()),
                                "max": float(values.max()),
                                "min": float(values.min()),
                                "std": float(values.std()),
                                "trend": "increasing" if values.iloc[-1] > values.iloc[0] else "decreasing"
                            }
                
                # Comparison metrics
                if len(keywords) > 1:
                    summary["comparison_metrics"] = {
                        "highest_average": max(summary["keyword_stats"].items(), 
                                             key=lambda x: x[1]["mean"])[0] if summary["keyword_stats"] else None,
                        "most_volatile": max(summary["keyword_stats"].items(), 
                                           key=lambda x: x[1]["std"])[0] if summary["keyword_stats"] else None,
                        "most_trending": max(summary["keyword_stats"].items(), 
                                           key=lambda x: abs(x[1]["max"] - x[1]["min"]))[0] if summary["keyword_stats"] else None
                    }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating comparison summary: {e}")
            return {"error": str(e)}
    
    def generate_summary_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics for trends data.
        
        Args:
            data (Dict): Trends data to analyze
            
        Returns:
            Dict containing summary statistics
        """
        try:
            summary = {
                "timestamp": datetime.now().isoformat(),
                "data_type": self._identify_data_type(data),
                "statistics": {},
                "insights": []
            }
            
            # Generate statistics based on data type
            if "interest_over_time" in data:
                summary["statistics"].update(self._generate_interest_summary(
                    self._dict_to_dataframe(data["interest_over_time"])
                ))
            
            if "comparison" in data:
                summary["statistics"].update(self._generate_comparison_summary(
                    self._dict_to_dataframe(data["comparison"].get("interest_data", {})),
                    data["comparison"].get("keywords", [])
                ))
            
            # Generate insights
            summary["insights"] = self._generate_insights(data)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary statistics: {e}")
            return {"error": str(e)}
    
    def _identify_data_type(self, data: Dict[str, Any]) -> str:
        """Identify the type of data being analyzed."""
        if "comparison" in data:
            return "keyword_comparison"
        elif "interest_over_time" in data:
            return "historical_trends"
        elif "trends" in data:
            return "trending_searches"
        else:
            return "unknown"
    
    def _dict_to_dataframe(self, data_dict: Dict[str, Any]) -> pd.DataFrame:
        """Convert dictionary data to DataFrame format."""
        try:
            if "timeline" in data_dict:
                # Convert timeline data to DataFrame
                timeline_data = []
                for item in data_dict["timeline"]:
                    timeline_data.append({
                        "date": pd.to_datetime(item["date"]),
                        item["keyword"]: item["interest"]
                    })
                
                if timeline_data:
                    df = pd.DataFrame(timeline_data)
                    df.set_index("date", inplace=True)
                    return df
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error converting dict to DataFrame: {e}")
            return pd.DataFrame()
    
    def _generate_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate insights from the data."""
        insights = []
        
        try:
            # Add insights based on data type and content
            if "trends" in data and data["trends"]:
                insights.append(f"Found {len(data['trends'])} trending searches")
            
            if "interest_over_time" in data and "statistics" in data["interest_over_time"]:
                stats = data["interest_over_time"]["statistics"]
                if stats:
                    max_keyword = max(stats.items(), key=lambda x: x[1]["max"])[0]
                    insights.append(f"'{max_keyword}' had the highest peak interest")
            
            if "comparison" in data and "comparison_metrics" in data["comparison"]:
                metrics = data["comparison"]["comparison_metrics"]
                if metrics.get("highest_average"):
                    insights.append(f"'{metrics['highest_average']}' had the highest average interest")
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
        
        return insights
    
    def export_to_json(self, data: Dict[str, Any], filepath: str) -> None:
        """Export data to JSON format."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Data exported to JSON: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def export_to_csv(self, data: Dict[str, Any], filepath: str) -> None:
        """Export data to CSV format."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Convert data to DataFrame format
            if "interest_over_time" in data and "timeline" in data["interest_over_time"]:
                timeline_data = data["interest_over_time"]["timeline"]
                df = pd.DataFrame(timeline_data)
                df.to_csv(filepath, index=False)
            else:
                # Export as flattened JSON
                df = pd.json_normalize(data)
                df.to_csv(filepath, index=False)
            
            logger.info(f"Data exported to CSV: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def export_to_excel(self, data: Dict[str, Any], filepath: str) -> None:
        """Export data to Excel format."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Export different data types to different sheets
                if "interest_over_time" in data and "timeline" in data["interest_over_time"]:
                    timeline_data = data["interest_over_time"]["timeline"]
                    df_timeline = pd.DataFrame(timeline_data)
                    df_timeline.to_excel(writer, sheet_name='Timeline', index=False)
                
                if "statistics" in data:
                    df_stats = pd.DataFrame(data["statistics"]).T
                    df_stats.to_excel(writer, sheet_name='Statistics')
                
                if "related_topics" in data:
                    topics_data = []
                    for keyword, topics in data["related_topics"].items():
                        for topic_type, topic_list in topics.items():
                            for topic in topic_list:
                                topic["keyword"] = keyword
                                topic["type"] = topic_type
                                topics_data.append(topic)
                    
                    if topics_data:
                        df_topics = pd.DataFrame(topics_data)
                        df_topics.to_excel(writer, sheet_name='Related_Topics', index=False)
            
            logger.info(f"Data exported to Excel: {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise 