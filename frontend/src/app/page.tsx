"use client";
import { useState, useEffect, useRef } from "react";

type ContentType = 'reddit' | 'youtube';

declare global {
  interface Window {
    adsbygoogle: any;
  }
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [contentType, setContentType] = useState<ContentType>('youtube');
  const [inputValue, setInputValue] = useState('');
  const [customSummary, setCustomSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPrerollAd, setShowPrerollAd] = useState(false);
  const footerAdRef = useRef<HTMLModElement>(null);

  useEffect(() => {
    if (localStorage.theme === 'dark' || 
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      setDarkMode(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  useEffect(() => {
    // Initialize footer ad
    try {
      if (footerAdRef.current) {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    } catch (err) {
      console.error('Error loading footer ad:', err);
    }
  }, []);

  const toggleDarkMode = () => {
    if (darkMode) {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
    } else {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
    }
    setDarkMode(!darkMode);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Show pre-roll ad before generating newsletter
    setShowPrerollAd(true);
    
    // Wait for ad to be displayed
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    setIsLoading(true);
    setShowPrerollAd(false);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: contentType,
          input: inputValue,
          customSummary: customSummary,
        }),
      });

      if (!response.ok) throw new Error('Failed to generate newsletter');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `crypto-newsletter-${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error:', error);
      // You might want to add error handling UI here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_auto] items-center justify-items-center min-h-screen p-4 sm:p-8 pb-16 sm:pb-20 gap-8 sm:gap-16 font-[family-name:var(--font-geist-sans)] bg-white dark:bg-gray-900 transition-colors duration-200">
      <main className="flex flex-col gap-6 sm:gap-8 row-start-2 items-center text-center w-full max-w-2xl px-2 sm:px-0">
        <h1 className="text-2xl sm:text-4xl font-bold text-gray-500 dark:text-white mb-2 sm:mb-4">
          Media Newsletter & Summary Generator
        </h1>

        <div className="flex gap-4 items-center mb-4 sm:mb-8">
          <button
            onClick={toggleDarkMode}
            className="rounded-full border border-solid text-blue-500 border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-gray-200 dark:hover:bg-gray-800 text-sm sm:text-base h-8 sm:h-10 px-3 sm:px-4"
          >
            {darkMode ? '🌞' : '🌙'} <span className="hidden sm:inline ml-1">{darkMode ? 'Light Mode' : 'Dark Mode'}</span>
          </button>
        </div>

        <div className="w-full p-4 sm:p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div className="flex gap-2 sm:gap-4 mb-4 sm:mb-6">
            <button
              onClick={() => setContentType('youtube')}
              className={`flex-1 py-2 px-2 sm:px-4 rounded-lg transition-colors text-sm sm:text-base ${
                contentType === 'youtube'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              YouTube
            </button>
            <button
              onClick={() => setContentType('reddit')}
              className={`flex-1 py-2 px-2 sm:px-4 rounded-lg transition-colors text-sm sm:text-base ${
                contentType === 'reddit'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              Reddit
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4">
            <div>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={contentType === 'youtube' ? 'Enter YouTube URL' : 'Enter Subreddit name'}
                className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                required
              />
            </div>

            <div>
              <textarea
                value={customSummary}
                onChange={(e) => setCustomSummary(e.target.value)}
                placeholder="Enter custom summary or additional information (optional)"
                className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white min-h-[100px] resize-y"
                rows={4}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating...
                </span>
              ) : (
                'Generate Newsletter'
              )}
            </button>
          </form>
        </div>

        <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 px-4">
          <p>Generate a detailed summary from your chosen source.</p>
          <p className="mt-1">Add custom summary information to enhance the newsletter.</p>
          <p className="mt-1">The newsletter will be downloaded as a markdown file.</p>
        </div>
      </main>

      {showPrerollAd && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white p-4 rounded-lg w-full max-w-sm sm:max-w-md">
            <ins
              className="adsbygoogle"
              style={{ display: 'block', minHeight: '250px' }}
              data-ad-client="YOUR-ADSENSE-CLIENT-ID"
              data-ad-slot="YOUR-AD-SLOT-ID"
              data-ad-format="auto"
              data-full-width-responsive="true"
            />
            <p className="text-center mt-4 text-sm sm:text-base">Please wait while we prepare your newsletter...</p>
          </div>
        </div>
      )}

      <footer className="row-start-3 w-full max-w-4xl mx-auto px-4">
        <div className="mb-4 sm:mb-6">
          <ins
            className="adsbygoogle"
            style={{ display: 'block', minHeight: '100px' }}
            data-ad-client="YOUR-ADSENSE-CLIENT-ID"
            data-ad-slot="YOUR-FOOTER-AD-SLOT-ID"
            data-ad-format="auto"
            data-full-width-responsive="true"
            ref={footerAdRef}
          />
        </div>
        
        <div className="flex gap-4 sm:gap-6 flex-wrap items-center justify-center text-xs sm:text-sm text-gray-600 dark:text-gray-400">
          <p>Powered by AI for optimal summary intelligence</p>
        </div>
      </footer>
    </div>
  );
}
