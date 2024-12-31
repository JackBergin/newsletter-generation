"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or default to system preference
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

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] bg-white dark:bg-gray-900 transition-colors duration-200">
      <main className="flex flex-col gap-8 row-start-2 items-center text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Crypto Market Intelligence Hub
        </h1>

        <div className="flex gap-4 items-center flex-col sm:flex-row mb-8">
          <button
            onClick={toggleDarkMode}
            className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-gray-100 dark:hover:bg-gray-800 text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            {darkMode ? '🌞 Light Mode' : '🌙 Dark Mode'}
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-4xl">
          <a
            className="p-6 rounded-lg border border-solid border-black/[.08] dark:border-white/[.145] hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            href="/youtube"
          >
            <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
              📺 YouTube Analysis
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Daily summaries from top crypto YouTubers and market analysts.
            </p>
          </a>

          <a
            className="p-6 rounded-lg border border-solid border-black/[.08] dark:border-white/[.145] hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            href="/reddit"
          >
            <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
              💬 Reddit Insights
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Community discussions and trending topics from crypto subreddits.
            </p>
          </a>
        </div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center text-gray-600 dark:text-gray-400">
        <p>Updated daily with the latest market intelligence</p>
        <div className="flex gap-4">
          <a
            className="hover:underline hover:underline-offset-4"
            href="/about"
          >
            About
          </a>
          <a
            className="hover:underline hover:underline-offset-4"
            href="/archive"
          >
            Archive
          </a>
        </div>
      </footer>
    </div>
  );
}
