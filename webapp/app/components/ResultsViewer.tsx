'use client';

import { TrendingUp, TrendingDown, Minus, FileText, Download, BarChart3, Target, Search, Globe, Zap, Users, Lightbulb, Sparkles, CheckCircle, AlertCircle } from 'lucide-react';

interface ResultsViewerProps {
  results: {
    analysis_config?: any;
    phase1_results?: any;
    phase2_results?: any;
    phase3_results?: any;
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
      phasesCompleted?: number;
      opportunitiesIdentified?: number;
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
        return <Minus className="h-4 w-4 text-slate-600" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return 'text-green-600';
      case 'decreasing':
        return 'text-red-600';
      default:
        return 'text-slate-600';
    }
  };

  return (
    <div className="space-y-8">
      {/* Success Header */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-8 border border-green-200/60">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg">
            <CheckCircle className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Analysis Complete!</h2>
            <div className="text-slate-600">Your three-phase analysis has been completed successfully with actionable insights.</div>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-white" />
            </div>
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">Keywords</span>
          </div>
          <p className="text-sm font-medium text-slate-600 mb-1">Total Keywords</p>
          <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{results.summary.totalKeywords}</p>
        </div>

        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
              <Target className="h-5 w-5 text-white" />
            </div>
            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">Phases</span>
          </div>
          <p className="text-sm font-medium text-slate-600 mb-1">Phases Completed</p>
          <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{results.summary.phasesCompleted || 3}</p>
        </div>

        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl flex items-center justify-center">
              <Lightbulb className="h-5 w-5 text-white" />
            </div>
            <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded-full font-medium">Opportunities</span>
          </div>
          <p className="text-sm font-medium text-slate-600 mb-1">Opportunities</p>
          <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{results.summary.opportunitiesIdentified || 0}</p>
        </div>

        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl flex items-center justify-center">
              <Zap className="h-5 w-5 text-white" />
            </div>
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full font-medium">Speed</span>
          </div>
          <p className="text-sm font-medium text-slate-600 mb-1">Processing Time</p>
          <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{results.summary.processingTime}</p>
        </div>
      </div>

      {/* Phase 1 Results - Paid Advertising Analysis */}
      {results.phase1_results && (
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden">
          <div className="px-8 py-6 border-b border-slate-200/60 bg-gradient-to-r from-blue-50 to-indigo-50">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
                <Target className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Phase 1: Paid Advertising Strength Analysis</h3>
            </div>
          </div>
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span>Ad Strength Assessment</span>
                </h4>
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200/60">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                          <TrendingUp className="h-4 w-4 text-white" />
                        </div>
                        <span className="font-semibold text-green-800">Good Ads</span>
                      </div>
                      <span className="text-2xl font-bold text-green-600">{results.phase1_results.ad_strength_assessment.good_ads}</span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-red-50 to-pink-50 rounded-xl p-6 border border-red-200/60">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                          <TrendingDown className="h-4 w-4 text-white" />
                        </div>
                        <span className="font-semibold text-red-800">Bad Ads</span>
                      </div>
                      <span className="text-2xl font-bold text-red-600">{results.phase1_results.ad_strength_assessment.bad_ads}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <Lightbulb className="h-5 w-5 text-yellow-600" />
                  <span>Key Insights</span>
                </h4>
                <div className="space-y-3">
                  {results.phase1_results.ad_strength_assessment.messaging_insights.map((insight: string, index: number) => (
                    <div key={index} className="bg-slate-50/80 backdrop-blur-sm rounded-xl p-4 border border-slate-200/60">
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-slate-700">{insight}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mt-8">
              <h4 className="text-lg font-semibold text-slate-900 mb-6 flex items-center space-x-2">
                <Search className="h-5 w-5 text-blue-600" />
                <span>Positioning Gaps Identified</span>
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {results.phase1_results.ad_strength_assessment.positioning_gaps.map((gap: string, index: number) => (
                  <div key={index} className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-200/60">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-sm text-slate-700">{gap}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Phase 2 Results - Trends & Look-alike Discovery */}
      {results.phase2_results && (
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden">
          <div className="px-8 py-6 border-b border-slate-200/60 bg-gradient-to-r from-green-50 to-emerald-50">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
                <Search className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Phase 2: Trends & Look-alike Discovery</h3>
            </div>
          </div>
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span>Trend Intelligence Summary</span>
                </h4>
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200/60">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-green-800">Total Keywords Discovered</span>
                      <span className="text-2xl font-bold text-green-600">{results.phase2_results.trend_intelligence.total_keywords_discovered}</span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200/60">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-blue-800">High Momentum Keywords</span>
                      <span className="text-2xl font-bold text-blue-600">{results.phase2_results.trend_intelligence.high_momentum_keywords}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <Globe className="h-5 w-5 text-blue-600" />
                  <span>Geographic Insights</span>
                </h4>
                <div className="space-y-3">
                  {results.phase2_results.trend_intelligence.geographic_insights.map((insight: string, index: number) => (
                    <div key={index} className="bg-slate-50/80 backdrop-blur-sm rounded-xl p-4 border border-slate-200/60">
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-slate-700">{insight}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Expanded Keywords */}
            {results.phase2_results.expanded_keywords && results.phase2_results.expanded_keywords.length > 0 && (
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <Sparkles className="h-5 w-5 text-purple-600" />
                  <span>Expanded Keyword Universe</span>
                </h4>
                <div className="space-y-4">
                  {results.phase2_results.expanded_keywords.slice(0, 5).map((keywordData: any, index: number) => (
                    <div key={index} className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-white/40">
                      <div className="flex items-center justify-between mb-4">
                        <h5 className="font-semibold text-slate-900">{keywordData.original}</h5>
                        <div className="flex items-center space-x-3">
                          <span className="text-sm text-slate-500">Momentum:</span>
                          <span className="text-sm font-bold text-blue-600 bg-blue-100 px-3 py-1 rounded-full">{keywordData.trend_data.momentum}</span>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {keywordData.lookalikes.slice(0, 4).map((lookalike: string, idx: number) => (
                          <div key={idx} className="bg-slate-100/80 backdrop-blur-sm rounded-lg p-3 text-sm text-slate-700 font-medium">
                            {lookalike}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Phase 3 Results - Competitive Analysis */}
      {results.phase3_results && (
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden">
          <div className="px-8 py-6 border-b border-slate-200/60 bg-gradient-to-r from-purple-50 to-violet-50">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl flex items-center justify-center">
                <Users className="h-5 w-5 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Phase 3: Competitive Strengths & Weaknesses Analysis</h3>
            </div>
          </div>
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <Target className="h-5 w-5 text-purple-600" />
                  <span>Opportunity Matrix</span>
                </h4>
                <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200/60">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-green-800">High Trend, Low Competition</span>
                    <span className="text-2xl font-bold text-green-600">{results.phase3_results.opportunity_matrix.high_trend_low_competition}</span>
                  </div>
                </div>
              </div>
              
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span>Organic Opportunities</span>
                </h4>
                <div className="space-y-3">
                  {results.phase3_results.opportunity_matrix.organic_opportunities.map((opportunity: string, index: number) => (
                    <div key={index} className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200/60">
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-slate-700">{opportunity}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-blue-600" />
                  <span>Paid Opportunities</span>
                </h4>
                <div className="space-y-3">
                  {results.phase3_results.opportunity_matrix.paid_opportunities.map((opportunity: string, index: number) => (
                    <div key={index} className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-200/60">
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-slate-700">{opportunity}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Competitor Weaknesses */}
            {results.phase3_results.opportunity_matrix.competitor_weaknesses && results.phase3_results.opportunity_matrix.competitor_weaknesses.length > 0 && (
              <div className="mt-8 space-y-6">
                <h4 className="text-lg font-semibold text-slate-900 flex items-center space-x-2">
                  <AlertCircle className="h-5 w-5 text-red-600" />
                  <span>Competitor Weaknesses</span>
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {results.phase3_results.opportunity_matrix.competitor_weaknesses.map((weakness: string, index: number) => (
                    <div key={index} className="bg-gradient-to-r from-red-50 to-pink-50 rounded-xl p-4 border border-red-200/60">
                      <div className="flex items-start space-x-3">
                        <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-slate-700">{weakness}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Trends Analysis */}
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden">
        <div className="px-8 py-6 border-b border-slate-200/60 bg-slate-50/50">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-slate-600 to-slate-700 rounded-xl flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-white" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Trend Analysis Results</h3>
          </div>
        </div>
        <div className="p-8">
          <div className="space-y-4">
            {results.trends.map((trend, index) => (
              <div key={index} className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-white/40 hover:shadow-lg transition-all duration-300">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    {getTrendIcon(trend.trend)}
                    <div>
                      <p className="font-semibold text-slate-900">{trend.keyword}</p>
                      <p className={`text-sm font-medium ${getTrendColor(trend.trend)}`}>
                        {trend.trend.charAt(0).toUpperCase() + trend.trend.slice(1)} trend
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">{trend.value}</p>
                    <p className="text-sm text-slate-500">Interest Score</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Generated Reports */}
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden">
        <div className="px-8 py-6 border-b border-slate-200/60 bg-slate-50/50">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-slate-600 to-slate-700 rounded-xl flex items-center justify-center">
              <FileText className="h-5 w-5 text-white" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Generated Reports</h3>
          </div>
        </div>
        <div className="p-8">
          <div className="space-y-4">
            {results.reports.map((report, index) => (
              <div key={index} className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-white/40 hover:shadow-lg transition-all duration-300">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
                      <FileText className="h-5 w-5 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold text-slate-900">{report.name}</p>
                      <p className="text-sm text-slate-500">{report.type}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => window.open(`/api/download/${report.name}`, '_blank')}
                    className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center space-x-2"
                  >
                    <Download className="h-4 w-4" />
                    <span>Download</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 