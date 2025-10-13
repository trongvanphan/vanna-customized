# Vanna with Umbrella Gateway - Complete Setup

This repository contains a fully configured Vanna SQL generation system using:
- **Umbrella Gateway** (VS Code extension) for LLM access to GitHub Copilot models
- **PgVector** for embeddings and training data storage
- **Oracle Database** for querying HR data
- **Flask** for web UI

## 📁 Project Structure

```
vanna/
├── config.py                          # ⭐ Centralized configuration
├── quick_start_flask.py               # 🚀 Main Flask application
├── test_umbrella_connection.py        # 🧪 Connection test script
├── UMBRELLA_GATEWAY_SETUP.md          # 📖 Detailed Umbrella Gateway guide
├── FLASK_SETUP_GUIDE.md               # 📘 Flask deployment guide
├── FLASK_QUICKSTART_SUMMARY.md        # 📝 Quick reference
└── .github/copilot-instructions.md    # 🤖 AI agent instructions
```

## 🚀 Quick Start (15 minutes)

### Prerequisites

- ✅ VS Code with Umbrella Gateway extension
- ✅ PostgreSQL 12+ with pgvector extension
- ✅ Oracle Database (XE or higher)
- ✅ Python 3.9+
- ✅ GitHub Copilot subscription

### Step 1: Install Dependencies

```bash
cd /Users/trongpv6/Documents/GitHub/vanna

# Install Vanna with all required extras
pip install -e '.[pgvector,oracle]'

# Or install individually
pip install psycopg2-binary oracledb requests flask
```

### Step 2: Setup Umbrella Gateway

1. **Install Extension** (if not already installed)
   - Open VS Code
   - Extensions → Search "Umbrella Gateway"
   - Install and reload

2. **Start Server**
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
   - Run: "Umbrella Gateway: Start Server"
   - Wait for confirmation notification

3. **Get Auth Token**
   ```bash
   cat .vscode/settings.json | grep authToken
   ```
   
   Look for:
   ```json
   "umbrella-gateway.authToken": "ug_abc123xyz..."
   ```

### Step 3: Configure Databases & LLM

Edit `config.py`:

```python
# Umbrella Gateway LLM
LLM_CONFIG = {
    'api_key': 'ug_abc123xyz...',  # ← Paste your token
    'endpoint': 'http://localhost:8765',
    'model': 'copilot/claude-sonnet-4',
}

# PgVector Database (already configured)
PGVECTOR_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'admin',
    'password': 'admin123',
}

# Oracle Database (already configured)
DATA_DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'database': 'XEPDB1',
    'schema': 'hr',
    'user': 'hr',
    'password': 'hr123',
}
```

### Step 4: Setup Databases

**PgVector:**
```bash
# Create database (if not exists)
createdb -U admin mydb

# Install pgvector extension
psql -U admin -d mydb -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

**Oracle:**
```bash
# Verify connection
sqlplus hr/hr123@localhost:1521/XEPDB1

# Check tables exist
SELECT COUNT(*) FROM user_tables;
```

### Step 5: Test Connection

```bash
python test_umbrella_connection.py
```

Expected output:
```
╔══════════════════════════════════════════════════╗
║          UMBRELLA GATEWAY CONNECTION TEST         ║
╚══════════════════════════════════════════════════╝

============================================================
  1. Testing Umbrella Gateway Health
============================================================
   Endpoint: http://localhost:8765
   ✅ Server is running!

============================================================
  2. Testing Authentication
============================================================
   ✅ Authentication successful!

============================================================
  3. Testing Available Models
============================================================
   ✅ Found 4 models:
      • copilot/claude-sonnet-4 (copilot)
      • copilot/gpt-4o (copilot)
      • copilot/gpt-4o-mini (copilot)
      • copilot/o1-preview (copilot)

============================================================
  4. Testing Chat Endpoint
============================================================
   ✅ Chat successful!

============================================================
  5. Testing PgVector Database
============================================================
   ✅ PostgreSQL connected!
   ✅ pgvector extension installed!

============================================================
  6. Testing Oracle Database
============================================================
   ✅ Oracle connected!
   ✅ Schema 'hr' accessible

============================================================
  Summary
============================================================
   ✅ PASS - Health
   ✅ PASS - Auth
   ✅ PASS - Models
   ✅ PASS - Chat
   ✅ PASS - Pgvector
   ✅ PASS - Oracle

   Result: 6/6 tests passed

   🎉 All tests passed! Ready to run Vanna.
