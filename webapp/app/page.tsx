'use client';

import { useState } from 'react';
import { 
  Play, TrendingUp, BarChart3, FileText, Settings, Download, AlertCircle, CheckCircle, 
  Target, Search, Globe, Sparkles, Zap, Lightbulb, MapPin, Users, Home as HomeIcon, Building, 
  Folder, CreditCard, DollarSign, Shield, MessageSquare, Calendar, HelpCircle, 
  Terminal, Bell, Moon, ArrowLeft, ChevronRight, PaperPlane, Plus
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

export default function HomePage() {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('setup');
  const [currentPhase, setCurrentPhase] = useState<'phase1' | 'phase2' | 'phase3' | null>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [analysisConfig, setAnalysisConfig] = useState<any>(null);
  const [activeNav, setActiveNav] = useState('dashboard');

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
        trends: [
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
          totalKeywords: data.length,
          totalLocations: location ? 1 : 8,
          successRate: 95.2,
          processingTime: '10.5 seconds',
          phasesCompleted: 3,
          opportunitiesIdentified: Math.floor(Math.random() * 20) + 10
        },
        urls: []
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

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: HomeIcon },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'organization', label: 'Organization', icon: Building },
    { id: 'projects', label: 'Projects', icon: Folder },
    { id: 'transactions', label: 'Transactions', icon: CreditCard },
    { id: 'invoices', label: 'Invoices', icon: DollarSign },
    { id: 'payments', label: 'Payments', icon: CreditCard },
    { id: 'members', label: 'Members', icon: Users },
    { id: 'permissions', label: 'Permissions', icon: Shield },
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'meetings', label: 'Meetings', icon: Calendar },
  ];

  const bottomNavItems = [
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'help', label: 'Help', icon: HelpCircle },
    { id: 'console', label: 'Console', icon: Terminal },
  ];

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar Navigation */}
      <div className="w-64 bg-muted/50 border-r border-border">
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-8">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Sparkles className="h-4 w-4 text-primary-foreground" />
            </div>
            <h1 className="text-lg font-semibold">Trends Engine</h1>
          </div>
          
          {/* Main Navigation */}
          <nav className="space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveNav(item.id)}
                  className={cn(
                    "w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                    activeNav === item.id
                      ? "bg-muted text-foreground"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
          
          {/* Bottom Navigation */}
          <div className="mt-8 pt-6 border-t border-border">
            <nav className="space-y-2">
              {bottomNavItems.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => setActiveNav(item.id)}
                    className={cn(
                      "w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                      activeNav === item.id
                        ? "bg-muted text-foreground"
                        : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex h-16 items-center px-6">
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <span className="text-sm font-medium">Home</span>
            </div>
            <div className="ml-auto flex items-center space-x-2">
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-4 w-4" />
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></div>
              </Button>
              <Button variant="ghost" size="icon">
                <Moon className="h-4 w-4" />
              </Button>
              <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center">
                <Users className="h-4 w-4" />
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold">Dashboard</h1>
          </div>

          {/* Analysis Setup */}
          {currentStep === 'setup' && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="h-5 w-5" />
                    <span>Start New Analysis</span>
                  </CardTitle>
                  <CardDescription>
                    Choose your analysis type and input data to begin the three-phase analysis process.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card className="p-4 border-2 border-dashed border-muted-foreground/25 hover:border-primary/50 transition-colors cursor-pointer">
                      <div className="text-center">
                        <Target className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                        <h3 className="font-semibold">Keyword Analysis</h3>
                        <p className="text-sm text-muted-foreground">Analyze seed keywords for trends and opportunities</p>
                      </div>
                    </Card>
                    <Card className="p-4 border-2 border-dashed border-muted-foreground/25 hover:border-primary/50 transition-colors cursor-pointer">
                      <div className="text-center">
                        <Globe className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                        <h3 className="font-semibold">URL Analysis</h3>
                        <p className="text-sm text-muted-foreground">Analyze competitor URLs for insights</p>
                      </div>
                    </Card>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium">Keywords or URLs (one per line)</label>
                      <Textarea 
                        placeholder="Enter keywords or URLs here..."
                        className="mt-1"
                        rows={4}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Location (optional)</label>
                      <Input 
                        placeholder="e.g., United States, New York"
                        className="mt-1"
                      />
                    </div>
                    <Button 
                      className="w-full"
                      onClick={() => handleStartAnalysis('keywords', ['artificial intelligence', 'machine learning'], 'United States')}
                      disabled={isRunning}
                    >
                      {isRunning ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Running Analysis...
                        </>
                      ) : (
                        <>
                          <Play className="h-4 w-4 mr-2" />
                          Start Analysis
                        </>
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Three-Phase Progress */}
          {isRunning && (
            <Card className="mb-6">
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
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span>Analysis Complete</span>
                  </CardTitle>
                  <CardDescription>
                    Your three-phase analysis has been completed successfully.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold text-primary">{results.summary.totalKeywords}</div>
                      <div className="text-sm text-muted-foreground">Keywords Analyzed</div>
                    </div>
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{results.summary.successRate}%</div>
                      <div className="text-sm text-muted-foreground">Success Rate</div>
                    </div>
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">{results.summary.opportunitiesIdentified}</div>
                      <div className="text-sm text-muted-foreground">Opportunities Found</div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="font-semibold">Top Trends</h3>
                    <div className="space-y-2">
                      {results.trends.map((trend: any, index: number) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                          <span className="font-medium">{trend.keyword}</span>
                          <Badge variant={trend.trend === 'increasing' ? 'default' : 'secondary'}>
                            {trend.trend} ({trend.value})
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
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
            <div className="flex justify-center space-x-4 mt-6">
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
        </main>
      </div>
    </div>
  );
} 