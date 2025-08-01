#!/usr/bin/env python3
"""
Example script for Google Search Trends API Project

This script demonstrates how to use the TrendsAnalyzer to fetch and analyze
Google Search Trends data.
"""

import asyncio
import json
from datetime import datetime
from src.trends_analyzer import TrendsAnalyzer


def main():
    """Main function demonstrating the usage of TrendsAnalyzer."""
    
    print("🚀 Google Search Trends API Project - Example Usage")
    print("=" * 60)
    
    # Initialize the analyzer
    print("\n1. Initializing Trends Analyzer...")
    analyzer = TrendsAnalyzer(
        api_client="pytrends",
        language="en-US",
        timezone=360,
        retries=3,
        timeout=30
    )
    
    # Example 1: Get trending searches
    print("\n2. Fetching current trending searches...")
    try:
        trending_data = analyzer.get_trending_searches(geo="US", limit=10)
        if "error" not in trending_data:
            print(f"✅ Found {trending_data['count']} trending searches:")
            for i, trend in enumerate(trending_data['trends'][:5], 1):
                print(f"   {i}. {trend}")
        else:
            print(f"❌ Error: {trending_data['error']}")
    except Exception as e:
        print(f"❌ Error fetching trending searches: {e}")
    
    # Example 2: Get historical trends for a keyword
    print("\n3. Analyzing historical trends for 'artificial intelligence'...")
    try:
        historical_data = analyzer.get_historical_trends(
            keyword="artificial intelligence",
            timeframe="today 12-m",
            geo="US"
        )
        
        if "error" not in historical_data:
            print("✅ Historical data retrieved successfully!")
            
            # Get summary statistics
            summary = analyzer.get_summary_statistics(historical_data)
            if "statistics" in summary and "overall_stats" in summary["statistics"]:
                stats = summary["statistics"]["overall_stats"]
                print(f"   📊 Average interest: {stats.get('mean', 'N/A'):.1f}")
                print(f"   📈 Peak interest: {stats.get('max', 'N/A'):.1f}")
                print(f"   📉 Minimum interest: {stats.get('min', 'N/A'):.1f}")
            
            # Export data
            export_path = analyzer.export_data(historical_data, format="json")
            print(f"   💾 Data exported to: {export_path}")
            
            # Create visualization
            viz_path = analyzer.create_visualization(historical_data, chart_type="line")
            print(f"   📊 Visualization saved to: {viz_path}")
            
        else:
            print(f"❌ Error: {historical_data['error']}")
    except Exception as e:
        print(f"❌ Error analyzing historical trends: {e}")
    
    # Example 3: Compare multiple keywords
    print("\n4. Comparing multiple keywords...")
    try:
        comparison_data = analyzer.compare_keywords(
            keywords=["python", "javascript", "java"],
            timeframe="today 12-m",
            geo="US"
        )
        
        if "error" not in comparison_data:
            print("✅ Keyword comparison completed!")
            
            # Show comparison metrics
            if "comparison" in comparison_data and "summary_stats" in comparison_data["comparison"]:
                metrics = comparison_data["comparison"]["summary_stats"].get("comparison_metrics", {})
                if metrics.get("highest_average"):
                    print(f"   🏆 Highest average interest: {metrics['highest_average']}")
                if metrics.get("most_volatile"):
                    print(f"   📊 Most volatile: {metrics['most_volatile']}")
            
            # Create comparison visualization
            comp_viz_path = analyzer.create_visualization(comparison_data, chart_type="line")
            print(f"   📊 Comparison chart saved to: {comp_viz_path}")
            
        else:
            print(f"❌ Error: {comparison_data['error']}")
    except Exception as e:
        print(f"❌ Error comparing keywords: {e}")
    
    # Example 4: Get related topics and queries
    print("\n5. Finding related topics and queries...")
    try:
        related_topics = analyzer.get_related_topics(
            keyword="machine learning",
            timeframe="today 12-m",
            geo="US"
        )
        
        if "error" not in related_topics and "related_topics" in related_topics:
            topics = related_topics["related_topics"].get("machine learning", {})
            if topics.get("top"):
                print("✅ Top related topics:")
                for i, topic in enumerate(topics["top"][:3], 1):
                    if isinstance(topic, dict) and "topic_title" in topic:
                        print(f"   {i}. {topic['topic_title']}")
        
        related_queries = analyzer.get_related_queries(
            keyword="machine learning",
            timeframe="today 12-m",
            geo="US"
        )
        
        if "error" not in related_queries and "related_queries" in related_queries:
            queries = related_queries["related_queries"].get("machine learning", {})
            if queries.get("top"):
                print("✅ Top related queries:")
                for i, query in enumerate(queries["top"][:3], 1):
                    if isinstance(query, dict) and "query" in query:
                        print(f"   {i}. {query['query']}")
                        
    except Exception as e:
        print(f"❌ Error fetching related data: {e}")
    
    # Example 5: Geographic trends
    print("\n6. Analyzing geographic trends...")
    try:
        geo_data = analyzer.get_geographic_trends(
            keyword="climate change",
            timeframe="today 12-m",
            countries=["US", "GB", "CA", "AU", "DE"]
        )
        
        if "error" not in geo_data and "geographic_data" in geo_data:
            print("✅ Geographic analysis completed!")
            geo_stats = geo_data["geographic_data"]
            
            # Find country with highest interest
            if geo_stats:
                highest_country = max(geo_stats.items(), key=lambda x: x[1]["average_interest"])
                print(f"   🌍 Highest interest: {highest_country[0]} ({highest_country[1]['average_interest']:.1f})")
                
                # Create geographic visualization
                geo_viz_path = analyzer.create_visualization(geo_data, chart_type="heatmap")
                print(f"   📊 Geographic chart saved to: {geo_viz_path}")
        else:
            print(f"❌ Error: {geo_data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error analyzing geographic trends: {e}")
    
    # Example 6: Async real-time trends
    print("\n7. Fetching real-time trends (async)...")
    async def fetch_realtime():
        try:
            realtime_data = await analyzer.get_realtime_trends(geo="US")
            if "error" not in realtime_data:
                print("✅ Real-time trends fetched successfully!")
                if realtime_data.get("trends"):
                    print("   🔥 Current trending searches:")
                    for i, trend in enumerate(realtime_data["trends"][:3], 1):
                        print(f"      {i}. {trend}")
            else:
                print(f"❌ Error: {realtime_data['error']}")
        except Exception as e:
            print(f"❌ Error fetching real-time trends: {e}")
    
    # Run async function
    asyncio.run(fetch_realtime())
    
    print("\n" + "=" * 60)
    print("🎉 Example completed successfully!")
    print("\n📁 Check the 'data/exports' directory for generated files:")
    print("   - JSON/CSV/Excel data exports")
    print("   - PNG visualization charts")
    print("   - HTML interactive dashboards")
    
    print("\n🔗 Next steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Explore the Jupyter notebooks in the 'notebooks' directory")
    print("   3. Check the documentation in the 'docs' directory")
    print("   4. Run tests: python -m pytest tests/")
    print("   5. Customize the code for your specific needs!")


if __name__ == "__main__":
    main() 