"""
Configuration Loader for myDbAssistant UI
Loads configuration from JSON files and DDL/Documentation/Training data from separate files
"""

import json
import os
from pathlib import Path

# Base directory for UI configuration
UI_DIR = Path(__file__).parent
CONFIG_DIR = UI_DIR / 'config'

# Training data directory (separate from UI config)
TRAINING_BASE_DIR = UI_DIR.parent / 'trainingMyDb'
DDL_DIR = TRAINING_BASE_DIR / 'ddl'
DOC_DIR = TRAINING_BASE_DIR / 'documentation'
TRAINING_DIR = TRAINING_BASE_DIR / 'trainingpairs'


class ConfigLoader:
    """Loads and manages configuration from JSON files"""
    
    def __init__(self, config_dir=CONFIG_DIR):
        self.config_dir = Path(config_dir)
        self._cache = {}
    
    def load_json(self, filename):
        """Load a JSON configuration file"""
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_llm_config(self):
        """Load LLM configuration"""
        return self.load_json('llm.json')
    
    def load_database_config(self):
        """Load database configuration"""
        return self.load_json('database.json')
    
    def load_flask_config(self):
        """Load Flask configuration"""
        return self.load_json('flask.json')
    
    def load_chromadb_config(self):
        """Load ChromaDB configuration"""
        return self.load_json('chromadb.json')
    
    def load_training_config(self):
        """Load training configuration"""
        return self.load_json('training.json')
    
    def save_json(self, filename, data):
        """Save configuration to JSON file"""
        filepath = self.config_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_llm_config(self, updates):
        """Update LLM configuration"""
        config = self.load_llm_config()
        config.update(updates)
        self.save_json('llm.json', config)
        return config
    
    def update_database_config(self, updates):
        """Update database configuration"""
        config = self.load_database_config()
        config.update(updates)
        self.save_json('database.json', config)
        return config
    
    def update_flask_config(self, updates):
        """Update Flask configuration"""
        config = self.load_flask_config()
        config.update(updates)
        self.save_json('flask.json', config)
        return config
    
    def update_training_config(self, updates):
        """Update training configuration"""
        config = self.load_training_config()
        config.update(updates)
        self.save_json('training.json', config)
        return config


class DataLoader:
    """Loads DDL, documentation, and training data from files"""
    
    def __init__(self, ddl_dir=DDL_DIR, doc_dir=DOC_DIR, training_dir=TRAINING_DIR):
        self.ddl_dir = Path(ddl_dir)
        self.doc_dir = Path(doc_dir)
        self.training_dir = Path(training_dir)
    
    def load_ddl(self, filename='hr_schema.sql'):
        """Load DDL from SQL file"""
        filepath = self.ddl_dir / filename
        if not filepath.exists():
            return ""
        
        with open(filepath, 'r') as f:
            return f.read()
    
    def load_all_ddl(self):
        """Load all DDL files from ddl directory"""
        ddl_content = []
        for filepath in self.ddl_dir.glob('*.sql'):
            with open(filepath, 'r') as f:
                ddl_content.append(f.read())
        return '\n\n'.join(ddl_content)
    
    def load_documentation(self, filename='hr_business_rules.md'):
        """Load documentation from markdown file"""
        filepath = self.doc_dir / filename
        if not filepath.exists():
            return ""
        
        with open(filepath, 'r') as f:
            return f.read()
    
    def load_all_documentation(self):
        """Load all documentation files from documentation directory"""
        doc_content = []
        for filepath in self.doc_dir.glob('*.md'):
            with open(filepath, 'r') as f:
                doc_content.append(f.read())
        return '\n\n'.join(doc_content)
    
    def load_training_pairs(self, filename='hr_examples.json'):
        """Load training pairs from JSON file"""
        filepath = self.training_dir / filename
        if not filepath.exists():
            return []
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_all_training_pairs(self):
        """Load all training pairs from trainingpairs directory"""
        all_pairs = []
        for filepath in self.training_dir.glob('*.json'):
            with open(filepath, 'r') as f:
                pairs = json.load(f)
                if isinstance(pairs, list):
                    all_pairs.extend(pairs)
        return all_pairs
    
    def save_training_pairs(self, pairs, filename='hr_examples.json'):
        """Save training pairs to JSON file"""
        filepath = self.training_dir / filename
        with open(filepath, 'w') as f:
            json.dump(pairs, f, indent=2)


