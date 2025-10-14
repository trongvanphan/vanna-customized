/**
 * Chart renderer component
 * Renders interactive Plotly charts from Flask backend
 */

'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';
import { usePlotlyFigure } from '@/hooks/useQuery';
import type { PlotlyFigure } from '@/lib/types';

// Dynamically import Plot to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-96">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  ),
});

interface ChartRendererProps {
  figureId?: string;
  className?: string;
}

export function ChartRenderer({ figureId, className = '' }: ChartRendererProps) {
  const { data, isLoading, error } = usePlotlyFigure(figureId, !!figureId);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  // Detect theme changes
  useEffect(() => {
    const isDark = document.documentElement.classList.contains('dark');
    setTheme(isDark ? 'dark' : 'light');

    // Watch for theme changes
    const observer = new MutationObserver(() => {
      const isDark = document.documentElement.classList.contains('dark');
      setTheme(isDark ? 'dark' : 'light');
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  if (!figureId) {
    return null;
  }

  if (isLoading) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center h-96">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center h-96">
            <p className="text-destructive">Failed to load chart</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data || !data.fig) {
    return null;
  }

  const figure: PlotlyFigure = data.fig;

  // Merge layout with dark mode settings
  const layout = {
    ...figure.layout,
    autosize: true,
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: {
      ...figure.layout.font,
      color: theme === 'dark' ? '#e5e7eb' : '#1f2937',
    },
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="w-full">
          <Plot
            data={figure.data}
            layout={layout}
            config={{
              responsive: true,
              displayModeBar: true,
              displaylogo: false,
              ...figure.config,
            }}
            style={{ width: '100%', height: '500px' }}
            useResizeHandler={true}
          />
        </div>
      </CardContent>
    </Card>
  );
}
