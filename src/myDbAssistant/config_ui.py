#!/usr/bin/env python3
"""
Configuration UI Extension for Vanna Flask App
Adds endpoints and UI for managing all configuration settings
"""

from flask import jsonify, request, render_template_string
from ui import ConfigLoader
import json
from pathlib import Path


class ConfigUI:
    """Add configuration management UI to Flask app"""
    
    def __init__(self, flask_app, vn_instance):
        self.app = flask_app
        self.vn = vn_instance
        self.config_loader = ConfigLoader()
        self.register_routes()
    
    def register_routes(self):
        """Register all configuration routes"""
        
        # Get all configurations
        self.app.route('/api/v0/get_config', methods=['GET'])(self.get_all_config)
        
        # Update specific configurations
        self.app.route('/api/v0/update_llm_config', methods=['POST'])(self.update_llm_config)
        self.app.route('/api/v0/update_database_config', methods=['POST'])(self.update_database_config)
        self.app.route('/api/v0/update_chromadb_config', methods=['POST'])(self.update_chromadb_config)
        self.app.route('/api/v0/update_flask_config', methods=['POST'])(self.update_flask_config)
        self.app.route('/api/v0/update_training_config', methods=['POST'])(self.update_training_config)
        
        # Test connections
        self.app.route('/api/v0/test_database_connection', methods=['POST'])(self.test_database_connection)
        self.app.route('/api/v0/test_llm_connection', methods=['POST'])(self.test_llm_connection)
        
        # Load training data
        self.app.route('/api/v0/load_training_data', methods=['POST'])(self.load_training_data)
        
        # Settings page
        self.app.route('/settings', methods=['GET'])(self.settings_page)
    
    def get_all_config(self):
        """Get all current configurations"""
        try:
            return jsonify({
                'llm': self.config_loader.load_llm_config(),
                'database': self.config_loader.load_database_config(),
                'chromadb': self.config_loader.load_chromadb_config(),
                'flask': self.config_loader.load_flask_config(),
                'training': self.config_loader.load_training_config()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_llm_config(self):
        """Update LLM configuration"""
        try:
            data = request.json
            self.config_loader.update_llm_config(data)
            return jsonify({'message': 'LLM configuration updated successfully', 'config': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_database_config(self):
        """Update database configuration"""
        try:
            data = request.json
            self.config_loader.update_database_config(data)
            return jsonify({'message': 'Database configuration updated successfully', 'config': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_chromadb_config(self):
        """Update ChromaDB configuration"""
        try:
            data = request.json
            self.config_loader.update_chromadb_config(data)
            return jsonify({'message': 'ChromaDB configuration updated successfully', 'config': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_flask_config(self):
        """Update Flask configuration"""
        try:
            data = request.json
            self.config_loader.update_flask_config(data)
            return jsonify({'message': 'Flask configuration updated successfully', 'config': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_training_config(self):
        """Update training configuration"""
        try:
            data = request.json
            self.config_loader.update_training_config(data)
            return jsonify({'message': 'Training configuration updated successfully', 'config': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def test_database_connection(self):
        """Test database connection with provided parameters"""
        try:
            data = request.json
            db_type = data.get('type')
            
            # Import database driver based on type
            if db_type == 'oracle':
                import oracledb
                dsn = f"{data['host']}:{data['port']}/{data['database']}"
                conn = oracledb.connect(user=data['user'], password=data['password'], dsn=dsn)
                conn.close()
                return jsonify({'success': True, 'message': 'Oracle connection successful'})
            
            elif db_type in ('postgres', 'postgresql'):
                import psycopg2
                conn = psycopg2.connect(
                    host=data['host'],
                    port=data['port'],
                    database=data['database'],
                    user=data['user'],
                    password=data['password']
                )
                conn.close()
                return jsonify({'success': True, 'message': 'PostgreSQL connection successful'})
            
            elif db_type == 'mysql':
                import pymysql
                conn = pymysql.connect(
                    host=data['host'],
                    port=int(data['port']),
                    database=data['database'],
                    user=data['user'],
                    password=data['password']
                )
                conn.close()
                return jsonify({'success': True, 'message': 'MySQL connection successful'})
            
            elif db_type in ('mssql', 'sqlserver'):
                import pyodbc
                conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={data['host']},{data['port']};DATABASE={data['database']};UID={data['user']};PWD={data['password']}"
                conn = pyodbc.connect(conn_str)
                conn.close()
                return jsonify({'success': True, 'message': 'SQL Server connection successful'})
            
            else:
                return jsonify({'success': False, 'message': f'Unsupported database type: {db_type}'}), 400
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    def test_llm_connection(self):
        """Test LLM connection with provided parameters"""
        try:
            import requests
            data = request.json
            
            # Test health endpoint (Copilot Socket Core)
            health_url = f"{data['endpoint']}/health"
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                # Try to get models list for additional verification
                try:
                    models_url = f"{data['endpoint']}/models"
                    models_response = requests.get(models_url, timeout=5)
                    if models_response.status_code == 200:
                        models_data = models_response.json()
                        available_models = [m.get('id', m.get('name', '')) for m in models_data.get('models', [])]
                        return jsonify({
                            'success': True, 
                            'message': f'Copilot Socket Core is healthy. Available models: {", ".join(available_models)}'
                        })
                except:
                    pass
                
                return jsonify({'success': True, 'message': 'Copilot Socket Core endpoint is healthy'})
            else:
                return jsonify({'success': False, 'message': f'Health check failed: {response.status_code}'}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    def load_training_data(self):
        """Load training data from configured path"""
        try:
            from ui import train_from_files
            
            # Get current training config
            training_config = self.config_loader.load_training_config()
            
            # Load training data
            stats = train_from_files(self.vn, verbose=True)
            
            message = f"Training data loaded successfully! "
            message += f"DDL files: {stats.get('ddl_loaded', 0)}, "
            message += f"Documentation: {stats.get('docs_loaded', 0)}, "
            message += f"Training pairs: {stats.get('pairs_loaded', 0)}"
            
            if stats.get('errors'):
                message += f" | Errors: {len(stats['errors'])}"
            
            return jsonify({
                'success': True, 
                'message': message,
                'stats': stats
            })
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error loading training data: {str(e)}'}), 500

    def settings_page(self):
        """Render settings page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyDBAssistant Settings</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .header p {
            color: #666;
            font-size: 16px;
        }
// ...existing code...
        <a href="/" class="back-link">← Back to MyDBAssistant</a>
        
        <div class="header">
            <h1>⚙️ MyDBAssistant Settings</h1>
            <p>Manage all configuration settings from one place</p>
        </div>
        
        <div id="alert" class="alert"></div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('llm')">🤖 LLM</button>
            <button class="tab" onclick="showTab('database')">🗄️ Database</button>
            <button class="tab" onclick="showTab('chromadb')">📊 ChromaDB</button>
            <button class="tab" onclick="showTab('flask')">🌐 Flask</button>
            <button class="tab" onclick="showTab('training')">📚 Training</button>
        </div>
        
        <!-- LLM Configuration -->
        <div id="llm-section" class="config-section active">
            <h2>🤖 LLM Configuration</h2>
            <p style="color: #666; margin-bottom: 20px;">Configure Copilot Socket Core connection</p>
            
            <div class="form-group">
                <label>API Key (Optional)</label>
                <input type="password" id="llm-api-key" placeholder="Leave empty for localhost">
                <small>NOT required for localhost. Only needed for remote deployment.</small>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>Endpoint</label>
                    <input type="text" id="llm-endpoint" value="http://localhost:8765">
                    <small>Copilot Socket Core server URL</small>
                </div>
                
                <div class="form-group">
                    <label>Model</label>
                    <select id="llm-model">
                        <option value="copilot/gpt-4.1">copilot/gpt-4.1</option>
                        <option value="copilot/gpt-4o">copilot/gpt-4o</option>
                        <option value="copilot/grok-code-fast-1">copilot/grok-code-fast-1</option>
                        <option value="copilot/gpt-5-mini" selected>copilot/gpt-5-mini (Default)</option>
                        <option value="copilot/claude-sonnet-4.5">copilot/claude-sonnet-4.5</option>
                        <option value="copilot/gpt-5">copilot/gpt-5</option>
                    </select>
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>Temperature (0-1)</label>
                    <input type="number" id="llm-temperature" min="0" max="1" step="0.1" value="0.5">
                    <small>Higher = more creative</small>
                </div>
                
                <div class="form-group">
                    <label>Max Tokens</label>
                    <input type="number" id="llm-max-tokens" value="50000">
                </div>
                
                <div class="form-group">
                    <label>Max Tool Rounds</label>
                    <input type="number" id="llm-max-tool-rounds" min="1" max="200" value="20">
                    <small>Tool calling iterations (1-200)</small>
                </div>
                
                <div class="form-group">
                    <label>Timeout (seconds)</label>
                    <input type="number" id="llm-timeout" value="60">
                </div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-test" onclick="testLLM()">🧪 Test Connection</button>
                <button class="btn btn-primary" onclick="saveLLM()">💾 Save LLM Config</button>
            </div>
        </div>
        
        <!-- Database Configuration -->
        <div id="database-section" class="config-section">
            <h2>🗄️ Database Configuration</h2>
            <p style="color: #666; margin-bottom: 20px;">Configure your data database connection</p>
            
            <div class="form-group">
                <label>Database Type</label>
                <select id="db-type" onchange="updateDBFields()">
                    <option value="oracle">Oracle</option>
                    <option value="postgres">PostgreSQL</option>
                    <option value="mysql">MySQL</option>
                    <option value="mssql">Microsoft SQL Server</option>
                </select>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>Host</label>
                    <input type="text" id="db-host" value="localhost">
                </div>
                
                <div class="form-group">
                    <label>Port</label>
                    <input type="number" id="db-port" value="1521">
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>Database / SID</label>
                    <input type="text" id="db-database" placeholder="XEPDB1">
                </div>
                
                <div class="form-group">
                    <label>Schema</label>
                    <input type="text" id="db-schema" placeholder="hr">
                </div>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" id="db-user" placeholder="hr">
                </div>
                
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="db-password" placeholder="password">
                </div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-test" onclick="testDatabase()">🧪 Test Connection</button>
                <button class="btn btn-primary" onclick="saveDatabase()">💾 Save Database Config</button>
            </div>
        </div>
        
        <!-- ChromaDB Configuration -->
        <div id="chromadb-section" class="config-section">
            <h2>📊 ChromaDB Configuration</h2>
            <p style="color: #666; margin-bottom: 20px;">Configure vector database settings</p>
            
            <div class="form-group">
                <label>Storage Path</label>
                <input type="text" id="chromadb-path" value="./chromadb">
                <small>Local directory for vector storage</small>
            </div>
            
            <div class="row">
                <div class="form-group">
                    <label>SQL Results</label>
                    <input type="number" id="chromadb-sql-results" value="5" min="1" max="20">
                    <small>Number of similar SQL examples to retrieve</small>
                </div>
                
                <div class="form-group">
                    <label>DDL Results</label>
                    <input type="number" id="chromadb-ddl-results" value="5" min="1" max="20">
                    <small>Number of DDL schemas to retrieve</small>
                </div>
                
                <div class="form-group">
                    <label>Documentation Results</label>
                    <input type="number" id="chromadb-doc-results" value="5" min="1" max="20">
                    <small>Number of documentation snippets to retrieve</small>
                </div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" onclick="saveChromaDB()">💾 Save ChromaDB Config</button>
            </div>
        </div>
        
        <!-- Flask Configuration -->
        <div id="flask-section" class="config-section">
            <h2>🌐 Flask Configuration</h2>
            <p style="color: #666; margin-bottom: 20px;">Configure web server settings (requires restart)</p>
            
            <div class="row">
                <div class="form-group">
                    <label>Host</label>
                    <input type="text" id="flask-host" value="0.0.0.0">
                    <small>0.0.0.0 = all interfaces, 127.0.0.1 = localhost only</small>
                </div>
                
                <div class="form-group">
                    <label>Port</label>
                    <input type="number" id="flask-port" value="8084">
                </div>
            </div>
            
            <div class="form-group">
                <label>Debug Mode</label>
                <select id="flask-debug">
                    <option value="true">Enabled (Development)</option>
                    <option value="false">Disabled (Production)</option>
                </select>
                <small>⚠️ Disable in production for security</small>
            </div>
            
            <div class="form-group">
                <label>Page Title</label>
                <input type="text" id="flask-title" value="Vanna AI - Database Assistant">
            </div>
            
            <div class="form-group">
                <label>Subtitle</label>
                <input type="text" id="flask-subtitle" value="Ask questions in natural language">
            </div>
            
            <div class="form-group">
                <label>Allow LLM to See Data</label>
                <select id="flask-allow-data">
                    <option value="true">Yes (Better results)</option>
                    <option value="false">No (More secure)</option>
                </select>
                <small>When enabled, LLM can see sample data for better SQL generation</small>
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" onclick="saveFlask()">💾 Save Flask Config</button>
                <button class="btn btn-secondary" onclick="restartServer()">🔄 Restart Server</button>
            </div>
        </div>
        
        <!-- Training Configuration -->
        <div id="training-section" class="config-section">
            <h2>📚 Training Configuration</h2>
            <p style="color: #666; margin-bottom: 20px;">Configure training data loading</p>
            
            <div class="form-group">
                <label>Auto-Train on Startup</label>
                <select id="training-auto">
                    <option value="true">Enabled</option>
                    <option value="false">Disabled</option>
                </select>
                <small>Automatically load training data when server starts</small>
            </div>
            
            <div class="form-group">
                <label>Training Data Path</label>
                <input type="text" id="training-path" value="../trainingMyDb">
                <small>Directory containing DDL, documentation, and Q&A pairs</small>
            </div>
            
            <div class="form-group">
                <label>Load DDL Files</label>
                <select id="training-ddl">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Load Documentation</label>
                <select id="training-docs">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Load Training Pairs</label>
                <select id="training-pairs">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Skip if Exists</label>
                <select id="training-skip">
                    <option value="true">Yes (Faster)</option>
                    <option value="false">No (Force reload)</option>
                </select>
                <small>Skip if training data already loaded in ChromaDB</small>
            </div>
            
            <div class="form-group">
                <label>Verbose Logging</label>
                <select id="training-verbose">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            
            <div class="button-group">
                <button class="btn btn-test" onclick="loadTrainingDataNow()">🚀 Load Training Data Now</button>
                <button class="btn btn-primary" onclick="saveTraining()">💾 Save Training Config</button>
            </div>
        </div>
        
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 10px; color: #666;">Processing...</p>
        </div>
    </div>
    
    <script>
        // Database port mapping
        const DB_PORTS = {
            'oracle': 1521,
            'postgres': 5432,
            'mysql': 3306,
            'mssql': 1433
        };
        
        // Load configuration on page load
        window.onload = async () => {
            await loadConfig();
        };
        
        async function loadConfig() {
            try {
                const response = await fetch('/api/v0/get_config');
                const config = await response.json();
                
                // Load LLM config
                if (config.llm) {
                    document.getElementById('llm-api-key').value = config.llm.api_key || '';
                    document.getElementById('llm-endpoint').value = config.llm.endpoint || 'http://localhost:8765';
                    document.getElementById('llm-model').value = config.llm.model || 'copilot/gpt-5-mini';
                    document.getElementById('llm-temperature').value = config.llm.temperature || 0.5;
                    document.getElementById('llm-max-tokens').value = config.llm.max_tokens || 50000;
                    document.getElementById('llm-max-tool-rounds').value = config.llm.max_tool_rounds || 20;
                    document.getElementById('llm-timeout').value = config.llm.timeout || 60;
                }
                
                // Load Database config
                if (config.database) {
                    document.getElementById('db-type').value = config.database.type || 'oracle';
                    document.getElementById('db-host').value = config.database.host || 'localhost';
                    document.getElementById('db-port').value = config.database.port || 1521;
                    document.getElementById('db-database').value = config.database.database || '';
                    document.getElementById('db-schema').value = config.database.schema || '';
                    document.getElementById('db-user').value = config.database.user || '';
                    document.getElementById('db-password').value = config.database.password || '';
                }
                
                // Load ChromaDB config
                if (config.chromadb) {
                    document.getElementById('chromadb-path').value = config.chromadb.path || './chromadb';
                    document.getElementById('chromadb-sql-results').value = config.chromadb.n_results_sql || 5;
                    document.getElementById('chromadb-ddl-results').value = config.chromadb.n_results_ddl || 5;
                    document.getElementById('chromadb-doc-results').value = config.chromadb.n_results_documentation || 5;
                }
                
                // Load Flask config
                if (config.flask) {
                    document.getElementById('flask-host').value = config.flask.host || '0.0.0.0';
                    document.getElementById('flask-port').value = config.flask.port || 8084;
                    document.getElementById('flask-debug').value = config.flask.debug ? 'true' : 'false';
                    
                    if (config.flask.ui_settings) {
                        document.getElementById('flask-title').value = config.flask.ui_settings.title || '';
                        document.getElementById('flask-subtitle').value = config.flask.ui_settings.subtitle || '';
                        document.getElementById('flask-allow-data').value = config.flask.ui_settings.allow_llm_to_see_data ? 'true' : 'false';
                    }
                }
                
                // Load Training config
                if (config.training) {
                    document.getElementById('training-auto').value = config.training.auto_train_on_startup ? 'true' : 'false';
                    document.getElementById('training-path').value = config.training.training_data_path || '../trainingMyDb';
                    
                    if (config.training.training_settings) {
                        document.getElementById('training-ddl').value = config.training.training_settings.load_ddl ? 'true' : 'false';
                        document.getElementById('training-docs').value = config.training.training_settings.load_documentation ? 'true' : 'false';
                        document.getElementById('training-pairs').value = config.training.training_settings.load_training_pairs ? 'true' : 'false';
                        document.getElementById('training-skip').value = config.training.training_settings.skip_if_exists ? 'true' : 'false';
                        document.getElementById('training-verbose').value = config.training.training_settings.verbose ? 'true' : 'false';
                    }
                }
            } catch (error) {
                showAlert('Error loading configuration: ' + error.message, 'error');
            }
        }
        
        function showTab(tabName) {
            // Hide all sections
            document.querySelectorAll('.config-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(tabName + '-section').classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        function updateDBFields() {
            const dbType = document.getElementById('db-type').value;
            document.getElementById('db-port').value = DB_PORTS[dbType];
        }
        
        function showAlert(message, type) {
            const alert = document.getElementById('alert');
            alert.className = `alert alert-${type} show`;
            alert.textContent = message;
            
            setTimeout(() => {
                alert.classList.remove('show');
            }, 5000);
        }
        
        function showLoading() {
            document.getElementById('loading').classList.add('show');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('show');
        }
        
        async function saveLLM() {
            showLoading();
            try {
                const data = {
                    api_key: document.getElementById('llm-api-key').value,
                    endpoint: document.getElementById('llm-endpoint').value,
                    model: document.getElementById('llm-model').value,
                    temperature: parseFloat(document.getElementById('llm-temperature').value),
                    max_tokens: parseInt(document.getElementById('llm-max-tokens').value),
                    max_tool_rounds: parseInt(document.getElementById('llm-max-tool-rounds').value),
                    timeout: parseInt(document.getElementById('llm-timeout').value)
                };
                
                const response = await fetch('/api/v0/update_llm_config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (response.ok) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function saveDatabase() {
            showLoading();
            try {
                const data = {
                    type: document.getElementById('db-type').value,
                    host: document.getElementById('db-host').value,
                    port: parseInt(document.getElementById('db-port').value),
                    database: document.getElementById('db-database').value,
                    schema: document.getElementById('db-schema').value,
                    user: document.getElementById('db-user').value,
                    password: document.getElementById('db-password').value
                };
                
                const response = await fetch('/api/v0/update_database_config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (response.ok) {
                    showAlert('✅ ' + result.message + ' (Restart server to apply)', 'success');
                } else {
                    showAlert('❌ ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function saveChromaDB() {
            showLoading();
            try {
                const data = {
                    path: document.getElementById('chromadb-path').value,
                    n_results_sql: parseInt(document.getElementById('chromadb-sql-results').value),
                    n_results_ddl: parseInt(document.getElementById('chromadb-ddl-results').value),
                    n_results_documentation: parseInt(document.getElementById('chromadb-doc-results').value)
                };
                
                const response = await fetch('/api/v0/update_chromadb_config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (response.ok) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function saveFlask() {
            showLoading();
            try {
                const data = {
                    host: document.getElementById('flask-host').value,
                    port: parseInt(document.getElementById('flask-port').value),
                    debug: document.getElementById('flask-debug').value === 'true',
                    ui_settings: {
                        title: document.getElementById('flask-title').value,
                        subtitle: document.getElementById('flask-subtitle').value,
                        allow_llm_to_see_data: document.getElementById('flask-allow-data').value === 'true'
                    }
                };
                
                const response = await fetch('/api/v0/update_flask_config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (response.ok) {
                    showAlert('✅ ' + result.message + ' (Restart server to apply)', 'success');
                } else {
                    showAlert('❌ ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function saveTraining() {
            showLoading();
            try {
                const data = {
                    auto_train_on_startup: document.getElementById('training-auto').value === 'true',
                    training_data_path: document.getElementById('training-path').value,
                    training_settings: {
                        load_ddl: document.getElementById('training-ddl').value === 'true',
                        load_documentation: document.getElementById('training-docs').value === 'true',
                        load_training_pairs: document.getElementById('training-pairs').value === 'true',
                        skip_if_exists: document.getElementById('training-skip').value === 'true',
                        verbose: document.getElementById('training-verbose').value === 'true'
                    }
                };
                
                const response = await fetch('/api/v0/update_training_config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (response.ok) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.error, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function loadTrainingDataNow() {
            if (!confirm('🚀 This will load training data from the configured path. This may take a few moments. Continue?')) {
                return;
            }
            
            showLoading();
            try {
                const response = await fetch('/api/v0/load_training_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.message, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function testLLM() {
            showLoading();
            try {
                const data = {
                    endpoint: document.getElementById('llm-endpoint').value
                };
                
                const response = await fetch('/api/v0/test_llm_connection', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.message, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        async function testDatabase() {
            showLoading();
            try {
                const data = {
                    type: document.getElementById('db-type').value,
                    host: document.getElementById('db-host').value,
                    port: parseInt(document.getElementById('db-port').value),
                    database: document.getElementById('db-database').value,
                    user: document.getElementById('db-user').value,
                    password: document.getElementById('db-password').value
                };
                
                const response = await fetch('/api/v0/test_database_connection', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('✅ ' + result.message, 'success');
                } else {
                    showAlert('❌ ' + result.message, 'error');
                }
            } catch (error) {
                showAlert('❌ Error: ' + error.message, 'error');
            } finally {
                hideLoading();
            }
        }
        
        function restartServer() {
            if (confirm('⚠️ This will restart the server. Continue?')) {
                showAlert('🔄 Server restart must be done manually. Save all configs and run: python3 quick_start_flask_ui.py', 'info');
            }
        }
    </script>
</body>
</html>
        """
        return render_template_string(html)
