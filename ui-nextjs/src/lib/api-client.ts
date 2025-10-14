/**
 * Axios-based API client for Flask backend
 * Centralized API calls with error handling and type safety
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  AskQuestionRequest,
  AskQuestionResponse,
  PlotlyFigureResponse,
  AppConfig,
  LLMConfig,
  DatabaseConfig,
  ChromaDBConfig,
  FlaskConfig,
  TrainingConfig,
  UpdateConfigResponse,
  ConnectionTestResult,
  TrainingDataLoadResult,
  APIError,
} from './types';

/**
 * Base URL for Flask API
 * Uses environment variable or defaults to localhost:8084
 */
const FLASK_URL = process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084';

/**
 * Create Axios instance with default configuration
 */
const client: AxiosInstance = axios.create({
  baseURL: FLASK_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor for logging (development only)
 */
client.interceptors.request.use(
  (config) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor for error handling
 */
client.interceptors.response.use(
  (response) => response,
  (error: AxiosError<APIError>) => {
    if (error.response) {
      // Server responded with error status
      const apiError: APIError = {
        error: error.response.data?.error || error.message,
        code: error.response.status.toString(),
        details: error.response.data?.details,
      };
      return Promise.reject(apiError);
    } else if (error.request) {
      // Request made but no response
      const apiError: APIError = {
        error: 'No response from server. Please check if Flask backend is running.',
        code: 'NETWORK_ERROR',
        details: error.message,
      };
      return Promise.reject(apiError);
    } else {
      // Error in request setup
      const apiError: APIError = {
        error: error.message,
        code: 'REQUEST_ERROR',
      };
      return Promise.reject(apiError);
    }
  }
);

// ============================================================================
// Question & Answer API
// ============================================================================

/**
 * Ask a natural language question
 * POST /api/v0/ask
 */
export async function askQuestion(data: AskQuestionRequest): Promise<AskQuestionResponse> {
  const response = await client.post<AskQuestionResponse>('/api/v0/ask', data);
  return response.data;
}

/**
 * Get Plotly figure for query result
 * GET /api/v0/generate_plotly_figure?id={figureId}
 */
export async function getPlotlyFigure(figureId: string): Promise<PlotlyFigureResponse> {
  const response = await client.get<PlotlyFigureResponse>('/api/v0/generate_plotly_figure', {
    params: { id: figureId },
  });
  return response.data;
}

// ============================================================================
// Configuration API
// ============================================================================

/**
 * Get all configurations
 * GET /api/v0/get_config
 */
export async function getConfig(): Promise<AppConfig> {
  const response = await client.get<AppConfig>('/api/v0/get_config');
  return response.data;
}

/**
 * Update LLM configuration
 * POST /api/v0/update_llm_config
 */
export async function updateLLMConfig(config: Partial<LLMConfig>): Promise<UpdateConfigResponse> {
  const response = await client.post<UpdateConfigResponse>('/api/v0/update_llm_config', config);
  return response.data;
}

/**
 * Update database configuration
 * POST /api/v0/update_database_config
 */
export async function updateDatabaseConfig(
  config: DatabaseConfig
): Promise<UpdateConfigResponse> {
  const response = await client.post<UpdateConfigResponse>(
    '/api/v0/update_database_config',
    config
  );
  return response.data;
}

/**
 * Update ChromaDB configuration
 * POST /api/v0/update_chromadb_config
 */
export async function updateChromaDBConfig(
  config: ChromaDBConfig
): Promise<UpdateConfigResponse> {
  const response = await client.post<UpdateConfigResponse>(
    '/api/v0/update_chromadb_config',
    config
  );
  return response.data;
}

/**
 * Update Flask configuration
 * POST /api/v0/update_flask_config
 */
export async function updateFlaskConfig(config: FlaskConfig): Promise<UpdateConfigResponse> {
  const response = await client.post<UpdateConfigResponse>('/api/v0/update_flask_config', config);
  return response.data;
}

/**
 * Update training configuration
 * POST /api/v0/update_training_config
 */
export async function updateTrainingConfig(
  config: TrainingConfig
): Promise<UpdateConfigResponse> {
  const response = await client.post<UpdateConfigResponse>(
    '/api/v0/update_training_config',
    config
  );
  return response.data;
}

// ============================================================================
// Connection Testing API
// ============================================================================

/**
 * Test database connection
 * POST /api/v0/test_database_connection
 */
export async function testDatabaseConnection(
  config: DatabaseConfig
): Promise<ConnectionTestResult> {
  const response = await client.post<ConnectionTestResult>(
    '/api/v0/test_database_connection',
    config
  );
  return response.data;
}

/**
 * Test LLM connection
 * POST /api/v0/test_llm_connection
 */
export async function testLLMConnection(params: {
  endpoint: string;
  api_key?: string;
}): Promise<ConnectionTestResult> {
  const response = await client.post<ConnectionTestResult>('/api/v0/test_llm_connection', params);
  return response.data;
}

// ============================================================================
// Training Data API
// ============================================================================

/**
 * Load training data from configured directory
 * POST /api/v0/load_training_data
 */
export async function loadTrainingData(): Promise<TrainingDataLoadResult> {
  const response = await client.post<TrainingDataLoadResult>('/api/v0/load_training_data');
  return response.data;
}

/**
 * Export API client instance for advanced usage
 */
export default client;
