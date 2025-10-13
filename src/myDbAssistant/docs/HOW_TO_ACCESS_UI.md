# 🌐 How to Access the Vanna Web UI

## ✅ Flask Server is Now Running!

Your Vanna Flask application with Umbrella Gateway LLM is successfully running.

## 🔗 Access the Web Interface

Open your web browser and go to:

```
http://localhost:8084/
```

Or alternatively:

```
http://127.0.0.1:8084/
```

## 🎯 What You Should See

The Vanna AI web interface with:
- **Title**: "Vanna AI - Oracle HR Database"
- **Subtitle**: "Ask questions about the HR database in natural language"
- A text input box to ask questions
- Example suggested questions
- SQL code display area
- Results table display
- Chart visualization (if applicable)

## 💬 Try These Example Questions

Once the UI loads, you can ask:

1. **"Who are the highest paid employees?"**
   - Shows top 10 employees by salary

2. **"How many employees are in each department?"**
   - Groups employees by department with counts

3. **"What is the average salary by job title?"**
   - Shows average salaries grouped by job title

4. **"Show me all employees"**
   - Lists all employees from the HR database

## 🔧 If You Get "Not Found" Error

This means the Flask server is initializing. The correct fix has been applied:

### What Was Fixed:
- Changed from incorrectly passing a Flask app instance
- Now using `VannaFlaskApp` which creates its own Flask app
- The Flask app is accessed via `vanna_flask.flask_app.run()`

### The Working Code:
```python
from vanna.flask import VannaFlaskApp

# Create VannaFlaskApp (creates its own Flask app internally)
vanna_flask = VannaFlaskApp(
    vn=vn, 
    allow_llm_to_see_data=True,
    title="Vanna AI - Oracle HR Database",
    subtitle="Ask questions about the HR database in natural language"
)

# Run Flask server
vanna_flask.flask_app.run(host='0.0.0.0', port=8084, debug=True)
```

## 🚀 Starting the Server

If the server is not running, start it with:

```bash
cd /Users/trongpv6/Documents/GitHub/vanna
python3 quick_start_flask.py
```

You should see:
```
🌐 Launching Flask UI at http://0.0.0.0:8084
 * Serving Flask app 'vanna.flask'
 * Debug mode: on
```

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where `quick_start_flask.py` is running.

## 📊 How It Works

1. **You ask a question** in natural language
2. **Vanna retrieves** similar examples from ChromaDB
3. **Umbrella Gateway** (GitHub Copilot LLM) generates SQL
4. **Oracle database** executes the query
5. **Results displayed** in a table (and chart if applicable)

## 🎨 Features Available in the UI

- ✅ **Natural language input**: Ask questions in plain English
- ✅ **SQL generation**: See the generated SQL code
- ✅ **Query execution**: Automatic execution against Oracle DB
- ✅ **Results table**: View query results in a formatted table
- ✅ **CSV download**: Download results as CSV
- ✅ **Chart visualization**: Auto-generated charts for numerical data
- ✅ **Training data view**: See example questions and DDL
- ✅ **Suggested questions**: Quick-start question templates

## 🔍 API Endpoints (Optional)

If you want to use the API directly instead of the UI:

```bash
# Get configuration
curl http://localhost:8084/api/v0/get_config

# Generate SQL
curl -X POST http://localhost:8084/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "Who are the highest paid employees?"}'

# Run SQL
curl -X POST http://localhost:8084/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM hr.employees LIMIT 10"}'
```

## 💡 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not Found" error | Wait a moment for server to fully initialize, then refresh browser |
| Page won't load | Check Flask is running: `lsof -i:8084` |
| Port in use | Kill process: `lsof -ti:8084 \| xargs kill -9` |
| SQL errors | Check Oracle DB is running: `docker ps \| grep oracle` |
| No results | Verify Umbrella Gateway is running (localhost:8765) |

## ✅ Verification Checklist

Before using the UI, ensure:

- [x] Flask server running on port 8084
- [x] Umbrella Gateway running on port 8765 (VS Code extension)
- [x] Oracle database running (Docker container)
- [x] ChromaDB directory exists (./chromadb/)
- [x] Training data loaded (you'll see checkmarks in startup logs)

## 📖 More Information

- **Full Setup Guide**: `SETUP_COMPLETE.md`
- **Quick Reference**: `QUICK_START.md`
- **Test Connections**: Run `python3 test_umbrella_connection.py`
- **Flask Integration**: `README_UMBRELLA_GATEWAY.md`

---

**🎉 Enjoy querying your Oracle HR database in natural language!**
