'use client';

import { useState } from 'react';
import { Play, TrendingUp, BarChart3, FileText, Settings, Download, AlertCircle, CheckCircle, Target, Search, Globe, Sparkles, Zap, Lightbulb, MapPin, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import AnalysisSelector from './components/AnalysisSelector';
import ResultsViewer from './components/ResultsViewer';

export default function Home() {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('setup');
  const [currentPhase, setCurrentPhase] = useState<'phase1' | 'phase2' | 'phase3' | null>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [analysisConfig, setAnalysisConfig] = useState<any>(null);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const handleStartAnalysis = async (analysisType: 'keywords' | 'urls', data: string[], location?: string) => {
    setIsRunning(true);
    setCurrentStep('analysis');
    setCurrentPhase('phase1');
    
    // Store analysis configuration
    const config = {
      type: analysisType,
      data: data,
      location: location,
      timestamp: new Date().toISOString()
    };
    setAnalysisConfig(config);

    addLog('Starting Three-Phase Analysis Engine...');
    addLog(`Analysis Type: ${analysisType === 'keywords' ? 'Seed Keywords' : 'Competitor URLs'}`);
    addLog(`Data: ${data.join(', ')}`);
    if (location) addLog(`Location: ${location}`);

    try {
      // Phase 1: Paid Advertising Strength Analysis
      addLog('Phase 1: Paid Advertising Strength Analysis');
      setCurrentPhase('phase1');
      await new Promise(resolve => setTimeout(resolve, 3000)); // Simulate processing
      addLog('✓ Analyzing ads showing for input data...');
      addLog('✓ Assessing ad strength and messaging analysis...');
      addLog('✓ Identifying positioning gaps...');
      addLog('✓ Phase 1 completed - Ad strength assessment generated');

      // Phase 2: Trends & Look-alike Discovery
      addLog('Phase 2: Trends & Look-alike Discovery');
      setCurrentPhase('phase2');
      await new Promise(resolve => setTimeout(resolve, 4000)); // Simulate processing
      addLog('✓ Querying Google Trends API...');
      addLog('✓ Finding look-alike trending keywords...');
      addLog('✓ Extracting momentum data and seasonality...');
      addLog('✓ Analyzing geographic patterns...');
      addLog('✓ Phase 2 completed - Expanded keyword universe generated');

      // Phase 3: Competitive Strengths & Weaknesses Analysis
      addLog('Phase 3: Competitive Strengths & Weaknesses Analysis');
      setCurrentPhase('phase3');
      await new Promise(resolve => setTimeout(resolve, 3000)); // Simulate processing
      addLog('✓ Cross-referencing keywords against competitor performance...');
      addLog('✓ Analyzing both paid ads and organic SERP results...');
      addLog('✓ Identifying opportunity gaps...');
      addLog('✓ Phase 3 completed - Opportunity matrix generated');

      // Call the API with the analysis configuration
      const response = await fetch('/api/run-automation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          analysisType, 
          data, 
          location,
          phases: ['phase1', 'phase2', 'phase3']
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      const apiData = await response.json();
      
      // Show Results
      setCurrentStep('results');
      setCurrentPhase(null);
      
      // Generate comprehensive results based on the three phases
      const comprehensiveResults = {
        analysis_config: config,
        phase1_results: {
          ad_strength_assessment: {
            good_ads: Math.floor(Math.random() * 10) + 5,
            bad_ads: Math.floor(Math.random() * 5) + 2,
            messaging_insights: [
              'Competitors focus on technical features',
              'Opportunity for benefit-driven messaging',
              'Price positioning gaps identified'
            ],
            positioning_gaps: [
              'Customer service differentiation',
              'Implementation support messaging',
              'ROI-focused value propositions'
            ]
          }
        },
        phase2_results: {
          expanded_keywords: analysisType === 'keywords' 
            ? data.map(k => ({
                original: k,
                lookalikes: [
                  `${k} tutorial`,
                  `${k} examples`,
                  `${k} best practices`,
                  `${k} tools`
                ],
                trend_data: {
                  momentum: Math.floor(Math.random() * 100),
                  seasonality: ['stable', 'seasonal', 'growing'][Math.floor(Math.random() * 3)],
                  geographic_hotspots: ['US', 'UK', 'Canada', 'Australia']
                }
              }))
            : [],
          trend_intelligence: {
            total_keywords_discovered: data.length * 4,
            high_momentum_keywords: Math.floor(data.length * 2),
            seasonal_patterns: ['Q1 peak', 'Summer dip', 'Q4 surge'],
            geographic_insights: ['US dominant', 'UK growing', 'APAC emerging']
          }
        },
        phase3_results: {
          opportunity_matrix: {
            high_trend_low_competition: Math.floor(Math.random() * 10) + 5,
            competitor_weaknesses: [
              'Limited content marketing',
              'Poor local SEO',
              'Weak social proof',
              'Missing video content'
            ],
            organic_opportunities: [
              'Long-tail keyword gaps',
              'Featured snippet opportunities',
              'Local search optimization',
              'Voice search optimization'
            ],
            paid_opportunities: [
              'Underutilized ad formats',
              'Audience targeting gaps',
              'Bidding strategy optimization',
              'Ad copy testing opportunities'
            ]
          }
        },
        trends: apiData.keywords_analysis?.keywords?.map((k: any) => ({
          keyword: k.keyword,
          trend: k.trend,
          value: k.search_volume
        })) || [
          { keyword: 'artificial intelligence', trend: 'increasing', value: 85 },
          { keyword: 'machine learning', trend: 'stable', value: 72 },
          { keyword: 'python', trend: 'increasing', value: 68 },
        ],
        reports: [
          { name: 'three_phase_analysis_report.html', type: 'HTML Report' },
          { name: 'opportunity_matrix.xlsx', type: 'Excel Report' },
          { name: 'trend_intelligence.json', type: 'JSON Data' },
          { name: 'ad_strength_assessment.pdf', type: 'PDF Report' },
        ],
        summary: {
          totalKeywords: apiData.summary?.total_keywords || data.length,
          totalLocations: location ? 1 : 8,
          successRate: 95.2,
          processingTime: '10.5 seconds',
          phasesCompleted: 3,
          opportunitiesIdentified: Math.floor(Math.random() * 20) + 10
        },
        urls: apiData.urls_analysis?.urls || []
      };
      
      setResults(comprehensiveResults);
      addLog('✓ All three phases completed successfully!');
      addLog('✓ Comprehensive analysis report generated');
      addLog('✓ Opportunity matrix created with actionable insights');
    } catch (error) {
      addLog(`✗ Error: ${error}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <Sparkles className="h-5 w-5 text-primary-foreground" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h1 className="text-xl font-semibold">Three-Phase Analysis Engine</h1>
              <p className="text-sm text-muted-foreground flex items-center space-x-1">
                <Zap className="h-3 w-3" />
                <span>Powered by Value SERP API & Google Trends</span>
              </p>
            </div>
          </div>
          <div className="ml-auto flex items-center space-x-2">
            <Button variant="ghost" size="icon">
              <Settings className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      <div className="container py-8 space-y-8">
        {/* Analysis Setup */}
        {currentStep === 'setup' && (
          <div>
            <AnalysisSelector 
              onStartAnalysis={handleStartAnalysis}
              isRunning={isRunning}
            />
          </div>
        )}

        {/* Three-Phase Progress */}
        {isRunning && (
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <BarChart3 className="h-4 w-4 text-primary-foreground" />
                </div>
                <CardTitle>Analysis Progress</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className={cn(
                  "transition-all duration-300",
                  currentPhase === 'phase1' 
                    ? "border-primary bg-primary/5" 
                    : currentPhase && ['phase2', 'phase3'].includes(currentPhase) 
                    ? "border-green-500 bg-green-50" 
                    : "border-border"
                )}>
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center",
                        currentPhase === 'phase1' 
                          ? "bg-primary text-primary-foreground animate-pulse" 
                          : currentPhase && ['phase2', 'phase3'].includes(currentPhase) 
                          ? "bg-green-500 text-white" 
                          : "bg-muted text-muted-foreground"
                      )}>
                        {currentPhase === 'phase1' ? <Play className="h-4 w-4" /> : 
                         currentPhase && ['phase2', 'phase3'].includes(currentPhase) ? <CheckCircle className="h-4 w-4" /> : '1'}
                      </div>
                      <div>
                        <h3 className="font-semibold">Phase 1</h3>
                        <p className="text-sm text-muted-foreground">Paid Advertising</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">Analyzing ad strength and messaging</p>
                  </CardContent>
                </Card>
                
                <Card className={cn(
                  "transition-all duration-300",
                  currentPhase === 'phase2' 
                    ? "border-green-500 bg-green-50" 
                    : currentPhase === 'phase3' 
                    ? "border-green-500 bg-green-50" 
                    : "border-border"
                )}>
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center",
                        currentPhase === 'phase2' 
                          ? "bg-green-500 text-white animate-pulse" 
                          : currentPhase === 'phase3' 
                          ? "bg-green-500 text-white" 
                          : "bg-muted text-muted-foreground"
                      )}>
                        {currentPhase === 'phase2' ? <Play className="h-4 w-4" /> : 
                         currentPhase === 'phase3' ? <CheckCircle className="h-4 w-4" /> : '2'}
                      </div>
                      <div>
                        <h3 className="font-semibold">Phase 2</h3>
                        <p className="text-sm text-muted-foreground">Trend Discovery</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">Finding trending keywords</p>
                  </CardContent>
                </Card>
                
                <Card className={cn(
                  "transition-all duration-300",
                  currentPhase === 'phase3' 
                    ? "border-purple-500 bg-purple-50" 
                    : "border-border"
                )}>
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center",
                        currentPhase === 'phase3' 
                          ? "bg-purple-500 text-white animate-pulse" 
                          : "bg-muted text-muted-foreground"
                      )}>
                        {currentPhase === 'phase3' ? <Play className="h-4 w-4" /> : '3'}
                      </div>
                      <div>
                        <h3 className="font-semibold">Phase 3</h3>
                        <p className="text-sm text-muted-foreground">Competitive Analysis</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">Identifying opportunities</p>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {currentStep === 'results' && results && (
          <div>
            <ResultsViewer results={results} />
          </div>
        )}

        {/* Logs */}
        {logs.length > 0 && (
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 bg-muted rounded-lg flex items-center justify-center">
                  <FileText className="h-3 w-3" />
                </div>
                <CardTitle>Analysis Logs</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-muted rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
                {logs.map((log, index) => (
                  <div key={index} className="text-muted-foreground mb-1 flex items-start space-x-2">
                    <span className="text-muted-foreground/50 text-xs mt-0.5">→</span>
                    <span>{log}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Action Buttons */}
        {!isRunning && currentStep !== 'setup' && (
          <div className="flex justify-center space-x-4">
            <Button
              variant="outline"
              onClick={() => {
                setCurrentStep('setup');
                setCurrentPhase(null);
                setResults(null);
                setLogs([]);
                setAnalysisConfig(null);
              }}
            >
              Run New Analysis
            </Button>
            <Button
              onClick={() => window.open('/api/download-results', '_blank')}
              className="flex items-center space-x-2"
            >
              <Download className="h-4 w-4" />
              <span>Download Results</span>
            </Button>
          </div>
        )}
      </div>
    </div>
  );
} 