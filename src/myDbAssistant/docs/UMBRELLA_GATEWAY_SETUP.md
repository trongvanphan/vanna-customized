# Umbrella Gateway Setup for Vanna

This guide explains how to use **Umbrella Gateway** (VS Code extension) as the LLM provider for Vanna's SQL generation.

## 📋 Overview

**Umbrella Gateway** provides HTTP API access to GitHub Copilot models directly from VS Code. This setup allows Vanna to use powerful Copilot models (Claude, GPT-4o, etc.) for SQL generation.

### Architecture

```
┌─────────────────────┐
│  Vanna Flask App    │
│  (quick_start_flask)│
└──────────┬──────────┘
           │ HTTP POST /chat
           ▼
┌─────────────────────┐
│ Umbrella Gateway    │
│ (VS Code Extension) │
│ localhost:8765      │
└──────────┬──────────┘
           │ GitHub Copilot API
           ▼
┌─────────────────────┐
│ Copilot Models:     │
│ • claude-sonnet-4   │
│ • gpt-4o            │
│ • gpt-4o-mini       │
│ • o1-preview        │
└─────────────────────┘
```

## 🚀 Quick Start (5 Steps)

### Step 1: Install Umbrella Gateway Extension

1. Open VS Code
2. Go to Extensions (Cmd+Shift+X)
3. Search for **"Umbrella Gateway"**
4. Install the extension
5. Reload VS Code if needed

### Step 2: Start Umbrella Gateway Server

1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: **"Umbrella Gateway: Start Server"**
3. Press Enter
4. Server starts at `http://localhost:8765`

You should see a notification: "Umbrella Gateway server started on port 8765"

### Step 3: Get Your Auth Token

The auth token is automatically created in `.vscode/settings.json` in your workspace.

**Option A: Check the file directly**
```bash
cat .vscode/settings.json
```

Look for:
```json
{
  "umbrella-gateway.authToken": "ug_abc123xyz...",
  "umbrella-gateway.model": "copilot/claude-sonnet-4",
  "umbrella-gateway.port": 8765
}
```

**Option B: Generate a new token**
1. Press `Cmd+Shift+P`
2. Run: **"Umbrella Gateway: Regenerate Auth Token"**
3. Token is saved to `.vscode/settings.json`

### Step 4: Update config.py

Edit `/Users/trongpv6/Documents/GitHub/vanna/config.py`:

```python
LLM_CONFIG = {
    'api_type': 'umbrella-gateway',
    'api_key': 'ug_abc123xyz...',  # ← Paste your token here
    'endpoint': 'http://localhost:8765',
    'model': 'copilot/claude-sonnet-4',  # Best for SQL generation
    'temperature': 0.7,
}
```

**Or use environment variable:**
```bash
export UMBRELLA_AUTH_TOKEN='ug_abc123xyz...'
```

### Step 5: Run Vanna

```bash
cd /Users/trongpv6/Documents/GitHub/vanna
python quick_start_flask.py
```

You should see:
```
✅ Initialized Umbrella Gateway LLM
   └─ Endpoint: http://localhost:8765
   └─ Model: copilot/claude-sonnet-4
   └─ Session ID: vanna_session_1234567890
```

## 🔧 Configuration Details

### Available Models

Umbrella Gateway supports multiple Copilot models:

| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `copilot/claude-sonnet-4` | SQL generation, coding | Fast | Excellent |
| `copilot/gpt-4o` | Complex reasoning | Medium | Excellent |
| `copilot/gpt-4o-mini` | Quick queries | Very Fast | Good |
| `copilot/o1-preview` | Complex problems | Slow | Best |

**Recommendation for Vanna:** Use `copilot/claude-sonnet-4` (default)

### Get Available Models Programmatically

```python
import requests

response = requests.get(
    'http://localhost:8765/models',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

models = response.json()['models']
for model in models:
    print(f"{model['id']} - {model['provider']}")
```

### Configuration Options

Edit `config.py` or set environment variables:

