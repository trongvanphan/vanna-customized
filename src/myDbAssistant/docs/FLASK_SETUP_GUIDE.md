# Complete Flask UI Setup Guide for Vanna

## Two Ways to Use Flask with Vanna

### Option 1: Built-in Quick Start (5 minutes)

Use Vanna's built-in Flask interface - perfect for quick testing!

**Step 1: Create your Vanna instance**

Create a file `my_vanna.py`:

```python
from vanna.pgvector import PgVector_VectorStore
from vanna.base import VannaBase
import requests

# Your custom LLM
class MyCustomLLM(VannaBase):
    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)
        if config is None:
            config = {}
        
        self.api_key = config.get('api_key')
        self.api_endpoint = config.get('endpoint', 'https://your-api.com')
        self.model = config.get('model', 'your-model')
    
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        # Customize based on your LLM API
        response = requests.post(
            f"{self.api_endpoint}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": prompt,
                "temperature": kwargs.get('temperature', 0.7)
            }
        )
        return response.json()['choices'][0]['message']['content']

# Combine with PgVector
class MyVanna(PgVector_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)

# Initialize
vn = MyVanna(config={
    # PgVector connection (for embeddings/training data)
    'connection_string': 'postgresql://user:password@localhost:5432/vanna_vectors',
    
    # Your LLM config
    'api_key': 'your-llm-api-key',
    'endpoint': 'https://your-llm-api.com',
    'model': 'your-model-name'
})

# Connect to your actual data database
vn.connect_to_postgres(
    host="localhost",
    dbname="your_business_database",
    user="your_user",
    password="your_password",
    port=5432
)

if __name__ == '__main__':
    # Launch built-in Flask UI
    vn.flask()  # Opens at http://localhost:8084
```

**Step 2: Run it**
```bash
python my_vanna.py
```

Your browser will open automatically at `http://localhost:8084`!

---

### Option 2: Full Customization (Production-ready)

Use the standalone Flask repository for complete control.

**Step 1: Clone the Flask repository**

```bash
cd /Users/trongpv6/Documents/GitHub
git clone https://github.com/vanna-ai/vanna-flask
cd vanna-flask
```

**Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 3: Copy your LLM class**

Copy your `MyCustomLLM` class from above into the vanna-flask directory as `my_llm.py`.

**Step 4: Customize `app.py`**

Edit the `app.py` file in vanna-flask:

```python
from flask import Flask
from vanna.flask import VannaFlaskApp
from vanna.pgvector import PgVector_VectorStore
from my_llm import MyCustomLLM

class MyVanna(PgVector_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)

# Initialize Vanna
vn = MyVanna(config={
    'connection_string': 'postgresql://user:password@localhost:5432/vanna_vectors',
    'api_key': 'your-llm-api-key',
    'endpoint': 'https://your-llm-api.com',
    'model': 'your-model-name'
})

# Connect to your data database
vn.connect_to_postgres(
    host="localhost",
    dbname="your_business_database",
    user="your_user",
    password="your_password",
    port=5432
)

# Optional: Train with some initial data
vn.train(ddl="""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        total_sales DECIMAL(10,2)
    );
""")

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this!

# Attach Vanna to Flask
VannaFlaskApp(vn, app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

**Step 5: Run the app**

```bash
python app.py
```

Open your browser to `http://localhost:8080`

---

## Environment Variables (Recommended for Production)

Create a `.env` file:

```env
# PgVector Database (for Vanna's training data)
PGVECTOR_CONNECTION=postgresql://user:password@localhost:5432/vanna_vectors

# Your Data Database (what users query)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_business_database
DB_USER=your_user
DB_PASSWORD=your_password

# Your LLM API
LLM_API_KEY=your-llm-api-key
LLM_ENDPOINT=https://your-llm-api.com
LLM_MODEL=your-model-name

# Flask
FLASK_SECRET_KEY=change-this-to-a-random-string
```

