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
from flask_cors import CORS

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
    
    def connect_to_oracle(self, user=None, password=None, dsn=None, **kwargs):
        """
        Enhanced Oracle connection with better connection management.
        Overrides base class to fix DPY-1001 connection issues.
        """
        try:
            import oracledb
        except ImportError:
            raise Exception("You need to install oracledb: pip install oracledb")
        
        if not dsn or not user or not password:
            raise Exception("Please provide DSN, user, and password for Oracle connection")
        
        # Store connection parameters for reconnection if needed
        self._oracle_params = {
            'user': user,
            'password': password,
            'dsn': dsn,
            **kwargs
        }
        
        # Create initial connection
        try:
            conn = oracledb.connect(**self._oracle_params)
            print(f"✅ Oracle connection established to {dsn}")
        except oracledb.Error as e:
            raise Exception(f"Failed to connect to Oracle: {e}")
        
        def run_sql_oracle(sql: str):
            """Execute SQL with automatic reconnection on connection errors"""
            import pandas as pd
            
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    # Check if connection is alive, reconnect if needed
                    nonlocal conn
                    try:
                        # Test connection with a simple ping
                        test_cursor = conn.cursor()
                        test_cursor.close()
                    except:
                        # Connection is dead, reconnect
                        print("⚠️  Connection lost, reconnecting...")
                        conn = oracledb.connect(**self._oracle_params)
                        print("✅ Reconnected to Oracle")
                    
                    # Clean up SQL (Oracle doesn't like trailing semicolons)
                    sql = sql.rstrip()
                    if sql.endswith(';'):
                        sql = sql[:-1]
                    
                    # Execute query
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    
                    # Check if this is a SELECT query
                    if cursor.description:
                        # Fetch results for SELECT queries
                        results = cursor.fetchall()
                        columns = [desc[0] for desc in cursor.description]
                        df = pd.DataFrame(results, columns=columns)
                        cursor.close()
                        return df
                    else:
                        # For non-SELECT queries (INSERT, UPDATE, DELETE)
                        conn.commit()
                        cursor.close()
                        return pd.DataFrame()
                        
                except oracledb.Error as e:
                    error_obj, = e.args
                    if attempt < max_retries - 1 and error_obj.code in [1001, 3113, 3114]:
                        # Connection errors - retry
                        print(f"⚠️  Oracle error {error_obj.code}, retrying...")
                        try:
                            conn = oracledb.connect(**self._oracle_params)
                        except:
                            pass
                        continue
                    else:
                        # Other errors or max retries reached
                        conn.rollback()
                        raise Exception(f"Oracle error: {e}")
                except Exception as e:
                    conn.rollback()
                    raise e
            
            raise Exception("Failed to execute SQL after retries")
        
        self.run_sql = run_sql_oracle
        self.run_sql_is_set = True
        self.dialect = "Oracle SQL"

# =============================================================================
# Main Setup
# =============================================================================

