# Phase 1: Data Model & TypeScript Interfaces

**Feature**: Convert Flask UI to Next.js Application  
**Date**: October 13, 2025

## Overview

This document defines TypeScript interfaces and data models for the Next.js frontend, based on the Flask API contracts and business entities from the feature specification.

## Core Entities

### 1. Question & Query Result

```typescript
/**
 * User's natural language question
 */
export interface Question {
  /** Unique identifier (client-generated) */
  id: string;
  /** Natural language question text */
  text: string;
  /** Timestamp when question was asked */
  timestamp: Date;
  /** Session ID for conversation context */
  sessionId?: string;
}

/**
 * SQL query result from Vanna
 */
export interface QueryResult {
  /** Generated SQL query */
  sql: string;
  /** Execution status */
  status: 'success' | 'error';
  /** Result data as array of rows */
  data?: Record<string, any>[];
  /** Column metadata */
  columns?: ColumnMetadata[];
  /** Error message if status is 'error' */
  error?: string;
  /** Execution time in milliseconds */
  executionTime?: number;
  /** Whether a chart should be generated */
  hasChart?: boolean;
  /** Chart figure ID (for fetching chart data) */
  chartId?: string;
}

/**
 * Column metadata for result tables
 */
export interface ColumnMetadata {
  /** Column name */
  name: string;
  /** Data type (from DataFrame.dtypes) */
  type: string;
  /** Whether column is numeric (for chart generation) */
  isNumeric: boolean;
}

/**
 * Plotly figure data from backend
 */
export interface PlotlyFigure {
  /** Figure data traces */
  data: Plotly.Data[];
  /** Figure layout configuration */
  layout: Partial<Plotly.Layout>;
  /** Figure configuration options */
  config?: Partial<Plotly.Config>;
}

/**
 * Complete question-answer interaction
 */
export interface QuestionAnswer {
  question: Question;
  result?: QueryResult;
  figure?: PlotlyFigure;
  /** Loading state */
  isLoading: boolean;
  /** Error state */
  error?: Error;
}
```

---

### 2. Configuration Entities

```typescript
/**
 * LLM (Copilot Socket Core) configuration
 */
export interface LLMConfig {
  /** API endpoint URL */
  endpoint: string;
  /** Authentication token (optional for localhost) */
  api_key?: string;
  /** LLM model identifier */
  model: string;
  /** Temperature for generation (0.0 - 1.0) */
  temperature: number;
  /** Maximum tokens per response */
  max_tokens: number;
  /** Maximum tool rounds */
  max_tool_rounds: number;
  /** Request timeout in seconds */
  timeout: number;
}

/**
 * Database connection configuration
 */
export interface DatabaseConfig {
  /** Database type */
  type: 'oracle' | 'postgres' | 'mysql' | 'mssql';
  /** Database host */
  host: string;
  /** Database port */
  port: number;
  /** Database name */
  database: string;
  /** Database schema */
  schema: string;
  /** Database user */
  user: string;
  /** Database password (handled securely by backend) */
  password: string;
}

/**
 * ChromaDB vector store configuration
 */
export interface ChromaDBConfig {
  /** Number of SQL examples to retrieve */
  n_results_sql: number;
  /** Number of DDL schemas to retrieve */
  n_results_ddl: number;
  /** Number of documentation entries to retrieve */
  n_results_documentation: number;
  /** Persistence directory path */
  persist_directory?: string;
}

/**
 * Flask server configuration
 */
export interface FlaskConfig {
  /** Flask host */
  host: string;
  /** Flask port */
  port: number;
  /** Debug mode */
  debug: boolean;
  /** UI title */
  title: string;
  /** UI subtitle */
  subtitle: string;
  /** Allow LLM to see data */
  allow_llm_to_see_data: boolean;
}

/**
 * Training data configuration
 */
export interface TrainingConfig {
  /** Auto-train on startup */
  auto_train_on_startup: boolean;
  /** Training data directory path */
  training_data_path: string;
  /** Training settings */
  training_settings: {
    load_ddl: boolean;
    load_documentation: boolean;
    load_training_pairs: boolean;
    skip_if_exists: boolean;
    verbose: boolean;
  };
}

/**
 * Complete configuration object
 */
export interface AppConfig {
  llm: LLMConfig;
  database: DatabaseConfig;
  chromadb: ChromaDBConfig;
  flask: FlaskConfig;
  training: TrainingConfig;
}
```

---

### 3. Training Data Entities

