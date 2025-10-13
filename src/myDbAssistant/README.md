# myDbAssistant - Vanna AI Database Assistant

Natural language SQL query generator using Vanna AI with Copilot Socket Core (VSCode Extension) and multiple database support.

## 🎯 Features

- **Natural Language to SQL**: Ask questions in plain English, get SQL queries
- **Multi-Database Support**: Oracle, PostgreSQL, MySQL, Microsoft SQL Server
- **ChromaDB Vector Store**: Local file-based vector storage (no external database needed)
- **Copilot Socket Core Integration**: Uses GitHub Copilot models via VSCode extension
- **Tool Calling Support**: Auto tool execution for enhanced query generation
- **Flask Web UI**: Clean, modern interface for asking questions and viewing results
- **JSON Configuration**: Flexible, easy-to-edit configuration system
- **Training Control**: Manual or automatic training modes
- **Auto-learning**: Learns from your questions and SQL pairs
- **Settings UI**: Web-based configuration management

## 📋 Prerequisites

1. **Python 3.11+**
2. **Database** - One of: Oracle, PostgreSQL, MySQL, or Microsoft SQL Server
3. **VS Code** with [Copilot Socket Core extension](https://github.com/CopilotGateway/CopilotGateway-Core) installed
4. **GitHub Copilot** subscription (required for Copilot Socket Core)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 2. Configure Copilot Socket Core

1. Open VS Code with this workspace
2. Install the Copilot Socket Core extension
3. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
4. Run: `Copilot Socket: Start Server`
5. Run: `Copilot Socket: Grant Access` (if prompted)
6. The server will start on `http://localhost:8080`
7. Verify health: `curl http://localhost:8080/health`

### 3. Update Configuration

Edit `ui/config/database.json` to match your database setup:
  "database": "XEPDB1",
  "schema": "hr",
  "user": "hr",
  "password": "hr123"
}
```

**For PostgreSQL:**
```json
{
  "type": "postgres",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "schema": "public",
  "user": "postgres",
  "password": "postgres"
}
```

**For MySQL:**
```json
{
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "mydb",
  "schema": "mydb",
  "user": "root",
  "password": "root"
}
```

**For Microsoft SQL Server:**
```json
{
  "type": "mssql",
  "host": "localhost",
  "port": 1433,
  "database": "mydb",
  "schema": "dbo",
  "user": "sa",
  "password": "YourStrong!Passw0rd"
}
```

**Required database drivers:**
```bash
pip install 'vanna[oracle]'    # For Oracle (note the quotes!)
pip install 'vanna[postgres]'  # For PostgreSQL  
pip install 'vanna[mysql]'     # For MySQL
pip install 'vanna[mssql]'     # For SQL Server
```

**Note for zsh users (macOS default):** The quotes are **required** because zsh treats `[]` as special characters.

Copilot Socket Core configuration is in `ui/config/llm.json`:

```json
{
  "api_key": "",
  "endpoint": "http://localhost:8080",
  "model": "copilot/gpt-4o",
  "max_tool_rounds": 5
}
```

**No API key required** for localhost. The extension handles authentication via VSCode.

See `docs/database-examples.md` for complete configuration examples.

### 4. Test Connections

Before running the main application, verify Copilot Socket Core is running:

```bash
# Check health
curl http://localhost:8080/health

# Check available models
curl http://localhost:8080/models
```

Expected output:
```
{"status": "ok"}
```
✅ PASS - Health
✅ PASS - Auth
✅ PASS - Models
✅ PASS - Chat
✅ PASS - Chromadb
✅ PASS - Oracle

🎉 All tests passed! Ready to run Vanna.
```

### 5. Run the Application

```bash
python3 quick_start_flask_ui.py
```

The Flask UI will launch at: **http://localhost:8084**

**🎛️ Settings Page:** Access **http://localhost:8084/settings** to configure all settings through the UI!

## 📖 Usage

### Web UI

1. Open http://localhost:8084 in your browser
2. Type a question in natural language:
   - "Show me all employees"
   - "Who are the highest paid employees?"
   - "How many employees are in each department?"
3. Click **Generate SQL**
4. Review the generated SQL
5. Click **Run SQL** to execute and see results
6. View data visualizations (if applicable)

### Settings UI (NEW!)

Access **http://localhost:8084/settings** to manage all configurations through a modern UI:

**🤖 LLM Settings**
- API Key / Auth Token
- Endpoint URL
- Model selection (GPT-4, GPT-5, Claude, etc.)
- Temperature, max tokens, timeout
- Test connection button

**🗄️ Database Settings**
- Database type (Oracle, PostgreSQL, MySQL, SQL Server)
- Host, port, database name
- Schema, username, password
- Test connection button

**📊 ChromaDB Settings**
- Storage path
- Number of results for SQL/DDL/Documentation retrieval

**🌐 Flask Settings**
- Host and port configuration
- Debug mode toggle
- UI title and subtitle
- LLM data visibility settings