```

### Step 6: Run Vanna Flask App

```bash
python quick_start_flask.py
```

Expected output:
```
============================================================
🤖 Vanna Flask Setup - Oracle HR Database
============================================================

🔧 Current Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LLM Configuration:
  • Type: umbrella-gateway
  • Endpoint: http://localhost:8765
  • Model: copilot/claude-sonnet-4

PgVector Database:
  • Connection: postgresql://admin:***@localhost:5432/mydb

Data Database (Oracle):
  • Type: oracle
  • Host: localhost:1521
  • Database: XEPDB1
  • Schema: hr

🚀 Initializing Vanna...
✅ Initialized Umbrella Gateway LLM
   └─ Endpoint: http://localhost:8765
   └─ Model: copilot/claude-sonnet-4
   └─ Session ID: vanna_session_1234567890
✅ Vanna initialized successfully!

📊 Connecting to Oracle database: XEPDB1 (schema: hr)...
✅ Connected to Oracle database!
✅ Using schema: hr

📚 Setting up initial training data...
   ✅ Added DDL
   ✅ Added DDL
   ✅ Added DDL
   ✅ Added documentation
   ✅ Added: Show me all employees in the HR department...

✨ Training complete!

🧪 Testing SQL generation...
   Question: Show me all employees
   Generated SQL: SELECT * FROM employees;

🌐 Launching Flask UI at http://0.0.0.0:8084
   Press Ctrl+C to stop

 * Running on http://0.0.0.0:8084
```

### Step 7: Open Flask UI

Open browser: **http://localhost:8084**

Try asking:
- "Show me all employees in the HR department"
- "What are the top 5 highest paid employees?"
- "List departments with employee counts"
- "Find employees hired in 2024"

## 🔧 Configuration

All settings are centralized in `config.py`:

| Setting | Environment Variable | Default | Description |
|---------|---------------------|---------|-------------|
| **Umbrella Gateway** | | | |
| `api_key` | `UMBRELLA_AUTH_TOKEN` | (required) | Auth token from .vscode/settings.json |
| `endpoint` | `UMBRELLA_ENDPOINT` | `http://localhost:8765` | Gateway URL |
| `model` | `UMBRELLA_MODEL` | `copilot/claude-sonnet-4` | Copilot model |
| **PgVector** | | | |
| `host` | `PGVECTOR_HOST` | `localhost` | PostgreSQL host |
| `port` | `PGVECTOR_PORT` | `5432` | PostgreSQL port |
| `database` | `PGVECTOR_DB` | `mydb` | Database name |
| `user` | `PGVECTOR_USER` | `admin` | Username |
| `password` | `PGVECTOR_PASSWORD` | `admin123` | Password |
| **Oracle** | | | |
| `host` | `DB_HOST` | `localhost` | Oracle host |
| `port` | `DB_PORT` | `1521` | Oracle port |
| `database` | `DB_NAME` | `XEPDB1` | Service name |
| `schema` | `DB_SCHEMA` | `hr` | Schema name |
| `user` | `DB_USER` | `hr` | Username |
| `password` | `DB_PASSWORD` | `hr123` | Password |

### Using Environment Variables

```bash
# Create .env file
cat > .env << EOF
UMBRELLA_AUTH_TOKEN=ug_abc123xyz...
UMBRELLA_MODEL=copilot/gpt-4o
PGVECTOR_PASSWORD=secure_password
DB_PASSWORD=secure_password
EOF

# Load and run
export $(cat .env | xargs)
python quick_start_flask.py
```

## 🧪 Testing

### Test Individual Components

```bash
# Test Umbrella Gateway connection
python -c "import config; import requests; r = requests.get(f\"{config.LLM_CONFIG['endpoint']}/health\"); print(r.json())"

# Test PgVector connection
python -c "import config; import psycopg2; conn = psycopg2.connect(**config.PGVECTOR_CONFIG); print('✅ PgVector OK')"

# Test Oracle connection
python -c "import config; import oracledb; print('✅ Oracle OK')"

# Test full configuration
python config.py
```

### Test Full Integration

```bash
python test_umbrella_connection.py
```

## 🐛 Troubleshooting

### Umbrella Gateway Issues