```typescript
/**
 * Training data statistics
 */
export interface TrainingDataStats {
  /** Total number of training items */
  total: number;
  /** Number of DDL schemas */
  ddlCount: number;
  /** Number of documentation entries */
  documentationCount: number;
  /** Number of question-SQL pairs */
  trainingPairsCount: number;
  /** Last updated timestamp */
  lastUpdated?: Date;
}

/**
 * Training data load result
 */
export interface TrainingDataLoadResult {
  /** Number of DDL files loaded */
  ddl_loaded: number;
  /** Number of documentation files loaded */
  docs_loaded: number;
  /** Number of training pairs loaded */
  pairs_loaded: number;
  /** Any errors encountered */
  errors: string[];
  /** Success message */
  message: string;
}

/**
 * Training data item (for display)
 */
export interface TrainingDataItem {
  /** Item ID */
  id: string;
  /** Item type */
  type: 'sql' | 'ddl' | 'doc';
  /** Item content */
  content: string;
  /** Creation timestamp */
  created_at?: Date;
}
```

---

### 4. UI State Entities

```typescript
/**
 * Theme mode
 */
export type ThemeMode = 'light' | 'dark';

/**
 * Settings tab identifier
 */
export type SettingsTab = 'llm' | 'database' | 'chromadb' | 'flask' | 'training';

/**
 * Connection test result
 */
export interface ConnectionTestResult {
  /** Test success status */
  success: boolean;
  /** Success or error message */
  message: string;
  /** Response time in milliseconds */
  responseTime?: number;
}

/**
 * Loading state for async operations
 */
export interface LoadingState {
  /** Is operation in progress */
  isLoading: boolean;
  /** Loading message to display */
  message?: string;
  /** Progress percentage (0-100) */
  progress?: number;
}

/**
 * Error state
 */
export interface ErrorState {
  /** Error occurred */
  hasError: boolean;
  /** Error message */
  message?: string;
  /** Error code (if available) */
  code?: string;
  /** Detailed error for debugging */
  details?: any;
}

/**
 * Toast notification
 */
export interface ToastNotification {
  /** Unique ID */
  id: string;
  /** Notification type */
  type: 'success' | 'error' | 'info' | 'warning';
  /** Notification title */
  title: string;
  /** Notification message */
  message?: string;
  /** Duration in milliseconds (0 = permanent) */
  duration?: number;
}
```

---

### 5. API Request/Response Types

```typescript
/**
 * Request to ask a question
 */
export interface AskQuestionRequest {
  /** Natural language question */
  question: string;
  /** Optional session ID for conversation context */
  sessionId?: string;
}

/**
 * Response from ask question endpoint
 */
export interface AskQuestionResponse {
  /** Generated SQL query */
  sql: string;
  /** Query execution result */
  data?: Record<string, any>[];
  /** Column names */
  columns?: string[];
  /** Error message if query failed */
  error?: string;
  /** Chart figure ID if chart available */
  figure_id?: string;
}

/**
 * Request to update configuration
 */
export interface UpdateConfigRequest<T> {
  /** Configuration data */
  config: Partial<T>;
}

/**
 * Response from update configuration
 */
export interface UpdateConfigResponse {
  /** Success status */
  success: boolean;
  /** Success message */
  message: string;
  /** Updated configuration */
  config?: any;
}

/**
 * Request to test connection
 */
export interface TestConnectionRequest {
  /** Connection parameters to test */
  params: Partial<DatabaseConfig> | Partial<LLMConfig>;
}

/**
 * Generic API error response
 */
export interface APIError {
  /** Error message */
  error: string;
  /** Error code */
  code?: string;
  /** Additional details */
  details?: any;
}
```

---

## Data Validation Schemas (Zod)