```python
LLM_CONFIG = {
    'api_type': 'umbrella-gateway',
    
    # Auth token (from .vscode/settings.json)
    'api_key': os.getenv('UMBRELLA_AUTH_TOKEN', 'your-token'),
    
    # Gateway endpoint (default: localhost:8765)
    'endpoint': os.getenv('UMBRELLA_ENDPOINT', 'http://localhost:8765'),
    
    # Model selection
    'model': os.getenv('UMBRELLA_MODEL', 'copilot/claude-sonnet-4'),
    
    # Temperature (0.0-1.0, lower = more deterministic)
    'temperature': float(os.getenv('LLM_TEMPERATURE', '0.7')),
}
```

## 🧪 Testing the Connection

### 1. Health Check

```bash
curl http://localhost:8765/health
```

Expected response:
```json
{"status":"ok","version":"1.0.0"}
```

### 2. Test Chat Endpoint

```bash
curl -X POST http://localhost:8765/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Generate SQL: Show all employees",
    "sessionId": "test_session",
    "model": "copilot/claude-sonnet-4"
  }'
```

Expected response:
```json
{
  "text": "SELECT * FROM employees;",
  "sessionId": "test_session"
}
```

### 3. Test from Python

```python
import requests

def test_umbrella_gateway(token):
    response = requests.post(
        'http://localhost:8765/chat',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'message': 'What is SQL?',
            'sessionId': 'test_123',
            'model': 'copilot/claude-sonnet-4'
        }
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

# Run test
test_umbrella_gateway('your-token-here')
```

## 🐛 Troubleshooting

### Error: "Connection refused"

**Problem:** Umbrella Gateway server is not running.

**Solutions:**
1. Check if server is running:
   ```bash
   curl http://localhost:8765/health
   ```
2. Start the server:
   - Press `Cmd+Shift+P`
   - Run: "Umbrella Gateway: Start Server"
3. Check VS Code output panel for errors

### Error: "401 Unauthorized"

**Problem:** Invalid or missing auth token.

**Solutions:**
1. Verify token in `.vscode/settings.json`
2. Copy the exact token to `config.py`
3. Regenerate token:
   - Press `Cmd+Shift+P`
   - Run: "Umbrella Gateway: Regenerate Auth Token"

### Error: "403 Forbidden"

**Problem:** Access not granted to the API.

**Solutions:**
1. Press `Cmd+Shift+P`
2. Run: **"Umbrella Gateway: Grant Access"**
3. Restart the server

### Error: "503 Service Unavailable"

**Problem:** Model is unavailable or GitHub Copilot subscription issue.

**Solutions:**
1. Try a different model:
   ```python
   LLM_CONFIG['model'] = 'copilot/gpt-4o-mini'
   ```
2. Check GitHub Copilot subscription status
3. Verify you're signed into GitHub in VS Code

### Error: "Cannot reach Umbrella Gateway"

**Problem:** Connection error from Vanna to Gateway.

**Solutions:**
1. Verify VS Code is open with the workspace
2. Check Umbrella Gateway extension is installed
3. Ensure server is started (see above)
4. Check port is not blocked:
   ```bash
   lsof -i :8765
   ```

### Server on Different Port

If Umbrella Gateway uses a different port:

1. Check `.vscode/settings.json`:
   ```json
   {
     "umbrella-gateway.port": 9000
   }
   ```

2. Update `config.py`:
   ```python
   LLM_CONFIG = {
       'endpoint': 'http://localhost:9000',
       ...
   }
   ```

## 📊 Session Management

Umbrella Gateway maintains conversation context using sessions:

```python
# Vanna automatically creates a session ID
session_id = f"vanna_session_{int(time.time())}"

# First SQL generation uses this session
sql1 = vn.generate_sql("Show all employees")

# Follow-up questions maintain context
sql2 = vn.generate_sql("Now add salary column")
```

### View Active Sessions

```bash
curl http://localhost:8765/sessions \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete a Session

```bash
curl -X DELETE http://localhost:8765/sessions/vanna_session_123 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔒 Security Notes

