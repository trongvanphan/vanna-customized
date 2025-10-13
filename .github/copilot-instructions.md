# Vanna AI Coding Agent Instructions

## Project Overview
Vanna is an MIT-licensed RAG (Retrieval-Augmented Generation) framework for SQL generation. It uses LLMs and vector databases to convert natural language questions into SQL queries.

## Core Architecture

### Multiple Inheritance Pattern
**Critical:** Vanna uses multiple inheritance to compose LLM + VectorStore combinations. This is the fundamental design pattern:

```python
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)
```

- **Base class**: `VannaBase` (`src/vanna/base/base.py`) defines the contract via abstract methods
- **LLM providers**: `src/vanna/{openai,anthropic,gemini,ollama,mistral,...}/*_chat.py` - implement `submit_prompt()`, `system_message()`, etc.
- **Vector stores**: `src/vanna/{chromadb,pinecone,qdrant,pgvector,...}/*_vector.py` - implement `generate_embedding()`, `add_*()`, `get_*()` methods
- Users combine any LLM + VectorStore via multiple inheritance

### Method Naming Convention (Enforced)
Follow this strict nomenclature from `src/vanna/base/base.py`:

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `vn.get_` | Fetch data from retrieval layer | `get_related_ddl()`, `get_similar_question_sql()` |
| `vn.add_` | Add to retrieval layer | `add_question_sql()`, `add_ddl()`, `add_documentation()` |
| `vn.generate_` | AI-generated content | `generate_sql()`, `generate_plotly_code()`, `generate_embedding()` |
| `vn.run_` | Execute code/SQL | `run_sql()` |
| `vn.remove_` | Remove from retrieval layer | `remove_training_data()` |
| `vn.connect_` | Database connections | `connect_to_snowflake()`, `connect_to_postgres()` |

**Never deviate from these prefixes** when adding new methods to VannaBase or subclasses.

## Key Workflows

### Adding a New LLM Provider
1. Create `src/vanna/{provider}/{provider}_chat.py`
2. Inherit from `VannaBase`
3. Implement required abstract methods: `submit_prompt()`, `system_message()`, `user_message()`, `assistant_message()`
4. Export in `src/vanna/{provider}/__init__.py`
5. Add optional dependency to `pyproject.toml` under `[project.optional-dependencies]`
6. Create test in `tests/test_vanna.py` using multiple inheritance pattern

**Example structure** (see `src/vanna/openai/openai_chat.py`):
```python
from ..base import VannaBase

class NewProvider_Chat(VannaBase):
    def __init__(self, client=None, config=None):
        VannaBase.__init__(self, config=config)
        if config is None:
            config = {}
        
        # Initialize API client
        self.api_key = config.get('api_key', os.getenv('PROVIDER_API_KEY'))
        self.model = config.get('model', 'default-model')
        
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        # Call provider's API and return response
        # prompt is a list of message dicts from above methods
        pass
```

### Adding a New Vector Store
1. Create `src/vanna/{vectorstore}/{vectorstore}_vector.py`
2. Inherit from `VannaBase`
3. Implement: `generate_embedding()`, `add_question_sql()`, `add_ddl()`, `add_documentation()`, `get_similar_question_sql()`, `get_related_ddl()`, `get_related_documentation()`, `get_training_data()`, `remove_training_data()`
4. Use `deterministic_uuid()` from `vanna.utils` for generating IDs (ensures idempotent adds)
5. Follow ChromaDB implementation (`src/vanna/chromadb/chromadb_vector.py`) as reference

**Critical details**:
- **IDs must be deterministic**: Use `deterministic_uuid(content) + "-{sql|ddl|doc}"` suffix to prevent duplicates
- **Return embeddings as `List[float]`**: The `generate_embedding()` method must return float list
- **Store as JSON**: Question-SQL pairs stored as JSON: `{"question": "...", "sql": "..."}`
- **n_results configuration**: Support `n_results_sql`, `n_results_ddl`, `n_results_documentation` in config

**Example pattern**:
```python
from ..utils import deterministic_uuid

def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
    question_sql_json = json.dumps({"question": question, "sql": sql}, ensure_ascii=False)
    id = deterministic_uuid(question_sql_json) + "-sql"
    
    # Store in your vector DB with embedding
    self.collection.add(
        documents=question_sql_json,
        embeddings=self.generate_embedding(question_sql_json),
        ids=id
    )
    return id
```

