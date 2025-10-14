/**
 * Zod validation schemas for Vanna configurations
 * Provides runtime type validation and TypeScript type inference
 */

import { z } from 'zod';

// ============================================================================
// Configuration Validation Schemas
// ============================================================================

/**
 * Database configuration validation schema
 */
export const databaseConfigSchema = z.object({
  type: z.enum(['oracle', 'postgres', 'mysql', 'mssql'], {
    errorMap: () => ({ message: 'Database type must be oracle, postgres, mysql, or mssql' }),
  }),
  host: z.string().min(1, 'Host is required'),
  port: z.number().int().positive('Port must be a positive integer'),
  database: z.string().min(1, 'Database name is required'),
  schema: z.string().min(1, 'Schema is required'),
  user: z.string().min(1, 'User is required'),
  password: z.string().min(1, 'Password is required'),
});

/**
 * LLM configuration validation schema
 */
export const llmConfigSchema = z.object({
  endpoint: z.string().url('Endpoint must be a valid URL'),
  api_key: z.string().optional(),
  model: z.string().min(1, 'Model is required'),
  temperature: z.number().min(0).max(1, 'Temperature must be between 0 and 1'),
  max_tokens: z.number().int().positive('Max tokens must be a positive integer'),
  max_tool_rounds: z.number().int().positive('Max tool rounds must be a positive integer'),
  timeout: z.number().int().positive('Timeout must be a positive integer'),
});

/**
 * ChromaDB configuration validation schema
 */
export const chromadbConfigSchema = z.object({
  n_results_sql: z.number().int().positive('SQL results must be a positive integer'),
  n_results_ddl: z.number().int().positive('DDL results must be a positive integer'),
  n_results_documentation: z
    .number()
    .int()
    .positive('Documentation results must be a positive integer'),
  persist_directory: z.string().optional(),
});

/**
 * Flask configuration validation schema
 */
export const flaskConfigSchema = z.object({
  host: z.string().min(1, 'Host is required'),
  port: z.number().int().positive('Port must be a positive integer'),
  debug: z.boolean(),
  title: z.string().min(1, 'Title is required'),
  subtitle: z.string().min(1, 'Subtitle is required'),
  allow_llm_to_see_data: z.boolean(),
});

/**
 * Training configuration validation schema
 */
export const trainingConfigSchema = z.object({
  auto_train_on_startup: z.boolean(),
  training_data_path: z.string().min(1, 'Training data path is required'),
  training_settings: z.object({
    load_ddl: z.boolean(),
    load_documentation: z.boolean(),
    load_training_pairs: z.boolean(),
    skip_if_exists: z.boolean(),
    verbose: z.boolean(),
  }),
});

/**
 * Complete app configuration validation schema
 */
export const appConfigSchema = z.object({
  llm: llmConfigSchema,
  database: databaseConfigSchema,
  chromadb: chromadbConfigSchema,
  flask: flaskConfigSchema,
  training: trainingConfigSchema,
});

// ============================================================================
// Type Inference from Schemas
// ============================================================================

/**
 * Infer TypeScript types from Zod schemas
 * These should match the interfaces in types.ts
 */
export type DatabaseConfigInput = z.infer<typeof databaseConfigSchema>;
export type LLMConfigInput = z.infer<typeof llmConfigSchema>;
export type ChromaDBConfigInput = z.infer<typeof chromadbConfigSchema>;
export type FlaskConfigInput = z.infer<typeof flaskConfigSchema>;
export type TrainingConfigInput = z.infer<typeof trainingConfigSchema>;
export type AppConfigInput = z.infer<typeof appConfigSchema>;

// ============================================================================
// Validation Helper Functions
// ============================================================================

/**
 * Validate database configuration
 */
export function validateDatabaseConfig(data: unknown) {
  return databaseConfigSchema.safeParse(data);
}

/**
 * Validate LLM configuration
 */
export function validateLLMConfig(data: unknown) {
  return llmConfigSchema.safeParse(data);
}

/**
 * Validate ChromaDB configuration
 */
export function validateChromaDBConfig(data: unknown) {
  return chromadbConfigSchema.safeParse(data);
}

/**
 * Validate Flask configuration
 */
export function validateFlaskConfig(data: unknown) {
  return flaskConfigSchema.safeParse(data);
}

/**
 * Validate Training configuration
 */
export function validateTrainingConfig(data: unknown) {
  return trainingConfigSchema.safeParse(data);
}

/**
 * Validate complete app configuration
 */
export function validateAppConfig(data: unknown) {
  return appConfigSchema.safeParse(data);
}
