#!/usr/bin/env python3
"""
Value SERP API Example Script

This script demonstrates how to use the Value SERP API client to get
comprehensive SERP (Search Engine Results Page) data including Google Search,
Maps, Shopping, News, Products, and Reviews.

Before running this script:
1. Get your API key from https://valueserp.com/
2. Set the VALUE_SERP_API_KEY environment variable or update the script
"""

import os
import json
import pandas as pd
from datetime import datetime
from src.api_clients.valueserp_client import ValueSerpClient


def main():
    """Main function demonstrating Value SERP API usage."""
    
    # Get API key from environment variable
    api_key = os.getenv('VALUE_SERP_API_KEY')
    if not api_key:
        print("❌ Please set the VALUE_SERP_API_KEY environment variable")
        print("   You can get your API key from: https://valueserp.com/")
        return
    
    # Initialize the Value SERP client
    print("🚀 Initializing Value SERP client...")
    client = ValueSerpClient(api_key=api_key)
    
    # Example queries to test
    test_queries = [
        "artificial intelligence",
        "python programming",
        "coffee shops near me",
        "iPhone 15",
        "climate change news"
    ]
    
    print(f"\n📊 Testing Value SERP API with {len(test_queries)} queries...")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}/{len(test_queries)}: '{query}'")
        print("-" * 40)
        
        try:
            # Get comprehensive SERP insights
            insights = client.get_serp_insights(
                query=query,
                location="United States",
                gl="us",
                hl="en",
                num=5  # Limit to 5 results for demo
            )
            
            # Display summary
            summary = insights.get('summary', {})
            print(f"📈 Results Summary:")
            print(f"   • Search Results: {summary.get('total_search_results', 0)}")
            print(f"   • Places Results: {summary.get('total_places_results', 0)}")
            print(f"   • Shopping Results: {summary.get('total_shopping_results', 0)}")
            print(f"   • News Results: {summary.get('total_news_results', 0)}")
            
            # Show top search results
            search_results = insights.get('search_results', [])
            if search_results:
                print(f"\n🔗 Top Search Results:")
                for j, result in enumerate(search_results[:3], 1):
                    print(f"   {j}. {result.get('title', 'N/A')}")
                    print(f"      URL: {result.get('link', 'N/A')}")
                    print(f"      Position: {result.get('position', 'N/A')}")
            
            # Show top news results
            news_results = insights.get('news_results', [])
            if news_results:
                print(f"\n📰 Top News Results:")
                for j, result in enumerate(news_results[:2], 1):
                    print(f"   {j}. {result.get('title', 'N/A')}")
                    print(f"      Source: {result.get('source', 'N/A')}")
                    print(f"      Date: {result.get('date', 'N/A')}")
            
            # Show top places results
            places_results = insights.get('places_results', [])
            if places_results:
                print(f"\n📍 Top Places Results:")
                for j, result in enumerate(places_results[:2], 1):
                    print(f"   {j}. {result.get('title', 'N/A')}")
                    print(f"      Address: {result.get('address', 'N/A')}")
                    print(f"      Rating: {result.get('rating', 'N/A')}")
            
            # Show top shopping results
            shopping_results = insights.get('shopping_results', [])
            if shopping_results:
                print(f"\n🛍️ Top Shopping Results:")
                for j, result in enumerate(shopping_results[:2], 1):
                    print(f"   {j}. {result.get('title', 'N/A')}")
                    print(f"      Price: {result.get('price', 'N/A')}")
                    print(f"      Source: {result.get('source', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error processing query '{query}': {e}")
        
        print("\n" + "=" * 60)
    
    # Demonstrate individual API endpoints
    print("\n🎯 Testing Individual API Endpoints...")
    print("=" * 60)
    
    # Test search endpoint
    print("\n🔍 Testing Search Endpoint:")
    search_data = client.search("machine learning", num=3)
    if search_data:
        results = client.extract_search_results(search_data)
        df = client.to_dataframe(results)
        print(f"   Found {len(results)} search results")
        if not df.empty:
            print(f"   Top result: {df.iloc[0]['title']}")
    
    # Test news endpoint
    print("\n📰 Testing News Endpoint:")
    news_data = client.news("tech news", num=3)
    if news_data:
        results = client.extract_news_results(news_data)
        df = client.to_dataframe(results)
        print(f"   Found {len(results)} news results")
        if not df.empty:
            print(f"   Top news: {df.iloc[0]['title']}")
    
    # Test places endpoint
    print("\n📍 Testing Places Endpoint:")
    places_data = client.places("restaurants", num=3)
    if places_data:
        results = client.extract_places_results(places_data)
        df = client.to_dataframe(results)
        print(f"   Found {len(results)} places results")
        if not df.empty:
            print(f"   Top place: {df.iloc[0]['title']}")
    
    # Test shopping endpoint
    print("\n🛍️ Testing Shopping Endpoint:")
    shopping_data = client.shopping("laptop", num=3)
    if shopping_data:
        results = client.extract_shopping_results(shopping_data)
        df = client.to_dataframe(results)
        print(f"   Found {len(results)} shopping results")
        if not df.empty:
            print(f"   Top product: {df.iloc[0]['title']}")
    
    print("\n✅ Value SERP API demonstration completed!")
    print("\n💡 Tips:")
    print("   • Use the get_serp_insights() method for comprehensive data")
    print("   • Individual endpoints are available for specific data types")
    print("   • Results can be converted to pandas DataFrames for analysis")
    print("   • Check the API documentation for more parameters and options")


def save_results_to_file(insights, filename=None):
    """
    Save SERP insights to a JSON file.
    
    Args:
        insights (Dict): SERP insights data
        filename (str): Output filename (optional)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"serp_insights_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to: {filename}")


def export_to_excel(insights, filename=None):
    """
    Export SERP insights to Excel file with multiple sheets.
    
    Args:
        insights (Dict): SERP insights data
        filename (str): Output filename (optional)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"serp_insights_{timestamp}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Search results
        if insights.get('search_results'):
            df_search = pd.DataFrame(insights['search_results'])
            df_search.to_excel(writer, sheet_name='Search_Results', index=False)
        
        # News results
        if insights.get('news_results'):
            df_news = pd.DataFrame(insights['news_results'])
            df_news.to_excel(writer, sheet_name='News_Results', index=False)
        
        # Places results
        if insights.get('places_results'):
            df_places = pd.DataFrame(insights['places_results'])
            df_places.to_excel(writer, sheet_name='Places_Results', index=False)
        
        # Shopping results
        if insights.get('shopping_results'):
            df_shopping = pd.DataFrame(insights['shopping_results'])
            df_shopping.to_excel(writer, sheet_name='Shopping_Results', index=False)
        
        # Summary
        df_summary = pd.DataFrame([insights.get('summary', {})])
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"📊 Results exported to Excel: {filename}")


if __name__ == "__main__":
    main() 