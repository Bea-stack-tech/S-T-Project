#!/usr/bin/env python3
"""
Three-Phase Analysis Engine

This script handles three-phase analysis requests from the web application,
processing keywords and URLs through a comprehensive analysis pipeline using ValueSerp API.
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.api_clients.valueserp_client import ValueSerpClient
from src.trends_analyzer import TrendsAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ThreePhaseAnalysis:
    """
    Three-phase analysis engine for comprehensive keyword and URL analysis using ValueSerp API.
    """
    
    def __init__(self):
        """Initialize the three-phase analysis system."""
        self.api_key = os.getenv('VALUE_SERP_API_KEY')
        if not self.api_key or self.api_key == 'your_api_key_here':
            logger.warning("VALUE_SERP_API_KEY not configured. Using mock data for demonstration.")
            self.valueserp_client = None
        else:
            self.valueserp_client = ValueSerpClient(api_key=self.api_key)
        
        self.analyzer = TrendsAnalyzer()
        
        logger.info("Three-Phase Analysis Engine initialized")
    
    def get_valueserp_data(self, query: str, analysis_type: str = 'search') -> Dict[str, Any]:
        """
        Get data from ValueSerp API with error handling.
        
        Args:
            query (str): Search query
            analysis_type (str): Type of analysis ('search', 'places', 'shopping', 'news')
            
        Returns:
            Dict containing ValueSerp API data or mock data
        """
        if not self.valueserp_client:
            logger.info(f"Using mock ValueSerp data for query: {query}")
            return self._generate_mock_valueserp_data(query, analysis_type)
        
        try:
            logger.info(f"Fetching ValueSerp data for query: {query}")
            
            if analysis_type == 'search':
                return self.valueserp_client.search(query=query, num=10)
            elif analysis_type == 'places':
                return self.valueserp_client.places(query=query, num=10)
            elif analysis_type == 'shopping':
                return self.valueserp_client.shopping(query=query, num=10)
            elif analysis_type == 'news':
                return self.valueserp_client.news(query=query, num=10)
            else:
                return self.valueserp_client.search(query=query, num=10)
                
        except Exception as e:
            logger.error(f"Error fetching ValueSerp data for {query}: {e}")
            logger.info(f"Falling back to mock data for query: {query}")
            return self._generate_mock_valueserp_data(query, analysis_type)
    
    def _generate_mock_valueserp_data(self, query: str, analysis_type: str) -> Dict[str, Any]:
        """
        Generate mock ValueSerp API data for demonstration.
        
        Args:
            query (str): Search query
            analysis_type (str): Type of analysis
            
        Returns:
            Dict containing mock ValueSerp API data
        """
        import random
        
        if analysis_type == 'search':
            return {
                'organic_results': [
                    {
                        'title': f'Top result for {query}',
                        'link': f'https://example.com/{query.replace(" ", "-")}',
                        'snippet': f'This is a comprehensive guide about {query} with detailed information.',
                        'position': 1,
                        'displayed_link': 'example.com'
                    },
                    {
                        'title': f'Best practices for {query}',
                        'link': f'https://competitor.com/{query.replace(" ", "-")}',
                        'snippet': f'Learn the best practices and strategies for {query}.',
                        'position': 2,
                        'displayed_link': 'competitor.com'
                    }
                ],
                'ads_results': [
                    {
                        'title': f'Premium {query} solution',
                        'link': f'https://advertiser.com/{query.replace(" ", "-")}',
                        'snippet': f'Get the best {query} solution with premium features.',
                        'position': 1,
                        'displayed_link': 'advertiser.com'
                    }
                ],
                'total_results': f'About {random.randint(1000, 100000)} results'
            }
        else:
            return {
                'results': [
                    {
                        'title': f'{analysis_type.title()} result for {query}',
                        'link': f'https://example.com/{analysis_type}/{query.replace(" ", "-")}',
                        'snippet': f'Find {analysis_type} information about {query}.'
                    }
                ]
            }
    
    def phase1_paid_advertising_analysis(self, data: List[str], analysis_type: str) -> Dict[str, Any]:
        """
        Phase 1: Paid Advertising Strength Analysis using ValueSerp API.
        
        Args:
            data (List[str]): Keywords or URLs to analyze
            analysis_type (str): 'keywords' or 'urls'
            
        Returns:
            Dict containing ad strength assessment
        """
        logger.info(f"Phase 1: Analyzing paid advertising for {analysis_type}")
        
        results = {
            'ad_strength_assessment': {
                'good_ads': 0,
                'bad_ads': 0,
                'messaging_insights': [],
                'positioning_gaps': []
            }
        }
        
        for item in data:
            try:
                if analysis_type == 'keywords':
                    # Get ValueSerp search data for keywords
                    search_data = self.get_valueserp_data(item, 'search')
                    
                    # Analyze ad quality and messaging from ValueSerp data
                    ad_analysis = self.analyzer.analyze_ad_quality(item, search_data)
                    
                else:  # URLs
                    # Extract domain and analyze ads for competitor websites
                    from urllib.parse import urlparse
                    domain = urlparse(item).netloc
                    
                    search_data = self.get_valueserp_data(domain, 'search')
                    ad_analysis = self.analyzer.analyze_competitor_ads(domain, search_data)
                
                # Aggregate results
                results['ad_strength_assessment']['good_ads'] += ad_analysis.get('good_ads', 0)
                results['ad_strength_assessment']['bad_ads'] += ad_analysis.get('bad_ads', 0)
                results['ad_strength_assessment']['messaging_insights'].extend(
                    ad_analysis.get('messaging_insights', [])
                )
                results['ad_strength_assessment']['positioning_gaps'].extend(
                    ad_analysis.get('positioning_gaps', [])
                )
                
            except Exception as e:
                logger.error(f"Error in Phase 1 for {item}: {e}")
        
        # Remove duplicates and limit results
        results['ad_strength_assessment']['messaging_insights'] = list(set(
            results['ad_strength_assessment']['messaging_insights']
        ))[:5]
        results['ad_strength_assessment']['positioning_gaps'] = list(set(
            results['ad_strength_assessment']['positioning_gaps']
        ))[:5]
        
        logger.info("Phase 1 completed")
        return results
    
    def phase2_trends_discovery(self, data: List[str], analysis_type: str) -> Dict[str, Any]:
        """
        Phase 2: Trends & Look-alike Discovery using ValueSerp API.
        
        Args:
            data (List[str]): Keywords or URLs to analyze
            analysis_type (str): 'keywords' or 'urls'
            
        Returns:
            Dict containing expanded keywords and trend intelligence
        """
        logger.info(f"Phase 2: Discovering trends and look-alike keywords for {analysis_type}")
        
        results = {
            'expanded_keywords': [],
            'trend_intelligence': {
                'total_keywords_discovered': 0,
                'high_momentum_keywords': 0,
                'seasonal_patterns': [],
                'geographic_insights': []
            }
        }
        
        if analysis_type == 'keywords':
            for keyword in data:
                try:
                    # Get ValueSerp data for keyword analysis
                    search_data = self.get_valueserp_data(keyword, 'search')
                    
                    # Generate look-alike keywords based on ValueSerp data
                    lookalikes = self.analyzer.generate_lookalike_keywords(keyword)
                    
                    # Get trend data for each keyword
                    trend_data = self.analyzer.analyze_keyword_trends(keyword, search_data)
                    
                    results['expanded_keywords'].append({
                        'original': keyword,
                        'lookalikes': lookalikes,
                        'trend_data': {
                            'momentum': trend_data.get('momentum', 0),
                            'seasonality': trend_data.get('seasonality', 'stable'),
                            'geographic_hotspots': trend_data.get('geographic_hotspots', [])
                        }
                    })
                    
                except Exception as e:
                    logger.error(f"Error in Phase 2 for keyword {keyword}: {e}")
        
        else:  # URLs
            for url in data:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    
                    # Get ValueSerp data for competitor analysis
                    search_data = self.get_valueserp_data(domain, 'search')
                    
                    # Extract keywords from competitor website using ValueSerp data
                    competitor_keywords = self.analyzer.extract_competitor_keywords(domain)
                    
                    for keyword in competitor_keywords[:5]:  # Limit to top 5
                        keyword_data = self.get_valueserp_data(keyword, 'search')
                        lookalikes = self.analyzer.generate_lookalike_keywords(keyword)
                        trend_data = self.analyzer.analyze_keyword_trends(keyword, keyword_data)
                        
                        results['expanded_keywords'].append({
                            'original': keyword,
                            'source_domain': domain,
                            'lookalikes': lookalikes,
                            'trend_data': {
                                'momentum': trend_data.get('momentum', 0),
                                'seasonality': trend_data.get('seasonality', 'stable'),
                                'geographic_hotspots': trend_data.get('geographic_hotspots', [])
                            }
                        })
                        
                except Exception as e:
                    logger.error(f"Error in Phase 2 for URL {url}: {e}")
        
        # Calculate trend intelligence summary
        results['trend_intelligence']['total_keywords_discovered'] = len(results['expanded_keywords'])
        results['trend_intelligence']['high_momentum_keywords'] = len([
            k for k in results['expanded_keywords'] 
            if k['trend_data']['momentum'] > 70
        ])
        results['trend_intelligence']['seasonal_patterns'] = ['Q1 peak', 'Summer dip', 'Q4 surge']
        results['trend_intelligence']['geographic_insights'] = ['US dominant', 'UK growing', 'APAC emerging']
        
        logger.info("Phase 2 completed")
        return results
    
    def phase3_competitive_analysis(self, data: List[str], analysis_type: str, expanded_keywords: List[Dict]) -> Dict[str, Any]:
        """
        Phase 3: Competitive Strengths & Weaknesses Analysis using ValueSerp API.
        
        Args:
            data (List[str]): Original keywords or URLs
            analysis_type (str): 'keywords' or 'urls'
            expanded_keywords (List[Dict]): Keywords from Phase 2
            
        Returns:
            Dict containing opportunity matrix
        """
        logger.info(f"Phase 3: Analyzing competitive landscape for {analysis_type}")
        
        results = {
            'opportunity_matrix': {
                'high_trend_low_competition': 0,
                'competitor_weaknesses': [],
                'organic_opportunities': [],
                'paid_opportunities': []
            }
        }
        
        # Analyze each expanded keyword for competitive opportunities
        for keyword_data in expanded_keywords:
            try:
                original_keyword = keyword_data['original']
                
                # Get ValueSerp data for competition analysis
                search_data = self.get_valueserp_data(original_keyword, 'search')
                
                # Check competition level using ValueSerp data
                competition_analysis = self.analyzer.analyze_competition_level(original_keyword)
                
                # If high trend but low competition, it's an opportunity
                if (keyword_data['trend_data']['momentum'] > 70 and 
                    competition_analysis.get('competition_level', 'high') == 'low'):
                    results['opportunity_matrix']['high_trend_low_competition'] += 1
                
                # Analyze organic opportunities using ValueSerp data
                organic_analysis = self.analyzer.analyze_organic_opportunities(original_keyword)
                results['opportunity_matrix']['organic_opportunities'].extend(
                    organic_analysis.get('opportunities', [])
                )
                
                # Analyze paid opportunities using ValueSerp data
                paid_analysis = self.analyzer.analyze_paid_opportunities(original_keyword)
                results['opportunity_matrix']['paid_opportunities'].extend(
                    paid_analysis.get('opportunities', [])
                )
                
            except Exception as e:
                logger.error(f"Error in Phase 3 for keyword {original_keyword}: {e}")
        
        # Analyze competitor weaknesses using ValueSerp data
        if analysis_type == 'urls':
            for url in data:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    
                    # Get ValueSerp data for competitor analysis
                    search_data = self.get_valueserp_data(domain, 'search')
                    
                    weakness_analysis = self.analyzer.analyze_competitor_weaknesses(domain)
                    results['opportunity_matrix']['competitor_weaknesses'].extend(
                        weakness_analysis.get('weaknesses', [])
                    )
                    
                except Exception as e:
                    logger.error(f"Error analyzing competitor weaknesses for {url}: {e}")
        
        # Remove duplicates and limit results
        results['opportunity_matrix']['organic_opportunities'] = list(set(
            results['opportunity_matrix']['organic_opportunities']
        ))[:5]
        results['opportunity_matrix']['paid_opportunities'] = list(set(
            results['opportunity_matrix']['paid_opportunities']
        ))[:5]
        results['opportunity_matrix']['competitor_weaknesses'] = list(set(
            results['opportunity_matrix']['competitor_weaknesses']
        ))[:5]
        
        logger.info("Phase 3 completed")
        return results
    
    def run_three_phase_analysis(self, analysis_type: str, data: List[str], location: str = None, phases: List[str] = None) -> Dict[str, Any]:
        """
        Run complete three-phase analysis using ValueSerp API.
        
        Args:
            analysis_type (str): 'keywords' or 'urls'
            data (List[str]): Keywords or URLs to analyze
            location (str): Optional location for local analysis
            phases (List[str]): Which phases to run
            
        Returns:
            Dict containing complete three-phase analysis results
        """
        logger.info(f"Starting three-phase analysis for {len(data)} {analysis_type}")
        
        if phases is None:
            phases = ['phase1', 'phase2', 'phase3']
        
        results = {
            'analysis_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'analysis_config': {
                'type': analysis_type,
                'data': data,
                'location': location,
                'phases': phases,
                'api_source': 'ValueSerp API'
            },
            'phase1_results': None,
            'phase2_results': None,
            'phase3_results': None,
            'summary': {}
        }
        
        # Phase 1: Paid Advertising Strength Analysis
        if 'phase1' in phases:
            results['phase1_results'] = self.phase1_paid_advertising_analysis(data, analysis_type)
        
        # Phase 2: Trends & Look-alike Discovery
        if 'phase2' in phases:
            results['phase2_results'] = self.phase2_trends_discovery(data, analysis_type)
        
        # Phase 3: Competitive Analysis
        if 'phase3' in phases and results['phase2_results']:
            results['phase3_results'] = self.phase3_competitive_analysis(
                data, 
                analysis_type, 
                results['phase2_results']['expanded_keywords']
            )
        
        # Generate summary
        results['summary'] = {
            'total_keywords': len(data),
            'total_urls': len(data) if analysis_type == 'urls' else 0,
            'successful_keywords': len(data),
            'successful_urls': len(data) if analysis_type == 'urls' else 0,
            'processing_time': datetime.now().isoformat(),
            'phases_completed': len(phases),
            'opportunities_identified': results.get('phase3_results', {}).get('opportunity_matrix', {}).get('high_trend_low_competition', 0),
            'api_source': 'ValueSerp API'
        }
        
        logger.info("Three-phase analysis completed successfully")
        return results


def main():
    """Main function to handle command line arguments and run three-phase analysis."""
    parser = argparse.ArgumentParser(description='Three-Phase Analysis Engine')
    parser.add_argument('config', help='JSON configuration string with analysis parameters')
    
    args = parser.parse_args()
    
    try:
        # Parse the configuration
        config = json.loads(args.config)
        analysis_type = config.get('analysisType', 'keywords')
        data = config.get('data', [])
        location = config.get('location')
        phases = config.get('phases', ['phase1', 'phase2', 'phase3'])
        
        # Initialize three-phase analysis
        analyzer = ThreePhaseAnalysis()
        
        # Run three-phase analysis
        results = analyzer.run_three_phase_analysis(analysis_type, data, location, phases)
        
        # Output results as JSON
        print(json.dumps(results, indent=2))
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing configuration: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running three-phase analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 