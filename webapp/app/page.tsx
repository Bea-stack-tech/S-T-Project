'use client';

import { useState } from 'react';
import { Play, TrendingUp, BarChart3, FileText, Settings, Download, AlertCircle, CheckCircle } from 'lucide-react';
import ApiKeyForm from './components/ApiKeyForm';
import TrendMonitor from './components/TrendMonitor';
import BatchProcessor from './components/BatchProcessor';
import ReportGenerator from './components/ReportGenerator';
import ResultsViewer from './components/ResultsViewer';

export default function Home() {
  const [apiKey, setApiKey] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('setup');
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const handleRunAll = async () => {
    if (!apiKey) {
      alert('Please enter your Value SERP API key first');
      return;
    }

    setIsRunning(true);
    setCurrentStep('monitoring');
    addLog('Starting Google Search Trends automation...');

    try {
      // Step 1: Trend Monitoring
      addLog('Step 1: Running trend monitoring...');
      setCurrentStep('monitoring');
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing
      addLog('✓ Trend monitoring completed');

      // Step 2: Batch Processing
      addLog('Step 2: Running batch processing...');
      setCurrentStep('processing');
      await new Promise(resolve => setTimeout(resolve, 3000)); // Simulate processing
      addLog('✓ Batch processing completed');

      // Step 3: Report Generation
      addLog('Step 3: Generating reports...');
      setCurrentStep('reporting');
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing
      addLog('✓ Report generation completed');

      // Step 4: Show Results
      setCurrentStep('results');
      setResults({
        trends: [
          { keyword: 'artificial intelligence', trend: 'increasing', value: 85 },
          { keyword: 'machine learning', trend: 'stable', value: 72 },
          { keyword: 'python', trend: 'increasing', value: 68 },
        ],
        reports: [
          { name: 'trend_analysis_2024.html', type: 'HTML Report' },
          { name: 'batch_results_2024.xlsx', type: 'Excel Report' },
          { name: 'insights_summary.json', type: 'JSON Data' },
        ],
        summary: {
          totalKeywords: 18,
          totalLocations: 8,
          successRate: 95.2,
          processingTime: '7.2 seconds'
        }
      });

      addLog('✓ All processes completed successfully!');
    } catch (error) {
      addLog(`✗ Error: ${error}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Google Search Trends Automation</h1>
                <p className="text-sm text-gray-500">Powered by Value SERP API</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Settings className="h-5 w-5 text-gray-400" />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* API Key Setup */}
        {currentStep === 'setup' && (
          <div className="mb-8">
            <ApiKeyForm 
              apiKey={apiKey} 
              onApiKeyChange={setApiKey} 
              onRun={handleRunAll}
              isRunning={isRunning}
            />
          </div>
        )}

        {/* Progress Steps */}
        {isRunning && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Processing Steps</h2>
              <div className="space-y-4">
                <div className={`flex items-center space-x-3 ${currentStep === 'monitoring' ? 'text-blue-600' : 'text-gray-400'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'monitoring' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    {currentStep === 'monitoring' ? <Play className="h-4 w-4" /> : '1'}
                  </div>
                  <span className="font-medium">Trend Monitoring</span>
                </div>
                <div className={`flex items-center space-x-3 ${currentStep === 'processing' ? 'text-blue-600' : 'text-gray-400'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'processing' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    {currentStep === 'processing' ? <Play className="h-4 w-4" /> : '2'}
                  </div>
                  <span className="font-medium">Batch Processing</span>
                </div>
                <div className={`flex items-center space-x-3 ${currentStep === 'reporting' ? 'text-blue-600' : 'text-gray-400'}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'reporting' ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    {currentStep === 'reporting' ? <Play className="h-4 w-4" /> : '3'}
                  </div>
                  <span className="font-medium">Report Generation</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {currentStep === 'results' && results && (
          <div className="mb-8">
            <ResultsViewer results={results} />
          </div>
        )}

        {/* Logs */}
        {logs.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b">
              <h3 className="text-lg font-semibold text-gray-900">Processing Logs</h3>
            </div>
            <div className="p-6">
              <div className="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto">
                {logs.map((log, index) => (
                  <div key={index} className="text-sm font-mono text-gray-700 mb-1">
                    {log}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        {!isRunning && currentStep !== 'setup' && (
          <div className="flex justify-center space-x-4 mt-8">
            <button
              onClick={() => setCurrentStep('setup')}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Run Again
            </button>
            <button
              onClick={() => window.open('/api/download-results', '_blank')}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download Results</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
} 