def get_vanna_config():
    """
    Get Vanna configuration combining all settings
    Returns a dict compatible with Vanna initialization
    """
    config_loader = ConfigLoader()
    
    llm = config_loader.load_llm_config()
    chromadb = config_loader.load_chromadb_config()
    
    return {
        # ChromaDB config
        'path': chromadb.get('path', './chromadb'),
        'collection_name': chromadb.get('collection_name', 'vanna_training_data'),
        
        # LLM config
        'api_key': llm.get('api_key'),
        'endpoint': llm.get('endpoint'),
        'model': llm.get('model'),
        'temperature': llm.get('temperature', 0.7),
        'max_tokens': llm.get('max_tokens', 4096),
        'timeout': llm.get('timeout', 60),
    }


def get_database_connection_params():
    """
    Get database connection parameters
    Returns a dict compatible with database connection methods
    """
    config_loader = ConfigLoader()
    db = config_loader.load_database_config()
    
    return {
        'type': db.get('type', 'oracle'),
        'host': db.get('host'),
        'port': db.get('port'),
        'database': db.get('database'),
        'schema': db.get('schema'),
        'user': db.get('user'),
        'password': db.get('password'),
    }


def get_flask_params():
    """
    Get Flask server parameters
    Returns a dict compatible with Flask app.run()
    """
    config_loader = ConfigLoader()
    flask = config_loader.load_flask_config()
    
    return {
        'host': flask.get('host', '0.0.0.0'),
        'port': flask.get('port', 8084),
        'debug': flask.get('debug', True),
        'secret_key': flask.get('secret_key', 'change-this-in-production'),
    }


def get_initial_training_data():
    """
    Get initial training data (DDL, documentation, training pairs)
    Returns a dict with 'ddl', 'documentation', and 'training_pairs'
    """
    data_loader = DataLoader()
    
    return {
        'ddl': data_loader.load_all_ddl(),
        'documentation': data_loader.load_all_documentation(),
        'training_pairs': data_loader.load_all_training_pairs(),
    }


def should_auto_train():
    """
    Check if auto-training is enabled in configuration
    Returns True if training should happen on startup
    """
    config_loader = ConfigLoader()
    training_config = config_loader.load_training_config()
    return training_config.get('auto_train_on_startup', False)


def train_from_files(vn, verbose=True):
    """
    Train Vanna from files in trainingMyDb directory
    Respects training configuration settings
    
    Args:
        vn: Vanna instance to train
        verbose: Print progress messages
    
    Returns:
        dict with training statistics
    """
    config_loader = ConfigLoader()
    training_config = config_loader.load_training_config()
    
    settings = training_config.get('training_settings', {})
    load_ddl = settings.get('load_ddl', True)
    load_docs = settings.get('load_documentation', True)
    load_pairs = settings.get('load_training_pairs', True)
    skip_if_exists = settings.get('skip_if_exists', True)
    
    data_loader = DataLoader()
    stats = {
        'ddl_loaded': 0,
        'docs_loaded': 0,
        'pairs_loaded': 0,
        'errors': []
    }
    
    if verbose:
        print("\n📚 Training from files...")
        print(f"   Source: {TRAINING_BASE_DIR}")
    
    # Load DDL
    if load_ddl:
        try:
            ddl = data_loader.load_all_ddl()
            if ddl:
                vn.train(ddl=ddl)
                stats['ddl_loaded'] = len(ddl)
                if verbose:
                    print(f"   ✅ Loaded DDL: {len(ddl)} characters")
        except Exception as e:
            error_msg = str(e)
            if skip_if_exists and 'existing' in error_msg.lower():
                if verbose:
                    print(f"   ℹ️  DDL already exists (skipped)")
            else:
                stats['errors'].append(f"DDL: {error_msg[:100]}")
                if verbose:
                    print(f"   ⚠️  DDL error: {error_msg[:50]}...")
    
    # Load documentation
    if load_docs:
        try:
            docs = data_loader.load_all_documentation()
            if docs:
                vn.train(documentation=docs)
                stats['docs_loaded'] = len(docs)
                if verbose:
                    print(f"   ✅ Loaded documentation: {len(docs)} characters")
        except Exception as e:
            error_msg = str(e)
            if skip_if_exists and 'existing' in error_msg.lower():
                if verbose:
                    print(f"   ℹ️  Documentation already exists (skipped)")
            else:
                stats['errors'].append(f"Documentation: {error_msg[:100]}")
                if verbose:
                    print(f"   ⚠️  Documentation error: {error_msg[:50]}...")
    
    # Load training pairs
    if load_pairs:
        pairs = data_loader.load_all_training_pairs()
        for pair in pairs:
            try:
                vn.train(question=pair['question'], sql=pair['sql'])
                stats['pairs_loaded'] += 1
                if verbose:
                    print(f"   ✅ Loaded: {pair['question'][:50]}...")
            except Exception as e:
                error_msg = str(e)
                if skip_if_exists and 'existing' in error_msg.lower():
                    if verbose:
                        print(f"   ℹ️  Pair already exists: {pair['question'][:30]}...")
                else:
                    stats['errors'].append(f"Pair '{pair['question'][:30]}': {error_msg[:100]}")
                    if verbose:
                        print(f"   ⚠️  Pair error: {error_msg[:50]}...")
    
    if verbose:
        print(f"\n✨ Training complete!")
        print(f"   DDL: {stats['ddl_loaded']} chars")
        print(f"   Docs: {stats['docs_loaded']} chars")
        print(f"   Pairs: {stats['pairs_loaded']} loaded")
        if stats['errors']:
            print(f"   Errors: {len(stats['errors'])}")
    
    return stats


