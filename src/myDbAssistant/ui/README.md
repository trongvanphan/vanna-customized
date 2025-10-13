# myDbAssistant UI Configuration

This directory contains flexible, JSON-based configuration for the myDbAssistant application.

## 📁 Directory Structure

```
ui/
├── config/
│   ├── llm.json              # LLM (Umbrella Gateway) configuration
│   ├── database.json         # Database connection settings
│   ├── flask.json            # Flask web server configuration
│   └── chromadb.json         # ChromaDB vector database settings
├── ddl/
│   └── hr_schema.sql         # Database DDL scripts
├── documentation/
│   └── hr_business_rules.md  # Business rules and documentation
├── trainingpairs/
│   └── hr_examples.json      # Question-SQL training pairs
├── config_loader.py          # Configuration loader utility
└── README.md                 # This file
```

## 🎯 Key Features

### 1. **Flexible JSON Configuration**
All settings are stored in easy-to-edit JSON files:
- **llm.json** - LLM API settings (endpoint, model, temperature)
- **database.json** - Database connection (host, port, credentials)
- **flask.json** - Web UI settings (port, debug mode, theme)
- **chromadb.json** - Vector database settings

### 2. **Separated Training Data**
Training data is organized by type:
- **DDL** (`.sql` files) - Database schema definitions
- **Documentation** (`.md` files) - Business rules and context
- **Training Pairs** (`.json` files) - Example question-SQL pairs

### 3. **Easy Customization**
No code changes needed - just edit JSON files!

## ⚙️ Configuration Files

### LLM Configuration (`config/llm.json`)

```json
{
  "api_type": "umbrella-gateway",
  "api_key": "sk-abcdef123456",
  "endpoint": "http://localhost:8765",
  "model": "copilot/gpt-5-mini",
  "temperature": 0.7,
  "max_tokens": 4096,
  "timeout": 60
}
```

**Key Settings:**
- `api_key` - Your Umbrella Gateway auth token
- `endpoint` - Umbrella Gateway URL
- `model` - Which model to use (gpt-5-mini, claude-sonnet-4, etc.)
- `temperature` - 0.0 = deterministic, 1.0 = creative

**Get your API key:**
```bash
cat ../../.vscode/settings.json | grep authToken
```

### Database Configuration (`config/database.json`)

```json
{
  "type": "oracle",
  "host": "localhost",
  "port": 1521,
  "database": "XEPDB1",
  "schema": "hr",
  "user": "hr",
  "password": "hr123"
}
```

**Supported Database Types:**
- `oracle` - Oracle Database
- `postgres` - PostgreSQL
- `mysql` - MySQL
- `snowflake` - Snowflake
- And more...

### Flask Configuration (`config/flask.json`)

```json
{
  "host": "0.0.0.0",
  "port": 8084,
  "debug": true,
  "ui_settings": {
    "title": "Vanna AI - Database Assistant",
    "allow_llm_to_see_data": true,
    "auto_train": true
  }
}
```

**Key Settings:**
- `host` - `0.0.0.0` = network accessible, `127.0.0.1` = localhost only
- `port` - Web UI port (change if 8084 is in use)
- `debug` - Enable debug mode (disable in production)
- `allow_llm_to_see_data` - Allow LLM to see actual data
- `auto_train` - Save successful Q&A pairs automatically

### ChromaDB Configuration (`config/chromadb.json`)

```json
{
  "path": "./chromadb",
  "collection_name": "vanna_training_data",
  "retrieval_settings": {
    "n_results_sql": 10,
    "n_results_ddl": 10,
    "n_results_documentation": 10
  }
}
```

**Key Settings:**
- `path` - Local directory for vector storage
- `collection_name` - ChromaDB collection name
- `n_results_*` - Number of similar items to retrieve

### Training Control Configuration (`config/training.json`)

```json
{
  "auto_train_on_startup": false,
  "training_data_path": "../trainingMyDb",
  "training_settings": {
    "load_ddl": true,
    "load_documentation": true,
    "load_training_pairs": true,
    "skip_if_exists": true,
    "verbose": true
  }
}
```

**Key Settings:**
- `auto_train_on_startup` - **false** = manual training, **true** = auto-train on app start
- `training_data_path` - Path to training data directory (relative to ui/ or absolute)
- `load_ddl` - Load database schema definitions
- `load_documentation` - Load business rules and documentation
- `load_training_pairs` - Load example question-SQL pairs
- `skip_if_exists` - Skip re-training if data already exists in vector DB
- `verbose` - Print detailed progress during training

