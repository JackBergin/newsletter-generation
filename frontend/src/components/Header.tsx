"use client";
import { useState, useEffect } from 'react';
import { I3Logo } from './I3Logo';


export const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header 
      className={`
        fixed top-0 left-0 right-0 z-50
        transition-all duration-200 ease-in-out
        ${isScrolled 
          ? 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm shadow-sm' 
          : 'bg-white dark:bg-gray-900'}
      `}
    >
      <div className="max-w-7xl mx-10">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-1">
            <I3Logo />
          </div>
        </div>
      </div>
    </header>
  );
};
