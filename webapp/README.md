# Google Search Trends Web Application

A modern web interface for Google Search Trends automation, built with Next.js and React, similar to the [bta-app repository](https://github.com/mikerhodesideas/bta-app) structure.

## 🚀 Features

- **User-Friendly Interface**: Clean, modern web interface built with Next.js and TailwindCSS
- **API Key Management**: Secure input and validation of Value SERP API keys
- **One-Click Automation**: Run all automation scripts with a single button click
- **Real-Time Progress**: Live progress tracking and logging
- **Results Visualization**: Beautiful display of trend analysis results
- **Report Downloads**: Easy access to generated reports and data

## 🛠️ Technologies Used

- **Frontend**: React with Next.js 15 App Router
- **Styling**: TailwindCSS with custom design system
- **Icons**: Lucide React
- **Charts**: Chart.js with React Chart.js 2
- **Backend**: Next.js API routes
- **Integration**: Python scripts via child processes

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+ with required dependencies
- Value SERP API key from [https://valueserp.com/](https://valueserp.com/)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to webapp directory
cd webapp

# Install Node.js dependencies
npm install

# Install Python dependencies (from parent directory)
cd ..
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys (optional for web interface)
VALUE_SERP_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
# Start the development server
npm run dev
```

The application will be available at `http://localhost:3000`

## 🎯 How to Use

### Step 1: Enter Your API Key
1. Open the web application in your browser
2. Enter your Value SERP API key in the secure input field
3. Click "Validate API Key" to verify it works
4. Once validated, the "Run Automation" button will be enabled

### Step 2: Run Automation
1. Click the "Run Automation" button
2. Watch the real-time progress as the system:
   - Monitors trends for configured keywords
   - Processes batch data across multiple locations
   - Generates comprehensive reports
3. View the results and download generated files

### Step 3: View Results
- **Summary Cards**: Overview of processed data
- **Trend Analysis**: Visual representation of keyword trends
- **Generated Reports**: Download HTML, Excel, and JSON reports
- **Processing Logs**: Detailed logs of the automation process

## 📁 Project Structure

```
webapp/
├── app/                          # Next.js App Router
│   ├── components/               # React components
│   │   ├── ApiKeyForm.tsx       # API key input form
│   │   └── ResultsViewer.tsx    # Results display
│   ├── api/                     # API routes
│   │   ├── run-automation/      # Main automation endpoint
│   │   └── validate-api-key/    # API key validation
│   ├── globals.css              # Global styles
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Main page
├── scripts/                     # Web automation scripts
│   └── web_automation.py        # Main automation orchestrator
├── package.json                 # Node.js dependencies
├── next.config.mjs             # Next.js configuration
├── tailwind.config.ts          # TailwindCSS configuration
└── README.md                   # This file
```

## 🔧 Configuration

### API Key Validation
The application validates your Value SERP API key by making a test request to the API. For security, the key is not stored permanently.

### Automation Settings
The web interface uses the same configuration files as the command-line scripts:
- `config/monitor_config.json` - Trend monitoring settings
- `config/batch_config.json` - Batch processing settings
- `config/report_config.json` - Report generation settings

### Customization
You can customize the automation by editing the configuration files in the parent directory.

## 🔒 Security Features

- **API Key Protection**: Keys are not stored in the database
- **Input Validation**: Secure validation of API keys
- **Error Handling**: Graceful error handling and user feedback
- **Rate Limiting**: Built-in rate limiting for API calls

## 📊 Output and Results

### Generated Files
- **HTML Reports**: Interactive web reports with charts
- **Excel Reports**: Spreadsheet format with multiple sheets
- **JSON Data**: Raw data for further processing
- **Charts**: PNG images of trend visualizations

### File Locations
- Reports: `reports/` directory
- Data: `data/batch_results/` directory
- Logs: `logs/` directory

## 🔄 Integration with Python Scripts

The web application integrates with your existing Python automation scripts:

1. **Trend Monitor** (`scripts/trend_monitor.py`)
2. **Batch Processor** (`scripts/batch_processor.py`)
3. **Report Generator** (`scripts/report_generator.py`)

The web interface orchestrates these scripts and provides a user-friendly way to run them.

## 🚀 Deployment

### Local Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Validation Fails**
   - Ensure your Value SERP API key is correct
   - Check your internet connection
   - Verify the API key has sufficient credits

2. **Python Scripts Not Found**
   - Ensure you're running from the correct directory
   - Check that Python dependencies are installed
   - Verify the PYTHONPATH is set correctly

3. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Debug Mode
```bash
# Enable debug logging
export DEBUG=*
npm run dev
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the main [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Bea-stack-tech/S-T-Project/issues)
- **Documentation**: [Wiki](https://github.com/Bea-stack-tech/S-T-Project/wiki)
- **Value SERP API**: [https://valueserp.com/](https://valueserp.com/)

---

**Note**: This web application is designed for educational and research purposes. Please respect API rate limits and terms of service when using it. 