**📚 Training Settings**
- Auto-train on startup toggle
- Training data path
- Load DDL/Documentation/Training pairs toggles
- Skip if exists option
- Verbose logging

All settings are saved to JSON files in `ui/config/` and can be edited through the UI or manually.

### Programmatic Usage

```python
from quick_start_flask import MyVanna
import config

# Initialize
vn = MyVanna(config_dict=config.get_vanna_config())

# Connect to database
vn.connect_to_oracle(
    dsn=f"{config.DATA_DB_CONFIG['host']}:{config.DATA_DB_CONFIG['port']}/{config.DATA_DB_CONFIG['database']}",
    user=config.DATA_DB_CONFIG['user'],
    password=config.DATA_DB_CONFIG['password']
)

# Generate SQL
sql = vn.generate_sql("Show me employees with salary > 10000")
print(sql)

# Run SQL
df = vn.run_sql(sql)
print(df.head())
```

## 🗂️ File Structure

```
src/myDbAssistant/
├── config.py                       # Centralized configuration
├── quick_start_flask.py            # Main Flask application
├── test_umbrella_connection.py     # Connection test script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
└── chromadb/                       # Vector database storage (auto-created)
```

## 🔧 Configuration Details

### ChromaDB (Vector Store)
- **Type**: Local file-based
- **Storage**: `./chromadb/` directory
- **No external database** required
- Automatically created on first run

### Oracle Database
- **Format**: `host:port/sid` or `host:port/service_name`
- **Example**: `localhost:1521/XEPDB1`
- **Schema**: Queries use schema prefix (e.g., `hr.employees`)

### Umbrella Gateway
- **Endpoint**: `http://localhost:8765` (default)
- **Auth**: Bearer token from `.vscode/settings.json`
- **Models**: 
  - `copilot/gpt-4` (most capable)
  - `copilot/gpt-5-mini` (fast, efficient)
  - `copilot/claude-sonnet-4` (alternative)
  - See all: http://localhost:8765/models

### Flask UI
- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `8084`
- **Debug**: Enabled by default (disable in production)

## 📚 Training Data

The application includes initial training data:

1. **DDL Schemas**: Table definitions for employees, departments, jobs
2. **Documentation**: Business rules and data definitions
3. **Q&A Pairs**: Example questions and SQL queries

To add more training:

```python
# Add new DDL
vn.train(ddl="CREATE TABLE my_table (...)")

# Add documentation
vn.train(documentation="Business rule: ...")

# Add Q&A pair
vn.train(
    question="What is the total revenue?",
    sql="SELECT SUM(amount) FROM sales"
)
```

Training data is stored persistently in ChromaDB and reused across sessions.

## 🐛 Troubleshooting

### "Cannot connect to Copilot Socket Core"
- **Solution**: Start the server in VS Code:
  - `Cmd+Shift+P` → `Copilot Socket: Start Server`
  - Wait for "Server started on port 8080" notification
  - Check health: `curl http://localhost:8080/health`

### "Copilot not available"
- **Solution**: Grant access to Copilot:
  - `Cmd+Shift+P` → `Copilot Socket: Grant Access`
  - Verify GitHub Copilot subscription is active
  - Restart VSCode if needed

### "Model not available"
- **Solution**: Check available models:
  ```bash
  curl http://localhost:8080/models
  ```
  Use one of: `copilot/gpt-4o`, `copilot/claude-sonnet-4`, `copilot/gpt-3.5-turbo`

### "Cannot connect to database"
- **Solutions**:
  - Verify database is running
  - Check credentials in `ui/config/database.json`
  - Test connection manually:
    - Oracle: `sqlplus hr/hr123@localhost:1521/XEPDB1`
    - PostgreSQL: `psql -h localhost -U postgres -d mydb`
    - MySQL: `mysql -h localhost -u root -p`

### "ChromaDB errors"
- **Solution**: Delete and recreate:
  ```bash
  rm -rf chromadb/
  python3 quick_start_flask_ui.py  # Will recreate automatically
  ```

### "Port 8084 already in use"
- **Solution**: Change port in `ui/config/flask.json`:
  ```json
  {"port": 8085}
  ```
  Or via Settings UI: http://localhost:8084/settings

## 🔒 Security Notes

## 🧪 Testing the Migration

We've migrated from Umbrella Gateway to Copilot Socket Core. Test your setup:

### Quick Test (Recommended)

```bash
# Run comprehensive test suite (7 tests)
python3 test_copilot_socket_core.py

# Or quick smoke test
python3 quick_test.py

# Or compare both APIs (if you have Umbrella Gateway)
python3 compare_apis.py
```

**Expected output:**
```
✅ All tests passed! (7/7)
🎉 Copilot Socket Core is ready to use!
```

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test available models
curl http://localhost:8080/models

