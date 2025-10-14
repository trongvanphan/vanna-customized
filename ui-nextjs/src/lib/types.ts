/**
 * Core TypeScript interfaces for Vanna Next.js UI
 * Based on Flask API contracts and data model specification
 */

import type * as Plotly from 'plotly.js';

// ============================================================================
// Question & Query Result Entities
// ============================================================================

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
  /** Column names (simple array) */
  columnNames?: string[];
  /** Column data types */
  dtypes?: Record<string, string>;
  /** Error message if status is 'error' */
  error?: string;
  /** Execution time in milliseconds */
  executionTime?: number;
  /** Execution time from backend */
  execution_time?: number;
  /** Whether a chart should be generated */
  hasChart?: boolean;
  /** Chart figure ID (for fetching chart data) */
  chartId?: string;
  /** Figure ID from backend */
  figure_id?: string;
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

// ============================================================================
// Configuration Entities
// ============================================================================

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

// ============================================================================
// Training Data Entities
// ============================================================================

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
  /** Success status */
  success: boolean;
  /** Success message */
  message: string;
  /** Training statistics */
  stats?: {
    /** Number of DDL files loaded */
    ddl_loaded: number;
    /** Number of documentation files loaded */
    docs_loaded: number;
    /** Number of training pairs loaded */
    pairs_loaded: number;
    /** Any errors encountered */
    errors?: string[];
  };
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

// ============================================================================
// UI State Entities
// ============================================================================

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
  /** Response time from backend */
  response_time?: number;
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

// ============================================================================
// API Request/Response Types
// ============================================================================

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
  /** Column data types */
  dtypes?: Record<string, string>;
  /** Error message if query failed */
  error?: string;
  /** Execution time in milliseconds */
  execution_time?: number;
  /** Chart figure ID if chart available */
  figure_id?: string;
}

/**
 * Response from get plotly figure endpoint
 */
export interface PlotlyFigureResponse {
  /** Response type identifier */
  type: string;
  /** Figure ID */
  id: string;
  /** Plotly figure data */
  fig: PlotlyFigure;
}

/**
 * Request to update configuration
 */
export interface UpdateConfigRequest<T> {
  /** Configuration data */
  config?: Partial<T>;
}

/**
 * Response from update configuration
 */
export interface UpdateConfigResponse {
  /** Success status */
  success?: boolean;
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
  params?: Partial<DatabaseConfig> | Partial<LLMConfig>;
  /** Endpoint for LLM test */
  endpoint?: string;
  /** API key for LLM test */
  api_key?: string;
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
