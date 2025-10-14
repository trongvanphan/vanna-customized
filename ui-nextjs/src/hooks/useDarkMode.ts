/**
 * Custom hook for dark mode management
 * Wraps next-themes with localStorage persistence
 */

'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';

export type ThemeMode = 'light' | 'dark' | 'system';

/**
 * Hook for managing dark mode state
 * Provides theme switching with localStorage persistence
 */
export function useDarkMode() {
  const { theme, setTheme, systemTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // Avoid hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  const currentTheme = theme === 'system' ? systemTheme : theme;
  const isDark = currentTheme === 'dark';

  const toggleTheme = () => {
    setTheme(isDark ? 'light' : 'dark');
  };

  const setLightTheme = () => setTheme('light');
  const setDarkTheme = () => setTheme('dark');
  const setSystemTheme = () => setTheme('system');

  return {
    theme: currentTheme as ThemeMode,
    isDark,
    isLight: !isDark,
    mounted,
    toggleTheme,
    setLightTheme,
    setDarkTheme,
    setSystemTheme,
    setTheme,
  };
}

// Re-export for convenience
export { useTheme };
