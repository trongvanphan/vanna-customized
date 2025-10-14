/**
 * React Query hooks for API calls
 * Provides type-safe mutations and queries for Vanna operations
 */

'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { askQuestion, getPlotlyFigure } from '@/lib/api-client';
import { questionKeys, plotlyKeys } from '@/lib/query-keys';
import type { AskQuestionRequest } from '@/lib/types';

/**
 * Mutation hook for asking questions
 * Handles question submission and SQL generation
 */
export function useAskQuestion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: AskQuestionRequest) => askQuestion(data),
    onSuccess: () => {
      // Invalidate question queries on success
      queryClient.invalidateQueries({ queryKey: questionKeys.all });
    },
  });
}

/**
 * Query hook for fetching Plotly figures
 * Fetches chart data by figure ID
 */
export function usePlotlyFigure(figureId: string | undefined, enabled: boolean = true) {
  return useQuery({
    queryKey: plotlyKeys.figure(figureId || ''),
    queryFn: () => {
      if (!figureId) throw new Error('Figure ID is required');
      return getPlotlyFigure(figureId);
    },
    enabled: enabled && !!figureId,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
}