def print_config_summary():
    """Print a summary of all configuration"""
    config_loader = ConfigLoader()
    
    print("\n" + "="*60)
    print("📋 UI CONFIGURATION SUMMARY")
    print("="*60)
    
    # LLM Config
    llm = config_loader.load_llm_config()
    print("\n🤖 LLM Configuration:")
    print(f"   Type: {llm.get('api_type')}")
    print(f"   Endpoint: {llm.get('endpoint')}")
    print(f"   Model: {llm.get('model')}")
    print(f"   Temperature: {llm.get('temperature')}")
    
    # Database Config
    db = config_loader.load_database_config()
    print("\n🏢 Database Configuration:")
    print(f"   Type: {db.get('type')}")
    print(f"   Host: {db.get('host')}:{db.get('port')}")
    print(f"   Database: {db.get('database')}")
    print(f"   Schema: {db.get('schema')}")
    print(f"   User: {db.get('user')}")
    
    # Flask Config
    flask = config_loader.load_flask_config()
    print("\n🌐 Flask Configuration:")
    print(f"   Host: {flask.get('host')}:{flask.get('port')}")
    print(f"   Debug: {flask.get('debug')}")
    print(f"   Title: {flask.get('ui_settings', {}).get('title')}")
    
    # ChromaDB Config
    chromadb = config_loader.load_chromadb_config()
    print("\n🗄️  ChromaDB Configuration:")
    print(f"   Path: {chromadb.get('path')}")
    print(f"   Collection: {chromadb.get('collection_name')}")
    
    # Training Config
    training = config_loader.load_training_config()
    print("\n🎓 Training Configuration:")
    print(f"   Auto-train on startup: {training.get('auto_train_on_startup')}")
    print(f"   Training data path: {training.get('training_data_path')}")
    settings = training.get('training_settings', {})
    print(f"   Load DDL: {settings.get('load_ddl', True)}")
    print(f"   Load Documentation: {settings.get('load_documentation', True)}")
    print(f"   Load Training Pairs: {settings.get('load_training_pairs', True)}")
    
    # Data files
    data_loader = DataLoader()
    ddl_files = list(Path(DDL_DIR).glob('*.sql'))
    doc_files = list(Path(DOC_DIR).glob('*.md'))
    training_files = list(Path(TRAINING_DIR).glob('*.json'))
    
    print("\n📁 Data Files:")
    print(f"   DDL Scripts: {len(ddl_files)} files")
    for f in ddl_files:
        print(f"      - {f.name}")
    print(f"   Documentation: {len(doc_files)} files")
    for f in doc_files:
        print(f"      - {f.name}")
    print(f"   Training Pairs: {len(training_files)} files")
    for f in training_files:
        print(f"      - {f.name}")
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    # Test configuration loading
    print_config_summary()
    
    # Example usage
    print("\n" + "="*60)
    print("📝 EXAMPLE USAGE")
    print("="*60 + "\n")
    
    print("# Load configurations:")
    print("from ui.config_loader import ConfigLoader, DataLoader")
    print("from ui.config_loader import get_vanna_config, get_database_connection_params")
    print("")
    print("# Get Vanna config")
    print("vanna_config = get_vanna_config()")
    print("")
    print("# Get database params")
    print("db_params = get_database_connection_params()")
    print("")
    print("# Load training data")
    print("data_loader = DataLoader()")
    print("ddl = data_loader.load_all_ddl()")
    print("docs = data_loader.load_all_documentation()")
    print("pairs = data_loader.load_all_training_pairs()")
    print("")
