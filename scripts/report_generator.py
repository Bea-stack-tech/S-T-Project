#!/usr/bin/env python3
"""
Report Generator Script

This script generates comprehensive reports and visualizations from Google Search Trends data.
It can create various types of reports including trend analysis, comparisons, and insights.

Features:
- Automated report generation
- Multiple report formats (PDF, HTML, Excel)
- Customizable templates
- Interactive visualizations
- Trend insights and recommendations
- Scheduled reporting
"""

import os
import json
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add parent directory to path to import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_clients.pytrends_client import PyTrendsClient
from src.api_clients.valueserp_client import ValueSerpClient
from src.trends_analyzer import TrendsAnalyzer
from src.visualizations.trends_visualizer import TrendsVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/report_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Report generation class for creating comprehensive trend reports.
    """
    
    def __init__(self, config_file: str = "config/report_config.json"):
        """
        Initialize the report generator.
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config = self.load_config(config_file)
        self.analyzer = TrendsAnalyzer()
        self.pytrends_client = PyTrendsClient()
        self.visualizer = TrendsVisualizer()
        
        # Initialize Value SERP client if API key is available
        self.valueserp_client = None
        if os.getenv('VALUE_SERP_API_KEY'):
            self.valueserp_client = ValueSerpClient(api_key=os.getenv('VALUE_SERP_API_KEY'))
        
        # Create output directories
        self.create_output_directories()
        
        logger.info("Report Generator initialized")
    
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
            "report_types": {
                "trend_analysis": True,
                "comparison_report": True,
                "geographic_analysis": True,
                "insights_report": True,
                "executive_summary": True
            },
            "keywords": [
                "artificial intelligence", "machine learning", "python",
                "data science", "deep learning", "blockchain"
            ],
            "locations": ["US", "GB", "CA", "AU", "DE", "FR"],
            "timeframes": ["today 1-m", "today 3-m", "today 12-m"],
            "output": {
                "formats": ["html", "pdf", "excel"],
                "directory": "reports/",
                "include_charts": True,
                "include_insights": True,
                "template": "default"
            },
            "visualization": {
                "style": "seaborn",
                "color_palette": "husl",
                "figure_size": [12, 8],
                "dpi": 300
            },
            "insights": {
                "trend_threshold": 10,
                "correlation_threshold": 0.7,
                "include_recommendations": True
            }
        }
    
    def create_output_directories(self):
        """Create necessary output directories."""
        output_dir = self.config['output']['directory']
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('reports/charts', exist_ok=True)
        os.makedirs('reports/templates', exist_ok=True)
    
    def collect_trend_data(self, keywords: List[str], locations: List[str], timeframes: List[str]) -> Dict[str, Any]:
        """
        Collect trend data for report generation.
        
        Args:
            keywords (List[str]): Keywords to analyze
            locations (List[str]): Geographic locations
            timeframes (List[str]): Time periods
            
        Returns:
            Dictionary containing collected data
        """
        data = {
            'trends': {},
            'related_topics': {},
            'related_queries': {},
            'geographic_data': {},
            'metadata': {
                'collected_at': datetime.now().isoformat(),
                'keywords': keywords,
                'locations': locations,
                'timeframes': timeframes
            }
        }
        
        logger.info("Collecting trend data...")
        
        for keyword in keywords:
            data['trends'][keyword] = {}
            data['related_topics'][keyword] = {}
            data['related_queries'][keyword] = {}
            
            for location in locations:
                data['trends'][keyword][location] = {}
                data['geographic_data'][f"{keyword}_{location}"] = {}
                
                for timeframe in timeframes:
                    try:
                        # Get interest over time
                        payload = {
                            'kw_list': [keyword],
                            'geo': location,
                            'timeframe': timeframe
                        }
                        
                        trend_data = self.pytrends_client.get_interest_over_time(payload)
                        if trend_data is not None and not trend_data.empty:
                            data['trends'][keyword][location][timeframe] = trend_data
                        
                        # Get related topics
                        topics_data = self.pytrends_client.get_related_topics(payload)
                        if topics_data:
                            data['related_topics'][keyword][f"{location}_{timeframe}"] = topics_data
                        
                        # Get related queries
                        queries_data = self.pytrends_client.get_related_queries(payload)
                        if queries_data:
                            data['related_queries'][keyword][f"{location}_{timeframe}"] = queries_data
                        
                        # Get geographic interest
                        geo_data = self.pytrends_client.get_interest_by_region(payload)
                        if geo_data is not None and not geo_data.empty:
                            data['geographic_data'][f"{keyword}_{location}"][timeframe] = geo_data
                        
                        logger.info(f"Collected data for {keyword} in {location} ({timeframe})")
                        
                    except Exception as e:
                        logger.error(f"Error collecting data for {keyword} in {location} ({timeframe}): {e}")
        
        return data
    
    def generate_trend_analysis_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trend analysis report.
        
        Args:
            data (Dict): Collected trend data
            
        Returns:
            Dictionary containing trend analysis
        """
        logger.info("Generating trend analysis report...")
        
        analysis = {
            'summary': {},
            'trends': {},
            'insights': [],
            'recommendations': []
        }
        
        for keyword in data['trends']:
            analysis['trends'][keyword] = {}
            
            for location in data['trends'][keyword]:
                analysis['trends'][keyword][location] = {}
                
                for timeframe in data['trends'][keyword][location]:
                    trend_data = data['trends'][keyword][location][timeframe]
                    
                    if trend_data is not None and not trend_data.empty:
                        # Calculate trend statistics
                        values = trend_data[keyword].dropna()
                        if len(values) > 0:
                            stats = {
                                'mean': values.mean(),
                                'std': values.std(),
                                'min': values.min(),
                                'max': values.max(),
                                'trend_direction': 'increasing' if values.iloc[-1] > values.iloc[0] else 'decreasing',
                                'volatility': values.std() / values.mean() if values.mean() > 0 else 0,
                                'data_points': len(values)
                            }
                            
                            analysis['trends'][keyword][location][timeframe] = stats
                            
                            # Generate insights
                            if stats['trend_direction'] == 'increasing' and stats['mean'] > 50:
                                analysis['insights'].append({
                                    'type': 'high_trend',
                                    'keyword': keyword,
                                    'location': location,
                                    'timeframe': timeframe,
                                    'message': f"{keyword} shows strong upward trend in {location}"
                                })
                            
                            if stats['volatility'] > 0.5:
                                analysis['insights'].append({
                                    'type': 'high_volatility',
                                    'keyword': keyword,
                                    'location': location,
                                    'timeframe': timeframe,
                                    'message': f"{keyword} shows high volatility in {location}"
                                })
        
        return analysis
    
    def generate_comparison_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comparison report between keywords and locations.
        
        Args:
            data (Dict): Collected trend data
            
        Returns:
            Dictionary containing comparison analysis
        """
        logger.info("Generating comparison report...")
        
        comparison = {
            'keyword_comparisons': {},
            'location_comparisons': {},
            'correlations': {},
            'rankings': {}
        }
        
        # Compare keywords across locations
        for location in data['metadata']['locations']:
            comparison['location_comparisons'][location] = {}
            
            for timeframe in data['metadata']['timeframes']:
                keyword_scores = {}
                
                for keyword in data['trends']:
                    if location in data['trends'][keyword] and timeframe in data['trends'][keyword][location]:
                        trend_data = data['trends'][keyword][location][timeframe]
                        if trend_data is not None and not trend_data.empty:
                            values = trend_data[keyword].dropna()
                            if len(values) > 0:
                                keyword_scores[keyword] = values.mean()
                
                if keyword_scores:
                    # Sort by score
                    sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
                    comparison['location_comparisons'][location][timeframe] = {
                        'rankings': sorted_keywords,
                        'top_keyword': sorted_keywords[0][0] if sorted_keywords else None,
                        'score_range': {
                            'min': min(keyword_scores.values()),
                            'max': max(keyword_scores.values())
                        }
                    }
        
        # Compare locations for each keyword
        for keyword in data['trends']:
            comparison['keyword_comparisons'][keyword] = {}
            
            for timeframe in data['metadata']['timeframes']:
                location_scores = {}
                
                for location in data['metadata']['locations']:
                    if location in data['trends'][keyword] and timeframe in data['trends'][keyword][location]:
                        trend_data = data['trends'][keyword][location][timeframe]
                        if trend_data is not None and not trend_data.empty:
                            values = trend_data[keyword].dropna()
                            if len(values) > 0:
                                location_scores[location] = values.mean()
                
                if location_scores:
                    sorted_locations = sorted(location_scores.items(), key=lambda x: x[1], reverse=True)
                    comparison['keyword_comparisons'][keyword][timeframe] = {
                        'rankings': sorted_locations,
                        'top_location': sorted_locations[0][0] if sorted_locations else None,
                        'score_range': {
                            'min': min(location_scores.values()),
                            'max': max(location_scores.values())
                        }
                    }
        
        return comparison
    
    def generate_geographic_analysis_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate geographic analysis report.
        
        Args:
            data (Dict): Collected trend data
            
        Returns:
            Dictionary containing geographic analysis
        """
        logger.info("Generating geographic analysis report...")
        
        geo_analysis = {
            'regional_insights': {},
            'hotspots': {},
            'regional_comparisons': {}
        }
        
        for key, geo_data in data['geographic_data'].items():
            keyword, location = key.split('_', 1)
            
            for timeframe, region_data in geo_data.items():
                if region_data is not None and not region_data.empty:
                    # Find top regions
                    top_regions = region_data.nlargest(5, keyword)
                    
                    geo_analysis['hotspots'][f"{keyword}_{timeframe}"] = {
                        'top_regions': top_regions.to_dict('records'),
                        'total_regions': len(region_data),
                        'regional_variance': region_data[keyword].var()
                    }
                    
                    # Regional insights
                    if region_data[keyword].max() > 80:
                        geo_analysis['regional_insights'][f"{keyword}_{timeframe}"] = {
                            'type': 'high_interest',
                            'message': f"{keyword} shows very high interest in {top_regions.index[0]}",
                            'top_region': top_regions.index[0],
                            'score': region_data[keyword].max()
                        }
        
        return geo_analysis
    
    def generate_insights_report(self, data: Dict[str, Any], trend_analysis: Dict[str, Any], 
                               comparison: Dict[str, Any], geo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights and recommendations report.
        
        Args:
            data (Dict): Collected trend data
            trend_analysis (Dict): Trend analysis results
            comparison (Dict): Comparison analysis results
            geo_analysis (Dict): Geographic analysis results
            
        Returns:
            Dictionary containing insights and recommendations
        """
        logger.info("Generating insights report...")
        
        insights = {
            'key_findings': [],
            'trend_insights': [],
            'opportunities': [],
            'recommendations': [],
            'risk_factors': []
        }
        
        # Analyze trend insights
        for insight in trend_analysis.get('insights', []):
            insights['trend_insights'].append(insight)
            
            if insight['type'] == 'high_trend':
                insights['opportunities'].append({
                    'type': 'trending_topic',
                    'keyword': insight['keyword'],
                    'location': insight['location'],
                    'recommendation': f"Consider creating content around {insight['keyword']} for {insight['location']} market"
                })
        
        # Analyze geographic opportunities
        for key, hotspot in geo_analysis.get('hotspots', {}).items():
            keyword = key.split('_')[0]
            top_region = hotspot['top_regions'][0] if hotspot['top_regions'] else None
            
            if top_region:
                insights['opportunities'].append({
                    'type': 'geographic_opportunity',
                    'keyword': keyword,
                    'region': top_region,
                    'recommendation': f"Focus on {keyword} content for {top_region} market"
                })
        
        # Generate recommendations
        if insights['opportunities']:
            insights['recommendations'].append({
                'priority': 'high',
                'category': 'content_strategy',
                'recommendation': "Develop content around trending topics identified in analysis"
            })
        
        # Risk factors
        for insight in trend_analysis.get('insights', []):
            if insight['type'] == 'high_volatility':
                insights['risk_factors'].append({
                    'type': 'volatility',
                    'keyword': insight['keyword'],
                    'risk': f"High volatility in {insight['keyword']} trends may indicate unstable interest"
                })
        
        return insights
    
    def create_visualizations(self, data: Dict[str, Any], report_id: str):
        """
        Create visualizations for the report.
        
        Args:
            data (Dict): Collected trend data
            report_id (str): Report identifier
        """
        logger.info("Creating visualizations...")
        
        # Set style
        plt.style.use(self.config['visualization']['style'])
        sns.set_palette(self.config['visualization']['color_palette'])
        
        charts_dir = f"reports/charts/{report_id}/"
        os.makedirs(charts_dir, exist_ok=True)
        
        # Create trend charts
        for keyword in data['trends']:
            for location in data['trends'][keyword]:
                for timeframe in data['trends'][keyword][location]:
                    trend_data = data['trends'][keyword][location][timeframe]
                    
                    if trend_data is not None and not trend_data.empty:
                        plt.figure(figsize=tuple(self.config['visualization']['figure_size']))
                        
                        plt.plot(trend_data.index, trend_data[keyword], linewidth=2, marker='o')
                        plt.title(f"{keyword} Trends in {location} ({timeframe})")
                        plt.xlabel('Date')
                        plt.ylabel('Interest')
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        filename = f"{charts_dir}{keyword}_{location}_{timeframe.replace(' ', '_')}.png"
                        plt.savefig(filename, dpi=self.config['visualization']['dpi'], bbox_inches='tight')
                        plt.close()
        
        # Create comparison charts
        for keyword in data['trends']:
            plt.figure(figsize=tuple(self.config['visualization']['figure_size']))
            
            for location in data['trends'][keyword]:
                for timeframe in data['trends'][keyword][location]:
                    trend_data = data['trends'][keyword][location][timeframe]
                    if trend_data is not None and not trend_data.empty:
                        plt.plot(trend_data.index, trend_data[keyword], label=f"{location} ({timeframe})")
            
            plt.title(f"{keyword} - Location Comparison")
            plt.xlabel('Date')
            plt.ylabel('Interest')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            filename = f"{charts_dir}{keyword}_comparison.png"
            plt.savefig(filename, dpi=self.config['visualization']['dpi'], bbox_inches='tight')
            plt.close()
    
    def generate_html_report(self, data: Dict[str, Any], analyses: Dict[str, Any], report_id: str):
        """
        Generate HTML report.
        
        Args:
            data (Dict): Collected trend data
            analyses (Dict): Analysis results
            report_id (str): Report identifier
        """
        logger.info("Generating HTML report...")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Google Search Trends Report - {report_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .insight {{ background-color: #e8f4fd; padding: 10px; margin: 10px 0; border-radius: 3px; }}
                .recommendation {{ background-color: #e8f8e8; padding: 10px; margin: 10px 0; border-radius: 3px; }}
                .chart {{ text-align: center; margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Google Search Trends Analysis Report</h1>
                <p><strong>Report ID:</strong> {report_id}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Keywords:</strong> {', '.join(data['metadata']['keywords'])}</p>
                <p><strong>Locations:</strong> {', '.join(data['metadata']['locations'])}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <p>This report provides comprehensive analysis of Google Search Trends for the specified keywords and locations.</p>
            </div>
            
            <div class="section">
                <h2>Key Insights</h2>
        """
        
        # Add insights
        for insight in analyses.get('insights', {}).get('trend_insights', []):
            html_content += f'<div class="insight"><strong>{insight["type"].title()}:</strong> {insight["message"]}</div>'
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
        """
        
        # Add recommendations
        for rec in analyses.get('insights', {}).get('recommendations', []):
            html_content += f'<div class="recommendation"><strong>{rec["category"].title()}:</strong> {rec["recommendation"]}</div>'
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>Trend Analysis</h2>
                <table>
                    <tr>
                        <th>Keyword</th>
                        <th>Location</th>
                        <th>Timeframe</th>
                        <th>Trend Direction</th>
                        <th>Average Interest</th>
                    </tr>
        """
        
        # Add trend data
        for keyword in data['trends']:
            for location in data['trends'][keyword]:
                for timeframe in data['trends'][keyword][location]:
                    trend_data = data['trends'][keyword][location][timeframe]
                    if trend_data is not None and not trend_data.empty:
                        values = trend_data[keyword].dropna()
                        if len(values) > 0:
                            direction = 'increasing' if values.iloc[-1] > values.iloc[0] else 'decreasing'
                            avg_interest = values.mean()
                            html_content += f"""
                                <tr>
                                    <td>{keyword}</td>
                                    <td>{location}</td>
                                    <td>{timeframe}</td>
                                    <td>{direction}</td>
                                    <td>{avg_interest:.1f}</td>
                                </tr>
                            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        # Save HTML file
        filename = f"{self.config['output']['directory']}report_{report_id}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved: {filename}")
    
    def generate_excel_report(self, data: Dict[str, Any], analyses: Dict[str, Any], report_id: str):
        """
        Generate Excel report.
        
        Args:
            data (Dict): Collected trend data
            analyses (Dict): Analysis results
            report_id (str): Report identifier
        """
        logger.info("Generating Excel report...")
        
        filename = f"{self.config['output']['directory']}report_{report_id}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for keyword in data['trends']:
                for location in data['trends'][keyword]:
                    for timeframe in data['trends'][keyword][location]:
                        trend_data = data['trends'][keyword][location][timeframe]
                        if trend_data is not None and not trend_data.empty:
                            values = trend_data[keyword].dropna()
                            if len(values) > 0:
                                summary_data.append({
                                    'Keyword': keyword,
                                    'Location': location,
                                    'Timeframe': timeframe,
                                    'Average Interest': values.mean(),
                                    'Max Interest': values.max(),
                                    'Min Interest': values.min(),
                                    'Trend Direction': 'increasing' if values.iloc[-1] > values.iloc[0] else 'decreasing'
                                })
            
            if summary_data:
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Insights sheet
            insights_data = []
            for insight in analyses.get('insights', {}).get('trend_insights', []):
                insights_data.append({
                    'Type': insight['type'],
                    'Keyword': insight['keyword'],
                    'Location': insight['location'],
                    'Timeframe': insight['timeframe'],
                    'Message': insight['message']
                })
            
            if insights_data:
                df_insights = pd.DataFrame(insights_data)
                df_insights.to_excel(writer, sheet_name='Insights', index=False)
            
            # Recommendations sheet
            rec_data = []
            for rec in analyses.get('insights', {}).get('recommendations', []):
                rec_data.append({
                    'Priority': rec['priority'],
                    'Category': rec['category'],
                    'Recommendation': rec['recommendation']
                })
            
            if rec_data:
                df_rec = pd.DataFrame(rec_data)
                df_rec.to_excel(writer, sheet_name='Recommendations', index=False)
        
        logger.info(f"Excel report saved: {filename}")
    
    def generate_report(self, report_id: Optional[str] = None):
        """
        Generate comprehensive report.
        
        Args:
            report_id (str): Optional report identifier
        """
        if report_id is None:
            report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        logger.info(f"Generating report: {report_id}")
        
        # Collect data
        data = self.collect_trend_data(
            self.config['keywords'],
            self.config['locations'],
            self.config['timeframes']
        )
        
        # Generate analyses
        analyses = {
            'trend_analysis': self.generate_trend_analysis_report(data),
            'comparison': self.generate_comparison_report(data),
            'geographic_analysis': self.generate_geographic_analysis_report(data)
        }
        
        # Generate insights
        analyses['insights'] = self.generate_insights_report(
            data, analyses['trend_analysis'], analyses['comparison'], analyses['geographic_analysis']
        )
        
        # Create visualizations
        if self.config['output']['include_charts']:
            self.create_visualizations(data, report_id)
        
        # Generate reports in different formats
        for format_type in self.config['output']['formats']:
            if format_type == 'html':
                self.generate_html_report(data, analyses, report_id)
            elif format_type == 'excel':
                self.generate_excel_report(data, analyses, report_id)
        
        logger.info(f"Report generation completed: {report_id}")
        
        return {
            'report_id': report_id,
            'data': data,
            'analyses': analyses,
            'files_generated': [
                f"reports/report_{report_id}.html",
                f"reports/report_{report_id}.xlsx"
            ]
        }


def main():
    """Main function to run report generation."""
    parser = argparse.ArgumentParser(description='Generate Google Search Trends reports')
    parser.add_argument('--config', '-c', default='config/report_config.json',
                       help='Configuration file path')
    parser.add_argument('--report-id', '-r', help='Report identifier')
    parser.add_argument('--keywords', '-k', nargs='+', help='Keywords to analyze')
    parser.add_argument('--locations', '-l', nargs='+', help='Locations to analyze')
    parser.add_argument('--timeframes', '-t', nargs='+', help='Timeframes to analyze')
    
    args = parser.parse_args()
    
    print("📊 Starting Google Search Trends Report Generator")
    print("=" * 60)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Initialize and run generator
    generator = ReportGenerator(args.config)
    
    # Override config with command line arguments
    if args.keywords:
        generator.config['keywords'] = args.keywords
    if args.locations:
        generator.config['locations'] = args.locations
    if args.timeframes:
        generator.config['timeframes'] = args.timeframes
    
    result = generator.generate_report(report_id=args.report_id)
    
    print(f"\n✅ Report generation completed!")
    print(f"Report ID: {result['report_id']}")
    print(f"Files generated: {len(result['files_generated'])}")
    for file in result['files_generated']:
        print(f"  - {file}")


if __name__ == "__main__":
    main() 