**Manual Training Example:**
```python
from ui import should_auto_train, train_from_files

if should_auto_train():
    print("Auto-training enabled")
    stats = train_from_files(vn, verbose=True)
else:
    print("Auto-training disabled - train manually when needed")
    # Later, when ready to train:
    stats = train_from_files(vn)
    print(f"Loaded: {stats['ddl_loaded']} DDL, {stats['docs_loaded']} docs, {stats['pairs_loaded']} pairs")
```

**Why disable auto-training?**
- Faster startup (no training delay)
- Control when training happens (e.g., after adding new data)
- Avoid re-training on every restart if data unchanged
- Better for production (train once, reuse)

## 📝 Training Data Files

### Training Data Location

**Important:** Training data is now stored in `trainingMyDb/` (separate from UI config):

```
trainingMyDb/
├── ddl/
│   └── hr_schema.sql
├── documentation/
│   └── hr_business_rules.md
└── trainingpairs/
    └── hr_examples.json
```

This separation ensures:
- ✅ UI folder contains only UI-related configuration
- ✅ Training data in dedicated location for easy management
- ✅ Can be version controlled separately
- ✅ Easy to swap different training datasets

### DDL Scripts (`trainingMyDb/ddl/*.sql`)

Add your database schema definitions here:

```sql
-- Example: hr_schema.sql
CREATE TABLE employees (
    employee_id NUMBER(6) PRIMARY KEY,
    first_name VARCHAR2(20),
    ...
);
```

**Multiple files supported:**
- `hr_schema.sql`
- `sales_schema.sql`
- `analytics_schema.sql`
- All `.sql` files in `trainingMyDb/ddl/` will be loaded automatically

### Documentation (`trainingMyDb/documentation/*.md`)

Add business rules and context:

```markdown
# HR Database Business Rules

## Salaries
- All salaries are in USD
- Commission ranges from 0.0 to 1.0
...
```

**Multiple files supported:**
- `hr_business_rules.md`
- `data_dictionary.md`
- `query_guidelines.md`
- All `.md` files in `trainingMyDb/documentation/` will be loaded automatically

### Training Pairs (`trainingMyDb/trainingpairs/*.json`)

Add example question-SQL pairs:

```json
[
  {
    "question": "Who are the highest paid employees?",
    "sql": "SELECT ... ORDER BY salary DESC FETCH FIRST 10 ROWS ONLY",
    "category": "salary",
    "difficulty": "easy"
  }
]
```

**Multiple files supported:**
- `hr_examples.json`
- `sales_examples.json`
- `advanced_queries.json`
- All `.json` files in `trainingMyDb/trainingpairs/` will be loaded automatically

## 🚀 Usage

### Basic Configuration Loading

```python
from ui.config_loader import ConfigLoader, DataLoader
from ui.config_loader import get_vanna_config, get_database_connection_params

# Quick method - get all Vanna config
vanna_config = get_vanna_config()
db_params = get_database_connection_params()
flask_params = get_flask_params()

# Or use the loaders directly
config_loader = ConfigLoader()
llm_config = config_loader.load_llm_config()
db_config = config_loader.load_database_config()
training_config = config_loader.load_training_config()

# Load training data
data_loader = DataLoader()
ddl = data_loader.load_all_ddl()
docs = data_loader.load_all_documentation()
pairs = data_loader.load_all_training_pairs()
```

### Training Control (New!)

```python
from ui import should_auto_train, train_from_files

# Check if auto-training is enabled
if should_auto_train():
    print("Training automatically on startup...")
    stats = train_from_files(vn, verbose=True)
    print(f"✅ Loaded {stats['ddl_loaded']} DDL files")
    print(f"✅ Loaded {stats['docs_loaded']} documentation files")
    print(f"✅ Loaded {stats['pairs_loaded']} training pairs")
else:
    print("⏸️ Auto-training disabled")
    print("💡 Train manually when ready: train_from_files(vn)")
    
# Manual training anytime
stats = train_from_files(vn, verbose=True)
if stats['errors']:
    print(f"⚠️ {stats['errors']} errors encountered")
```

**Training Statistics:**
- `ddl_loaded` - Number of DDL files successfully loaded
- `docs_loaded` - Number of documentation files loaded
- `pairs_loaded` - Number of Q&A pairs loaded
- `errors` - Number of errors encountered

### Example Integration

```python
from ui.config_loader import get_vanna_config, get_database_connection_params
from ui.config_loader import DataLoader
from vanna.chromadb import ChromaDB_VectorStore
from your_llm import MyCustomLLM

# Initialize Vanna with UI config
vn = MyVanna(config_dict=get_vanna_config())

# Connect to database using UI config
db_params = get_database_connection_params()
vn.connect_to_oracle(
    dsn=f"{db_params['host']}:{db_params['port']}/{db_params['database']}",
    user=db_params['user'],
    password=db_params['password']
)

# Load and train with UI data
data_loader = DataLoader()
vn.train(ddl=data_loader.load_all_ddl())
vn.train(documentation=data_loader.load_all_documentation())

for pair in data_loader.load_all_training_pairs():
    vn.train(question=pair['question'], sql=pair['sql'])
```

