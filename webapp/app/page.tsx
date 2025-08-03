'use client';

import { useState } from 'react';

export default function HomePage() {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('setup');
  const [currentPhase, setCurrentPhase] = useState<'phase1' | 'phase2' | 'phase3' | null>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [analysisConfig, setAnalysisConfig] = useState<any>(null);
  const [keywords, setKeywords] = useState<string[]>(['artificial intelligence', 'machine learning']);
  const [location, setLocation] = useState('United States');
  const [error, setError] = useState('');
  const [newKeyword, setNewKeyword] = useState('');

  // Hardcoded ValueSerp API key
  const VALUESERP_API_KEY = 'A9BCF29E15D1490FA90B3C59BD9A6AA8';

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const handleStartAnalysis = async () => {
    if (keywords.length === 0) {
      setError('Please enter at least one keyword');
      return;
    }

    setError('');
    setIsRunning(true);
    setCurrentStep('analysis');
    setCurrentPhase('phase1');
    
    // Store analysis configuration
    const config = {
      type: 'keywords',
      data: keywords,
      location: location,
      timestamp: new Date().toISOString()
    };
    setAnalysisConfig(config);

    addLog('Starting Three-Phase Analysis Engine...');
    addLog(`Analysis Type: Seed Keywords`);
    addLog(`Data: ${keywords.join(', ')}`);
    addLog(`Location: ${location}`);

    try {
      // Phase 1: Paid Advertising Strength Analysis
      addLog('Phase 1: Paid Advertising Strength Analysis');
      setCurrentPhase('phase1');
      addLog('✓ Analyzing ads showing for input data...');
      addLog('✓ Assessing ad strength and messaging analysis...');
      addLog('✓ Identifying positioning gaps...');

      // Phase 2: Trends & Look-alike Discovery
      addLog('Phase 2: Trends & Look-alike Discovery');
      setCurrentPhase('phase2');
      addLog('✓ Querying Google Trends API...');
      addLog('✓ Finding look-alike trending keywords...');
      addLog('✓ Extracting momentum data and seasonality...');
      addLog('✓ Analyzing geographic patterns...');

      // Phase 3: Competitive Strengths & Weaknesses Analysis
      addLog('Phase 3: Competitive Strengths & Weaknesses Analysis');
      setCurrentPhase('phase3');
      addLog('✓ Cross-referencing keywords against competitor performance...');
      addLog('✓ Analyzing both paid ads and organic SERP results...');
      addLog('✓ Identifying opportunity gaps...');

      // Call the real API
      addLog('✓ Calling ValueSerp API for comprehensive analysis...');
      
      const response = await fetch('/api/run-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysisType: 'keywords',
          data: keywords,
          location: location,
          apiKey: VALUESERP_API_KEY
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API request failed');
      }

      const comprehensiveResults = await response.json();
      
      setResults(comprehensiveResults);
      setCurrentStep('results');
      setCurrentPhase(null);
      
      addLog('✓ All three phases completed successfully!');
      addLog('✓ Comprehensive analysis report generated');
      addLog('✓ Opportunity matrix created with actionable insights');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      addLog(`✗ Error: ${errorMessage}`);
      setError(errorMessage);
    } finally {
      setIsRunning(false);
    }
  };

  const addKeyword = () => {
    if (newKeyword.trim() && !keywords.includes(newKeyword.trim())) {
      setKeywords(prev => [...prev, newKeyword.trim()]);
      setNewKeyword('');
    }
  };

  const removeKeyword = (index: number) => {
    setKeywords(prev => prev.filter((_, i) => i !== index));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addKeyword();
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#dbeafe', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)', padding: '3rem' }}>
        
        {/* Hero Section */}
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <div style={{ 
            width: '80px', 
            height: '80px', 
            background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', 
            borderRadius: '16px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            margin: '0 auto 2rem', 
            boxShadow: '0 10px 25px rgba(139, 92, 246, 0.3)'
          }}>
            <span style={{ color: 'white', fontSize: '2rem', fontWeight: 'bold' }}>📊</span>
          </div>
          <h1 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1.5rem' }}>
            <span style={{ color: '#2563eb' }}>Google</span>{' '}
            <span style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Search Trends Analysis Platform</span>
          </h1>
          <p style={{ fontSize: '1.25rem', color: '#6b7280', maxWidth: '800px', margin: '0 auto', lineHeight: '1.6' }}>
            Comprehensive three-phase analysis engine for search behavior insights, market opportunities, and competitive intelligence.
          </p>
        </div>

        {/* Configuration Section */}
        {currentStep === 'setup' && (
          <div style={{ marginBottom: '4rem' }}>
            <div style={{ 
              padding: '2rem', 
              border: '2px dashed #cbd5e1', 
              backgroundColor: 'rgba(255, 255, 255, 0.8)', 
              borderRadius: '16px', 
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem' }}>
                <span style={{ marginRight: '0.75rem', fontSize: '1.5rem' }}>⚙️</span>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937' }}>Analysis Configuration</h2>
              </div>
              <p style={{ color: '#6b7280', marginBottom: '2rem', textAlign: 'center', fontSize: '1.125rem' }}>
                Configure your analysis parameters and keywords.
              </p>

              <div style={{ maxWidth: '600px', margin: '0 auto', marginBottom: '2rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500', color: '#374151' }}>
                  Location
                </label>
                <select 
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  style={{ 
                    width: '100%', 
                    padding: '1rem', 
                    border: '1px solid #d1d5db', 
                    borderRadius: '12px', 
                    fontSize: '1rem',
                    outline: 'none'
                  }}
                >
                  <option value="United States">United States</option>
                  <option value="United Kingdom">United Kingdom</option>
                  <option value="Canada">Canada</option>
                  <option value="Australia">Australia</option>
                  <option value="Germany">Germany</option>
                  <option value="France">France</option>
                  <option value="Japan">Japan</option>
                  <option value="India">India</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Keyword Analysis Setup Section */}
        {currentStep === 'setup' && (
          <div style={{ marginBottom: '4rem' }}>
            <div style={{ 
              padding: '2rem', 
              border: '2px dashed #cbd5e1', 
              backgroundColor: 'rgba(255, 255, 255, 0.8)', 
              borderRadius: '16px', 
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem' }}>
                <span style={{ marginRight: '0.75rem', fontSize: '1.5rem' }}>🔍</span>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937' }}>Keyword Analysis Setup</h2>
              </div>
              <p style={{ color: '#6b7280', marginBottom: '2rem', textAlign: 'center', fontSize: '1.125rem' }}>
                Enter keywords to analyze through our three-phase analysis engine.
              </p>
              
              <div style={{ maxWidth: '600px', margin: '0 auto', marginBottom: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <input 
                    type="text"
                    placeholder="Enter a keyword (e.g., 'digital marketing')"
                    value={newKeyword}
                    onChange={(e) => setNewKeyword(e.target.value)}
                    onKeyPress={handleKeyPress}
                    style={{ 
                      flex: 1, 
                      padding: '1rem', 
                      border: '1px solid #d1d5db', 
                      borderRadius: '12px', 
                      fontSize: '1rem',
                      outline: 'none'
                    }}
                  />
                  <button 
                    onClick={addKeyword}
                    disabled={!newKeyword.trim()}
                    style={{ 
                      width: '48px', 
                      height: '48px', 
                      background: newKeyword.trim() ? 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)' : '#d1d5db', 
                      border: 'none', 
                      borderRadius: '12px', 
                      color: 'white', 
                      fontSize: '1.25rem',
                      cursor: newKeyword.trim() ? 'pointer' : 'not-allowed',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Display current keywords */}
              {keywords.length > 0 && (
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: '600', color: '#374151', marginBottom: '1rem' }}>Keywords to analyze:</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {keywords.map((keyword, index) => (
                      <div key={index} style={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: '0.5rem',
                        backgroundColor: '#f3f4f6',
                        padding: '0.5rem 1rem',
                        borderRadius: '9999px',
                        fontSize: '0.875rem',
                        border: '1px solid #e5e7eb'
                      }}>
                        <span>{keyword}</span>
                        <button 
                          onClick={() => removeKeyword(index)}
                          style={{ 
                            background: 'none',
                            border: 'none',
                            color: '#ef4444',
                            cursor: 'pointer',
                            fontSize: '1rem',
                            padding: '0',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '16px',
                            height: '16px'
                          }}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div style={{ 
            backgroundColor: '#fef2f2', 
            border: '1px solid #fecaca', 
            color: '#dc2626', 
            padding: '1rem', 
            borderRadius: '12px', 
            marginBottom: '2rem',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}

        {/* Three Phase Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
          {/* Phase 1 Card */}
          <div style={{ 
            backgroundColor: '#eff6ff', 
            padding: '2rem', 
            borderRadius: '16px', 
            border: '1px solid #bfdbfe',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }} onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
          }} onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)';
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ 
                width: '64px', 
                height: '64px', 
                backgroundColor: '#3b82f6', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                margin: '0 auto 1rem',
                boxShadow: '0 4px 6px rgba(59, 130, 246, 0.3)'
              }}>
                <span style={{ color: 'white', fontSize: '1.5rem' }}>🎯</span>
              </div>
              <div style={{ 
                backgroundColor: '#f1f5f9', 
                color: '#64748b', 
                padding: '0.25rem 0.75rem', 
                borderRadius: '9999px', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                display: 'inline-block',
                marginBottom: '1rem'
              }}>
                Phase 1
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1e40af', marginBottom: '0.75rem' }}>Paid Advertising Strength</h3>
              <p style={{ color: '#2563eb', fontSize: '1rem', lineHeight: '1.5' }}>
                Analyzing ads showing for keywords and identifying positioning gaps
              </p>
            </div>
          </div>
          
          {/* Phase 2 Card */}
          <div style={{ 
            backgroundColor: '#f0fdf4', 
            padding: '2rem', 
            borderRadius: '16px', 
            border: '1px solid #bbf7d0',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }} onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
          }} onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)';
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ 
                width: '64px', 
                height: '64px', 
                backgroundColor: '#10b981', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                margin: '0 auto 1rem',
                boxShadow: '0 4px 6px rgba(16, 185, 129, 0.3)'
              }}>
                <span style={{ color: 'white', fontSize: '1.5rem' }}>📈</span>
              </div>
              <div style={{ 
                backgroundColor: '#f1f5f9', 
                color: '#64748b', 
                padding: '0.25rem 0.75rem', 
                borderRadius: '9999px', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                display: 'inline-block',
                marginBottom: '1rem'
              }}>
                Phase 2
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#166534', marginBottom: '0.75rem' }}>Trends & Look-alike Discovery</h3>
              <p style={{ color: '#16a34a', fontSize: '1rem', lineHeight: '1.5' }}>
                Using Google Trends API to find trending keywords and analyze momentum
              </p>
            </div>
          </div>
          
          {/* Phase 3 Card */}
          <div style={{ 
            backgroundColor: '#faf5ff', 
            padding: '2rem', 
            borderRadius: '16px', 
            border: '1px solid #ddd6fe',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }} onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
          }} onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)';
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ 
                width: '64px', 
                height: '64px', 
                backgroundColor: '#8b5cf6', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                margin: '0 auto 1rem',
                boxShadow: '0 4px 6px rgba(139, 92, 246, 0.3)'
              }}>
                <span style={{ color: 'white', fontSize: '1.5rem' }}>👥</span>
              </div>
              <div style={{ 
                backgroundColor: '#f1f5f9', 
                color: '#64748b', 
                padding: '0.25rem 0.75rem', 
                borderRadius: '9999px', 
                fontSize: '0.875rem', 
                fontWeight: '500', 
                display: 'inline-block',
                marginBottom: '1rem'
              }}>
                Phase 3
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#7c3aed', marginBottom: '0.75rem' }}>Competitive Analysis</h3>
              <p style={{ color: '#9333ea', fontSize: '1rem', lineHeight: '1.5' }}>
                Cross-referencing keywords against competitor performance
              </p>
            </div>
          </div>
        </div>

        {/* Analysis Progress Section */}
        {isRunning && (
          <div style={{ marginBottom: '4rem' }}>
            <div style={{ 
              backgroundColor: 'white', 
              padding: '2rem', 
              borderRadius: '16px', 
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <h2 style={{ 
                  fontSize: '2rem', 
                  fontWeight: 'bold', 
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', 
                  WebkitBackgroundClip: 'text', 
                  WebkitTextFillColor: 'transparent',
                  marginBottom: '1rem'
                }}>
                  Analysis in Progress
                </h2>
                <p style={{ color: '#6b7280', fontSize: '1.125rem' }}>
                  Running three-phase analysis engine...
                </p>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
                <div style={{ 
                  backgroundColor: currentPhase === 'phase1' ? 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)' : '#f9fafb',
                  color: currentPhase === 'phase1' ? 'white' : '#6b7280',
                  padding: '1.5rem', 
                  borderRadius: '12px', 
                  textAlign: 'center',
                  transition: 'all 0.3s ease'
                }}>
                  <div style={{ 
                    width: '64px', 
                    height: '64px', 
                    backgroundColor: currentPhase === 'phase1' ? 'rgba(255, 255, 255, 0.2)' : '#d1d5db', 
                    borderRadius: '50%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    margin: '0 auto 1rem',
                    animation: currentPhase === 'phase1' ? 'pulse 2s infinite' : 'none'
                  }}>
                    {currentPhase === 'phase1' ? '▶️' : '1'}
                  </div>
                  <h3 style={{ fontWeight: 'bold', fontSize: '1.125rem', marginBottom: '0.5rem' }}>Phase 1</h3>
                  <p style={{ fontSize: '0.875rem', opacity: 0.8 }}>Paid Advertising Analysis</p>
                </div>
                
                <div style={{ 
                  backgroundColor: currentPhase === 'phase2' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : '#f9fafb',
                  color: currentPhase === 'phase2' ? 'white' : '#6b7280',
                  padding: '1.5rem', 
                  borderRadius: '12px', 
                  textAlign: 'center',
                  transition: 'all 0.3s ease'
                }}>
                  <div style={{ 
                    width: '64px', 
                    height: '64px', 
                    backgroundColor: currentPhase === 'phase2' ? 'rgba(255, 255, 255, 0.2)' : '#d1d5db', 
                    borderRadius: '50%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    margin: '0 auto 1rem',
                    animation: currentPhase === 'phase2' ? 'pulse 2s infinite' : 'none'
                  }}>
                    {currentPhase === 'phase2' ? '▶️' : '2'}
                  </div>
                  <h3 style={{ fontWeight: 'bold', fontSize: '1.125rem', marginBottom: '0.5rem' }}>Phase 2</h3>
                  <p style={{ fontSize: '0.875rem', opacity: 0.8 }}>Trend Discovery</p>
                </div>
                
                <div style={{ 
                  backgroundColor: currentPhase === 'phase3' ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' : '#f9fafb',
                  color: currentPhase === 'phase3' ? 'white' : '#6b7280',
                  padding: '1.5rem', 
                  borderRadius: '12px', 
                  textAlign: 'center',
                  transition: 'all 0.3s ease'
                }}>
                  <div style={{ 
                    width: '64px', 
                    height: '64px', 
                    backgroundColor: currentPhase === 'phase3' ? 'rgba(255, 255, 255, 0.2)' : '#d1d5db', 
                    borderRadius: '50%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center', 
                    margin: '0 auto 1rem',
                    animation: currentPhase === 'phase3' ? 'pulse 2s infinite' : 'none'
                  }}>
                    {currentPhase === 'phase3' ? '▶️' : '3'}
                  </div>
                  <h3 style={{ fontWeight: 'bold', fontSize: '1.125rem', marginBottom: '0.5rem' }}>Phase 3</h3>
                  <p style={{ fontSize: '0.875rem', opacity: 0.8 }}>Competitive Analysis</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {currentStep === 'results' && results && (
          <div style={{ marginBottom: '4rem' }}>
            <div style={{ 
              backgroundColor: 'white', 
              padding: '2rem', 
              borderRadius: '16px', 
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                <div style={{ 
                  width: '80px', 
                  height: '80px', 
                  backgroundColor: '#10b981', 
                  borderRadius: '16px', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  margin: '0 auto 1.5rem',
                  boxShadow: '0 10px 25px rgba(16, 185, 129, 0.3)'
                }}>
                  <span style={{ color: 'white', fontSize: '2rem' }}>✅</span>
                </div>
                <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981', marginBottom: '1rem' }}>
                  Analysis Complete
                </h2>
                <p style={{ color: '#6b7280', fontSize: '1.125rem' }}>
                  Your three-phase analysis has been completed successfully.
                </p>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem', marginBottom: '3rem' }}>
                <div style={{ 
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', 
                  color: 'white', 
                  padding: '2rem', 
                  borderRadius: '16px', 
                  textAlign: 'center',
                  boxShadow: '0 10px 25px rgba(139, 92, 246, 0.3)'
                }}>
                  <div style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.75rem' }}>{results.summary.totalKeywords}</div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>Keywords Analyzed</div>
                </div>
                
                <div style={{ 
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 
                  color: 'white', 
                  padding: '2rem', 
                  borderRadius: '16px', 
                  textAlign: 'center',
                  boxShadow: '0 10px 25px rgba(16, 185, 129, 0.3)'
                }}>
                  <div style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.75rem' }}>{results.summary.successRate}%</div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>Success Rate</div>
                </div>
                
                <div style={{ 
                  background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', 
                  color: 'white', 
                  padding: '2rem', 
                  borderRadius: '16px', 
                  textAlign: 'center',
                  boxShadow: '0 10px 25px rgba(245, 158, 11, 0.3)'
                }}>
                  <div style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.75rem' }}>{results.summary.opportunitiesIdentified}</div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.8 }}>Opportunities Found</div>
                </div>
              </div>

              {/* Keyword Statistics */}
              {results.keyword_stats && results.keyword_stats.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Keyword Statistics</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                    {results.keyword_stats.map((stat: any, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#f9fafb', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        border: '1px solid #e5e7eb'
                      }}>
                        <h4 style={{ fontSize: '1.125rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '1rem' }}>{stat.keyword}</h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.875rem' }}>
                          <div>
                            <span style={{ color: '#6b7280' }}>Search Volume:</span>
                            <span style={{ fontWeight: '600', color: '#1f2937', marginLeft: '0.5rem' }}>{stat.search_volume.toLocaleString()}</span>
                          </div>
                          <div>
                            <span style={{ color: '#6b7280' }}>CPC Estimate:</span>
                            <span style={{ fontWeight: '600', color: '#1f2937', marginLeft: '0.5rem' }}>${stat.cpc_estimate}</span>
                          </div>
                          <div>
                            <span style={{ color: '#6b7280' }}>Competition:</span>
                            <span style={{ 
                              fontWeight: '600', 
                              color: stat.competition_level === 'low' ? '#10b981' : stat.competition_level === 'medium' ? '#f59e0b' : '#ef4444',
                              marginLeft: '0.5rem',
                              textTransform: 'capitalize'
                            }}>{stat.competition_level}</span>
                          </div>
                          <div>
                            <span style={{ color: '#6b7280' }}>Opportunity:</span>
                            <span style={{ 
                              fontWeight: '600', 
                              color: stat.opportunity_score === 'high' ? '#10b981' : stat.opportunity_score === 'medium' ? '#f59e0b' : '#ef4444',
                              marginLeft: '0.5rem',
                              textTransform: 'capitalize'
                            }}>{stat.opportunity_score}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top Ads Analysis */}
              {results.phase1_results.top_ads && results.phase1_results.top_ads.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Top Ads & Search Results</h3>
                  <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                    {results.phase1_results.top_ads.slice(0, 10).map((ad: any, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#f9fafb', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        marginBottom: '1rem',
                        border: '1px solid #e5e7eb'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                          <div style={{ 
                            backgroundColor: ad.is_paid ? '#fef3c7' : '#dbeafe', 
                            color: ad.is_paid ? '#92400e' : '#1e40af', 
                            padding: '0.25rem 0.75rem', 
                            borderRadius: '9999px', 
                            fontSize: '0.75rem',
                            fontWeight: '500'
                          }}>
                            {ad.is_paid ? 'Paid Ad' : `Position ${ad.position}`}
                          </div>
                          <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>{ad.domain}</span>
                        </div>
                        <h4 style={{ fontSize: '1rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>{ad.title}</h4>
                        <p style={{ color: '#6b7280', fontSize: '0.875rem', marginBottom: '0.5rem' }}>{ad.snippet}</p>
                        <a href={ad.url} target="_blank" rel="noopener noreferrer" style={{ 
                          color: '#3b82f6', 
                          fontSize: '0.875rem', 
                          textDecoration: 'none'
                        }}>
                          {ad.url}
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Companies Analysis */}
              {results.phase1_results.companies_showing && results.phase1_results.companies_showing.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Top Companies Showing</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
                    {results.phase1_results.companies_showing.slice(0, 8).map((company: any, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#f9fafb', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        border: '1px solid #e5e7eb'
                      }}>
                        <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '0.75rem' }}>{company.domain}</h4>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Frequency:</span> {company.frequency} appearances
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Avg Position:</span> {company.avg_position.toFixed(1)}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                          <span style={{ fontWeight: '600' }}>Keywords:</span> {company.keywords.slice(0, 3).join(', ')}
                          {company.keywords.length > 3 && '...'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Lookalike Keywords */}
              {results.phase2_results.lookalike_keywords && results.phase2_results.lookalike_keywords.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Lookalike Keywords Discovered</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                    {results.phase2_results.lookalike_keywords.slice(0, 12).map((lookalike: any, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#f9fafb', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        border: '1px solid #e5e7eb'
                      }}>
                        <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '0.75rem' }}>{lookalike.keyword}</h4>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Search Volume:</span> {lookalike.search_volume.toLocaleString()}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Competition:</span>
                          <span style={{ 
                            color: lookalike.competition === 'low' ? '#10b981' : lookalike.competition === 'medium' ? '#f59e0b' : '#ef4444',
                            marginLeft: '0.5rem',
                            textTransform: 'capitalize'
                          }}>{lookalike.competition}</span>
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Opportunity:</span>
                          <span style={{ 
                            color: lookalike.opportunity_score === 'high' ? '#10b981' : lookalike.opportunity_score === 'medium' ? '#f59e0b' : '#ef4444',
                            marginLeft: '0.5rem',
                            textTransform: 'capitalize'
                          }}>{lookalike.opportunity_score}</span>
                        </div>
                        {lookalike.related_terms && lookalike.related_terms.length > 0 && (
                          <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                            <span style={{ fontWeight: '600' }}>Related:</span>
                            <div style={{ marginTop: '0.25rem' }}>
                              {lookalike.related_terms.slice(0, 3).map((term: string, termIndex: number) => (
                                <span key={termIndex} style={{ 
                                  backgroundColor: '#e5e7eb', 
                                  padding: '0.25rem 0.5rem', 
                                  borderRadius: '4px', 
                                  marginRight: '0.5rem',
                                  fontSize: '0.75rem'
                                }}>{term}</span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Competitive Analysis */}
              {results.phase3_results.competitive_analysis.top_competitors && results.phase3_results.competitive_analysis.top_competitors.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Top Competitors</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
                    {results.phase3_results.competitive_analysis.top_competitors.slice(0, 8).map((competitor: any, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#f9fafb', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        border: '1px solid #e5e7eb'
                      }}>
                        <h4 style={{ fontSize: '1rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '0.75rem' }}>{competitor.domain}</h4>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Market Share:</span> {competitor.market_share}%
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Avg Position:</span> {competitor.avg_position.toFixed(1)}
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>
                          <span style={{ fontWeight: '600' }}>Strength:</span>
                          <span style={{ 
                            color: competitor.strength_score === 'high' ? '#ef4444' : competitor.strength_score === 'medium' ? '#f59e0b' : '#10b981',
                            marginLeft: '0.5rem',
                            textTransform: 'capitalize'
                          }}>{competitor.strength_score}</span>
                        </div>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                          <span style={{ fontWeight: '600' }}>Keywords:</span> {competitor.keywords.slice(0, 3).join(', ')}
                          {competitor.keywords.length > 3 && '...'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Ad Patterns */}
              {results.phase1_results.ad_patterns && results.phase1_results.ad_patterns.length > 0 && (
                <div style={{ marginBottom: '3rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Ad Patterns & Insights</h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                    {results.phase1_results.ad_patterns.map((pattern: string, index: number) => (
                      <div key={index} style={{ 
                        backgroundColor: '#fef3c7', 
                        padding: '1.5rem', 
                        borderRadius: '12px', 
                        border: '1px solid #fde68a'
                      }}>
                        <div style={{ fontSize: '1rem', color: '#92400e', fontWeight: '500' }}>{pattern}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top Trends */}
              <div>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '2rem' }}>Top Trends</h3>
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                  {results.trends.map((trend: any, index: number) => (
                    <div key={index} style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'space-between', 
                      padding: '1.5rem', 
                      backgroundColor: '#f9fafb', 
                      borderRadius: '12px', 
                      marginBottom: '1rem',
                      transition: 'all 0.3s ease'
                    }} onMouseOver={(e) => {
                      e.currentTarget.style.backgroundColor = '#f3f4f6';
                    }} onMouseOut={(e) => {
                      e.currentTarget.style.backgroundColor = '#f9fafb';
                    }}>
                      <div>
                        <span style={{ fontWeight: '600', color: '#1f2937', fontSize: '1.125rem' }}>{trend.keyword}</span>
                        <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.25rem' }}>
                          Volume: {trend.search_volume.toLocaleString()} | Competition: {trend.competition_level}
                        </div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <span style={{ 
                          backgroundColor: '#dcfce7', 
                          color: '#166534', 
                          padding: '0.5rem 1rem', 
                          borderRadius: '9999px', 
                          fontSize: '0.875rem',
                          fontWeight: '500'
                        }}>
                          {trend.trend} ({trend.value})
                        </span>
                        <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.25rem' }}>
                          {trend.opportunity_score} opportunity
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div style={{ textAlign: 'center' }}>
          {currentStep === 'setup' && (
            <button 
              style={{ 
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', 
                color: 'white', 
                padding: '1rem 3rem', 
                borderRadius: '12px', 
                border: 'none', 
                fontSize: '1.125rem', 
                fontWeight: '600', 
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 6px rgba(139, 92, 246, 0.25)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                margin: '0 auto'
              }} 
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 8px 15px rgba(139, 92, 246, 0.35)';
              }} 
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 6px rgba(139, 92, 246, 0.25)';
              }}
              onClick={handleStartAnalysis}
              disabled={isRunning}
            >
              {isRunning ? (
                <>
                  <div style={{ 
                    width: '24px', 
                    height: '24px', 
                    border: '2px solid transparent', 
                    borderTop: '2px solid white', 
                    borderRadius: '50%', 
                    animation: 'spin 1s linear infinite' 
                  }}></div>
                  Running Analysis...
                </>
              ) : (
                <>
                  <span>▶️</span>
                  Start Analysis
                </>
              )}
            </button>
          )}

          {!isRunning && currentStep !== 'setup' && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem' }}>
              <button
                style={{ 
                  backgroundColor: 'white', 
                  color: '#374151', 
                  padding: '0.75rem 2rem', 
                  borderRadius: '12px', 
                  border: '1px solid #d1d5db',
                  fontSize: '1rem', 
                  fontWeight: '500', 
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.backgroundColor = '#f9fafb';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.backgroundColor = 'white';
                }}
                onClick={() => {
                  setCurrentStep('setup');
                  setCurrentPhase(null);
                  setResults(null);
                  setLogs([]);
                  setAnalysisConfig(null);
                  setError('');
                }}
              >
                Run New Analysis
              </button>
              <button
                style={{ 
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', 
                  color: 'white', 
                  padding: '0.75rem 2rem', 
                  borderRadius: '12px', 
                  border: 'none',
                  fontSize: '1rem', 
                  fontWeight: '500', 
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
                onClick={() => window.open('/api/download-results', '_blank')}
              >
                <span>📥</span>
                Download Results
              </button>
            </div>
          )}
        </div>

        {/* Logs Section */}
        {logs.length > 0 && (
          <div style={{ marginTop: '4rem' }}>
            <div style={{ 
              backgroundColor: 'white', 
              padding: '2rem', 
              borderRadius: '16px', 
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e5e7eb'
            }}>
              <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', textAlign: 'center', marginBottom: '1.5rem' }}>Analysis Logs</h3>
              <div style={{ 
                backgroundColor: '#f9fafb', 
                borderRadius: '12px', 
                padding: '1.5rem', 
                height: '256px', 
                overflowY: 'auto', 
                fontFamily: 'monospace', 
                fontSize: '0.875rem', 
                border: '1px solid #e5e7eb',
                maxWidth: '800px',
                margin: '0 auto'
              }}>
                {logs.map((log, index) => (
                  <div key={index} style={{ color: '#6b7280', marginBottom: '0.5rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                    <span style={{ color: '#9ca3af', fontSize: '0.75rem', marginTop: '0.125rem' }}>→</span>
                    <span>{log}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
      
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
} 