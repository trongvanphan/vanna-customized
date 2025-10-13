#!/usr/bin/env python3
"""
Quick Start Script for Vanna with Flask UI
Run this to test Vanna with Umbrella Gateway LLM and ChromaDB + Oracle

Configuration is centralized in config.py - edit that file instead!
"""

from vanna.chromadb import ChromaDB_VectorStore
from vanna.base import VannaBase
import requests
import time
import config  # Centralized configuration

# =============================================================================
# Custom LLM Class - Modify submit_prompt() for your API
# =============================================================================

class MyCustomLLM(VannaBase):
    def __init__(self, config_dict=None):
        VannaBase.__init__(self, config=config_dict)
        if config_dict is None:
            config_dict = {}
        
        # Umbrella Gateway configuration
        self.api_key = config_dict.get('api_key')
        self.api_endpoint = config_dict.get('endpoint', 'http://localhost:8765')
        self.model = config_dict.get('model', 'copilot/gpt-5-mini')
        self.temperature = config_dict.get('temperature', 0.7)
        self.session_id = f"vanna_session_{int(time.time())}"
        
        print(f"✅ Initialized Umbrella Gateway LLM")
        print(f"   └─ Endpoint: {self.api_endpoint}")
        print(f"   └─ Model: {self.model}")
        print(f"   └─ Session ID: {self.session_id}")
    
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        """
        Submit prompt to Umbrella Gateway API.
        
        Umbrella Gateway uses GitHub Copilot models with OpenAI-compatible interface.
        Endpoint: POST /chat
        Auth: Bearer token
        """
        try:
            # Prepare request
            url = f"{self.api_endpoint}/chat"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Build request body (OpenAI-compatible messages format)
            payload = {
                "messages": prompt,  # Already formatted as list of message dicts
                "sessionId": self.session_id,
                "model": self.model,
                "stream": False
            }
            
            # Make request
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60  # Longer timeout for complex SQL generation
            )
            
            # Handle errors
            if response.status_code == 401:
                raise Exception("Unauthorized - Check your auth token in config.py")
            elif response.status_code == 403:
                raise Exception("Forbidden - Run 'Grant Access' command in VS Code")
            elif response.status_code == 503:
                raise Exception(f"Service Unavailable - Try a different model")
            
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            return data.get('text', data.get('response', ''))
            
        except requests.exceptions.Timeout:
            print(f"⏱️  Request timeout - SQL generation took too long")
            raise
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Cannot reach Umbrella Gateway at {self.api_endpoint}")
            print(f"   Make sure:")
            print(f"   1. VS Code is open with the workspace")
            print(f"   2. Umbrella Gateway extension is installed")
            print(f"   3. Server is started (Cmd+Shift+P -> 'Umbrella Gateway: Start Server')")
            raise
        except Exception as e:
            print(f"❌ LLM API Error: {e}")
            raise

# =============================================================================
# Combine LLM with ChromaDB
# =============================================================================

class MyVanna(ChromaDB_VectorStore, MyCustomLLM):
    def __init__(self, config_dict=None):
        print("🚀 Initializing Vanna...")
        ChromaDB_VectorStore.__init__(self, config=config_dict)
        MyCustomLLM.__init__(self, config_dict=config_dict)
        print("✅ Vanna initialized successfully!")

# =============================================================================
# Main Setup
# =============================================================================

