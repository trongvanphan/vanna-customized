# Vanna AI Coding Agent Instructions

## Project Overview
Vanna is an MIT-licensed RAG (Retrieval-Augmented Generation) framework for SQL generation. It uses LLMs and vector databases to convert natural language questions into SQL queries, with automatic chart generation via Plotly.

**Repository Structure:**
- `src/vanna/` - Core Vanna framework (multiple inheritance architecture)
- `src/myDbAssistant/` - Custom implementation with Copilot Socket Core (GitHub Copilot via VS Code extension) + multi-database support
- `tests/` - Framework tests
- `training_data/` - Example training datasets

**Key Entry Points:**
- `src/vanna/base/base.py` - Core VannaBase class with ~2100 lines of framework logic
- `src/myDbAssistant/quick_start_flask_ui.py` - Production Flask app with custom LLM, settings UI, and branding
- `src/myDbAssistant/config_ui.py` - Web-based configuration management (/settings endpoint)
- `src/myDbAssistant/ui/config_loader.py` - JSON-based configuration system

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

### Chart Generation Workflow (Critical for AI Agents)
Vanna generates interactive Plotly charts through a **3-step pipeline**:

**1. Backend: Code Generation** (`src/vanna/base/base.py:735-756`)
```python
def generate_plotly_code(self, question: str, sql: str, df_metadata: str) -> str:
    # LLM generates Python plotly code from DataFrame.dtypes
    # Returns: "fig = px.bar(df, x='name', y='value')"
```

**2. Backend: Code Execution** (`src/vanna/base/base.py:2068-2119`)
```python
def get_plotly_figure(self, plotly_code: str, df: pd.DataFrame) -> plotly.graph_objs.Figure:
    ldict = {"df": df, "px": px, "go": go}
    exec(plotly_code, globals(), ldict)  # Execute LLM-generated code
    fig = ldict.get("fig", None)
    
    # Fallback logic if exec fails:
    if len(numeric_cols) >= 2:
        fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
    elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
        fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0])
    # ... more fallbacks
```

**3. Frontend: Rendering** (`src/vanna/flask/assets.py`)
```javascript
// Frontend uses Plotly.js
Plotly.newPlot(document.getElementById(containerId), figJSON, {responsive: true});
```

**Flask API Endpoints** (`src/vanna/flask/__init__.py:651-706`):
- `GET /api/v0/generate_plotly_figure` - Generates chart from cached SQL result
- Returns: `{"type": "plotly_figure", "id": "...", "fig": <JSON>}`
- Chart generation only if `should_generate_chart(df)` returns True (>1 row + numeric columns)

**Key Pattern:**
- LLM generates code string (not executed by LLM)
- Vanna executes code in sandboxed environment with `exec()`
- Frontend receives serialized Plotly figure JSON
- Never edit `src/vanna/flask/assets.py` - it's auto-generated

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

## myDbAssistant Custom Implementation

### Overview
`src/myDbAssistant/` is a production-ready example using:
- **Copilot Socket Core** - GitHub Copilot API access via VS Code extension (custom LLM implementation)
- **Multi-Database Support** - Oracle, PostgreSQL, MySQL, Microsoft SQL Server
- **JSON Configuration** - Flexible, file-based configuration system with web-based settings UI
- **Training Control** - Smart training with manual/automatic modes and duplicate detection

**Key difference from core Vanna:** Implements custom LLM provider (Copilot Socket Core) instead of standard providers like OpenAI/Anthropic, with comprehensive settings UI and multi-database configuration.

### Directory Structure
```
src/myDbAssistant/
├── ui/                          # JSON-based configuration system
│   ├── config/
│   │   ├── llm.json            # Copilot Socket Core settings (auth token, port, model)
│   │   ├── database.json       # Database connection params (type, host, port, credentials)
│   │   ├── flask.json          # Web UI settings (host, port, title, data visibility)
│   │   ├── chromadb.json       # Vector store settings (n_results_*, persist dir)
│   │   └── training.json       # Training control (auto_train, data paths, load options)
│   ├── config_loader.py        # Configuration utilities (JSON read/write)
│   └── __init__.py             # Exports: get_vanna_config, should_auto_train, train_from_files
│
├── trainingMyDb/               # Training data (separate from config)
│   ├── ddl/                    # SQL schema files
│   ├── documentation/          # Business rules (Markdown)
│   └── trainingpairs/          # Q&A examples (JSON)
│
├── quick_start_flask_ui.py    # Main application (uses JSON config, smart training)
├── config_ui.py               # Web-based settings UI at /settings (NEW!)
├── quick_start_flask.py       # Alternative (uses config.py)
├── config.py                  # Python-based config (legacy)
└── test_ui_config.py          # Configuration test suite
```