### Testing
```bash
# Install in editable mode with all dependencies
pip install -e '.[all]' tox pre-commit

# Run tests (requires API keys in environment)
tox -e py310  # Linux/standard
tox -e mac    # macOS

# Pre-commit hooks (flake8, brunette)
pre-commit install
```

## Code Patterns

### Configuration Handling
All components accept optional `config` dict:
```python
def __init__(self, config=None):
    VannaBase.__init__(self, config=config)
    if config is None:
        config = {}
    self.api_key = config.get('api_key', os.getenv('PROVIDER_API_KEY'))
```

### SQL Extraction
`extract_sql()` in `base.py` uses regex to handle:
- `CREATE TABLE ... AS SELECT`
- `WITH` clauses (CTEs)
- `SELECT` statements
- Markdown code blocks (```sql```)

Override if your LLM has different output formatting.

### Database Dialects
Set `self.dialect` (e.g., "Snowflake SQL", "PostgreSQL") to customize prompt generation. Used in `get_sql_prompt()` to guide LLM output.

### Error Handling
Use custom exceptions from `src/vanna/exceptions/__init__.py`:
- `ImproperlyConfigured` - missing/invalid config
- `DependencyError` - missing optional dependencies
- `ValidationError` - invalid user input
- `APIError` - API call failures

## Dependencies

**Core**: `requests`, `pandas`, `plotly`, `sqlparse`, `flask`, `sqlalchemy` (see `pyproject.toml`)

**Optional**: Install only what you need via extras:
```bash
pip install vanna[openai,chromadb]  # Minimal
pip install vanna[all]              # Everything
```

When adding features requiring new dependencies, always make them optional and document the extra in `pyproject.toml`.

## PR Guidelines (from CONTRIBUTING.md)
1. Install package in editable mode: `pip install -e '.[all]'`
2. Test on real notebooks - modify install command to use your branch:
   ```python
   %pip install 'git+https://github.com/vanna-ai/vanna@your-branch#egg=vanna[chromadb,snowflake,openai]'
   ```
3. Verify end-to-end workflow (train + ask) works with real data
4. Run `tox -e flake8` before submitting

## Important Files
- `src/vanna/base/base.py` - Core logic, abstract methods, train/ask orchestration
- `src/vanna/local.py` - Reference implementation (ChromaDB + OpenAI)
- `src/vanna/remote.py` - VannaDB hosted service client
- `training_data/*/questions.json` - Example training datasets

## RAG Training & Querying Flow

### Training (`vn.train()`)
The `train()` method in `base.py` is a convenience wrapper that routes to:
- `add_question_sql(question, sql)` - Stores Q&A pairs for few-shot examples
- `add_ddl(ddl)` - Stores schema/DDL for context retrieval
- `add_documentation(doc)` - Stores business context/definitions

**Training data format** (see `training_data/*/questions.json`):
```json
[
  {
    "question": "What are the top 10 customers by sales?",
    "sql": "SELECT customer_name, SUM(sales) as total FROM customers GROUP BY customer_name ORDER BY total DESC LIMIT 10"
  }
]
```

### Querying (`vn.ask()` / `vn.generate_sql()`)
1. **Retrieval**: Get similar question-SQL pairs, related DDL, and docs via embeddings
2. **Prompt construction**: `get_sql_prompt()` builds message list with context
3. **LLM call**: `submit_prompt()` sends to LLM
4. **Extraction**: `extract_sql()` parses SQL from LLM response (handles markdown, CTEs)
5. **Execution** (optional): `run_sql()` executes query if DB connected
6. **Auto-training** (optional): If `auto_train=True`, successful Q&A pairs are added to training

### Intermediate SQL Pattern
If LLM response contains `intermediate_sql` comment, Vanna:
1. Extracts and runs the intermediate query to introspect data
2. Includes results in follow-up prompt to generate final SQL
3. Requires `allow_llm_to_see_data=True` flag for security

## Flask UI & Visualization

