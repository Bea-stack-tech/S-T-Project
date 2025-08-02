'use client';

import { useState } from 'react';
import { Search, Globe, MapPin, Play, AlertCircle, Sparkles, Zap, Target, TrendingUp, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface AnalysisSelectorProps {
  onStartAnalysis: (analysisType: 'keywords' | 'urls', data: string[], location?: string) => void;
  isRunning: boolean;
}

export default function AnalysisSelector({ onStartAnalysis, isRunning }: AnalysisSelectorProps) {
  const [analysisType, setAnalysisType] = useState<'keywords' | 'urls'>('keywords');
  const [inputData, setInputData] = useState('');
  const [location, setLocation] = useState('');
  const [errors, setErrors] = useState<string[]>([]);

  const validateInput = () => {
    const errors: string[] = [];
    
    if (!inputData.trim()) {
      errors.push('Please enter keywords or URLs');
    }

    if (analysisType === 'urls') {
      const urls = inputData.split('\n').filter(u => u.trim());
      if (urls.length > 3) {
        errors.push('Maximum 3 competitor URLs allowed');
      }
      
      for (const url of urls) {
        try {
          new URL(url.trim());
        } catch {
          errors.push(`Invalid URL format: ${url}`);
        }
      }
    }

    setErrors(errors);
    return errors.length === 0;
  };

  const handleStartAnalysis = () => {
    if (!validateInput()) return;

    const data = inputData.split('\n').filter(item => item.trim());
    const locationValue = location.trim() || undefined;
    
    onStartAnalysis(analysisType, data, locationValue);
  };

  const getPlaceholder = () => {
    if (analysisType === 'keywords') {
      return 'artificial intelligence\nmachine learning\npython programming\ndata science';
    } else {
      return 'https://example.com\nhttps://competitor1.com\nhttps://competitor2.com';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader className="text-center pb-8">
          <div className="relative inline-block mb-6">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-2xl">
              <Sparkles className="h-10 w-10 text-white" />
            </div>
            <div className="absolute -top-2 -right-2 w-6 h-6 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center shadow-lg">
              <Zap className="h-3 w-3 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 bg-clip-text text-transparent mb-3">
            How do you want to start?
          </CardTitle>
          <CardDescription className="text-lg text-slate-600 max-w-2xl mx-auto">
            Choose your analysis approach and enter your data to unlock powerful insights
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Analysis Type Selection */}
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Target className="h-5 w-5 text-slate-600" />
            <CardTitle className="text-lg">Analysis Type</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card 
              className={cn(
                "cursor-pointer transition-all duration-300 hover:shadow-lg hover:-translate-y-1",
                analysisType === 'keywords' 
                  ? "border-blue-500 bg-gradient-to-br from-blue-50 to-indigo-50 shadow-lg" 
                  : "border-slate-200 bg-white hover:border-slate-300"
              )}
              onClick={() => setAnalysisType('keywords')}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={cn(
                    "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300",
                    analysisType === 'keywords' 
                      ? "bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-lg" 
                      : "bg-slate-100 text-slate-600"
                  )}>
                    <Search className="h-6 w-6" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="font-semibold text-slate-900">Seed Keywords</h3>
                      {analysisType === 'keywords' && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      )}
                    </div>
                    <p className="text-slate-600 mb-3">Analyze trends for specific keywords</p>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Keyword trend analysis</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Search volume insights</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Competition analysis</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card 
              className={cn(
                "cursor-pointer transition-all duration-300 hover:shadow-lg hover:-translate-y-1",
                analysisType === 'urls' 
                  ? "border-green-500 bg-gradient-to-br from-green-50 to-emerald-50 shadow-lg" 
                  : "border-slate-200 bg-white hover:border-slate-300"
              )}
              onClick={() => setAnalysisType('urls')}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={cn(
                    "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300",
                    analysisType === 'urls' 
                      ? "bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-lg" 
                      : "bg-slate-100 text-slate-600"
                  )}>
                    <Globe className="h-6 w-6" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="font-semibold text-slate-900">Competitor URLs</h3>
                      <Badge variant="secondary" className="text-xs">Max 3</Badge>
                      {analysisType === 'urls' && (
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      )}
                    </div>
                    <p className="text-slate-600 mb-3">Analyze competitor websites</p>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Competitor keyword discovery</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Market positioning analysis</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-slate-500">
                        <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
                        <span>Gap identification</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Input Data */}
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader>
          <div className="flex items-center space-x-2">
            {analysisType === 'keywords' ? (
              <Search className="h-5 w-5 text-blue-600" />
            ) : (
              <Globe className="h-5 w-5 text-green-600" />
            )}
            <CardTitle className="text-lg">
              {analysisType === 'keywords' ? 'Keywords' : 'Competitor URLs'}
            </CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative">
            <Textarea
              value={inputData}
              onChange={(e) => setInputData(e.target.value)}
              placeholder={getPlaceholder()}
              rows={5}
              className="w-full resize-none"
              disabled={isRunning}
            />
            <div className="absolute top-4 right-4 text-xs text-slate-400">
              {inputData.split('\n').filter(item => item.trim()).length} items
            </div>
          </div>
          <div className="text-sm text-slate-500 flex items-center space-x-2">
            <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
            <span>
              {analysisType === 'keywords' 
                ? 'Enter each keyword on a separate line'
                : 'Enter full URLs including https:// (maximum 3)'
              }
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Location Input */}
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <MapPin className="h-5 w-5 text-slate-600" />
            <CardTitle className="text-lg">Location (Optional)</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="B2B leaves blank, Local fills in"
            disabled={isRunning}
          />
          <div className="text-sm text-slate-500 flex items-center space-x-2">
            <div className="w-1 h-1 bg-slate-400 rounded-full"></div>
            <span>Leave blank for B2B analysis, or enter location for local business analysis</span>
          </div>
        </CardContent>
      </Card>

      {/* Error Messages */}
      {errors.length > 0 && (
        <Card className="border-red-200 bg-red-50/80">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <AlertCircle className="h-4 w-4 text-red-600" />
              </div>
              <CardTitle className="text-red-800">Please fix the following errors:</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {errors.map((error, index) => (
                <li key={index} className="flex items-center space-x-2 text-red-700">
                  <div className="w-1.5 h-1.5 bg-red-500 rounded-full"></div>
                  <span>{error}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Action Button */}
      <div className="flex justify-center pt-4">
        <Button
          onClick={handleStartAnalysis}
          disabled={isRunning || !inputData.trim()}
          size="lg"
          className="px-12 py-6 text-lg font-semibold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
        >
          {isRunning ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
              <span>Starting Analysis...</span>
            </>
          ) : (
            <>
              <Play className="h-5 w-5 mr-3" />
              <span>Start Three-Phase Analysis</span>
            </>
          )}
        </Button>
      </div>

      {/* Analysis Overview */}
      <Card className="bg-gradient-to-br from-slate-50 to-blue-50/50 border-slate-200/60">
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-slate-600 to-slate-700 rounded-xl flex items-center justify-center">
              <TrendingUp className="h-5 w-5 text-white" />
            </div>
            <CardTitle className="text-xl">Three-Phase Analysis Engine</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-white/60 backdrop-blur-sm border-white/40">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-white">1</span>
                  </div>
                  <h4 className="font-semibold text-slate-900">Paid Advertising</h4>
                </div>
                <div className="text-sm text-slate-600 mb-3">
                  {analysisType === 'keywords' 
                    ? 'Analyze ads showing for your seed keywords'
                    : 'Analyze ads showing for competitor websites'
                  }
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-blue-400 rounded-full"></div>
                    <span>Ad strength assessment</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-blue-400 rounded-full"></div>
                    <span>Messaging analysis</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-blue-400 rounded-full"></div>
                    <span>Positioning gaps</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/60 backdrop-blur-sm border-white/40">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-white">2</span>
                  </div>
                  <h4 className="font-semibold text-slate-900">Trend Discovery</h4>
                </div>
                <div className="text-sm text-slate-600 mb-3">
                  Take keywords → Google Trends API → Find look-alike trending keywords
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-green-400 rounded-full"></div>
                    <span>Expanded keyword universe</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-green-400 rounded-full"></div>
                    <span>Momentum data</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-green-400 rounded-full"></div>
                    <span>Geographic patterns</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white/60 backdrop-blur-sm border-white/40">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-violet-600 rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-white">3</span>
                  </div>
                  <h4 className="font-semibold text-slate-900">Competitive Analysis</h4>
                </div>
                <div className="text-sm text-slate-600 mb-3">
                  Cross-reference look-alike keywords against competitor performance
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-purple-400 rounded-full"></div>
                    <span>Opportunity matrix</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-purple-400 rounded-full"></div>
                    <span>Paid & organic insights</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-slate-500">
                    <div className="w-1 h-1 bg-purple-400 rounded-full"></div>
                    <span>Gap identification</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 