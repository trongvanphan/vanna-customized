# 🚀 Vanna Flask Setup - Your Custom LLM + PgVector

This directory contains everything you need to run Vanna with **Flask UI**, **PgVector**, and **your custom LLM**.

## 📋 What's Included

| File | Description | Size |
|------|-------------|------|
| `quick_start_flask.py` | **START HERE** - Ready-to-run script | 6.9KB |
| `FLASK_QUICKSTART_SUMMARY.md` | Quick reference guide | 6.6KB |
| `FLASK_SETUP_GUIDE.md` | Complete detailed setup guide | 10KB |
| `.github/copilot-instructions.md` | Updated with Flask focus | 530+ lines |

## ⚡ Fastest Way to Get Started

### Step 1: Edit Configuration (2 minutes)

Open `quick_start_flask.py` and update lines 15-30:

```python
# PgVector Database (stores Vanna's training data/embeddings)
PGVECTOR_CONNECTION = 'postgresql://user:password@localhost:5432/vanna_vectors'

# Your Data Database (what users will query)
DATA_DB_NAME = 'your_database'

# Your LLM API Configuration
LLM_API_KEY = 'your-api-key'
LLM_ENDPOINT = 'https://api.example.com'
LLM_MODEL = 'your-model'
```

### Step 2: Customize Your LLM API (3 minutes)

Edit the `submit_prompt()` method around line 62 to match your LLM's API format:

```python
def submit_prompt(self, prompt, **kwargs) -> str:
    # Example for OpenAI-compatible APIs
    response = requests.post(
        f"{self.api_endpoint}/chat/completions",
        headers={"Authorization": f"Bearer {self.api_key}"},
        json={"model": self.model, "messages": prompt}
    )
    return response.json()['choices'][0]['message']['content']
```

### Step 3: Run!

```bash
python quick_start_flask.py
```

The Flask UI will automatically open at **http://localhost:8084** 🎉

## 🎯 Two Deployment Options

### Option 1: Built-in Flask (Quick Testing)
- **Use**: `quick_start_flask.py`
- **Port**: 8084
- **Best for**: Quick testing, development
- **Time**: 5 minutes

### Option 2: vanna-flask Repository (Production)
- **Clone**: `git clone https://github.com/vanna-ai/vanna-flask`
- **Port**: 8080 (customizable)
- **Best for**: Production deployments, custom frontends
- **Features**: Full HTML/CSS/JS customization, authentication support

See `FLASK_SETUP_GUIDE.md` for detailed instructions on Option 2.

## 🗄️ Database Setup

### PgVector Database (for Vanna)
```sql
CREATE DATABASE vanna_vectors;
\c vanna_vectors
CREATE EXTENSION vector;
```

### Your Data Database
No changes needed - Vanna just needs read access to your existing database!

## 🔧 Common LLM Integrations

### OpenAI-Compatible APIs
Works with: Groq, Together.ai, Fireworks, Perplexity, OpenRouter

```python
def submit_prompt(self, prompt, **kwargs) -> str:
    response = requests.post(
        f"{self.api_endpoint}/v1/chat/completions",
        headers={"Authorization": f"Bearer {self.api_key}"},
        json={"model": self.model, "messages": prompt}
    )
    return response.json()['choices'][0]['message']['content']
```

### Anthropic Claude
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
            "messages": prompt[1:],
            "system": prompt[0]['content'],
            "max_tokens": 4096
        }
    )
    return response.json()['content'][0]['text']
```

### Google Gemini
Use the built-in integration:
```python
from vanna.google import GoogleGeminiChat
from vanna.pgvector import PgVector_VectorStore

class MyVanna(PgVector_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config=config)
```

## 📚 Training Your Model

```python
# Train with DDL
vn.train(ddl="""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        total_sales DECIMAL(10,2)
    )
""")

# Train with documentation
vn.train(documentation="Fiscal year starts in April")

# Train with Q&A pairs
vn.train(
    question="Who are the top customers?",
    sql="SELECT name, total_sales FROM customers ORDER BY total_sales DESC LIMIT 10"
)
```

## 🆘 Troubleshooting

### Issue: "Cannot connect to PgVector"
```bash
# macOS
brew install pgvector

# Ubuntu/Debian
sudo apt-get install postgresql-15-pgvector

# Then in PostgreSQL:
CREATE EXTENSION vector;
```

### Issue: "LLM API error"
- Verify your API key is correct
- Test the endpoint separately
- Check the API format matches your provider

### Issue: Flask won't start
```bash
# Install Flask dependencies
pip install vanna[all]

# Or manually:
pip install flask flask-sock flasgger
```

## 📖 Documentation Structure

```
├── README_FLASK_SETUP.md          ← You are here
├── FLASK_QUICKSTART_SUMMARY.md    ← Quick reference
├── FLASK_SETUP_GUIDE.md           ← Complete guide
├── quick_start_flask.py           ← Executable script
└── .github/copilot-instructions.md ← AI agent instructions
```

## 🎓 Learning Path

1. **Start**: Read `FLASK_QUICKSTART_SUMMARY.md` (5 min)
2. **Setup**: Edit and run `quick_start_flask.py` (10 min)
3. **Deep Dive**: Read `FLASK_SETUP_GUIDE.md` when needed
4. **Customize**: Modify UI using vanna-flask repo (optional)

## 💡 Key Concepts

- **Two Databases**: 
  - PgVector stores Vanna's training data (embeddings)
  - Your data database contains the actual business data
  
- **Multiple Inheritance**: 
  - Combine `PgVector_VectorStore` + Your `CustomLLM`
  - Order matters: VectorStore first, then LLM

- **Training**: 
  - Add DDL, documentation, and Q&A examples
  - More training = better SQL generation

- **Flask UI**: 
  - Built-in option: `vn.flask()` - instant
  - Custom option: vanna-flask repo - full control

## 🚀 Quick Commands

```bash
# Quick start
python quick_start_flask.py

# Full customization
git clone https://github.com/vanna-ai/vanna-flask
cd vanna-flask
pip install -r requirements.txt
# Edit app.py, then:
python app.py
```

## 📞 Support

- **Documentation**: https://vanna.ai/docs/
- **GitHub**: https://github.com/vanna-ai/vanna
- **Discord**: https://discord.gg/qUZYKHremx

---

**Ready to get started?** → Open `FLASK_QUICKSTART_SUMMARY.md` or run `python quick_start_flask.py`! 🚀
