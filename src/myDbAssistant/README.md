# myDbAssistant - Vanna AI Database Assistant

Natural language SQL query generator using Vanna AI with Umbrella Gateway (GitHub Copilot models) and Oracle Database.

## 🎯 Features

- **Natural Language to SQL**: Ask questions in plain English, get SQL queries
- **Oracle Database Support**: Pre-configured for Oracle HR schema
- **ChromaDB Vector Store**: Local file-based vector storage (no external database needed)
- **Umbrella Gateway Integration**: Uses GitHub Copilot models via VS Code extension
- **Flask Web UI**: Clean, modern interface for asking questions and viewing results
- **Auto-training**: Learns from your questions and SQL pairs

## 📋 Prerequisites

1. **Python 3.11+**
2. **Oracle Database** running with HR schema (or your own database)
3. **VS Code** with [Umbrella Gateway extension](https://github.com/vanna-ai/umbrella-gateway) installed
4. **GitHub Copilot** subscription (required for Umbrella Gateway)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 2. Configure Umbrella Gateway

1. Open VS Code with this workspace
2. Install the Umbrella Gateway extension
3. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
4. Run: `Umbrella Gateway: Start Server`
5. Run: `Umbrella Gateway: Grant Access` (if prompted)
6. The server will start on `http://localhost:8765`

### 3. Update Configuration

Edit `config.py` to match your setup:

```python
# LLM Configuration (Umbrella Gateway)
LLM_CONFIG = {
    'api_key': 'sk-abcdef123456',  # Your actual token
    'endpoint': 'http://localhost:8765',
    'model': 'copilot/gpt-5-mini',  # Or another available model
    'temperature': 0.7
}

# Oracle Database Configuration
DATA_DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'database': 'XEPDB1',  # Your SID or service name
    'schema': 'hr',         # Your schema
    'user': 'hr',           # Your username
    'password': 'hr123'     # Your password
}
```

**Finding your auth token:**
```bash
# Check your VS Code settings
cat ../.vscode/settings.json | grep authToken
```

### 4. Test Connections

Before running the main application, verify all connections:

```bash
python test_umbrella_connection.py
```

Expected output:
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
python quick_start_flask.py
```

The Flask UI will launch at: **http://localhost:8084**

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

### "Cannot connect to Umbrella Gateway"
- **Solution**: Start the server in VS Code:
  - `Cmd+Shift+P` → `Umbrella Gateway: Start Server`
  - Wait for "Server started on port 8765" notification

### "401 Unauthorized"
- **Solution**: Update auth token in `config.py`:
  ```bash
  cat ../.vscode/settings.json | grep authToken
  ```
  Copy the token value to `LLM_CONFIG['api_key']`

### "403 Forbidden"
- **Solution**: Grant access to the extension:
  - `Cmd+Shift+P` → `Umbrella Gateway: Grant Access`
  - Restart the server

### "Cannot connect to Oracle"
- **Solutions**:
  - Verify Oracle is running: `lsnrctl status`
  - Check credentials in `config.py`
  - Test connection: `sqlplus hr/hr123@localhost:1521/XEPDB1`

### "ChromaDB errors"
- **Solution**: Delete and recreate:
  ```bash
  rm -rf chromadb/
  python quick_start_flask.py  # Will recreate automatically
  ```

### "Port 8084 already in use"
- **Solution**: Change port in `config.py`:
  ```python
  FLASK_CONFIG = {'port': 8085, ...}
  ```

## 🔒 Security Notes

⚠️ **Important**: This is a development setup. For production:

1. **Never commit credentials**:
   - Use environment variables or secret management
   - Add `config.py` to `.gitignore` (already done)

2. **Disable Flask debug mode**:
   ```python
   FLASK_CONFIG = {'debug': False, ...}
   ```

3. **Use HTTPS** for production deployments

4. **Restrict network access**:
   ```python
   FLASK_CONFIG = {'host': '127.0.0.1', ...}  # Localhost only
   ```

5. **Sanitize user input** to prevent SQL injection

## 📦 Dependencies

### Core
- `vanna` - RAG framework for SQL generation
- `chromadb` - Vector database
- `oracledb` - Oracle database driver
- `Flask` - Web framework

### LLM & Utilities
- `requests` - HTTP client for Umbrella Gateway
- `pandas` - Data manipulation
- `plotly` - Visualizations
- `sqlparse` - SQL parsing

See `requirements.txt` for complete list with versions.

## 🤝 Contributing

This is a customized deployment of Vanna AI. For the main project:
- **Vanna GitHub**: https://github.com/vanna-ai/vanna
- **Documentation**: https://vanna.ai/docs

## 📄 License

This implementation follows Vanna AI's MIT License.

## 🆘 Support

For issues with:
- **Vanna framework**: https://github.com/vanna-ai/vanna/issues
- **Umbrella Gateway**: https://github.com/vanna-ai/umbrella-gateway/issues
- **This deployment**: Check `.github/copilot-instructions.md` in parent directory

## 🎓 Learn More

- **Vanna Docs**: https://vanna.ai/docs
- **Copilot Instructions**: See `.github/copilot-instructions.md` in parent directory
- **Setup Guide**: See `SETUP_COMPLETE.md` in parent directory
- **Quick Reference**: See `QUICK_START.md` in parent directory
