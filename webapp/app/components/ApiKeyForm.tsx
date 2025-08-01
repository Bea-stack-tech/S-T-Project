'use client';

import { useState } from 'react';
import { Key, Eye, EyeOff, Play, AlertCircle, CheckCircle } from 'lucide-react';

interface ApiKeyFormProps {
  apiKey: string;
  onApiKeyChange: (key: string) => void;
  onRun: () => void;
  isRunning: boolean;
}

export default function ApiKeyForm({ apiKey, onApiKeyChange, onRun, isRunning }: ApiKeyFormProps) {
  const [showKey, setShowKey] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState<'idle' | 'validating' | 'valid' | 'invalid'>('idle');

  const validateApiKey = async () => {
    if (!apiKey.trim()) {
      setValidationStatus('invalid');
      return;
    }

    setIsValidating(true);
    setValidationStatus('validating');

    try {
      // Simulate API key validation
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // For demo purposes, consider any non-empty key as valid
      if (apiKey.length > 10) {
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

  const handleKeyChange = (value: string) => {
    onApiKeyChange(value);
    setValidationStatus('idle');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-8">
      <div className="max-w-2xl mx-auto text-center">
        <div className="mb-8">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Key className="h-8 w-8 text-blue-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Setup Your Value SERP API Key</h2>
          <p className="text-gray-600">
            Enter your Value SERP API key to start analyzing Google Search Trends data
          </p>
        </div>

        <div className="space-y-6">
          {/* API Key Input */}
          <div>
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2">
              Value SERP API Key
            </label>
            <div className="relative">
              <input
                id="apiKey"
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => handleKeyChange(e.target.value)}
                placeholder="Enter your Value SERP API key"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 pr-12"
                disabled={isRunning}
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                disabled={isRunning}
              >
                {showKey ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
            
            {/* Validation Status */}
            {validationStatus !== 'idle' && (
              <div className="mt-2 flex items-center space-x-2">
                {validationStatus === 'validating' && (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span className="text-sm text-blue-600">Validating API key...</span>
                  </>
                )}
                {validationStatus === 'valid' && (
                  <>
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm text-green-600">API key is valid</span>
                  </>
                )}
                {validationStatus === 'invalid' && (
                  <>
                    <AlertCircle className="h-4 w-4 text-red-600" />
                    <span className="text-sm text-red-600">Invalid API key</span>
                  </>
                )}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={validateApiKey}
              disabled={!apiKey.trim() || isRunning || isValidating}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isValidating ? 'Validating...' : 'Validate API Key'}
            </button>
            
            <button
              onClick={onRun}
              disabled={!apiKey.trim() || isRunning || validationStatus !== 'valid'}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
            >
              {isRunning ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Running...</span>
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Run Automation</span>
                </>
              )}
            </button>
          </div>

          {/* Help Text */}
          <div className="text-sm text-gray-500">
            <p className="mb-2">
              <strong>Don't have an API key?</strong> Get one from{' '}
              <a 
                href="https://valueserp.com/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                Value SERP
              </a>
            </p>
            <p>
              Your API key will be used to fetch Google Search Trends data and will not be stored permanently.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 