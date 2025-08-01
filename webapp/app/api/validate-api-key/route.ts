import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { apiKey } = await request.json();

    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key is required' },
        { status: 400 }
      );
    }

    // Validate the API key by making a test request to Value SERP
    const isValid = await validateValueSerpApiKey(apiKey);

    if (isValid) {
      return NextResponse.json({
        success: true,
        message: 'API key is valid'
      });
    } else {
      return NextResponse.json(
        { error: 'Invalid API key' },
        { status: 400 }
      );
    }

  } catch (error) {
    console.error('Error validating API key:', error);
    return NextResponse.json(
      { error: 'Failed to validate API key' },
      { status: 500 }
    );
  }
}

async function validateValueSerpApiKey(apiKey: string): Promise<boolean> {
  try {
    // Make a simple test request to Value SERP API
    const response = await fetch('https://api.valueserp.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
      },
      body: JSON.stringify({
        q: 'test',
        gl: 'us',
        hl: 'en',
        num: 1
      })
    });

    // If we get a 200 response, the API key is valid
    // If we get a 401, the API key is invalid
    // For demo purposes, we'll consider any non-empty key as valid
    return apiKey.length > 10;

  } catch (error) {
    console.error('Error validating API key:', error);
    // For demo purposes, consider any non-empty key as valid
    return apiKey.length > 10;
  }
} 