### Flask App (`src/vanna/flask/`)
- `assets.py` - Contains embedded HTML/CSS/JS (auto-generated, don't edit manually)
- Use `vn.flask()` to launch web UI for asking questions
- Authentication via `auth.py` if needed

### Plotly Code Generation
`generate_plotly_code()` creates visualization code from DataFrame metadata:
- Uses `df.dtypes` to understand data structure
- Generates plotly code (not executed by Vanna, returned to user)
- Single-value DataFrames → Indicator charts
- Use `should_generate_chart()` to decide if visualization appropriate

## Database Connectors

### Connection Pattern
All `connect_to_*()` methods follow same pattern:
```python
def connect_to_database(...):
    # 1. Check for dependencies
    try:
        db_lib = __import__("database_library")
    except ImportError:
        raise DependencyError("Install via: pip install vanna[database]")
    
    # 2. Get credentials from config or env vars
    username = username or os.getenv('DB_USER')
    
    # 3. Create connection
    conn = db_lib.connect(...)
    
    # 4. Define run_sql function
    def run_sql_database(sql: str) -> pd.DataFrame:
        # Execute and return as DataFrame
        pass
    
    # 5. Set dialect and run_sql
    self.dialect = "Database SQL"  # Used in prompts
    self.run_sql = run_sql_database
    self.run_sql_is_set = True
```

**Supported databases**: PostgreSQL, MySQL, Snowflake, BigQuery, SQLite, DuckDB, Oracle, ClickHouse, etc. (see README)

### SQLite Special Case
`connect_to_sqlite()` can download DBs from URLs:
```python
vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')
# Downloads to local file if URL provided
```

## Common Pitfalls & Debugging

### 1. Multiple Inheritance Order Matters
```python
# CORRECT - VectorStore first, then LLM
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    pass

# WRONG - May cause method resolution issues
class MyVanna(OpenAI_Chat, ChromaDB_VectorStore):
    pass
```

### 2. Always Call Parent __init__ Explicitly
```python
# CORRECT
def __init__(self, config=None):
    ChromaDB_VectorStore.__init__(self, config=config)
    OpenAI_Chat.__init__(self, config=config)

# WRONG - super() doesn't work well with multiple inheritance here
def __init__(self, config=None):
    super().__init__(config=config)
```

### 3. Deterministic UUIDs Prevent Duplicates
```python
# Always use deterministic_uuid to avoid re-adding same training data
from vanna.utils import deterministic_uuid

id = deterministic_uuid(content) + "-sql"  # Suffix indicates type
```

### 4. Optional Dependencies
```python
# Check for optional deps before using
try:
    import snowflake.connector
except ImportError:
    raise DependencyError("Run: pip install vanna[snowflake]")
```

### 5. SQL Validation
`is_sql_valid()` only allows SELECT by default. Override to support other statements:
```python
def is_sql_valid(self, sql: str) -> bool:
    parsed = sqlparse.parse(sql)
    allowed_types = {'SELECT', 'INSERT', 'UPDATE'}  # Customize
    return any(stmt.get_type() in allowed_types for stmt in parsed)
```

### 6. Token Limits
- Default `max_tokens=14000` in config
- `str_to_approx_token_count()` uses simple heuristic: `len(string) / 4`
- Context truncated in `add_ddl_to_prompt()`, `add_documentation_to_prompt()`, etc.

### 7. Testing Requires API Keys
Set environment variables before running tests:
```bash
export VANNA_API_KEY=...
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
# etc.
```

### 8. Dialect-Specific SQL
Set `self.dialect` to get dialect-specific SQL generation:
```python
self.dialect = "Snowflake SQL"  # LLM sees this in prompt
# Prompt: "You are a Snowflake SQL expert..."
```

## Code Style

### Linting & Formatting
- **flake8**: Max line length 100, see `setup.cfg` for ignore rules
- **brunette**: Black-compatible formatter (Python 3.9+)
- **pre-commit**: Auto-runs on commit (install via `pre-commit install`)

### Common Ignore Patterns
From `setup.cfg`:
- `BLK100` - Black would make changes
- `W503` - Line break before binary operator
- `E203` - Whitespace before ':'
- `E722` - Bare except
- `F821` - Undefined name (false positives in generated code)
- `F841` - Assigned but never used

## Advanced Features

### Custom SQL Extraction
Override `extract_sql()` if your LLM uses different formatting:
```python
def extract_sql(self, llm_response: str) -> str:
    # Custom regex or parsing logic
    # Must handle your LLM's specific output format
    pass
```

### Static Documentation
Set once per instance, included in all prompts:
```python
vn.static_documentation = "Company-specific definitions and business rules"
```

### Language Localization
Set response language:
```python
vn = MyVanna(config={'language': 'Spanish'})
# LLM responses and summaries in Spanish
```

### Training Plans
For bulk training, use `TrainingPlan`:
```python
plan = vn.get_training_plan_generic(df_information_schema)
vn.train(plan=plan)  # Adds all DDL/docs from plan
```

## Quick Start Recipes

### Recipe 1: Custom LLM + PgVector
```python
from vanna.base import VannaBase
from vanna.pgvector import PgVector_VectorStore
import requests

class MyCustomLLM(VannaBase):
    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)
        if config is None:
            config = {}
        self.api_key = config.get('api_key')
        self.api_endpoint = config.get('endpoint', 'https://api.example.com')
        self.model = config.get('model', 'default-model')
    
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
    
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
    
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        # Customize this for your LLM's API
        response = requests.post(
            f"{self.api_endpoint}/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": prompt}
        )
        return response.json()['choices'][0]['message']['content']

# Combine with PgVector
class MyVanna(PgVector_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)

# Use it
vn = MyVanna(config={
    'connection_string': 'postgresql://user:pass@localhost/vanna_vectors',
    'api_key': 'your-llm-key',
    'endpoint': 'https://your-llm-api.com'
})
```

### Recipe 2: Ollama (Local) + ChromaDB + Flask
```python
from vanna.chromadb import ChromaDB_VectorStore
from vanna.ollama import Ollama

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={
    'model': 'llama2',  # or 'mistral', 'codellama', etc.
    'ollama_host': 'http://localhost:11434'
})

# Launch Flask UI
vn.flask()
```

### Recipe 3: Any LLM + Any VectorStore Pattern
The key is **multiple inheritance order**: VectorStore first, then LLM.

```python
class MyVanna(YourVectorStore, YourLLM):
    def __init__(self, config=None):
        YourVectorStore.__init__(self, config=config)  # First
        YourLLM.__init__(self, config=config)          # Second
```

## Flask UI Setup & Customization

### Built-in Flask Interface
Vanna includes a built-in Flask app in `src/vanna/flask/`. You can launch it directly:

```python
from vanna.pgvector import PgVector_VectorStore
from my_llm import MyCustomLLM

class MyVanna(PgVector_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        PgVector_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)

vn = MyVanna(config={
    'connection_string': 'postgresql://user:pass@localhost/vanna_vectors',
    'api_key': 'your-llm-key'
})

# Connect to your data database
vn.connect_to_postgres(
    host="localhost",
    dbname="your_data",
    user="user",
    password="password"
)

# Launch Flask UI
vn.flask()  # Opens browser at http://localhost:8084
```

### Using vanna-flask Repository
For more customization, use the standalone Flask app:

Repository: [vanna-ai/vanna-flask](https://github.com/vanna-ai/vanna-flask)

**Installation:**
```bash
git clone https://github.com/vanna-ai/vanna-flask
cd vanna-flask
pip install -r requirements.txt
```

**Customize `app.py`:**
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
    'connection_string': 'postgresql://user:pass@localhost/vanna_vectors',
    'api_key': 'your-llm-key',
    'endpoint': 'https://your-api.com'
})

