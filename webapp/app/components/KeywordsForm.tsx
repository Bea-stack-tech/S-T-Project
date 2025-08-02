'use client';

import { useState } from 'react';
import { Search, Play, AlertCircle, CheckCircle, Globe, Hash } from 'lucide-react';

interface KeywordsFormProps {
  onRun: (keywords: string[], urls: string[]) => void;
  isRunning: boolean;
}

export default function KeywordsForm({ onRun, isRunning }: KeywordsFormProps) {
  const [keywords, setKeywords] = useState('');
  const [urls, setUrls] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState<'idle' | 'validating' | 'valid' | 'invalid'>('idle');

  const validateInput = async () => {
    const keywordList = keywords.split('\n').filter(k => k.trim());
    const urlList = urls.split('\n').filter(u => u.trim());
    
    if (keywordList.length === 0 && urlList.length === 0) {
      setValidationStatus('invalid');
      return;
    }

    setIsValidating(true);
    setValidationStatus('validating');

    try {
      // Simulate validation
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Validate URLs format
      const validUrls = urlList.every(url => {
        try {
          new URL(url.trim());
          return true;
        } catch {
          return false;
        }
      });

      if (validUrls) {
        setValidationStatus('valid');
      } else {
        setValidationStatus('invalid');
      }
    } catch (error) {
      setValidationStatus('invalid');
    } finally {
      setIsValidating(false);
    }
  };

  const handleSubmit = () => {
    const keywordList = keywords.split('\n').filter(k => k.trim());
    const urlList = urls.split('\n').filter(u => u.trim());
    onRun(keywordList, urlList);
  };

  const handleKeywordsChange = (value: string) => {
    setKeywords(value);
    setValidationStatus('idle');
  };

  const handleUrlsChange = (value: string) => {
    setUrls(value);
    setValidationStatus('idle');
  };

  const hasValidInput = keywords.trim() || urls.trim();

  return (
    <div className="bg-white rounded-lg shadow-sm border p-8">
      <div className="max-w-2xl mx-auto text-center">
        <div className="mb-8">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="h-8 w-8 text-blue-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Enter Your Keywords or Website URLs</h2>
          <p className="text-gray-600">
            Enter keywords or website URLs to find search insights and trends
          </p>
        </div>

        <div className="space-y-6">
          {/* Keywords Input */}
          <div>
            <label htmlFor="keywords" className="block text-sm font-medium text-gray-700 mb-2">
              <Hash className="inline h-4 w-4 mr-1" />
              Keywords (one per line)
            </label>
            <textarea
              id="keywords"
              value={keywords}
              onChange={(e) => handleKeywordsChange(e.target.value)}
              placeholder="artificial intelligence&#10;machine learning&#10;python programming&#10;data science"
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              disabled={isRunning}
            />
            <p className="text-xs text-gray-500 mt-1">
              Enter each keyword on a separate line
            </p>
          </div>

          {/* URLs Input */}
          <div>
            <label htmlFor="urls" className="block text-sm font-medium text-gray-700 mb-2">
              <Globe className="inline h-4 w-4 mr-1" />
              Website URLs (one per line)
            </label>
            <textarea
              id="urls"
              value={urls}
              onChange={(e) => handleUrlsChange(e.target.value)}
              placeholder="https://example.com&#10;https://another-site.com"
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              disabled={isRunning}
            />
            <p className="text-xs text-gray-500 mt-1">
              Enter full URLs including https://
            </p>
          </div>

          {/* Validation Status */}
          {validationStatus !== 'idle' && (
            <div className="flex items-center justify-center space-x-2">
              {validationStatus === 'validating' && (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  <span className="text-sm text-blue-600">Validating input...</span>
                </>
              )}
              {validationStatus === 'valid' && (
                <>
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-green-600">Input is valid</span>
                </>
              )}
              {validationStatus === 'invalid' && (
                <>
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <span className="text-sm text-red-600">Please enter at least one keyword or valid URL</span>
                </>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={validateInput}
              disabled={!hasValidInput || isRunning || isValidating}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isValidating ? 'Validating...' : 'Validate Input'}
            </button>
            
            <button
              onClick={handleSubmit}
              disabled={!hasValidInput || isRunning || validationStatus !== 'valid'}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
            >
              {isRunning ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Analyze Trends</span>
                </>
              )}
            </button>
          </div>

          {/* Help Text */}
          <div className="text-sm text-gray-500">
            <p className="mb-2">
              <strong>How it works:</strong> Enter keywords or website URLs to analyze Google Search Trends data.
            </p>
            <p>
              The system will automatically fetch search insights using our configured Value SERP API.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 