## 🔧 Updating Configuration

### Method 1: Edit JSON Files Directly

Simply edit the JSON files in the `config/` directory:

```bash
# Edit LLM config
vi config/llm.json

# Edit database config
vi config/database.json
```

### Method 2: Programmatically Update

```python
from ui.config_loader import ConfigLoader

config_loader = ConfigLoader()

# Update LLM settings
config_loader.update_llm_config({
    'model': 'copilot/gpt-5',
    'temperature': 0.8
})

# Update database settings
config_loader.update_database_config({
    'host': 'production-db.example.com',
    'port': 1521
})

# Update Flask settings
config_loader.update_flask_config({
    'debug': False,
    'port': 8080
})
```

## 📊 View Current Configuration

```bash
cd ui
python config_loader.py
```

Output:
```
============================================================
📋 UI CONFIGURATION SUMMARY
============================================================

🤖 LLM Configuration:
   Type: umbrella-gateway
   Endpoint: http://localhost:8765
   Model: copilot/gpt-5-mini
   Temperature: 0.7

🏢 Database Configuration:
   Type: oracle
   Host: localhost:1521
   Database: XEPDB1
   Schema: hr
   User: hr

🌐 Flask Configuration:
   Host: 0.0.0.0:8084
   Debug: True
   Title: Vanna AI - Database Assistant

🗄️  ChromaDB Configuration:
   Path: ./chromadb
   Collection: vanna_training_data

📁 Data Files:
   DDL Scripts: 1 files
      - hr_schema.sql
   Documentation: 1 files
      - hr_business_rules.md
   Training Pairs: 1 files
      - hr_examples.json
```

## 🔐 Security Best Practices

### For Development
✅ JSON files with default values  
✅ Debug mode enabled  
✅ Network accessible (0.0.0.0)

### For Production
❌ **Never commit secrets to git!**

**Use environment variables:**
```python
import os
import json

# Load config
with open('config/database.json') as f:
    config = json.load(f)

# Override with environment variables
config['password'] = os.getenv('DB_PASSWORD', config['password'])
config['api_key'] = os.getenv('UMBRELLA_TOKEN', config['api_key'])
```

**Or use a `.env` file (add to .gitignore):**
```bash
# .env
DB_PASSWORD=secure_password_here
UMBRELLA_TOKEN=sk-real-token-here
FLASK_SECRET_KEY=random-secret-key-here
```

**Production checklist:**
- [ ] Change `flask.json` debug to `false`
- [ ] Change `flask.json` secret_key
- [ ] Use environment variables for passwords/tokens
- [ ] Set `flask.json` host to `127.0.0.1` if not using proxy
- [ ] Add `config/*.json` to `.gitignore` if they contain secrets
- [ ] Use HTTPS/SSL for production deployments

## 📚 Adding Your Own Data

### 1. Add Your Database Schema

Create `ddl/your_schema.sql`:
```sql
-- Your database tables
CREATE TABLE your_table (...);
```

### 2. Add Business Rules

Create `documentation/your_rules.md`:
```markdown
# Your Database Rules
- Business rule 1
- Business rule 2
```

### 3. Add Training Examples

Create `trainingpairs/your_examples.json`:
```json
[
  {
    "question": "Your question?",
    "sql": "SELECT ...",
    "category": "your_category"
  }
]
```

All files will be loaded automatically!

## 🎓 Examples

See the included example files in `trainingMyDb/`:
- `trainingMyDb/ddl/hr_schema.sql` - Oracle HR schema example
- `trainingMyDb/documentation/hr_business_rules.md` - Business rules example
- `trainingMyDb/trainingpairs/hr_examples.json` - Training pairs example

## 🆘 Troubleshooting

### "FileNotFoundError: Config file not found"
**Solution:** Make sure you're running from the correct directory:
```bash
cd src/myDbAssistant
python -c "from ui.config_loader import print_config_summary; print_config_summary()"
```

### "Invalid JSON"
**Solution:** Validate your JSON files:
```bash
python -m json.tool config/llm.json
```

### "Configuration not updating"
**Solution:** Check file permissions and restart the application after changes.

## 📖 Additional Resources

- **Main README**: `../README.md`
- **Parent Config**: `../config.py` (backward compatible)
- **Quick Start**: `../quick_start_flask.py`

---

**Happy configuring!** 🎉