# Test in Python
python3
>>> from quick_start_flask_ui import MyCustomLLM
>>> from ui import get_vanna_config
>>> llm = MyCustomLLM(config_dict=get_vanna_config())
>>> llm._ensure_session()  # Creates session automatically
>>> response = llm.submit_prompt([llm.user_message("Hello")])
>>> print(response)
```

**Full testing guide:** See `TESTING_MIGRATION.md`

## 📚 Documentation

- **User Guide**: This README
- **Testing Guide**: `TESTING_MIGRATION.md` - Complete test procedures
- **Settings UI Guide**: `docs/settings-ui-guide.md` - Web UI configuration
- **Migration Guide**: `docs/MIGRATION_TO_COPILOT_SOCKET_CORE.md` - API migration details
- **Technical Spec**: `docs/TECHNICAL_SPEC.md` - Copilot Socket Core API spec
- **Migration Summary**: `docs/LLM_API_MIGRATION_SUMMARY.md` - What changed

## ⚙️ Configuration Files

All configurations are in JSON format under `ui/config/`:

- **`llm.json`**: Copilot Socket Core settings (API endpoint, model, tool calling)
- **`database.json`**: Database connection details (Oracle, PostgreSQL, MySQL, SQL Server)
- **`chromadb.json`**: Vector store settings (retrieval parameters)
- **`flask.json`**: Web server settings (host, port, debug mode)
- **`training.json`**: Training control (auto-train toggle, data paths)

**Edit via:**
1. **Web UI**: http://localhost:8084/settings (recommended)
2. **Direct edit**: Modify JSON files manually
3. **Programmatic**: Use `ConfigLoader` class

## ⚠️ Production Considerations

⚠️ **Important**: This is a development setup. For production:

1. **Never commit credentials**:
   - Use environment variables or secret management
   - `ui/config/` directory is in `.gitignore`

2. **Disable Flask debug mode**:
   ```json
   // ui/config/flask.json
   {"debug": false, ...}
   ```

3. **Use HTTPS** for production deployments

4. **Restrict network access**:
   ```json
   // ui/config/flask.json
   {"host": "127.0.0.1", ...}  // Localhost only
   ```

5. **Sanitize user input** to prevent SQL injection

6. **Secure Settings UI**:
   - Add authentication (not included)
   - Restrict access via firewall
   - Use environment variables for sensitive data

## 📦 Dependencies

### Core
- `vanna` - RAG framework for SQL generation
- `chromadb` - Vector database
- `oracledb`, `psycopg2-binary`, `pymysql`, `pyodbc` - Database drivers
- `Flask` - Web framework

### LLM & Utilities
- `requests` - HTTP client for Copilot Socket Core API
- `pandas` - Data manipulation
- `plotly` - Visualizations
- `sqlparse` - SQL parsing

**Install all:**
```bash
pip install -r requirements.txt

# Or minimal install
pip install vanna requests flask chromadb

# Database-specific
pip install 'vanna[oracle]'     # Oracle
pip install 'vanna[postgres]'   # PostgreSQL
pip install 'vanna[mysql]'      # MySQL
pip install 'vanna[mssql]'      # SQL Server
```

See `requirements.txt` for complete list with versions.

## 🤝 Contributing

This is a customized deployment of Vanna AI. For the main project:
- **Vanna GitHub**: https://github.com/vanna-ai/vanna
- **Documentation**: https://vanna.ai/docs

## 📄 License

This implementation follows Vanna AI's MIT License.

## 🆘 Support & Troubleshooting

### Common Issues

**1. "Cannot connect to server"**
```bash
# Check if Copilot Socket Core is running
curl http://localhost:8080/health

# Start server in VSCode
# Cmd+Shift+P → "Copilot Socket: Start Server"
```

**2. "Empty response from LLM"**
```bash
# Check available models
curl http://localhost:8080/models

# Update model in ui/config/llm.json
```

**3. "Module not found: requests"**
```bash
pip install requests
```

**4. "Test failed"**
```bash
# Run comprehensive test
python3 test_copilot_socket_core.py

# See detailed troubleshooting
cat TESTING_MIGRATION.md
```

### Documentation

- **Testing Guide**: `TESTING_MIGRATION.md`
- **Settings UI**: `docs/settings-ui-guide.md`
- **Migration Guide**: `docs/MIGRATION_TO_COPILOT_SOCKET_CORE.md`
- **API Spec**: `docs/TECHNICAL_SPEC.md`
- **Copilot Instructions**: `.github/copilot-instructions.md` (parent directory)

### Getting Help

For issues with:
- **Vanna framework**: https://github.com/vanna-ai/vanna/issues
- **Copilot Socket Core**: https://github.com/CopilotGateway/CopilotGateway-Core/issues
- **This deployment**: See troubleshooting section above

## 🎓 Learn More

- **Vanna Docs**: https://vanna.ai/docs
- **Copilot Instructions**: See `.github/copilot-instructions.md` in parent directory
- **Setup Guide**: See `SETUP_COMPLETE.md` in parent directory
- **Quick Reference**: See `QUICK_START.md` in parent directory