### Custom LLM Implementation Pattern
**File:** `quick_start_flask_ui.py`

```python
from vanna.base import VannaBase
from vanna.chromadb import ChromaDB_VectorStore
import requests

class MyCustomLLM(VannaBase):
    def __init__(self, config_dict=None):
        VannaBase.__init__(self, config=config_dict)
        # Copilot Socket Core-specific initialization
        self.api_key = config_dict.get('api_key')  # Auth token from VS Code
        self.api_endpoint = config_dict.get('endpoint', 'http://127.0.0.1:8765')
        self.session_id = f"vanna_session_{int(time.time())}"
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        # POST to Copilot Socket Core /chat endpoint
        payload = {
            "messages": prompt,
            "sessionId": self.session_id,
            "model": self.model,
            "stream": False
        }
        response = requests.post(f"{self.api_endpoint}/chat", json=payload)
        return response.json()['choices'][0]['message']['content']

# Multiple inheritance: VectorStore FIRST, then LLM
class MyVanna(ChromaDB_VectorStore, MyCustomLLM):
    def __init__(self, config_dict=None):
        ChromaDB_VectorStore.__init__(self, config=config_dict)
        MyCustomLLM.__init__(self, config_dict=config_dict)
```

**Critical:** Session IDs allow Copilot Socket Core to maintain conversation context across multiple prompts.

### JSON Configuration System

**Loading configurations:**
```python
from ui import (
    get_vanna_config,              # LLM + ChromaDB merged config
    get_database_connection_params, # Database credentials
    get_flask_params,              # Flask server settings
    should_auto_train,             # Check training config
    train_from_files,              # Load training data
)

# Initialize with JSON config
vn = MyVanna(config_dict=get_vanna_config())

# Connect using JSON config
db_params = get_database_connection_params()
vn.connect_to_oracle(
    dsn=f"{db_params['host']}:{db_params['port']}/{db_params['database']}",
    user=db_params['user'],
    password=db_params['password']
)
```

**Programmatic updates:**
```python
from ui import ConfigLoader

loader = ConfigLoader()
loader.update_llm_config({'model': 'copilot/gpt-5'})
loader.update_training_config({'auto_train_on_startup': True})
```

### Multi-Database Support

myDbAssistant supports multiple database types through JSON configuration. Simply change the `type` field in `ui/config/database.json`:

**Supported Databases:**
- **Oracle** (`type: "oracle"`) - Default port 1521
- **PostgreSQL** (`type: "postgres"`) - Default port 5432
- **MySQL** (`type: "mysql"`) - Default port 3306
- **Microsoft SQL Server** (`type: "mssql"` or `"sqlserver"`) - Default port 1433

**Example configurations:**

```json
// Oracle
{
  "type": "oracle",
  "host": "localhost",
  "port": 1521,
  "database": "XEPDB1",
  "schema": "hr",
  "user": "hr",
  "password": "hr123"
}

// PostgreSQL
{
  "type": "postgres",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "schema": "public",
  "user": "postgres",
  "password": "postgres"
}

// MySQL
{
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "mydb",
  "schema": "mydb",
  "user": "root",
  "password": "root"
}

// Microsoft SQL Server
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

**Connection handling in `quick_start_flask_ui.py`:**
```python
if db_params['type'] == 'oracle':
    vn.connect_to_oracle(dsn=f"{host}:{port}/{database}", user=user, password=password)
elif db_params['type'] in ('postgres', 'postgresql'):
    vn.connect_to_postgres(host=host, port=port, dbname=database, user=user, password=password)
elif db_params['type'] == 'mysql':
    vn.connect_to_mysql(host=host, port=port, database=database, user=user, password=password)
elif db_params['type'] in ('mssql', 'sqlserver'):
    vn.connect_to_mssql(server=host, port=port, database=database, user=user, password=password)
