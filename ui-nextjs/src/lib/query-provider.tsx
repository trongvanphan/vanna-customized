/**
 * React Query provider wrapper component
 * Configures QueryClient with default options
 */

'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode, useState } from 'react';

/**
 * Default query client options
 */
const queryClientOptions = {
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
      retry: 1,
    },
    mutations: {
      retry: false,
    },
  },
};

/**
 * Query provider component
 * Wraps app with React Query context
 */
export function QueryProvider({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient(queryClientOptions));

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
