#!/usr/bin/env python3
"""
Quick Start Script for Vanna with Flask UI (Using UI Configuration)
This version uses the flexible JSON-based configuration from ui/ directory

Run: python quick_start_flask_ui.py
"""

from vanna.chromadb import ChromaDB_VectorStore
from vanna.base import VannaBase
import requests
import time

# Import UI configuration loaders
from ui import (
    get_vanna_config,
    get_database_connection_params,
    get_flask_params,
    DataLoader,
    print_config_summary,
    should_auto_train,
    train_from_files,
)

# =============================================================================
# Custom LLM Class - Uses configuration from ui/config/llm.json
# Copilot Socket Core API Integration
# =============================================================================

class MyCustomLLM(VannaBase):
    def __init__(self, config_dict=None):
        VannaBase.__init__(self, config=config_dict)
        if config_dict is None:
            config_dict = {}
        
        # Copilot Socket Core configuration (loaded from JSON)
        self.api_key = config_dict.get('api_key', '')  # Optional for localhost
        self.api_endpoint = config_dict.get('endpoint', 'http://localhost:8765')
        self.model = config_dict.get('model', 'copilot/gpt-4o')
        self.temperature = config_dict.get('temperature', 0.7)
        self.max_tokens = config_dict.get('max_tokens', 4096)
        self.max_tool_rounds = config_dict.get('max_tool_rounds', 5)
        self.timeout = config_dict.get('timeout', 60)
        self.session_id = None  # Will be created on first chat
        
        print(f"✅ Initialized Copilot Socket Core LLM")
        print(f"   └─ Endpoint: {self.api_endpoint}")
        print(f"   └─ Model: {self.model}")
        print(f"   └─ Temperature: {self.temperature}")
        print(f"   └─ Max Tool Rounds: {self.max_tool_rounds}")
    
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
    
    def _ensure_session(self):
        """Create session if not exists"""
        if self.session_id is None:
            try:
                url = f"{self.api_endpoint}/session/new"
                response = requests.post(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                self.session_id = data['session']['sessionId']
                print(f"   └─ Created new session: {self.session_id}")
            except Exception as e:
                print(f"⚠️  Could not create session (will use stateless mode): {e}")
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        """Submit prompt to Copilot Socket Core API
        
        Args:
            prompt: List of message dicts with role/content (Vanna format)
            **kwargs: Additional options
            
        Returns:
            Generated text response
        """
        try:
            # Ensure we have a session
            self._ensure_session()
            
            # Extract the last user message from prompt
            # Vanna passes a list of messages, we need to convert to single message
            user_message = ""
            for msg in prompt:
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
            
            # If no user message found, use the whole prompt as context
            if not user_message and prompt:
                user_message = str(prompt[-1].get('content', ''))
            
            url = f"{self.api_endpoint}/chat"
            headers = {
                "Content-Type": "application/json"
            }
            
            # Add API key if provided (optional for localhost)
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "message": user_message,
                "model": self.model,
                "maxToolRounds": self.max_tool_rounds
            }
            
            # Add session if available
            if self.session_id:
                payload["sessionId"] = self.session_id
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                raise Exception("Unauthorized - Check if Copilot Socket Core server is running")
            elif response.status_code == 404:
                raise Exception("Endpoint not found - Verify Copilot Socket Core is running on correct port")
            elif response.status_code == 500:
                error_detail = response.json().get('error', 'Internal server error')
                raise Exception(f"Server error: {error_detail}")
            
            response.raise_for_status()
            data = response.json()
            
            # Extract reply from response
            reply = data.get('reply', data.get('response', ''))
            
            # Log tool usage if any
            tool_calls = data.get('toolCalls', 0)
            if tool_calls > 0:
                print(f"   └─ Used {tool_calls} tool calls")
            
            return reply
            
        except requests.exceptions.Timeout:
            print(f"⏱️  Request timeout - SQL generation took too long")
            raise
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Cannot reach Copilot Socket Core at {self.api_endpoint}")
            print(f"   Make sure:")
            print(f"   1. VSCode is open with the Copilot Socket Core extension")
            print(f"   2. Extension is activated")
            print(f"   3. Server is started (Command: 'Copilot Socket: Start Server')")
            print(f"   4. Check health: curl {self.api_endpoint}/health")
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
    print("🤖 Vanna Flask Setup - Using UI Configuration")
    print("="*60 + "\n")
    
    # Show current configuration from JSON files
    print_config_summary()
    
    # Initialize Vanna with config from ui/config/*.json
    vn = MyVanna(config_dict=get_vanna_config())
    
    # Connect to database using config from ui/config/database.json
    db_params = get_database_connection_params()
    print(f"\n📊 Connecting to {db_params['type'].upper()} database: {db_params['database']} (schema: {db_params['schema']})...")
    
    try:
        if db_params['type'] == 'oracle':
            # Oracle connection
            dsn = f"{db_params['host']}:{db_params['port']}/{db_params['database']}"
            
            vn.connect_to_oracle(
                dsn=dsn,
                user=db_params['user'],
                password=db_params['password']
            )
            
            # Verify connection
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM all_tables WHERE owner = '{db_params['schema'].upper()}'")
            table_count = result.iloc[0]['TABLE_COUNT'] if not result.empty else 0
            
            print(f"✅ Connected to Oracle database")
            print(f"✅ Using schema: {db_params['schema']} ({table_count} tables found)")
        
        elif db_params['type'] == 'postgres' or db_params['type'] == 'postgresql':
            # PostgreSQL connection
            vn.connect_to_postgres(
                host=db_params['host'],
                port=db_params['port'],
                dbname=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
            )
            
            # Verify connection
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = '{db_params['schema']}'")
            table_count = result.iloc[0]['table_count'] if not result.empty else 0
            
            print(f"✅ Connected to PostgreSQL database")
            print(f"✅ Using schema: {db_params['schema']} ({table_count} tables found)")
        
        elif db_params['type'] == 'mysql':
            # MySQL connection
            vn.connect_to_mysql(
                host=db_params['host'],
                port=db_params['port'],
                database=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
            )
            
            # Verify connection
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = '{db_params['database']}'")
            table_count = result.iloc[0]['table_count'] if not result.empty else 0
            
            print(f"✅ Connected to MySQL database")
            print(f"✅ Using database: {db_params['database']} ({table_count} tables found)")
        
        elif db_params['type'] == 'mssql' or db_params['type'] == 'sqlserver':
            # Microsoft SQL Server connection
            vn.connect_to_mssql(
                server=db_params['host'],
                port=db_params['port'],
                database=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
            )
            
            # Verify connection
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = '{db_params['schema']}'")
            table_count = result.iloc[0]['table_count'] if not result.empty else 0
            
            print(f"✅ Connected to SQL Server database")
            print(f"✅ Using schema: {db_params['schema']} ({table_count} tables found)")
        
        else:
            print(f"⚠️  Database type '{db_params['type']}' not implemented in this example")
            print(f"   Supported types: oracle, postgres, mysql, mssql")
            print(f"   Add connection logic in quick_start_flask_ui.py if needed")
            return
            
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        print("\n💡 Make sure:")
        print("   1. Database is running")
        print("   2. Credentials in ui/config/database.json are correct")
        print("   3. Required database driver is installed")
        return
    
    # Check if auto-training is enabled
    if should_auto_train():
        print("\n📚 Auto-training enabled - Loading training data from trainingMyDb/...")
        stats = train_from_files(vn, verbose=True)
        print(f"\n✨ Training complete!")
        print(f"   DDL files loaded: {stats['ddl_loaded']}")
        print(f"   Documentation loaded: {stats['docs_loaded']}")
        print(f"   Training pairs loaded: {stats['pairs_loaded']}")
        if stats['errors']:
            print(f"   ⚠️  Errors encountered: {stats['errors']}")
    else:
        print("\n⏸️  Auto-training disabled (set auto_train_on_startup=true in ui/config/training.json to enable)")
        print("   💡 You can manually train by calling: train_from_files(vn)")
    
    # Test SQL generation
    print("\n🧪 Testing SQL generation...")
    test_question = "Show me all employees"
    sql = vn.generate_sql(test_question)
    print(f"   Question: {test_question}")
    print(f"   Generated SQL: {sql}")
    
    # Launch Flask UI using config from ui/config/flask.json
    flask_params = get_flask_params()
    print(f"\n🌐 Launching Flask UI at http://{flask_params['host']}:{flask_params['port']}")
    print("   Press Ctrl+C to stop\n")
    
    # Import Flask components
    from vanna.flask import VannaFlaskApp
    
    # Get UI settings from flask.json
    import json
    from pathlib import Path
    
    flask_config_path = Path(__file__).parent / 'ui' / 'config' / 'flask.json'
    with open(flask_config_path) as f:
        flask_full_config = json.load(f)
    
    ui_settings = flask_full_config.get('ui_settings', {})
    
    # Create VannaFlaskApp (this creates its own Flask app internally)
    vanna_flask = VannaFlaskApp(
        vn=vn,
        allow_llm_to_see_data=ui_settings.get('allow_llm_to_see_data', True),
        title=ui_settings.get('title', 'Vanna AI - Database Assistant'),
        subtitle=ui_settings.get('subtitle', 'Ask questions in natural language')
    )
    
    # Add configuration UI
    from config_ui import ConfigUI
    config_ui = ConfigUI(vanna_flask.flask_app, vn)
    print("✅ Configuration UI enabled at /settings")
    
    # Run Flask server
    vanna_flask.flask_app.run(
        host=flask_params['host'],
        port=flask_params['port'],
        debug=flask_params['debug']
    )


if __name__ == '__main__':
    print("\n🔍 Loading configuration from ui/ directory...\n")
    
    # Validate that config files exist
    from pathlib import Path
    
    config_dir = Path(__file__).parent / 'ui' / 'config'
    required_files = ['llm.json', 'database.json', 'flask.json', 'chromadb.json', 'training.json']
    
    missing_files = []
    for filename in required_files:
        if not (config_dir / filename).exists():
            missing_files.append(filename)
    
    if missing_files:
        print(f"❌ Missing configuration files in ui/config/:")
        for f in missing_files:
            print(f"   - {f}")
        print("\n💡 Make sure the ui/ directory is properly set up.")
        exit(1)
    
    # Run main setup
    main()
