#!/usr/bin/env python3
"""
FastAPI Server for Google Search Trends Project

This server provides API endpoints for the Google Search Trends analysis functionality.
It integrates with the Value SERP API and provides endpoints for trend analysis.
"""

import os
import json
import sys
from typing import List, Optional, Dict, Any
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please run: pip install fastapi uvicorn python-dotenv pydantic")
    sys.exit(1)

# Import our project modules with error handling
valueserp_client = None
trends_analyzer = None

try:
    from src.api_clients.valueserp_client import ValueSerpClient
    from src.trends_analyzer import TrendsAnalyzer
except ImportError as e:
    print(f"Warning: Could not import project modules: {e}")
    print("Some functionality may be limited")

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Google Search Trends API",
    description="API for analyzing Google Search Trends using Value SERP",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TrendAnalysisRequest(BaseModel):
    keywords: List[str]
    location: Optional[str] = "United States"
    timeframe: Optional[str] = "today 12-m"
    geo: Optional[str] = "US"

class TrendAnalysisResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

class SerpAnalysisRequest(BaseModel):
    query: str
    location: Optional[str] = "United States"
    gl: Optional[str] = "us"
    hl: Optional[str] = "en"
    num: Optional[int] = 10

# Initialize clients
api_key = os.getenv('VALUE_SERP_API_KEY')

if api_key and api_key != 'your_valueserp_api_key_here':
    try:
        valueserp_client = ValueSerpClient(api_key=api_key)
        trends_analyzer = TrendsAnalyzer()
    except Exception as e:
        print(f"Warning: Could not initialize clients: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Google Search Trends API",
        "version": "1.0.0",
        "status": "running",
        "api_key_configured": api_key is not None and api_key != 'your_valueserp_api_key_here',
        "clients_available": {
            "valueserp_client": valueserp_client is not None,
            "trends_analyzer": trends_analyzer is not None
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "api_key_configured": api_key is not None and api_key != 'your_valueserp_api_key_here',
        "clients_available": {
            "valueserp_client": valueserp_client is not None,
            "trends_analyzer": trends_analyzer is not None
        }
    }

@app.post("/api/trends/analyze", response_model=TrendAnalysisResponse)
async def analyze_trends(request: TrendAnalysisRequest):
    """Analyze trends for given keywords."""
    try:
        if not trends_analyzer:
            raise HTTPException(status_code=500, detail="Trends analyzer not available")
        
        results = {}
        for keyword in request.keywords:
            try:
                trend_data = trends_analyzer.get_historical_trends(
                    keyword=keyword,
                    timeframe=request.timeframe,
                    geo=request.geo
                )
                results[keyword] = trend_data
            except Exception as e:
                results[keyword] = {"error": str(e)}
        
        return TrendAnalysisResponse(
            success=True,
            data=results,
            message=f"Successfully analyzed trends for {len(request.keywords)} keywords"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/serp/analyze")
async def analyze_serp(request: SerpAnalysisRequest):
    """Analyze SERP data for a given query."""
    try:
        if not valueserp_client:
            raise HTTPException(status_code=500, detail="Value SERP client not available")
        
        insights = valueserp_client.get_serp_insights(
            query=request.query,
            location=request.location,
            gl=request.gl,
            hl=request.hl,
            num=request.num
        )
        
        return {
            "success": True,
            "data": insights,
            "message": f"Successfully analyzed SERP data for '{request.query}'"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/trending")
async def get_trending_searches():
    """Get current trending searches."""
    try:
        if not trends_analyzer:
            raise HTTPException(status_code=500, detail="Trends analyzer not available")
        
        trending = trends_analyzer.get_trending_searches()
        return {
            "success": True,
            "data": trending,
            "message": "Successfully retrieved trending searches"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
async def get_config():
    """Get current configuration status."""
    return {
        "api_key_configured": api_key is not None and api_key != 'your_valueserp_api_key_here',
        "clients_initialized": {
            "valueserp_client": valueserp_client is not None,
            "trends_analyzer": trends_analyzer is not None
        }
    }

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify the server is working."""
    return {
        "success": True,
        "message": "Server is running correctly",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Google Search Trends API server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000) 