1. **Token Storage**: Keep your auth token secure
   - Don't commit `.vscode/settings.json` to version control
   - Add to `.gitignore`:
     ```
     .vscode/settings.json
     ```

2. **Local Only**: Umbrella Gateway runs locally on `localhost:8765`
   - Only accessible from your machine
   - No external network access by default

3. **Environment Variables**: Use env vars in production:
   ```bash
   export UMBRELLA_AUTH_TOKEN='your-token'
   python quick_start_flask.py
   ```

## 📚 API Reference

### POST /chat

Main endpoint for SQL generation.

**Request:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a SQL expert"},
    {"role": "user", "content": "Generate SQL for top 10 customers"}
  ],
  "sessionId": "vanna_session_123",
  "model": "copilot/claude-sonnet-4",
  "stream": false
}
```

**Response:**
```json
{
  "text": "SELECT * FROM customers ORDER BY sales DESC LIMIT 10;",
  "sessionId": "vanna_session_123"
}
```

### GET /models

List available models.

**Request:**
```bash
curl http://localhost:8765/models \
  -H "Authorization: Bearer TOKEN"
```

**Response:**
```json
{
  "models": [
    {"id": "copilot/claude-sonnet-4", "provider": "copilot"},
    {"id": "copilot/gpt-4o", "provider": "copilot"},
    {"id": "copilot/gpt-4o-mini", "provider": "copilot"}
  ]
}
```

### GET /health

Server health check (no auth required).

**Request:**
```bash
curl http://localhost:8765/health
```

**Response:**
```json
{"status": "ok", "version": "1.0.0"}
```

## 🎯 Integration with Vanna

The integration is already implemented in `quick_start_flask.py`:

```python
class MyCustomLLM(VannaBase):
    def submit_prompt(self, prompt, **kwargs) -> str:
        """Submit to Umbrella Gateway"""
        response = requests.post(
            f"{self.api_endpoint}/chat",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "messages": prompt,
                "sessionId": self.session_id,
                "model": self.model,
                "stream": False
            }
        )
        return response.json()['text']
```

**Key Features:**
- ✅ Session persistence for context
- ✅ Error handling with helpful messages
- ✅ Configurable model selection
- ✅ Timeout handling (60s default)
- ✅ Automatic retry on connection errors

## 🚀 Production Deployment

### Using Environment Variables

Create `.env` file:
```bash
# Umbrella Gateway
UMBRELLA_AUTH_TOKEN=ug_abc123xyz...
UMBRELLA_ENDPOINT=http://localhost:8765
UMBRELLA_MODEL=copilot/claude-sonnet-4

# PgVector Database
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5432
PGVECTOR_DB=mydb
PGVECTOR_USER=admin
PGVECTOR_PASSWORD=admin123

# Oracle Database
DB_HOST=localhost
DB_PORT=1521
DB_NAME=XEPDB1
DB_SCHEMA=hr
DB_USER=hr
DB_PASSWORD=hr123
```

Load with:
```bash
export $(cat .env | xargs)
python quick_start_flask.py
```

### Docker Deployment

If deploying in Docker, ensure Umbrella Gateway is accessible:

1. Run Umbrella Gateway on host machine
2. Use `host.docker.internal` in Docker:
   ```python
   'endpoint': 'http://host.docker.internal:8765'
   ```

## 📖 Additional Resources

- **Interactive API Docs**: http://localhost:8765/docs
- **Server Config**: http://localhost:8765/config
- **Available Tools**: http://localhost:8765/tools

## 🎉 Next Steps

1. ✅ Umbrella Gateway installed and running
2. ✅ Auth token configured in `config.py`
3. ✅ Connection tested successfully
4. 🚀 Run `python quick_start_flask.py`
5. 🌐 Open Flask UI at http://localhost:8084
6. 💬 Ask questions in natural language!

**Example Questions to Try:**
- "Show me all employees in the HR department"
- "What are the top 5 highest paid employees?"
- "List all departments with their employee counts"
- "Find employees hired in the last 6 months"

Happy querying! 🎊
