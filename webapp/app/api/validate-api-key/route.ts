import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const apiKey = process.env.VALUE_SERP_API_KEY;
    
    if (!apiKey) {
      return NextResponse.json(
        { 
          valid: false, 
          error: 'Value SERP API key not configured. Please set VALUE_SERP_API_KEY in your environment variables.' 
        },
        { status: 400 }
      );
    }

    // Make a test request to validate the API key
    try {
      const testResponse = await fetch('https://api.valueserp.com/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-KEY': apiKey
        },
        body: JSON.stringify({
          q: 'test',
          engine: 'google',
          num: 1
        })
      });

      if (testResponse.ok) {
        return NextResponse.json({
          valid: true,
          message: 'API key is valid and working'
        });
      } else {
        return NextResponse.json({
          valid: false,
          error: 'API key validation failed'
        }, { status: 400 });
      }
    } catch (error) {
      return NextResponse.json({
        valid: false,
        error: 'Failed to validate API key'
      }, { status: 500 });
    }

  } catch (error) {
    console.error('Error validating API key:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 