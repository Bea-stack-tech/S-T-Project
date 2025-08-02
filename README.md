# Google Search Trends API Project

A comprehensive project for analyzing and visualizing Google Search Trends data using various APIs and tools.

## 🚀 Quick Start - One Command Setup

### Windows Users
```bash
# Double-click run.bat or run from command line:
run.bat
```

### Mac/Linux Users
```bash
# Make the script executable and run:
chmod +x run.sh
./run.sh
```

### Manual Run
```bash
# Run the auto-setup script:
python run.py
```

## 🎯 What the Auto-Setup Does

The `run.py` script automatically:

1. ✅ **Checks Prerequisites**: Python 3.8+, Node.js 18+, npm
2. ✅ **Creates Virtual Environment**: Sets up Python virtual environment
3. ✅ **Installs Dependencies**: All Python and Node.js packages
4. ✅ **Sets Up Environment**: Creates .env files from templates
5. ✅ **Creates Directories**: Data, logs, and export folders
6. ✅ **Starts Services**: Next.js frontend + Python backend
7. ✅ **Opens Browser**: Automatically opens the application

## 🚀 Features

- **Real-time Trend Analysis**: Fetch current trending searches and topics
- **Historical Data**: Analyze search trends over time periods
- **Geographic Insights**: Compare trends across different regions
- **Interactive Visualizations**: Beautiful charts and graphs
- **API Integration**: Multiple Google Trends API options
- **Data Export**: Export results in various formats (CSV, JSON, Excel)
- **Modern Web Interface**: Clean Next.js frontend with TailwindCSS

## 📋 Prerequisites

- **Python 3.8+** (automatically checked)
- **Node.js 18+** (automatically checked)
- **npm** (automatically checked)
- **Value SERP API Key** (optional, for enhanced features)

## 🛠️ Manual Installation (if needed)

### 1. Clone the repository
```bash
git clone https://github.com/Bea-stack-tech/S-T-Project.git
cd S-T-Project
```

### 2. Run the auto-setup
```bash
python run.py
```

### 3. Configure API Key (Optional)
1. Get your Value SERP API key from [https://valueserp.com/](https://valueserp.com/)
2. Edit `.env` file and add your API key:
   ```
   VALUE_SERP_API_KEY=your_actual_api_key_here
   ```

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

### Web Interface
1. Open `http://localhost:3000` in your browser
2. Enter keywords or URLs
3. Click "Analyze Trends"
4. View results and download reports

## 📁 Project Structure

```
S-T-Project/
├── run.py                 # 🚀 Auto-setup and run script
├── run.bat               # Windows startup script
├── run.sh                # Unix/Linux/Mac startup script
├── server.py             # FastAPI backend server
├── webapp/               # Next.js frontend
│   ├── app/             # React components
│   ├── components/      # UI components
│   └── package.json     # Node.js dependencies
├── src/                 # Python backend modules
│   ├── api_clients/     # API client implementations
│   ├── data_processors/ # Data processing utilities
│   └── visualizations/  # Chart and graph generators
├── scripts/             # Automation scripts
├── data/                # Data storage
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
The project uses environment variables for configuration:

- `VALUE_SERP_API_KEY`: Your Value SERP API key (optional)
- `API_CLIENT`: API client to use (default: pytrends)
- `LANGUAGE`: Language for requests (default: en-US)
- `TIMEZONE`: Timezone offset (default: 360)

### API Options

This project supports multiple Google Trends API options:

1. **pytrends** (Free, unofficial) - Default
   - No API key required
   - Limited rate limits
   - Good for basic analysis

2. **Value SERP API** (Paid, comprehensive)
   - Requires API key from https://valueserp.com/
   - High-quality, reliable data
   - Multiple endpoints for different data types

## 🧪 Testing

### API Endpoints
- **Health Check**: `http://localhost:8000/health`
- **API Documentation**: `http://localhost:8000/docs`
- **Test Endpoint**: `http://localhost:8000/api/test`

### Web Interface
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`

## 🔒 Security

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting to avoid API abuse
- Follow API terms of service

## 🆘 Troubleshooting

### Common Issues

1. **Python Version Error**
   - Ensure Python 3.8+ is installed
   - Run: `python --version`

2. **Node.js Not Found**
   - Install Node.js 18+ from https://nodejs.org/
   - Run: `node --version`

3. **Port Already in Use**
   - Stop other services using ports 3000 or 8000
   - Or modify the ports in the scripts

4. **Import Errors**
   - Run the auto-setup script: `python run.py`
   - It will install all missing dependencies

### Getting Help

- Check the logs in the `logs/` directory
- Verify all prerequisites are installed
- Ensure you have internet connection for dependency installation

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

---

**Note**: This project is for educational and research purposes. Please respect API rate limits and terms of service. 