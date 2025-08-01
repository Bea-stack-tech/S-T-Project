'use client';

import { TrendingUp, TrendingDown, Minus, FileText, Download, BarChart3 } from 'lucide-react';

interface ResultsViewerProps {
  results: {
    trends: Array<{
      keyword: string;
      trend: string;
      value: number;
    }>;
    reports: Array<{
      name: string;
      type: string;
    }>;
    summary: {
      totalKeywords: number;
      totalLocations: number;
      successRate: number;
      processingTime: string;
    };
  };
}

export default function ResultsViewer({ results }: ResultsViewerProps) {
  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'decreasing':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <Minus className="h-4 w-4 text-gray-600" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return 'text-green-600';
      case 'decreasing':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Keywords</p>
              <p className="text-2xl font-bold text-gray-900">{results.summary.totalKeywords}</p>
            </div>
            <BarChart3 className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Locations</p>
              <p className="text-2xl font-bold text-gray-900">{results.summary.totalLocations}</p>
            </div>
            <BarChart3 className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">{results.summary.successRate}%</p>
            </div>
            <BarChart3 className="h-8 w-8 text-yellow-600" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Processing Time</p>
              <p className="text-2xl font-bold text-gray-900">{results.summary.processingTime}</p>
            </div>
            <BarChart3 className="h-8 w-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* Trends Analysis */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">Trend Analysis Results</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {results.trends.map((trend, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getTrendIcon(trend.trend)}
                  <div>
                    <p className="font-medium text-gray-900">{trend.keyword}</p>
                    <p className={`text-sm font-medium ${getTrendColor(trend.trend)}`}>
                      {trend.trend.charAt(0).toUpperCase() + trend.trend.slice(1)} trend
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-gray-900">{trend.value}</p>
                  <p className="text-sm text-gray-500">Interest Score</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Generated Reports */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-semibold text-gray-900">Generated Reports</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {results.reports.map((report, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="font-medium text-gray-900">{report.name}</p>
                    <p className="text-sm text-gray-500">{report.type}</p>
                  </div>
                </div>
                <button
                  onClick={() => window.open(`/api/download/${report.name}`, '_blank')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
                >
                  <Download className="h-4 w-4" />
                  <span>Download</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Success Message */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
            <TrendingUp className="h-4 w-4 text-green-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-green-900">Analysis Complete!</h3>
            <p className="text-green-700">
              Your Google Search Trends analysis has been completed successfully. 
              All reports have been generated and are ready for download.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 