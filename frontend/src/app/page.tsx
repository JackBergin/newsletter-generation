"use client";
import { useState, useEffect } from "react";

type ContentType = 'reddit' | 'youtube';

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [contentType, setContentType] = useState<ContentType>('youtube');
  const [inputValue, setInputValue] = useState('');
  const [customSummary, setCustomSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (localStorage.theme === 'dark' || 
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      setDarkMode(true);
      document.documentElement.classList.add('dark');
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
    setIsLoading(true);

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
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-white dark:bg-gray-900 transition-colors duration-200">
      <main className="flex flex-col gap-8 row-start-2 items-center text-center">
        <h1 className="text-4xl font-bold text-gray-500 dark:text-white mb-4">
          Crypto Market Intelligence Hub
        </h1>

        <div className="flex gap-4 items-center flex-col sm:flex-row mb-8">
          <button
            onClick={toggleDarkMode}
            className="rounded-full border border-solid text-blue-500 border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-gray-200 dark:hover:bg-gray-800 text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            {darkMode ? '🌞 Light Mode' : '🌙 Dark Mode'}
          </button>
        </div>

        <div className="w-full max-w-2xl p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setContentType('youtube')}
              className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
                contentType === 'youtube'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              YouTube Video
            </button>
            <button
              onClick={() => setContentType('reddit')}
              className={`flex-1 py-2 px-4 rounded-lg transition-colors ${
                contentType === 'reddit'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              Reddit Channel
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
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

        <div className="text-sm text-gray-600 dark:text-gray-400">
          <p>Generate a detailed summary from your chosen source.</p>
          <p>Add custom summary information to enhance the newsletter.</p>
          <p>The newsletter will be downloaded as a markdown file.</p>
        </div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center text-gray-600 dark:text-gray-400">
        <p>Powered by AI for optimal summary intelligence</p>
      </footer>
    </div>
  );
}