# Connect to database
vn.connect_to_postgres(
    host="localhost",
    dbname="your_database",
    user="user",
    password="password"
)

# Create Flask app
app = Flask(__name__)
VannaFlaskApp(vn, app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

**Run:**
```bash
python app.py
# Open http://localhost:8080
```

### Customizing the Flask UI

**Note:** `src/vanna/flask/assets.py` is auto-generated - don't edit directly.

**To customize:**
1. Clone [vanna-flask](https://github.com/vanna-ai/vanna-flask)
2. Modify HTML templates in the repository
3. Update CSS/JavaScript as needed
4. The standalone repo gives you full control over:
   - Frontend design (HTML/CSS/JS)
   - API endpoints
   - Authentication
   - Multi-user support

**Pros of Flask:**
- Full control over frontend (HTML/CSS/JS)
- Better for production deployments
- Can integrate with existing web apps
- Support for authentication/authorization
- Can add custom endpoints and logic

## Notebook Testing Workflow

Before submitting PRs, test in real Jupyter notebooks:

```python
# In notebook, install from your branch
%pip install 'git+https://github.com/vanna-ai/vanna@your-branch#egg=vanna[chromadb,openai]'

# Test the full workflow
from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={'api_key': 'sk-...', 'model': 'gpt-4'})
vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')

# Train
vn.train(ddl="CREATE TABLE customers (...)")
vn.train(question="Top customers?", sql="SELECT ...")

# Ask
vn.ask("What are the top 10 customers by sales?")
```

Verify:
- ✅ Training data stored correctly
- ✅ SQL generation works
- ✅ Query execution successful  
- ✅ Plotly visualization renders
- ✅ No import errors
