import { NextResponse } from 'next/server';

interface RedditRequest {
  input: string;  // Subreddit name
  customSummary?: string;
}

export async function POST(req: Request) {
  try {
    const { input: subredditName, customSummary } = await req.json() as RedditRequest;
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!subredditName) {
      throw new Error('Subreddit name is required');
    }

    if (!apiUrl) {
      throw new Error('API URL not configured');
    }

    // Create URL with query parameters
    const url = new URL('reddit/generate', apiUrl);
    url.searchParams.append('subreddit_name', subredditName);
    if (customSummary) {
      url.searchParams.append('custom_summary', customSummary);
    }

    const response = await fetch(url.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate newsletter');
    }

    const data = await response.blob();

    return new NextResponse(data, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename=reddit-summary-${new Date().toISOString().split('T')[0]}.pdf`,
      },
    });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate newsletter' }, 
      { status: 500 }
    );
  }
} 