# 🚀 Quick Start Guide

## Start the Flask Server

```bash
cd /Users/trongpv6/Documents/GitHub/vanna
python3 quick_start_flask.py
```

## Access the Web UI

```
http://localhost:8084
```

## Stop the Server

Press `Ctrl+C` in the terminal

---

## Configuration Quick Reference

### Edit `config.py` for:

**Umbrella Gateway:**
```python
LLM_CONFIG = {
    'api_key': 'sk-abcdef123456',
    'endpoint': 'http://localhost:8765',
    'model': 'copilot/gpt-5-mini',
    'temperature': 0.7,
}
```

**Oracle Database:**
```python
DATA_DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'database': 'XEPDB1',
    'schema': 'hr',
    'user': 'hr',
    'password': 'hr123',
}
```

**ChromaDB:**
```python
CHROMADB_CONFIG = {
    'path': './chromadb',
}
```

**Flask:**
```python
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 8084,
    'debug': True,
}
```

---

## Test Everything

```bash
python3 test_umbrella_connection.py
```

Should show 6/6 tests passing:
- ✅ Umbrella Gateway health
- ✅ Authentication
- ✅ Available models
- ✅ Chat endpoint
- ✅ PostgreSQL (optional)
- ✅ Oracle database

---

## Key Files

| File | Purpose |
|------|---------|
| `quick_start_flask.py` | Main Flask application |
| `config.py` | All configuration settings |
| `test_umbrella_connection.py` | Test script (run before Flask) |
| `SETUP_COMPLETE.md` | Full documentation (READ THIS!) |

---

## Common Commands

**Start fresh (delete ChromaDB data):**
```bash
rm -rf ./chromadb
python3 quick_start_flask.py
```

**Check if port 8084 is in use:**
```bash
lsof -i:8084
```

**Kill process on port 8084:**
```bash
lsof -ti:8084 | xargs kill -9
```

**Check Oracle connection:**
```bash
docker ps | grep oracle
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Address already in use" | Kill process: `lsof -ti:8084 \| xargs kill -9` |
| "Oracle connection failed" | Check Docker: `docker ps \| grep oracle` |
| "Umbrella Gateway not responding" | Check VS Code extension is running on port 8765 |
| ChromaDB warnings | Normal! Means data already exists. To reset: `rm -rf ./chromadb` |

---

## 🎯 Your Setup Status

✅ **Vanna:** Installed and configured  
✅ **Umbrella Gateway:** Connected (localhost:8765)  
✅ **ChromaDB:** Running (./chromadb/)  
✅ **Oracle DB:** Connected (XEPDB1/hr schema, 7 tables)  
✅ **Flask UI:** Running (localhost:8084)  
✅ **SQL Generation:** Working (tested with "Show me all employees")  

**All systems operational!** 🎉

---

## 📖 Full Documentation

For detailed information, see:
- **`SETUP_COMPLETE.md`** - Complete setup guide with examples
- **`UMBRELLA_GATEWAY_SETUP.md`** - Umbrella Gateway integration guide
- **`.github/copilot-instructions.md`** - Vanna development guide

---

**Last Updated:** $(date)
**Status:** ✅ WORKING