def main():
    print("\n" + "="*60)
    print("🤖 Vanna Flask Setup - Oracle HR Database")
    print("="*60 + "\n")
    
    # Show current configuration
    config.print_config()
    
    # Initialize Vanna with config from config.py
    vn = MyVanna(config_dict=config.get_vanna_config())
    
    # Connect to Oracle database
    db_params = config.get_database_connection_params()
    print(f"\n📊 Connecting to Oracle database: {db_params['database']} (schema: {db_params['schema']})...")
    
    try:
        # Oracle connection via oracledb
        # Build DSN in format: host:port/sid
        dsn = f"{db_params['host']}:{db_params['port']}/{db_params['database']}"
        
        vn.connect_to_oracle(
            dsn=dsn,
            user=db_params['user'],
            password=db_params['password']
        )
        
        # Verify connection with a simple query
        result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM all_tables WHERE owner = '{db_params['schema'].upper()}'")
        table_count = result.iloc[0]['TABLE_COUNT'] if not result.empty else 0
        
        print(f"✅ Connected to Oracle database")
        print(f"✅ Using schema: {db_params['schema']} ({table_count} tables found)")
        
        # Note: We'll query with schema prefix (hr.employees) instead of ALTER SESSION
    except Exception as e:
        print(f"❌ Failed to connect to Oracle database: {e}")
        print("\n💡 Make sure:")
        print("   1. Oracle database is running")
        print("   2. oracledb package is installed: pip install vanna[oracle]")
        print("   3. Connection details in config.py are correct")
        return
    
    # Check if API key is set
    llm_config = config.LLM_CONFIG
    if llm_config['api_key'] == 'your-api-key':
        print("\n⚠️  WARNING: Using placeholder API key!")
        print("   Please update LLM_API_KEY in config.py with your actual API key.")
    
    # Initial training (only needed once)
    print("\n📚 Setting up initial training data...")
    print("   (If data already exists, this will skip duplicates)")
    
    # Add DDL (pass entire string, not iterate characters)
    try:
        vn.train(ddl=config.INITIAL_DDL)
        print(f"   ✅ Added DDL schema definitions")
    except Exception as e:
        print(f"   ℹ️  DDL might already exist: {str(e)[:50]}...")
    
    # Add documentation
    try:
        vn.train(documentation=config.INITIAL_DOCUMENTATION)
        print("   ✅ Added documentation")
    except Exception as e:
        print(f"   ℹ️  Documentation might already exist: {str(e)[:50]}...")
    
    # Add question-SQL pairs
    for pair in config.INITIAL_TRAINING_PAIRS:
        try:
            vn.train(question=pair['question'], sql=pair['sql'])
            print(f"   ✅ Added: {pair['question'][:50]}...")
        except Exception as e:
            print(f"   ℹ️  Pair might already exist: {str(e)[:50]}...")
    
    print("\n✨ Training complete!")
    
    # Test SQL generation
    print("\n🧪 Testing SQL generation...")
    test_question = "Show me all employees"
    sql = vn.generate_sql(test_question)
    print(f"   Question: {test_question}")
    print(f"   Generated SQL: {sql}")
    
    # Launch Flask UI using VannaFlaskApp
    flask_config = config.FLASK_CONFIG
    print(f"\n🌐 Launching Flask UI at http://{flask_config['host']}:{flask_config['port']}")
    print("   Press Ctrl+C to stop\n")
    
    # Import Flask components
    from vanna.flask import VannaFlaskApp
    
    # Create VannaFlaskApp (this creates its own Flask app internally)
    vanna_flask = VannaFlaskApp(
        vn=vn, 
        allow_llm_to_see_data=True,
        title="Vanna AI - Oracle HR Database",
        subtitle="Ask questions about the HR database in natural language"
    )
    
    # Run Flask server (use the app created by VannaFlaskApp)
    vanna_flask.flask_app.run(
        host=flask_config['host'], 
        port=flask_config['port'], 
        debug=flask_config['debug']
    )


if __name__ == '__main__':
    # Validate configuration before starting
    print("\n🔍 Validating configuration from config.py...")
    config.validate_config()
    
    # Check for placeholder API key
    if config.LLM_CONFIG['api_key'] == 'your-api-key':
        print("\n⚠️  WARNING: Using placeholder API key!")
        print("   Please update LLM_API_KEY in config.py with your actual API key.")
        print("\n   Continuing with placeholder (this will fail when calling LLM)...\n")
    
    # Run main setup
    main()