**Problem:** "Connection refused" to localhost:8765

**Solution:**
1. Ensure VS Code is open
2. Start server: `Cmd+Shift+P` → "Umbrella Gateway: Start Server"
3. Check `.vscode/settings.json` for custom port

**Problem:** "401 Unauthorized"

**Solution:**
1. Get token: `cat .vscode/settings.json | grep authToken`
2. Update `config.py` with exact token
3. Restart if needed

See `UMBRELLA_GATEWAY_SETUP.md` for detailed troubleshooting.

### Database Issues

**PgVector extension missing:**
```bash
psql -U admin -d mydb
CREATE EXTENSION vector;
```

**Oracle connection failed:**
```bash
# Test listener
lsnrctl status

# Test connection
sqlplus hr/hr123@localhost:1521/XEPDB1
```

## 📚 Documentation

- **UMBRELLA_GATEWAY_SETUP.md** - Complete Umbrella Gateway guide
- **FLASK_SETUP_GUIDE.md** - Flask deployment and customization
- **FLASK_QUICKSTART_SUMMARY.md** - Quick reference
- **.github/copilot-instructions.md** - AI agent development guide

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Web UI                         │
│                  (localhost:8084)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Vanna Core                             │
│              (quick_start_flask.py)                     │
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │ PgVector Store   │      │ Custom LLM       │       │
│  │ (Embeddings)     │      │ (Umbrella GW)    │       │
│  └──────────────────┘      └──────────────────┘       │
└──────────┬─────────────────────────┬──────────────────┘
           │                         │
           ▼                         ▼
┌──────────────────┐      ┌──────────────────────┐
│  PostgreSQL      │      │  Umbrella Gateway    │
│  (mydb)          │      │  (localhost:8765)    │
│  • Embeddings    │      │                      │
│  • Training data │      │  ┌────────────────┐  │
│  • DDL docs      │      │  │ GitHub Copilot │  │
└──────────────────┘      │  │ Models         │  │
                          │  │ • claude-4     │  │
                          │  │ • gpt-4o       │  │
           ┌──────────────┤  └────────────────┘  │
           │              └──────────────────────┘
           ▼
┌──────────────────┐
│  Oracle Database │
│  (XEPDB1/hr)     │
│  • employees     │
│  • departments   │
│  • jobs          │
└──────────────────┘
```

## 🚀 Advanced Usage

### Change Copilot Model

Edit `config.py`:
```python
LLM_CONFIG = {
    'model': 'copilot/gpt-4o',  # or gpt-4o-mini, o1-preview
}
```

### Add Custom Training Data

```python
from vanna.local import LocalVanna_Umb

vn = LocalVanna_Umb()

# Add DDL
vn.train(ddl="CREATE TABLE my_table (...)")

# Add documentation
vn.train(documentation="Business rules: ...")

# Add Q&A pairs
vn.train(
    question="Top 10 products by revenue?",
    sql="SELECT product, SUM(revenue) FROM sales GROUP BY product ORDER BY 2 DESC LIMIT 10"
)
```

### Deploy to Production

See `FLASK_SETUP_GUIDE.md` for:
- Using vanna-flask repository for customization
- Docker deployment
- Environment variable management
- Security best practices

## 📖 API Reference

### Umbrella Gateway Endpoints

- `GET /health` - Server health check
- `GET /models` - List available models
- `POST /chat` - Send chat message
- `GET /sessions` - List active sessions
- `GET /docs` - Interactive API documentation

### Vanna Methods

```python
# Training
vn.train(ddl="CREATE TABLE ...")
vn.train(documentation="...")
vn.train(question="...", sql="...")

# Querying
sql = vn.generate_sql("Show top customers")
df = vn.run_sql(sql)
fig = vn.generate_plotly_code(df)

# Flask UI
vn.flask()  # Launches web interface
```

## 🎉 Next Steps

1. ✅ All tests passing
2. ✅ Flask UI running
3. 🎯 Train with your specific data:
   - Add your database DDL
   - Add business documentation
   - Add example Q&A pairs
4. 🌐 Share with team
5. 📊 Generate SQL from natural language!

## 📧 Support

- **Umbrella Gateway Issues**: Check VS Code extension logs
- **Vanna Issues**: See [vanna.ai](https://vanna.ai)
- **Database Issues**: Check connection strings and credentials

Happy querying! 🚀