```typescript
import { z } from 'zod';

/**
 * Database configuration validation schema
 */
export const databaseConfigSchema = z.object({
  type: z.enum(['oracle', 'postgres', 'mysql', 'mssql']),
  host: z.string().min(1, 'Host is required'),
  port: z.number().int().positive('Port must be positive'),
  database: z.string().min(1, 'Database name is required'),
  schema: z.string().min(1, 'Schema is required'),
  user: z.string().min(1, 'User is required'),
  password: z.string().min(1, 'Password is required')
});

/**
 * LLM configuration validation schema
 */
export const llmConfigSchema = z.object({
  endpoint: z.string().url('Invalid endpoint URL'),
  api_key: z.string().optional(),
  model: z.string().min(1, 'Model is required'),
  temperature: z.number().min(0).max(1, 'Temperature must be between 0 and 1'),
  max_tokens: z.number().int().positive('Max tokens must be positive'),
  max_tool_rounds: z.number().int().positive('Max rounds must be positive'),
  timeout: z.number().int().positive('Timeout must be positive')
});

/**
 * ChromaDB configuration validation schema
 */
export const chromadbConfigSchema = z.object({
  n_results_sql: z.number().int().positive(),
  n_results_ddl: z.number().int().positive(),
  n_results_documentation: z.number().int().positive(),
  persist_directory: z.string().optional()
});

/**
 * Flask configuration validation schema
 */
export const flaskConfigSchema = z.object({
  host: z.string().min(1),
  port: z.number().int().positive(),
  debug: z.boolean(),
  title: z.string().min(1),
  subtitle: z.string().min(1),
  allow_llm_to_see_data: z.boolean()
});

/**
 * Training configuration validation schema
 */
export const trainingConfigSchema = z.object({
  auto_train_on_startup: z.boolean(),
  training_data_path: z.string().min(1),
  training_settings: z.object({
    load_ddl: z.boolean(),
    load_documentation: z.boolean(),
    load_training_pairs: z.boolean(),
    skip_if_exists: z.boolean(),
    verbose: z.boolean()
  })
});

/**
 * Question validation schema
 */
export const questionSchema = z.object({
  question: z.string().min(1, 'Question cannot be empty').max(1000, 'Question too long')
});
```

---

## Data Transformations

```typescript
/**
 * Transform Flask API response to QueryResult
 */
export function transformQueryResponse(response: any): QueryResult {
  return {
    sql: response.sql || '',
    status: response.error ? 'error' : 'success',
    data: response.data || [],
    columns: response.columns?.map((name: string, index: number) => ({
      name,
      type: response.dtypes?.[name] || 'unknown',
      isNumeric: ['int64', 'float64', 'int32', 'float32'].includes(response.dtypes?.[name])
    })),
    error: response.error,
    executionTime: response.execution_time,
    hasChart: !!response.figure_id,
    chartId: response.figure_id
  };
}

/**
 * Transform Plotly figure response
 */
export function transformPlotlyFigure(response: any): PlotlyFigure {
  return {
    data: response.data || [],
    layout: response.layout || {},
    config: response.config || { responsive: true }
  };
}

/**
 * Get default port for database type
 */
export function getDefaultPort(dbType: DatabaseConfig['type']): number {
  const ports: Record<DatabaseConfig['type'], number> = {
    oracle: 1521,
    postgres: 5432,
    mysql: 3306,
    mssql: 1433
  };
  return ports[dbType];
}

/**
 * Format query execution time
 */
export function formatExecutionTime(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(date);
}
```

---

## State Management Patterns

### React Query Keys

```typescript
/**
 * Query key factory for type-safe React Query keys
 */
export const queryKeys = {
  // Configuration queries
  config: {
    all: ['config'] as const,
    detail: () => [...queryKeys.config.all, 'detail'] as const
  },
  
  // Question queries
  questions: {
    all: ['questions'] as const,
    detail: (id: string) => [...queryKeys.questions.all, id] as const
  },
  
  // Training data queries
  training: {
    all: ['training'] as const,
    stats: () => [...queryKeys.training.all, 'stats'] as const
  },
  
  // Connection test queries
  connections: {
    database: () => ['connections', 'database'] as const,
    llm: () => ['connections', 'llm'] as const
  }
} as const;
```

### React Query Mutations

```typescript
/**
 * Mutation keys for tracking mutations
 */
export const mutationKeys = {
  askQuestion: 'askQuestion',
  updateConfig: 'updateConfig',
  testConnection: 'testConnection',
  loadTrainingData: 'loadTrainingData'
} as const;
```

---

## Type Guards

```typescript
/**
 * Check if error is API error
 */
export function isAPIError(error: unknown): error is APIError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'error' in error &&
    typeof (error as any).error === 'string'
  );
}

/**
 * Check if database config is valid
 */
export function isDatabaseConfig(config: unknown): config is DatabaseConfig {
  return databaseConfigSchema.safeParse(config).success;
}

/**
 * Check if query result has data
 */
export function hasQueryData(result: QueryResult): result is QueryResult & { data: Record<string, any>[] } {
  return result.status === 'success' && Array.isArray(result.data) && result.data.length > 0;
}
```

---

## Phase 1 Completion Checklist

- [x] Core entities defined (Question, QueryResult, PlotlyFigure)
- [x] Configuration entities defined (LLM, Database, ChromaDB, Flask, Training)
- [x] Training data entities defined
- [x] UI state entities defined
- [x] API request/response types defined
- [x] Zod validation schemas created
- [x] Data transformation functions defined
- [x] React Query keys and mutations defined
- [x] Type guards implemented
- [x] All types exported for use in components

**Status**: ✅ Phase 1 Data Model Complete - Ready for Contract Generation