```

**Required drivers:**
```bash
pip install 'vanna[oracle]'    # For Oracle
pip install 'vanna[postgres]'  # For PostgreSQL
pip install 'vanna[mysql]'     # For MySQL
pip install 'vanna[mssql]'     # For SQL Server
```

**Note:** Use quotes around `'vanna[...]'` to avoid shell interpretation issues (especially in zsh).

### Settings UI (NEW!)

**Location:** `src/myDbAssistant/config_ui.py`

A comprehensive web-based configuration interface accessible at `http://localhost:8084/settings`.

**Features:**
- **🤖 LLM Settings** - Configure Copilot Socket Core (API key, endpoint, model, temperature, max tokens, timeout)
- **🗄️ Database Settings** - Manage database connections (type, host, port, credentials) with connection testing
- **📊 ChromaDB Settings** - Adjust vector store retrieval parameters (SQL/DDL/documentation result counts)
- **🌐 Flask Settings** - Configure web server (host, port, debug mode, UI title/subtitle, data visibility)
- **📚 Training Settings** - Control training data loading (auto-train toggle, data paths, load options)

**Key Components:**

1. **API Endpoints** (in `config_ui.py`):
   - `GET /api/v0/get_config` - Fetch all current configurations
   - `POST /api/v0/update_llm_config` - Update LLM settings
   - `POST /api/v0/update_database_config` - Update database settings
   - `POST /api/v0/update_chromadb_config` - Update ChromaDB settings
   - `POST /api/v0/update_flask_config` - Update Flask settings
   - `POST /api/v0/update_training_config` - Update training settings
   - `POST /api/v0/test_database_connection` - Test database connectivity
   - `POST /api/v0/test_llm_connection` - Test LLM endpoint health
   - `POST /api/v0/load_training_data` - Manual training data load (NEW!)

2. **ConfigLoader Integration** (uses existing `ui/config_loader.py`):
   ```python
   from ui import ConfigLoader
   loader = ConfigLoader()
   loader.update_llm_config({'model': 'copilot/gpt-5'})
   loader.update_database_config({'type': 'postgres', 'port': 5432})
   ```

3. **Integration in Flask App** (`quick_start_flask_ui.py`):
   ```python
   from config_ui import ConfigUI
   config_ui = ConfigUI(vanna_flask.flask_app, vn)
   # Adds /settings route and all API endpoints
   ```

**Usage Workflow:**
1. Launch app: `python3 quick_start_flask_ui.py`
2. Navigate to: `http://localhost:8084/settings`
3. Configure settings through modern UI with validation
4. Test connections with built-in test buttons
5. Save changes (persists to JSON files in `ui/config/`)
6. Restart server if needed (Flask/Database changes)

**UI Features:**
- Tab-based navigation for different config sections
- Real-time validation and error messages
- Test connection buttons for LLM and database
- Auto-fills default ports based on database type
- Visual feedback (success/error alerts)
- Responsive design with modern styling
- Manual training data load button (with smart duplicate detection)

**Security Notes:**
- No built-in authentication (add for production)
- Passwords stored in JSON (use env vars for production)
- Settings UI saves directly to config files
- Already in .gitignore to prevent credential commits

See `docs/settings-ui-guide.md` for comprehensive usage guide.

### Training Control System

**Problem:** Original implementation always trained on startup → slow restarts, duplicate training.

**Solution:** `ui/config/training.json` controls when/how training happens:

```json
{
  "auto_train_on_startup": false,  // Manual control by default
  "training_data_path": "../trainingMyDb",
  "training_settings": {
    "load_ddl": true,
    "load_documentation": true,
    "load_training_pairs": true,
    "skip_if_exists": true,         // Skip if already trained
    "verbose": true
  }
}
```

**Smart Training Implementation** (`quick_start_flask_ui.py`):
```python
# Check if training data already exists in ChromaDB
existing_data = vn.get_training_data()
if existing_data and len(existing_data) > 0:
    print(f"✅ Training data already exists ({len(existing_data)} items)")
    print("   Skipping training data load to avoid duplicates.")
else:
    print("📚 No training data found, loading from files...")
    if should_auto_train():
        stats = train_from_files(vn, verbose=True)
        print(f"Loaded {stats['pairs_loaded']} training pairs")
```

**Usage patterns:**
```python
# Check if auto-training enabled
if should_auto_train():
    stats = train_from_files(vn, verbose=True)
    print(f"Loaded {stats['pairs_loaded']} training pairs")
else:
    print("⏸️ Auto-training disabled - train manually when needed")

# Manual training anytime via settings UI
# POST /api/v0/load_training_data
```

