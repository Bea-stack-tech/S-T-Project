# Google Search Trends API Project

A comprehensive project for analyzing and visualizing Google Search Trends data using various APIs and tools.

## 🚀 Features

- **Real-time Trend Analysis**: Fetch current trending searches and topics
- **Historical Data**: Analyze search trends over time periods
- **Geographic Insights**: Compare trends across different regions
- **Interactive Visualizations**: Beautiful charts and graphs
- **API Integration**: Multiple Google Trends API options
- **Data Export**: Export results in various formats (CSV, JSON, Excel)

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git
- API keys (depending on the service you choose)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bea-stack-tech/S-T-Project.git
   cd S-T-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🔧 Configuration

### API Options

This project supports multiple Google Trends API options:

1. **pytrends** (Free, unofficial)
   - No API key required
   - Limited rate limits
   - Good for basic analysis

2. **Google Trends API** (Official, paid)
   - Requires API key
   - Higher rate limits
   - More reliable

3. **Value SERP API** (Traject Data)
   - Comprehensive SERP data (Search, Maps, Shopping, News, Products, Reviews)
   - Requires API key from https://valueserp.com/
   - High-quality, reliable data
   - Multiple endpoints for different data types

4. **Alternative APIs** (Various providers)
   - Serpapi, RapidAPI, etc.
   - Different pricing models

## 📊 Usage Examples

### Basic Trend Analysis
```python
from src.trends_analyzer import TrendsAnalyzer

analyzer = TrendsAnalyzer()
trends = analyzer.get_trending_searches()
print(trends)
```

### Historical Data
```python
# Get search trends for a specific term
historical_data = analyzer.get_historical_trends(
    keyword="artificial intelligence",
    timeframe="2023-01-01 2024-01-01",
    geo="US"
)
```

### Geographic Comparison
```python
# Compare trends across countries
comparison = analyzer.compare_geographic_trends(
    keyword="climate change",
    countries=["US", "UK", "CA", "AU"]
)
```

### Value SERP API Integration
```python
from src.api_clients.valueserp_client import ValueSerpClient

# Initialize the client
client = ValueSerpClient(api_key="your_api_key")

# Get comprehensive SERP insights
insights = client.get_serp_insights(
    query="artificial intelligence",
    location="United States",
    gl="us",
    hl="en",
    num=10
)

# Access different result types
search_results = insights['search_results']
news_results = insights['news_results']
places_results = insights['places_results']
shopping_results = insights['shopping_results']

# Convert to DataFrame for analysis
import pandas as pd
df_search = pd.DataFrame(search_results)
df_news = pd.DataFrame(news_results)
```

### Individual Value SERP Endpoints
```python
# Google Search results
search_data = client.search("machine learning", num=10)

# Google News results
news_data = client.news("tech news", num=10)

# Google Maps results
places_data = client.places("restaurants", num=10)

# Google Shopping results
shopping_data = client.shopping("laptop", num=10)

# Google Product results
product_data = client.product("product_id_here")

# Google Reviews
reviews_data = client.place_reviews("place_id_here")
```

## 📁 Project Structure

```
S-T-Project/
├── src/
│   ├── __init__.py
│   ├── trends_analyzer.py      # Main analysis logic
│   ├── api_clients/            # API client implementations
│   ├── data_processors/        # Data processing utilities
│   └── visualizations/         # Chart and graph generators
├── data/
│   ├── raw/                    # Raw API responses
│   ├── processed/              # Cleaned and processed data
│   └── exports/                # Exported results
├── notebooks/                  # Jupyter notebooks for analysis
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── config/                     # Configuration files
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📈 Data Visualization

The project includes several visualization options:

- **Line Charts**: Time series trends
- **Heatmaps**: Geographic distribution
- **Bar Charts**: Top searches comparison
- **Word Clouds**: Trending topics
- **Interactive Dashboards**: Real-time monitoring

## 🔒 Security

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting to avoid API abuse
- Follow API terms of service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Bea-stack-tech/S-T-Project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Bea-stack-tech/S-T-Project/discussions)
- **Documentation**: [Wiki](https://github.com/Bea-stack-tech/S-T-Project/wiki)

## 🔄 Roadmap

- [ ] Real-time trend monitoring
- [ ] Machine learning predictions
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Social media integration

---

**Note**: This project is for educational and research purposes. Please respect API rate limits and terms of service. 