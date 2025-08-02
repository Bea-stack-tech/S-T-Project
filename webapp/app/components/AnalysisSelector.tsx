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
            <div className="w-20 h-20 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
              <Sparkles className="h-10 w-10 text-primary-foreground" />
            </div>
            <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center shadow-lg">
              <Zap className="h-3 w-3 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold mb-3">
            How do you want to start?
          </CardTitle>
          <CardDescription className="text-lg max-w-2xl mx-auto">
            Choose your analysis approach and enter your data to unlock powerful insights
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Analysis Type Selection */}
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Target className="h-5 w-5 text-muted-foreground" />
            <CardTitle>Analysis Type</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card 
              className={cn(
                "cursor-pointer transition-all duration-300 hover:shadow-lg",
                analysisType === 'keywords' 
                  ? "border-primary bg-primary/5" 
                  : "border-border hover:border-border"
              )}
              onClick={() => setAnalysisType('keywords')}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={cn(
                    "w-12 h-12 rounded-lg flex items-center justify-center transition-all duration-300",
                    analysisType === 'keywords' 
                      ? "bg-primary text-primary-foreground" 
                      : "bg-muted text-muted-foreground"
                  )}>
                    <Search className="h-6 w-6" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="font-semibold">Seed Keywords</h3>
                      {analysisType === 'keywords' && (
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                      )}
                    </div>
                    <p className="text-muted-foreground mb-3">Analyze trends for specific keywords</p>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <span>Keyword trend analysis</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <span>Search volume insights</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <span>Competition analysis</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card 
              className={cn(
                "cursor-pointer transition-all duration-300 hover:shadow-lg",
                analysisType === 'urls' 
                  ? "border-green-500 bg-green-50" 
                  : "border-border hover:border-border"
              )}
              onClick={() => setAnalysisType('urls')}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={cn(
                    "w-12 h-12 rounded-lg flex items-center justify-center transition-all duration-300",
                    analysisType === 'urls' 
                      ? "bg-green-500 text-white" 
                      : "bg-muted text-muted-foreground"
                  )}>
                    <Globe className="h-6 w-6" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="font-semibold">Competitor URLs</h3>
                      <Badge variant="secondary" className="text-xs">Max 3</Badge>
                      {analysisType === 'urls' && (
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      )}
                    </div>
                    <p className="text-muted-foreground mb-3">Analyze competitor websites</p>
                    <div className="space-y-1">
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <span>Competitor keyword discovery</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <span>Market positioning analysis</span>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
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
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            {analysisType === 'keywords' ? (
              <Search className="h-5 w-5 text-primary" />
            ) : (
              <Globe className="h-5 w-5 text-green-600" />
            )}
            <CardTitle>
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
            <div className="absolute top-4 right-4 text-xs text-muted-foreground">
              {inputData.split('\n').filter(item => item.trim()).length} items
            </div>
          </div>
          <div className="text-sm text-muted-foreground flex items-center space-x-2">
            <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
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
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-2">
            <MapPin className="h-5 w-5 text-muted-foreground" />
            <CardTitle>Location (Optional)</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="B2B leaves blank, Local fills in"
            disabled={isRunning}
          />
          <div className="text-sm text-muted-foreground flex items-center space-x-2">
            <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
            <span>Leave blank for B2B analysis, or enter location for local business analysis</span>
          </div>
        </CardContent>
      </Card>

      {/* Error Messages */}
      {errors.length > 0 && (
        <Card className="border-destructive bg-destructive/5">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-destructive/10 rounded-lg flex items-center justify-center">
                <AlertCircle className="h-4 w-4 text-destructive" />
              </div>
              <CardTitle className="text-destructive">Please fix the following errors:</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {errors.map((error, index) => (
                <li key={index} className="flex items-center space-x-2 text-destructive">
                  <div className="w-1.5 h-1.5 bg-destructive rounded-full"></div>
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
          className="px-12 py-6 text-lg font-semibold"
        >
          {isRunning ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-foreground mr-3"></div>
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
      <Card className="bg-muted/50">
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-muted rounded-lg flex items-center justify-center">
              <TrendingUp className="h-5 w-5" />
            </div>
            <CardTitle>Three-Phase Analysis Engine</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-primary-foreground">1</span>
                  </div>
                  <h4 className="font-semibold">Paid Advertising</h4>
                </div>
                <div className="text-sm text-muted-foreground mb-3">
                  {analysisType === 'keywords' 
                    ? 'Analyze ads showing for your seed keywords'
                    : 'Analyze ads showing for competitor websites'
                  }
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-primary rounded-full"></div>
                    <span>Ad strength assessment</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-primary rounded-full"></div>
                    <span>Messaging analysis</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-primary rounded-full"></div>
                    <span>Positioning gaps</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-white">2</span>
                  </div>
                  <h4 className="font-semibold">Trend Discovery</h4>
                </div>
                <div className="text-sm text-muted-foreground mb-3">
                  Take keywords → Google Trends API → Find look-alike trending keywords
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-green-500 rounded-full"></div>
                    <span>Expanded keyword universe</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-green-500 rounded-full"></div>
                    <span>Momentum data</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-green-500 rounded-full"></div>
                    <span>Geographic patterns</span>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                    <span className="text-sm font-bold text-white">3</span>
                  </div>
                  <h4 className="font-semibold">Competitive Analysis</h4>
                </div>
                <div className="text-sm text-muted-foreground mb-3">
                  Cross-reference look-alike keywords against competitor performance
                </div>
                <div className="space-y-1">
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-purple-500 rounded-full"></div>
                    <span>Opportunity matrix</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-purple-500 rounded-full"></div>
                    <span>Paid & organic insights</span>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                    <div className="w-1 h-1 bg-purple-500 rounded-full"></div>
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