**Why disable auto-training:**
- Faster startup (no training delay)
- Control when training happens
- Avoid re-training on every restart
- Better for production (train once, reuse ChromaDB)

### Copilot Socket Core Integration

**Prerequisites:**
1. VS Code with Copilot Socket Core extension installed
2. GitHub Copilot subscription
3. Server started: `Cmd+Shift+P` → "Copilot Socket Core: Start Server"

**Getting auth token:**
```bash
cat .vscode/settings.json | grep authToken
# Copy token to ui/config/llm.json
```

**Available models:**
- `copilot/gpt-5-mini` (fast, cheap) - **DEFAULT**
- `copilot/gpt-5` (balanced)
- `copilot/claude-sonnet-4` (powerful)
- `copilot/o1-mini` (reasoning)

**Configuration** (`ui/config/llm.json`):
```json
{
  "api_key": "your-auth-token-from-vscode",
  "endpoint": "http://127.0.0.1:8765",
  "model": "copilot/gpt-5-mini",
  "temperature": 0.5,
  "max_tokens": 50000,
  "timeout": 30,
  "max_rounds": 20
}
```

**Error handling:**
- 401 → Check auth token in `llm.json`
- 403 → Run "Grant Access" in VS Code
- 503 → Try different model
- Connection error → Verify server started

### Testing the Custom Implementation

**Run test suite:**
```bash
cd src/myDbAssistant
python test_ui_config.py
```

**Expected: 7/7 tests passing**
- Imports (verify all modules load)
- Config Files (validate JSON syntax)
- Data Files (check training data exists)
- ConfigLoader (test config loading)
- DataLoader (test data loading)
- Helper Functions (test get_vanna_config, etc.)
- Training Control (test should_auto_train, train_from_files)

**Integration test:**
```bash
python quick_start_flask_ui.py
# Should launch Flask on http://localhost:8084
```

### Development Workflow (myDbAssistant)

1. **Update configuration** - Edit JSON files in `ui/config/`
2. **Add training data** - Add files to `trainingMyDb/{ddl,documentation,trainingpairs}/`
3. **Test changes** - Run `python test_ui_config.py`
4. **Run application** - `python quick_start_flask_ui.py`

**No code changes needed** for configuration updates - just edit JSON files.

### Key Patterns to Follow

**1. Separate UI config from training data:**
- `ui/config/` → UI-related configuration
- `trainingMyDb/` → Training data (DDL, docs, Q&A)

**2. Training data organization:**
- DDL: `.sql` files in `trainingMyDb/ddl/`
- Docs: `.md` files in `trainingMyDb/documentation/`
- Pairs: `.json` files in `trainingMyDb/trainingpairs/`
- All files automatically loaded (glob pattern)

**3. Configuration precedence:**
- JSON files → Primary configuration
- Environment variables → Override secrets (production)
- `config.py` → Legacy support (backward compatible)

**4. Error messages must guide users:**
```python
except requests.exceptions.ConnectionError:
    print(f"❌ Connection Error: Cannot reach Copilot Socket Core")
    print(f"   Make sure:")
    print(f"   1. VS Code is open with the workspace")
    print(f"   2. Copilot Socket Core extension is installed")
    print(f"   3. Server is started (Cmd+Shift+P -> 'Copilot Socket Core: Start Server')")
```

### Adding New Custom LLM Providers

To add another custom LLM (like Copilot Socket Core):

1. Create LLM class inheriting from `VannaBase`
2. Implement required methods: `submit_prompt()`, `system_message()`, `user_message()`, `assistant_message()`
3. Add provider-specific config to `ui/config/llm.json`
4. Update `config_loader.py` if needed
5. Follow multiple inheritance pattern: `class MyVanna(VectorStore, CustomLLM)`

**See `quick_start_flask_ui.py` lines 28-107** for complete example.

### Adding New Custom LLM Providers

To add another custom LLM (like Umbrella Gateway):

1. Create LLM class inheriting from `VannaBase`
2. Implement required methods: `submit_prompt()`, `system_message()`, `user_message()`, `assistant_message()`
3. Add provider-specific config to `ui/config/llm.json`
4. Update `config_loader.py` if needed
5. Follow multiple inheritance pattern: `class MyVanna(VectorStore, CustomLLM)`

**See `quick_start_flask_ui.py` lines 28-107** for complete example.

