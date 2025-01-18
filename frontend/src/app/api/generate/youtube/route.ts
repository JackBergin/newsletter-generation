import { NextResponse } from 'next/server';

interface YouTubeRequest {
  input: string;  // YouTube URL
  customSummary?: string;
}

export async function POST(req: Request) {
  try {
    const { input: videoUrl, customSummary } = await req.json() as YouTubeRequest;
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!videoUrl) {
      throw new Error('YouTube URL is required');
    }

    if (!apiUrl) {
      throw new Error('API URL not configured');
    }

    // Create URL with query parameters
    const url = new URL('youtube/generate', apiUrl);
    url.searchParams.append('video_url', videoUrl);
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
        'Content-Disposition': `attachment; filename=youtube-summary-${new Date().toISOString().split('T')[0]}.pdf`,
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