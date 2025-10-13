"""
Centralized Configuration for Vanna Flask Application
Edit this file to configure your databases and LLM settings
"""

import os

# =============================================================================
# CHROMADB DATABASE (for Vanna's Training Data & Embeddings)
# =============================================================================
# ChromaDB is a lightweight, local vector database (no external database needed)
# Data will be stored in: ./chromadb/ directory

CHROMADB_CONFIG = {
    'path': os.getenv('CHROMADB_PATH', './chromadb'),  # Local directory for ChromaDB storage
}

# =============================================================================
# YOUR DATA DATABASE (Oracle - What Users Will Query)
# =============================================================================

DATA_DB_CONFIG = {
    'type': 'oracle',  # Database type
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 1521)),
    'database': os.getenv('DB_NAME', 'XEPDB1'),
    'schema': os.getenv('DB_SCHEMA', 'hr'),
    'user': os.getenv('DB_USER', 'hr'),
    'password': os.getenv('DB_PASSWORD', 'hr123'),
}

# =============================================================================
# LLM API CONFIGURATION - Umbrella Gateway
# =============================================================================

LLM_CONFIG = {
    # Umbrella Gateway settings
    'api_type': 'umbrella-gateway',  # Identifies this as Umbrella Gateway
    'api_key': os.getenv('UMBRELLA_AUTH_TOKEN', 'sk-abcdef123456'),  # Bearer token from .vscode/settings.json
    'endpoint': os.getenv('UMBRELLA_ENDPOINT', 'http://localhost:8765'),  # Umbrella Gateway base URL
    'model': os.getenv('UMBRELLA_MODEL', 'copilot/gpt-5-mini'),  # Default model (note: needs 'copilot/' prefix)
    'temperature': float(os.getenv('LLM_TEMPERATURE', '0.7')),
    
    # Available models (can be fetched from /models endpoint)
    'available_models': [
        'copilot/gpt-5-mini',       # Your default model
        'copilot/gpt-5',            # GPT-5
        'copilot/claude-sonnet-4',  # Best for coding
        'copilot/gpt-4o',           # Advanced reasoning
        'copilot/gpt-4o-mini',      # Fast responses
        'copilot/o3-mini',          # O3 mini
    ],
}

# =============================================================================
# FLASK APP CONFIGURATION
# =============================================================================

FLASK_CONFIG = {
    'host': os.getenv('FLASK_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_PORT', 8084)),
    'debug': os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
    'secret_key': os.getenv('FLASK_SECRET_KEY', 'change-this-secret-key-in-production'),
}

# =============================================================================
# INITIAL TRAINING DATA (Optional)
# =============================================================================

# Add your initial DDL statements here
INITIAL_DDL = """
-- HR Schema Tables
CREATE TABLE employees (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    last_name VARCHAR2(25) NOT NULL,
    email VARCHAR2(25) NOT NULL,
    phone_number VARCHAR2(20),
    hire_date DATE NOT NULL,
    job_id VARCHAR2(10) NOT NULL,
    salary NUMBER(8,2),
    commission_pct NUMBER(2,2),
    manager_id NUMBER(6),
    department_id NUMBER(4)
);

CREATE TABLE departments (
    department_id NUMBER(4) PRIMARY KEY,
    department_name VARCHAR2(30) NOT NULL,
    manager_id NUMBER(6),
    location_id NUMBER(4)
);

CREATE TABLE jobs (
    job_id VARCHAR2(10) PRIMARY KEY,
    job_title VARCHAR2(35) NOT NULL,
    min_salary NUMBER(6),
    max_salary NUMBER(6)
);
"""

# Add your business documentation here
INITIAL_DOCUMENTATION = """
HR Database Business Rules:
- All salaries are in USD
- Fiscal year starts in January
- Employee IDs are 6-digit numbers
- commission_pct is a percentage (0.0 to 1.0)
- department_id references the departments table
- manager_id references another employee
"""

# Add example question-SQL pairs here
INITIAL_TRAINING_PAIRS = [
    {
        "question": "Who are the highest paid employees?",
        "sql": "SELECT first_name, last_name, salary FROM hr.employees ORDER BY salary DESC FETCH FIRST 10 ROWS ONLY"
    },
    {
        "question": "How many employees are in each department?",
        "sql": "SELECT d.department_name, COUNT(e.employee_id) as employee_count FROM hr.departments d LEFT JOIN hr.employees e ON d.department_id = e.department_id GROUP BY d.department_name ORDER BY employee_count DESC"
    },
    {
        "question": "What is the average salary by job title?",
        "sql": "SELECT j.job_title, AVG(e.salary) as avg_salary FROM hr.jobs j JOIN hr.employees e ON j.job_id = e.job_id GROUP BY j.job_title ORDER BY avg_salary DESC"
    },
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_vanna_config():
    """Returns the configuration dict for Vanna initialization"""
    return {
        # ChromaDB config (local vector database)
        'path': CHROMADB_CONFIG['path'],
        
        # LLM config (Umbrella Gateway)
        'api_key': LLM_CONFIG['api_key'],
        'endpoint': LLM_CONFIG['endpoint'],
        'model': LLM_CONFIG['model'],
        'temperature': LLM_CONFIG['temperature'],
    }

def get_database_connection_params():
    """Returns the parameters for connecting to the data database"""
    return {
        'host': DATA_DB_CONFIG['host'],
        'port': DATA_DB_CONFIG['port'],
        'database': DATA_DB_CONFIG['database'],
        'user': DATA_DB_CONFIG['user'],
        'password': DATA_DB_CONFIG['password'],
        'schema': DATA_DB_CONFIG['schema'],
    }

def validate_config():
    """Validates that all required configuration is set"""
    errors = []
    
    # Check LLM config
    if LLM_CONFIG['api_key'] == 'your-api-key-here':
        errors.append("⚠️  LLM_API_KEY not set - using placeholder")
    
    # Check database configs
    if DATA_DB_CONFIG['password'] == 'hr123':
        errors.append("ℹ️  Using default Oracle HR schema credentials")
    
    return errors

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================

def print_config():
    """Prints the current configuration (for debugging)"""
    print("\n" + "="*60)
    print("📋 CURRENT CONFIGURATION")
    print("="*60)
    
    print("\n🗄️  ChromaDB (Vector Database):")
    print(f"   Storage Path: {CHROMADB_CONFIG['path']}")
    print(f"   Type: Local file-based (no external database needed)")
    
    print("\n🏢 Data Database (Oracle):")
    print(f"   Host: {DATA_DB_CONFIG['host']}:{DATA_DB_CONFIG['port']}")
    print(f"   Database: {DATA_DB_CONFIG['database']}")
    print(f"   Schema: {DATA_DB_CONFIG['schema']}")
    print(f"   User: {DATA_DB_CONFIG['user']}")
    
    print("\n🤖 LLM Configuration:")
    print(f"   Endpoint: {LLM_CONFIG['endpoint']}")
    print(f"   Model: {LLM_CONFIG['model']}")
    print(f"   Temperature: {LLM_CONFIG['temperature']}")
    
    print("\n🌐 Flask Configuration:")
    print(f"   Host: {FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}")
    print(f"   Debug: {FLASK_CONFIG['debug']}")
    
    # Show warnings
    warnings = validate_config()
    if warnings:
        print("\n⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    # Test the configuration
    print_config()
