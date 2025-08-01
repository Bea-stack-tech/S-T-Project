# Jupyter Notebooks

This directory contains Jupyter notebooks for interactive analysis of Google Search Trends data.

## Available Notebooks

### 1. trends_analysis_example.ipynb
A comprehensive example notebook that demonstrates:
- Fetching trending searches
- Analyzing historical trends
- Comparing multiple keywords
- Creating visualizations
- Exporting data in various formats
- Geographic analysis
- Interactive dashboards

## Getting Started

1. **Install Jupyter**: Make sure you have Jupyter installed:
   ```bash
   pip install jupyter
   ```

2. **Start Jupyter**: Navigate to this directory and start Jupyter:
   ```bash
   cd notebooks
   jupyter notebook
   ```

3. **Open the notebook**: Click on `trends_analysis_example.ipynb` to open it.

4. **Run cells**: Execute cells one by one or run all cells to see the complete analysis.

## Customization

You can customize the notebooks by:
- Changing keywords for analysis
- Modifying timeframes
- Adding new geographic locations
- Creating custom visualizations
- Integrating with other data sources

## Tips

- Make sure all dependencies are installed (see `requirements.txt`)
- The notebooks assume the `src` directory is in the parent directory
- Generated files will be saved in `../data/exports/`
- You can modify the analysis parameters in the first few cells

## Example Usage

```python
# In a notebook cell
from trends_analyzer import TrendsAnalyzer

# Initialize analyzer
analyzer = TrendsAnalyzer()

# Get trending searches
trends = analyzer.get_trending_searches(geo="US")

# Analyze historical data
data = analyzer.get_historical_trends("python", timeframe="today 12-m")

# Create visualization
analyzer.create_visualization(data, chart_type="line")
``` 