# 🚀 Your Flask Setup - Complete Summary

## What I've Done for You

### 1. ✅ Updated `.github/copilot-instructions.md`
- **Removed** Streamlit references
- **Added** comprehensive Flask UI setup section
- **Included** Flask customization guide with full examples
- **Updated** Quick Start Recipes to focus on Flask

### 2. ✅ Created `FLASK_SETUP_GUIDE.md` 
A complete step-by-step guide covering:
- **Option 1**: Built-in Flask (5-minute quick start)
- **Option 2**: Full customization with vanna-flask repo
- Environment variables setup
- Training your model
- Database configuration (PgVector + your data DB)
- Common LLM API formats (OpenAI, Anthropic, Gemini)
- Troubleshooting section

### 3. ✅ Created `quick_start_flask.py`
A ready-to-run Python script that:
- Sets up Vanna with PgVector + your custom LLM
- Connects to your database
- Launches Flask UI automatically
- Includes helpful status messages and error handling

---

## 🎯 Quick Start (2 Options)

### Option A: Instant Test (Built-in Flask)

**1. Edit `quick_start_flask.py`** with your configuration:
```python
# Around line 15-30, update these:
PGVECTOR_CONNECTION = 'postgresql://user:password@localhost:5432/vanna_vectors'
DATA_DB_NAME = 'your_database'
LLM_API_KEY = 'your-api-key'
LLM_ENDPOINT = 'https://your-api.com'
```

**2. Customize the LLM API call** (around line 62):
```python
def submit_prompt(self, prompt, **kwargs) -> str:
    # Modify this based on YOUR LLM's API format
    response = requests.post(...)
    return response.json()['choices'][0]['message']['content']
```

**3. Run it:**
```bash
cd /Users/trongpv6/Documents/GitHub/vanna
python quick_start_flask.py
```

Flask UI opens automatically at `http://localhost:8084` 🎉

---

### Option B: Full Customization (Production)

**1. Clone vanna-flask:**
```bash
cd /Users/trongpv6/Documents/GitHub
git clone https://github.com/vanna-ai/vanna-flask
cd vanna-flask
pip install -r requirements.txt
```

**2. Create `my_llm.py`** (copy from quick_start_flask.py):
```python
from vanna.base import VannaBase
import requests

class MyCustomLLM(VannaBase):
    # ... (copy the class from quick_start_flask.py)
```

**3. Edit `app.py`:**
```python
from vanna.pgvector import PgVector_VectorStore
from my_llm import MyCustomLLM

class MyVanna(PgVector_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)

vn = MyVanna(config={
    'connection_string': 'postgresql://user:pass@localhost/vanna_vectors',
    'api_key': 'your-key',
    'endpoint': 'https://your-api.com'
})

vn.connect_to_postgres(...)

from flask import Flask
from vanna.flask import VannaFlaskApp

app = Flask(__name__)
VannaFlaskApp(vn, app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

**4. Run:**
```bash
python app.py
# Open http://localhost:8080
```

---

## 📋 Database Setup Checklist

### PgVector Database (for Vanna's training data)
```sql
-- Create database
CREATE DATABASE vanna_vectors;

-- Connect to it
\c vanna_vectors

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

### Your Data Database
Already exists! Just make sure Vanna has read access.

Optional - create read-only user:
```sql
CREATE USER vanna_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE your_database TO vanna_readonly;
GRANT USAGE ON SCHEMA public TO vanna_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO vanna_readonly;
```

---

## 🔧 Common LLM API Formats

### If your LLM uses OpenAI-compatible API:
```python
def submit_prompt(self, prompt, **kwargs) -> str:
    response = requests.post(
        f"{self.api_endpoint}/v1/chat/completions",
        headers={"Authorization": f"Bearer {self.api_key}"},
        json={"model": self.model, "messages": prompt}
    )
    return response.json()['choices'][0]['message']['content']
```

### If your LLM uses Anthropic format:
```python
def submit_prompt(self, prompt, **kwargs) -> str:
    response = requests.post(
        f"{self.api_endpoint}/v1/messages",
        headers={
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": self.model,
            "messages": prompt[1:],  # Skip system message
            "system": prompt[0]['content'],  # System separate
            "max_tokens": 4096
        }
    )
    return response.json()['content'][0]['text']
```

### If your LLM is Groq, Together.ai, Fireworks, etc.:
Most use OpenAI-compatible format! Just change the endpoint:
- Groq: `https://api.groq.com/openai/v1`
- Together: `https://api.together.xyz/v1`
- Fireworks: `https://api.fireworks.ai/inference/v1`

---

## 📚 Training Your Model

Before asking questions, train Vanna:

```python
# Add table schemas
vn.train(ddl="""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        total_sales DECIMAL(10,2)
    )
""")

# Add business context
vn.train(documentation="""
    - Fiscal year starts in April
    - total_sales is in USD
""")

# Add example Q&A pairs
vn.train(
    question="Who are top customers?",
    sql="SELECT name, total_sales FROM customers ORDER BY total_sales DESC LIMIT 10"
)
```

You can also train from JSON files (see `training_data/` directory for examples).

---

## 🎯 Next Steps

1. **Set up PgVector database** (if not done)
2. **Edit `quick_start_flask.py`** with your credentials
3. **Customize the `submit_prompt()` method** for your LLM
4. **Run the script** and test!
5. **Train Vanna** with your database schema
6. **Ask questions** in the Flask UI!

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `FLASK_SETUP_GUIDE.md` | Complete setup guide with troubleshooting |
| `quick_start_flask.py` | Ready-to-run script |
| `.github/copilot-instructions.md` | Flask-focused AI agent instructions |
| This file | Quick summary and next steps |

---

## 🆘 Need Help?

**Common Issues:**

1. **"Cannot connect to PgVector"**
   - Make sure PostgreSQL is running
   - Install pgvector: `brew install pgvector` (macOS)
   - Enable extension: `CREATE EXTENSION vector;`

2. **"LLM API error"**
   - Check your API key is correct
   - Verify the endpoint URL
   - Test the API separately first

3. **"Port already in use"**
   - Built-in Flask uses port 8084
   - Standalone Flask uses port 8080
   - Change port in the code if needed

**Resources:**
- [Vanna Docs](https://vanna.ai/docs/)
- [vanna-flask Repo](https://github.com/vanna-ai/vanna-flask)
- [PgVector Docs](https://github.com/pgvector/pgvector)

---

Good luck! 🚀 The Flask UI should work perfectly with your custom LLM and PgVector setup!
