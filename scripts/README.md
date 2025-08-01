# Google Search Trends Automation Scripts

This directory contains automation scripts for Google Search Trends analysis, similar to the structure found in the [googleadsfree repository](https://github.com/kchinhara/googleadsfree/tree/main/Scripts). These scripts provide comprehensive automation capabilities for trend monitoring, batch processing, and report generation.

## 📁 Scripts Overview

### 🔍 `trend_monitor.py`
**Real-time Trend Monitoring and Alerting**

A continuous monitoring script that tracks Google Search Trends for specified keywords and sends alerts when significant changes are detected.

**Features:**
- Real-time trend monitoring with configurable intervals
- Multiple notification methods (email, Slack, webhook)
- Configurable alert thresholds
- Historical trend comparison
- Automated data storage

**Usage:**
```bash
# Run with default configuration
python scripts/trend_monitor.py

# Run with custom configuration
python scripts/trend_monitor.py --config config/custom_monitor_config.json
```

**Configuration:**
- Edit `config/monitor_config.json` to customize:
  - Keywords to monitor
  - Geographic locations
  - Alert thresholds
  - Notification settings
  - Monitoring intervals

### 📊 `batch_processor.py`
**Large-Scale Batch Processing**

Handles large-scale batch processing of Google Search Trends data across multiple keywords, locations, and timeframes.

**Features:**
- Parallel processing with configurable workers
- Progress tracking and resumption capabilities
- Data validation and error handling
- Export to multiple formats (JSON, CSV, Excel)
- Resource management and rate limiting

**Usage:**
```bash
# Run with default configuration
python scripts/batch_processor.py

# Run with specific keywords
python scripts/batch_processor.py --keywords "ai" "ml" "python"

# Run with specific locations
python scripts/batch_processor.py --locations "US" "GB" "CA"

# Resume from previous batch
python scripts/batch_processor.py --resume "20240101_120000"
```

**Configuration:**
- Edit `config/batch_config.json` to customize:
  - Keywords and locations to process
  - Processing parameters (workers, batch size)
  - Output formats and validation rules

### 📈 `report_generator.py`
**Automated Report Generation**

Generates comprehensive reports and visualizations from Google Search Trends data with insights and recommendations.

**Features:**
- Multiple report formats (HTML, Excel, PDF)
- Interactive visualizations and charts
- Trend insights and recommendations
- Geographic analysis
- Customizable templates

**Usage:**
```bash
# Generate report with default settings
python scripts/report_generator.py

# Generate report for specific keywords
python scripts/report_generator.py --keywords "artificial intelligence" "machine learning"

# Generate report with custom ID
python scripts/report_generator.py --report-id "ai_trends_2024"
```

**Configuration:**
- Edit `config/report_config.json` to customize:
  - Report types and content
  - Visualization settings
  - Output formats and templates

## 🛠️ Setup and Installation

### 1. Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Configuration Files
Each script uses JSON configuration files in the `config/` directory:

- `config/monitor_config.json` - Trend monitoring settings
- `config/batch_config.json` - Batch processing settings  
- `config/report_config.json` - Report generation settings

### 3. API Keys
Set up your API keys in the `.env` file:
```bash
# For Value SERP API (optional)
VALUE_SERP_API_KEY=your_api_key_here

# For other APIs (optional)
GOOGLE_API_KEY=your_google_api_key_here
SERPAPI_KEY=your_serpapi_key_here
```

## 📋 Usage Examples

### Trend Monitoring
```bash
# Start monitoring with default settings
python scripts/trend_monitor.py

# Monitor specific keywords
python scripts/trend_monitor.py --keywords "bitcoin" "ethereum" "crypto"

# Use custom configuration
python scripts/trend_monitor.py --config config/custom_monitor.json
```

### Batch Processing
```bash
# Process all configured keywords and locations
python scripts/batch_processor.py

# Process specific keywords only
python scripts/batch_processor.py --keywords "ai" "ml" "python"

# Process with custom settings
python scripts/batch_processor.py --locations "US" "GB" --timeframes "today 1-m"
```

### Report Generation
```bash
# Generate comprehensive report
python scripts/report_generator.py

# Generate report for specific analysis
python scripts/report_generator.py --keywords "blockchain" "crypto"

# Generate report with custom ID
python scripts/report_generator.py --report-id "crypto_analysis_2024"
```

## 🔧 Configuration

### Monitor Configuration (`config/monitor_config.json`)
```json
{
  "keywords": ["ai", "ml", "python"],
  "monitoring_interval": 3600,
  "alert_threshold": 20,
  "geographic_locations": ["US", "GB", "CA"],
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "sender_email": "your@email.com",
      "recipient_emails": ["alerts@company.com"]
    }
  }
}
```

### Batch Configuration (`config/batch_config.json`)
```json
{
  "keywords": ["ai", "ml", "python", "data science"],
  "locations": ["US", "GB", "CA", "AU"],
  "processing": {
    "max_workers": 4,
    "batch_size": 5,
    "delay_between_batches": 2
  },
  "output": {
    "format": ["json", "csv", "excel"],
    "directory": "data/batch_results/"
  }
}
```

### Report Configuration (`config/report_config.json`)
```json
{
  "keywords": ["ai", "ml", "python"],
  "locations": ["US", "GB", "CA"],
  "output": {
    "formats": ["html", "excel"],
    "include_charts": true,
    "include_insights": true
  },
  "visualization": {
    "style": "seaborn",
    "figure_size": [12, 8],
    "dpi": 300
  }
}
```

## 📊 Output and Results

### Trend Monitor Output
- **Logs**: `logs/trend_monitor.log`
- **Data**: `data/monitoring/trends_YYYYMMDD_HHMMSS.json`
- **Alerts**: Email, Slack, or webhook notifications

### Batch Processor Output
- **Results**: `data/batch_results/batch_YYYYMMDD_HHMMSS.json`
- **Reports**: `data/batch_results/report_YYYYMMDD_HHMMSS.json`
- **Logs**: `logs/batch_processor.log`

### Report Generator Output
- **HTML Reports**: `reports/report_YYYYMMDD_HHMMSS.html`
- **Excel Reports**: `reports/report_YYYYMMDD_HHMMSS.xlsx`
- **Charts**: `reports/charts/YYYYMMDD_HHMMSS/`
- **Logs**: `logs/report_generator.log`

## 🔄 Automation and Scheduling

### Using Cron (Linux/Mac)
```bash
# Add to crontab for daily reports
0 9 * * * cd /path/to/project && python scripts/report_generator.py

# Add to crontab for hourly monitoring
0 * * * * cd /path/to/project && python scripts/trend_monitor.py
```

### Using Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly, etc.)
4. Set action: `python scripts/report_generator.py`
5. Set start in: project directory

### Using Docker
```dockerfile
# Add to Dockerfile
COPY scripts/ /app/scripts/
COPY config/ /app/config/

# Run in container
CMD ["python", "scripts/trend_monitor.py"]
```

## 🚀 Advanced Usage

### Custom Scripts
You can create custom scripts by extending the base classes:

```python
from scripts.trend_monitor import TrendMonitor

class CustomMonitor(TrendMonitor):
    def custom_analysis(self, data):
        # Add custom analysis logic
        pass

# Use custom monitor
monitor = CustomMonitor()
monitor.start_monitoring()
```

### Integration with Other Tools
The scripts can be integrated with:
- **Data pipelines**: Apache Airflow, Luigi
- **Monitoring**: Prometheus, Grafana
- **Notification**: Slack, Discord, Teams
- **Storage**: AWS S3, Google Cloud Storage

## 🔒 Security and Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Respect API rate limits and terms of service
3. **Data Privacy**: Handle data according to privacy regulations
4. **Error Handling**: Monitor logs for errors and failures
5. **Backup**: Regularly backup configuration and data files

## 📝 Troubleshooting

### Common Issues

1. **API Rate Limits**: Increase delays between requests
2. **Memory Issues**: Reduce batch sizes or number of workers
3. **Network Errors**: Check internet connection and API endpoints
4. **Configuration Errors**: Validate JSON configuration files

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python scripts/trend_monitor.py
```

### Log Analysis
```bash
# View recent logs
tail -f logs/trend_monitor.log

# Search for errors
grep "ERROR" logs/*.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your custom scripts
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the main [LICENSE](../LICENSE) file for details.

---

**Note**: These scripts are designed for educational and research purposes. Please respect API rate limits and terms of service when using them. 