def main():
    print("\n" + "="*60)
    print("🤖 MyDBAssistant Setup - Using UI Configuration")
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
            
        elif db_params['type'] in ('postgres', 'postgresql'):
            # PostgreSQL connection
            vn.connect_to_postgres(
                host=db_params['host'],
                port=db_params['port'],
                dbname=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
            )
            
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
            
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = '{db_params['database']}'")
            table_count = result.iloc[0]['table_count'] if not result.empty else 0
            print(f"✅ Connected to MySQL database")
            print(f"✅ Using database: {db_params['database']} ({table_count} tables found)")
            
        elif db_params['type'] in ('mssql', 'sqlserver'):
            # Microsoft SQL Server connection
            vn.connect_to_mssql(
                server=db_params['host'],
                port=db_params['port'],
                database=db_params['database'],
                user=db_params['user'],
                password=db_params['password']
            )
            
            result = vn.run_sql(f"SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_params['schema']}'")
            table_count = result.iloc[0]['table_count'] if not result.empty else 0
            print(f"✅ Connected to SQL Server database")
            print(f"✅ Using schema: {db_params['schema']} ({table_count} tables found)")
            
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        print("\n💡 Check your database configuration in ui/config/database.json")
        return
    
    # Training control using JSON config
    if should_auto_train():
        print("\n📚 Auto-training enabled - checking training data...")
        try:
            # Check if training data already exists in ChromaDB
            existing_data = vn.get_training_data()
            
            if existing_data is not None and len(existing_data) > 0:
                print(f"✅ Training data already exists ({len(existing_data)} items)")
                print("   Skipping training to avoid duplicates")
                print("   💡 To force reload, delete chromadb/ folder and restart")
            else:
                print("   No existing training data found - loading from files...")
                stats = train_from_files(vn, verbose=True)
                print(f"\n✅ Training complete!")
                print(f"   - DDL files: {stats['ddl_loaded']}")
                print(f"   - Documentation: {stats['docs_loaded']}")
                print(f"   - Training pairs: {stats['pairs_loaded']}")
                if stats.get('errors', 0) > 0:
                    print(f"   ⚠️  Errors: {stats['errors']}")
        except Exception as e:
            print(f"⚠️  Training error: {e}")
            print("   Continuing anyway - you can train manually later")
    else:
        print("\n⏸️  Auto-training disabled in config")
        print("   💡 Enable in ui/config/training.json or train manually via /settings")
    
    # Launch Flask UI using config from ui/config/flask.json
    flask_params = get_flask_params()
    print(f"\n🌐 Launching Flask UI at http://{flask_params['host']}:{flask_params['port']}")
    print(f"   Settings page: http://{flask_params['host']}:{flask_params['port']}/settings")
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
        title=ui_settings.get('title', 'MyDBAssistant'),
        subtitle=ui_settings.get('subtitle', 'Ask questions in natural language'),
        logo=None,  # Remove Vanna logo
        show_training_data=True
    )
    
    # Enable CORS for Next.js frontend (allow all routes)
    CORS(vanna_flask.flask_app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],
         supports_credentials=True)
    print("✅ CORS enabled for Next.js frontend (localhost:3000)")
    
    # IMPORTANT: Add configuration UI FIRST (before any custom routes)
    from config_ui import ConfigUI
    config_ui = ConfigUI(vanna_flask.flask_app, vn)
    print("✅ Configuration UI enabled at /settings")
    
    # Import Flask at the top level for the custom routes
    from flask import Response, make_response, request
    
    # Inject custom CSS and JS into all HTML responses
    @vanna_flask.flask_app.after_request
    def inject_custom_assets(response):
        """Inject custom CSS/JS into HTML responses"""
        if response.content_type and 'text/html' in response.content_type:
            html = response.get_data(as_text=True)
            
            # Only inject if not already present
            if 'custom-branding-injected' not in html:
                # Inject CSS
                custom_css = """
                <style id="custom-branding-injected">
                /* Settings icon in top-right corner */
                .settings-icon-btn {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    width: 48px;
                    height: 48px;
                    background: #667eea;
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                    cursor: pointer;
                    transition: all 0.3s ease;
                    z-index: 9999;
                    text-decoration: none;
                }
                
                .settings-icon-btn:hover {
                    background: #5568d3;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
                }
                
                .settings-icon-btn svg {
                    width: 24px;
                    height: 24px;
                    color: white;
                }
                
                /* Hide Vanna logo/icon and text */
                img[src*="vanna"], 
                img[alt*="vanna"],
                img[alt*="Vanna"],
                img[alt*="Vanna Logo"],
                .logo img,
                [class*="logo"] img:first-child {
                    display: none !important;
                    visibility: hidden !important;
                }
                
                /* Hide checkmark icon */
                svg[class*="check"],
                .message-icon svg,
                [class*="icon"] svg path[d*="M5 13l4 4L19 7"] {
                    display: none !important;
                }
                </style>
                """
                
                # Inject JavaScript
                custom_js = """
                <script>
                (function() {
                    function initCustomUI() {
                        // Add settings icon button (top-right corner)
                        if (!document.getElementById('settings-icon-btn')) {
                            const settingsBtn = document.createElement('a');
                            settingsBtn.id = 'settings-icon-btn';
                            settingsBtn.href = '/settings';
                            settingsBtn.className = 'settings-icon-btn';
                            settingsBtn.title = 'Settings';
                            settingsBtn.innerHTML = `
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                            `;
                            document.body.appendChild(settingsBtn);
                        }
                        
                        // Replace page title
                        document.title = 'MyDBAssistant';
                        
                        // Remove all Vanna logos and checkmark icons (including alt text)
                        const imagesToRemove = document.querySelectorAll('img[src*="vanna"], img[alt*="vanna"], img[alt*="Vanna"], img[alt="Vanna Logo"]');
                        imagesToRemove.forEach(img => {
                            img.style.display = 'none';
                            img.style.visibility = 'hidden';
                            img.remove();
                        });
                        
                        // Remove checkmark SVG icons
                        const svgsToRemove = document.querySelectorAll('svg');
                        svgsToRemove.forEach(svg => {
                            const pathD = svg.querySelector('path')?.getAttribute('d');
                            if (pathD && (pathD.includes('M5 13l4 4L19 7') || pathD.includes('M9 12l2 2 4-4'))) {
                                svg.remove();
                            }
                        });
                        
                        // Replace all "Vanna" text with "MyDBAssistant"
                        const walker = document.createTreeWalker(
                            document.body,
                            NodeFilter.SHOW_TEXT,
                            null,
                            false
                        );
                        
                        const textNodes = [];
                        while (walker.nextNode()) {
                            if (walker.currentNode.nodeValue && walker.currentNode.nodeValue.includes('Vanna')) {
                                textNodes.push(walker.currentNode);
                            }
                        }
                        
                        textNodes.forEach(node => {
                            node.nodeValue = node.nodeValue.replace(/Vanna Logo|Vanna\\.AI|Vanna AI|Vanna/g, 'MyDBAssistant');
                        });
                    }
                    
                    // Run immediately
                    initCustomUI();
                    
                    // Run on page load
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', initCustomUI);
                    }
                    
                    // Re-run after dynamic content loads
                    const observer = new MutationObserver(function(mutations) {
                        initCustomUI();
                    });
                    
                    observer.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                })();
                </script>
                """
                
                # Inject before closing head tag
                if '</head>' in html:
                    html = html.replace('</head>', custom_css + '</head>')
                
                # Inject before closing body tag
                if '</body>' in html:
                    html = html.replace('</body>', custom_js + '</body>')
                
                response.set_data(html)
        
        return response
    
    # Add custom CSS injection route (for reference, but using after_request now)
    @vanna_flask.flask_app.route('/api/v0/custom_css', methods=['GET'])
    def get_custom_css():
        """Inject custom CSS to add settings icon"""
        css = """
        /* Settings icon in top-right corner */
        body::after {
            content: '';
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
        }
        
        .settings-icon-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            background: #667eea;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 9999;
            text-decoration: none;
        }
        
        .settings-icon-btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        }
        
        .settings-icon-btn svg {
            width: 24px;
            height: 24px;
            color: white;
        }
        
        /* Hide Vanna logo/icon and text */
        img[src*="vanna"], 
        img[alt*="vanna"],
        img[alt*="Vanna"],
        img[alt*="Vanna Logo"],
        .logo img,
        [class*="logo"] img:first-child {
            display: none !important;
        }
        
        /* Hide checkmark icon */
        svg[class*="check"],
        .message-icon svg,
        [class*="icon"] svg path[d*="M5 13l4 4L19 7"] {
            display: none !important;
        }
        
        """
        return Response(css, mimetype='text/css')
    
    # Add JavaScript injection for settings button and branding
    @vanna_flask.flask_app.route('/api/v0/custom_js', methods=['GET'])
    def get_custom_js():
        """Inject JavaScript to add settings button and remove Vanna branding"""
        js = """
        (function() {
            // Wait for DOM to load
            function initCustomUI() {
                // Add settings icon button (top-right corner)
                if (!document.getElementById('settings-icon-btn')) {
                    const settingsBtn = document.createElement('a');
                    settingsBtn.id = 'settings-icon-btn';
                    settingsBtn.href = '/settings';
                    settingsBtn.className = 'settings-icon-btn';
                    settingsBtn.title = 'Settings';
                    settingsBtn.innerHTML = `
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                    `;
                    document.body.appendChild(settingsBtn);
                }
                
                // Add inline Settings button below Open Debugger button
                const debuggerBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                    btn.textContent.includes('Open Debugger')
                );
                
                if (debuggerBtn && !document.getElementById('settings-btn-inline')) {
                    const settingsInlineBtn = document.createElement('a');
                    settingsInlineBtn.id = 'settings-btn-inline';
                    settingsInlineBtn.href = '/settings';
                    settingsInlineBtn.className = 'settings-btn-inline';
                    settingsInlineBtn.innerHTML = `
                        <svg style="display: inline-block; width: 16px; height: 16px; margin-right: 8px; vertical-align: middle;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                        Settings
                    `;
                    debuggerBtn.parentElement.appendChild(settingsInlineBtn);
                }
                
                // Replace page title
                document.title = 'MyDBAssistant';
                
                // Remove all Vanna logos and checkmark icons (including alt text)
                const imagesToRemove = document.querySelectorAll('img[src*="vanna"], img[alt*="vanna"], img[alt*="Vanna"], img[alt="Vanna Logo"]');
                imagesToRemove.forEach(img => img.remove());
                
                // Remove checkmark SVG icons (the one before "Go ahead and ask a question")
                const svgsToRemove = document.querySelectorAll('svg');
                svgsToRemove.forEach(svg => {
                    const pathD = svg.querySelector('path')?.getAttribute('d');
                    if (pathD && (pathD.includes('M5 13l4 4L19 7') || pathD.includes('M9 12l2 2 4-4'))) {
                        svg.remove();
                    }
                });
                
                // Replace all "Vanna" text with "MyDBAssistant" (including "Vanna Logo")
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                const textNodes = [];
                while (walker.nextNode()) {
                    if (walker.currentNode.nodeValue && walker.currentNode.nodeValue.includes('Vanna')) {
                        textNodes.push(walker.currentNode);
                    }
                }
                
                textNodes.forEach(node => {
                    node.nodeValue = node.nodeValue.replace(/Vanna Logo|Vanna\.AI|Vanna AI|Vanna/g, 'MyDBAssistant');
                });
            }
            
            // Run on page load
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initCustomUI);
            } else {
                initCustomUI();
            }
            
            // Re-run after dynamic content loads
            const observer = new MutationObserver(function(mutations) {
                initCustomUI();
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        })();
        """
        return Response(js, mimetype='application/javascript')
    
    print("✅ Custom branding and settings enabled")
    print("   └─ Settings icon in top-right corner")
    print("   └─ All 'Vanna' text replaced with 'MyDBAssistant'")
    print("   └─ Vanna logo removed")
    
    # Run Flask server
    vanna_flask.flask_app.run(
        host=flask_params['host'],
        port=flask_params['port'],
        debug=flask_params['debug']
    )

if __name__ == '__main__':
    # Validate configuration before starting
    print("\n🔍 Validating configuration from ui/config/*.json...")
    from ui.config_loader import ConfigLoader
    loader = ConfigLoader()
    
    # Check if auth token is set
    llm_config = loader.load_llm_config()
    if not llm_config.get('api_key') or llm_config.get('api_key') == 'your-api-key-here':
        print("\n⚠️  Warning: Copilot Socket Core API key not set!")
        print("   For localhost, this is optional (extension handles auth)")
        print("   For remote deployment, set it in ui/config/llm.json")
        print("\n   Get your token:")
        print("   cat .vscode/settings.json | grep authToken")
    
    main()
