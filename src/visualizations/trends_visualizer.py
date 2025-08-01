"""
Trends Visualizer for Google Search Trends API Project

This module provides visualization utilities for creating charts, graphs,
and other visual representations of Google Search Trends data.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from wordcloud import WordCloud

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)


class TrendsVisualizer:
    """
    Visualizer for Google Search Trends data.
    
    This class provides utilities for creating various types of charts
    and visualizations from trends data.
    """
    
    def __init__(self, 
                 style: str = "default",
                 color_palette: str = "husl",
                 figsize: tuple = (12, 8)):
        """
        Initialize the Trends Visualizer.
        
        Args:
            style (str): Plotting style ("default", "dark", "light")
            color_palette (str): Color palette for charts
            figsize (tuple): Default figure size (width, height)
        """
        self.style = style
        self.color_palette = color_palette
        self.figsize = figsize
        
        # Set up plotting style
        self._setup_style()
        
        logger.info(f"TrendsVisualizer initialized with style={style}")
    
    def _setup_style(self):
        """Set up the plotting style."""
        if self.style == "dark":
            plt.style.use('dark_background')
            sns.set_style("darkgrid")
        elif self.style == "light":
            plt.style.use('default')
            sns.set_style("whitegrid")
        else:
            plt.style.use('seaborn-v0_8')
            sns.set_style("whitegrid")
        
        sns.set_palette(self.color_palette)
    
    def create_line_chart(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a line chart from trends data.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the chart
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            if "interest_over_time" in data and "timeline" in data["interest_over_time"]:
                timeline_data = data["interest_over_time"]["timeline"]
                
                # Convert to DataFrame for easier plotting
                df = pd.DataFrame(timeline_data)
                df['date'] = pd.to_datetime(df['date'])
                
                # Plot each keyword
                keywords = df['keyword'].unique()
                for keyword in keywords:
                    keyword_data = df[df['keyword'] == keyword]
                    ax.plot(keyword_data['date'], keyword_data['interest'], 
                           label=keyword, linewidth=2, marker='o', markersize=4)
                
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('Interest', fontsize=12)
                ax.set_title('Google Trends Interest Over Time', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)
                plt.tight_layout()
                
            elif "comparison" in data and "interest_data" in data["comparison"]:
                # Plot comparison data
                interest_data = data["comparison"]["interest_data"]
                keywords = data["comparison"]["keywords"]
                
                for keyword in keywords:
                    if keyword in interest_data and "timeline" in interest_data[keyword]:
                        timeline_data = interest_data[keyword]["timeline"]
                        df = pd.DataFrame(timeline_data)
                        df['date'] = pd.to_datetime(df['date'])
                        
                        ax.plot(df['date'], df['interest'], 
                               label=keyword, linewidth=2, marker='o', markersize=4)
                
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('Interest', fontsize=12)
                ax.set_title('Keyword Comparison Over Time', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
            
            # Save the chart
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Line chart saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            raise
    
    def create_bar_chart(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a bar chart from trends data.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the chart
        """
        try:
            fig, ax = plt.subplots(figsize=self.figsize)
            
            if "trends" in data:
                # Bar chart for trending searches
                trends = data["trends"]
                if isinstance(trends, list) and len(trends) > 0:
                    # Take first 10 trends
                    top_trends = trends[:10]
                    labels = [str(trend) for trend in top_trends]
                    values = list(range(len(top_trends), 0, -1))  # Reverse order for ranking
                    
                    bars = ax.barh(labels, values, color=sns.color_palette("viridis", len(labels)))
                    ax.set_xlabel('Ranking', fontsize=12)
                    ax.set_title('Top Trending Searches', fontsize=14, fontweight='bold')
                    ax.invert_yaxis()  # Show top trend at the top
                    
                    # Add value labels on bars
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                               f'#{len(trends) - i}', ha='left', va='center')
            
            elif "interest_over_time" in data and "statistics" in data["interest_over_time"]:
                # Bar chart for keyword statistics
                stats = data["interest_over_time"]["statistics"]
                if stats:
                    keywords = list(stats.keys())
                    means = [stats[k]["mean"] for k in keywords]
                    
                    bars = ax.bar(keywords, means, color=sns.color_palette("Set3", len(keywords)))
                    ax.set_xlabel('Keywords', fontsize=12)
                    ax.set_ylabel('Average Interest', fontsize=12)
                    ax.set_title('Average Interest by Keyword', fontsize=14, fontweight='bold')
                    plt.xticks(rotation=45)
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                               f'{height:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save the chart
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Bar chart saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            raise
    
    def create_heatmap(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a heatmap from trends data.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the chart
        """
        try:
            if "comparison" in data and "correlation_matrix" in data["comparison"]:
                corr_matrix = data["comparison"]["correlation_matrix"]
                
                if corr_matrix:
                    # Convert to DataFrame
                    df_corr = pd.DataFrame(corr_matrix)
                    
                    fig, ax = plt.subplots(figsize=self.figsize)
                    
                    # Create heatmap
                    sns.heatmap(df_corr, annot=True, cmap='coolwarm', center=0,
                              square=True, linewidths=0.5, cbar_kws={"shrink": .8})
                    
                    ax.set_title('Keyword Correlation Matrix', fontsize=14, fontweight='bold')
                    plt.tight_layout()
                    
                    # Save the chart
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')
                    plt.close()
                    
                    logger.info(f"Heatmap saved to {save_path}")
                else:
                    logger.warning("No correlation matrix data available for heatmap")
            else:
                logger.warning("No comparison data available for heatmap")
                
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            raise
    
    def create_wordcloud(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a word cloud from trends data.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the chart
        """
        try:
            # Extract text data for word cloud
            text_data = []
            
            if "trends" in data and isinstance(data["trends"], list):
                text_data.extend(data["trends"])
            
            if "related_topics" in data:
                for keyword, topics in data["related_topics"].items():
                    for topic_type, topic_list in topics.items():
                        for topic in topic_list:
                            if isinstance(topic, dict) and "topic_title" in topic:
                                text_data.append(topic["topic_title"])
                            elif isinstance(topic, str):
                                text_data.append(topic)
            
            if "related_queries" in data:
                for keyword, queries in data["related_queries"].items():
                    for query_type, query_list in queries.items():
                        for query in query_list:
                            if isinstance(query, dict) and "query" in query:
                                text_data.append(query["query"])
                            elif isinstance(query, str):
                                text_data.append(query)
            
            if text_data:
                # Combine all text
                text = ' '.join([str(item) for item in text_data])
                
                # Create word cloud
                wordcloud = WordCloud(
                    width=800, height=600,
                    background_color='white',
                    colormap='viridis',
                    max_words=100,
                    relative_scaling=0.5,
                    random_state=42
                ).generate(text)
                
                fig, ax = plt.subplots(figsize=self.figsize)
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title('Trends Word Cloud', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                
                # Save the chart
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                logger.info(f"Word cloud saved to {save_path}")
            else:
                logger.warning("No text data available for word cloud")
                
        except Exception as e:
            logger.error(f"Error creating word cloud: {e}")
            raise
    
    def create_interactive_chart(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create an interactive chart using Plotly.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the chart (HTML format)
        """
        try:
            if "interest_over_time" in data and "timeline" in data["interest_over_time"]:
                timeline_data = data["interest_over_time"]["timeline"]
                
                # Convert to DataFrame
                df = pd.DataFrame(timeline_data)
                df['date'] = pd.to_datetime(df['date'])
                
                # Create interactive line chart
                fig = px.line(df, x='date', y='interest', color='keyword',
                            title='Google Trends Interest Over Time (Interactive)',
                            labels={'date': 'Date', 'interest': 'Interest', 'keyword': 'Keyword'})
                
                fig.update_layout(
                    title_font_size=16,
                    title_font_color='#2c3e50',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    hovermode='x unified'
                )
                
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                
                # Save as HTML
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                fig.write_html(save_path)
                
                logger.info(f"Interactive chart saved to {save_path}")
            else:
                logger.warning("No timeline data available for interactive chart")
                
        except Exception as e:
            logger.error(f"Error creating interactive chart: {e}")
            raise
    
    def create_dashboard(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a comprehensive dashboard with multiple charts.
        
        Args:
            data (Dict): Trends data to visualize
            save_path (str): Path to save the dashboard
        """
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Interest Over Time', 'Keyword Statistics', 
                              'Trending Searches', 'Correlation Matrix'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Add line chart (top left)
            if "interest_over_time" in data and "timeline" in data["interest_over_time"]:
                timeline_data = data["interest_over_time"]["timeline"]
                df = pd.DataFrame(timeline_data)
                df['date'] = pd.to_datetime(df['date'])
                
                keywords = df['keyword'].unique()
                for keyword in keywords:
                    keyword_data = df[df['keyword'] == keyword]
                    fig.add_trace(
                        go.Scatter(x=keyword_data['date'], y=keyword_data['interest'],
                                 mode='lines+markers', name=keyword),
                        row=1, col=1
                    )
            
            # Add bar chart (top right)
            if "interest_over_time" in data and "statistics" in data["interest_over_time"]:
                stats = data["interest_over_time"]["statistics"]
                if stats:
                    keywords = list(stats.keys())
                    means = [stats[k]["mean"] for k in keywords]
                    
                    fig.add_trace(
                        go.Bar(x=keywords, y=means, name='Average Interest'),
                        row=1, col=2
                    )
            
            # Add trending searches (bottom left)
            if "trends" in data and isinstance(data["trends"], list):
                trends = data["trends"][:10]  # Top 10
                fig.add_trace(
                    go.Bar(x=list(range(len(trends))), y=list(range(len(trends), 0, -1)),
                          text=trends, textposition='auto', name='Trending Searches'),
                    row=2, col=1
                )
            
            # Add correlation heatmap (bottom right)
            if "comparison" in data and "correlation_matrix" in data["comparison"]:
                corr_matrix = data["comparison"]["correlation_matrix"]
                if corr_matrix:
                    df_corr = pd.DataFrame(corr_matrix)
                    fig.add_trace(
                        go.Heatmap(z=df_corr.values, x=df_corr.columns, y=df_corr.index,
                                 colorscale='RdBu', name='Correlation'),
                        row=2, col=2
                    )
            
            # Update layout
            fig.update_layout(
                title_text="Google Trends Dashboard",
                title_font_size=20,
                showlegend=True,
                height=800
            )
            
            # Save as HTML
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.write_html(save_path)
            
            logger.info(f"Dashboard saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            raise
    
    def create_geographic_chart(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a geographic visualization of trends data.
        
        Args:
            data (Dict): Trends data with geographic information
            save_path (str): Path to save the chart
        """
        try:
            if "geographic_data" in data:
                geo_data = data["geographic_data"]
                
                if geo_data:
                    # Create choropleth map
                    countries = list(geo_data.keys())
                    values = [geo_data[country]["average_interest"] for country in countries]
                    
                    fig = go.Figure(data=go.Choropleth(
                        locations=countries,
                        z=values,
                        locationmode='ISO-3166-1',
                        colorscale='Viridis',
                        marker_line_color='darkgray',
                        marker_line_width=0.5,
                        colorbar_title="Average Interest"
                    ))
                    
                    fig.update_layout(
                        title_text=f"Geographic Distribution: {data.get('keyword', 'Unknown')}",
                        geo=dict(
                            showframe=False,
                            showcoastlines=True,
                            projection_type='equirectangular'
                        )
                    )
                    
                    # Save as HTML
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    fig.write_html(save_path)
                    
                    logger.info(f"Geographic chart saved to {save_path}")
                else:
                    logger.warning("No geographic data available")
            else:
                logger.warning("No geographic data in the provided data")
                
        except Exception as e:
            logger.error(f"Error creating geographic chart: {e}")
            raise
    
    def create_summary_chart(self, data: Dict[str, Any], save_path: str) -> None:
        """
        Create a summary chart with key statistics.
        
        Args:
            data (Dict): Trends data to summarize
            save_path (str): Path to save the chart
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Summary statistics
            if "summary_stats" in data:
                stats = data["summary_stats"]
                
                # Total keywords and data points
                if "total_keywords" in stats and "total_data_points" in stats:
                    ax1.pie([stats["total_keywords"], stats["total_data_points"]], 
                           labels=['Keywords', 'Data Points'], autopct='%1.1f%%')
                    ax1.set_title('Data Overview')
                
                # Date range
                if "date_range" in stats and "duration_days" in stats["date_range"]:
                    ax2.bar(['Duration'], [stats["date_range"]["duration_days"]])
                    ax2.set_title('Analysis Period (Days)')
                    ax2.set_ylabel('Days')
                
                # Overall statistics
                if "overall_stats" in stats:
                    overall = stats["overall_stats"]
                    metrics = ['Mean', 'Median', 'Std']
                    values = [overall.get('mean', 0), overall.get('median', 0), overall.get('std', 0)]
                    ax3.bar(metrics, values)
                    ax3.set_title('Overall Statistics')
                    ax3.set_ylabel('Interest Value')
                
                # Insights
                if "insights" in stats and stats["insights"]:
                    insights = stats["insights"][:5]  # Top 5 insights
                    ax4.text(0.1, 0.9, 'Key Insights:', transform=ax4.transAxes, 
                            fontsize=12, fontweight='bold')
                    for i, insight in enumerate(insights):
                        ax4.text(0.1, 0.8 - i*0.15, f'• {insight}', transform=ax4.transAxes, 
                                fontsize=10, wrap=True)
                    ax4.set_xlim(0, 1)
                    ax4.set_ylim(0, 1)
                    ax4.axis('off')
                    ax4.set_title('Insights')
            
            plt.tight_layout()
            
            # Save the chart
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Summary chart saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error creating summary chart: {e}")
            raise 