Then modify `app.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Vanna
vn = MyVanna(config={
    'connection_string': os.getenv('PGVECTOR_CONNECTION'),
    'api_key': os.getenv('LLM_API_KEY'),
    'endpoint': os.getenv('LLM_ENDPOINT'),
    'model': os.getenv('LLM_MODEL')
})

# Connect to your data database
vn.connect_to_postgres(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=int(os.getenv('DB_PORT', 5432))
)

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

---

## Training Your Model

Before users can ask questions, train Vanna with your database schema and example queries:

```python
# Add DDL (table definitions)
vn.train(ddl="""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        total_sales DECIMAL(10,2),
        created_at TIMESTAMP
    );
""")

# Add business documentation
vn.train(documentation="""
    - total_sales represents the lifetime sales for a customer in USD
    - We consider a customer "active" if they made a purchase in the last 90 days
    - The fiscal year starts in April
""")

# Add example question-SQL pairs
vn.train(
    question="Who are the top 10 customers by sales?",
    sql="""
        SELECT name, total_sales 
        FROM customers 
        ORDER BY total_sales DESC 
        LIMIT 10
    """
)

# Or train from a JSON file
import json

with open('training_questions.json', 'r') as f:
    questions = json.load(f)
    for item in questions:
        vn.train(question=item['question'], sql=item['sql'])
```

---

## Customizing the Flask UI

The vanna-flask repository allows you to:

1. **Modify HTML templates** - Change the layout and structure
2. **Update CSS** - Customize colors, fonts, spacing
3. **Add JavaScript** - Enhance interactivity
4. **Add authentication** - Integrate with your auth system
5. **Add custom endpoints** - Additional API routes
6. **Multi-tenant support** - Different databases per user

The repository is structured for easy customization - just modify the templates and static files.

---

## Common LLM API Formats

### OpenAI-Compatible (Groq, Together.ai, etc.)
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
            "messages": prompt[1:],  # Skip system message
            "system": prompt[0]['content'],  # System message separate
            "max_tokens": 4096
        }
    )
    return response.json()['content'][0]['text']
```

### Google Gemini (use built-in)
```python
from vanna.google import GoogleGeminiChat
from vanna.pgvector import PgVector_VectorStore

class MyVanna(PgVector_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config=config)
```

---

## Database Setup

### Create PgVector Database (for Vanna's training data)

```sql
-- Create database
CREATE DATABASE vanna_vectors;

-- Connect to it
\c vanna_vectors

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Vanna will create tables automatically when you first run it
```

### Your Data Database

This is your existing business database that users will query. Vanna just needs read access:

```sql
-- Create read-only user (recommended)
CREATE USER vanna_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE your_business_database TO vanna_readonly;
GRANT USAGE ON SCHEMA public TO vanna_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO vanna_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO vanna_readonly;
```

---

## Troubleshooting

### Issue: "Module not found: vanna.flask"
**Solution:** Install Flask extras:
```bash
pip install vanna[all]
# or
pip install flask flask-sock flasgger
```

### Issue: "Could not connect to PgVector"
**Solution:** Ensure pgvector extension is installed:
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-15-pgvector

# macOS
brew install pgvector
```

Then create the extension in your database:
```sql
CREATE EXTENSION vector;
```

### Issue: Flask UI doesn't show
**Solution:** Check that you're returning the vn.flask() call:
```python
if __name__ == '__main__':
    vn.flask()  # Don't assign to variable, just call it
```

### Issue: LLM API errors
**Solution:** Test your LLM connection separately:
```python
test_prompt = [
    vn.system_message("You are a helpful assistant."),
    vn.user_message("Say hello!")
]
response = vn.submit_prompt(test_prompt)
print(response)
```

---

## Next Steps

1. ✅ Set up PgVector database
2. ✅ Create your custom LLM class
3. ✅ Train Vanna with your schema
4. ✅ Launch Flask UI
5. 🎯 Test with real questions!

**Resources:**
- [Vanna Documentation](https://vanna.ai/docs/)
- [vanna-flask Repository](https://github.com/vanna-ai/vanna-flask)
- [PgVector Documentation](https://github.com/pgvector/pgvector)
