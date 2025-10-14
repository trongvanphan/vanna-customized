/**
 * React Query keys factory
 * Centralized query key management for type-safe caching
 */

/**
 * Query keys for questions and results
 */
export const questionKeys = {
  all: ['questions'] as const,
  lists: () => [...questionKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...questionKeys.lists(), filters] as const,
  details: () => [...questionKeys.all, 'detail'] as const,
  detail: (id: string) => [...questionKeys.details(), id] as const,
  ask: (question: string, sessionId?: string) =>
    [...questionKeys.all, 'ask', question, sessionId] as const,
};

/**
 * Query keys for Plotly figures
 */
export const plotlyKeys = {
  all: ['plotly'] as const,
  figure: (id: string) => [...plotlyKeys.all, 'figure', id] as const,
};

/**
 * Query keys for configurations
 */
export const configKeys = {
  all: ['config'] as const,
  get: () => [...configKeys.all, 'get'] as const,
  llm: () => [...configKeys.all, 'llm'] as const,
  database: () => [...configKeys.all, 'database'] as const,
  chromadb: () => [...configKeys.all, 'chromadb'] as const,
  flask: () => [...configKeys.all, 'flask'] as const,
  training: () => [...configKeys.all, 'training'] as const,
};

/**
 * Query keys for training data
 */
export const trainingKeys = {
  all: ['training'] as const,
  stats: () => [...trainingKeys.all, 'stats'] as const,
  items: () => [...trainingKeys.all, 'items'] as const,
  load: () => [...trainingKeys.all, 'load'] as const,
};

/**
 * Query keys for connection tests
 */
export const connectionKeys = {
  all: ['connection'] as const,
  testDatabase: (config: any) => [...connectionKeys.all, 'database', config] as const,
  testLLM: (params: any) => [...connectionKeys.all, 'llm', params] as const,
};
