# Webapp Setup Guide

## Quick Setup

### 1. Get Your Value SERP API Key

1. Visit [Value SERP](https://valueserp.com/)
2. Sign up for an account
3. Get your API key from the dashboard

### 2. Configure the API Key

1. Copy the environment template:
   ```bash
   cp env.example .env.local
   ```

2. Edit `.env.local` and replace `your_api_key_here` with your actual Value SERP API key:
   ```
   VALUE_SERP_API_KEY=your_actual_api_key_here
   ```

3. Restart the development server:
   ```bash
   npm run dev
   ```

### 3. Test the Setup

1. Open the webapp at `http://localhost:3000`
2. Enter some keywords or URLs
3. Click "Analyze Trends"
4. The system should now use your API key automatically

## Troubleshooting

### API Key Not Working
- Make sure your API key is correct
- Check that you have sufficient credits in your Value SERP account
- Verify the `.env.local` file is in the correct location

### Python Scripts Not Found
- Ensure you're running from the webapp directory
- Check that Python dependencies are installed: `pip install -r ../requirements.txt`
- Verify the PYTHONPATH is set correctly

### Build Errors
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility
- Verify all dependencies are installed

## Security Notes

- The API key is stored in environment variables and never exposed to the frontend
- The `.env.local` file should not be committed to version control
- API requests are made server-side for security 