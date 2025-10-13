#!/usr/bin/env python3
"""
Test script to verify UI configuration setup
Run this to validate all UI config files and data files
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import ui module
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that UI package can be imported"""
    print("1️⃣  Testing imports...")
    try:
        from ui import (
            ConfigLoader,
            DataLoader,
            get_vanna_config,
            get_database_connection_params,
            get_flask_params,
            print_config_summary,
            should_auto_train,
            train_from_files,
        )
        print("   ✅ All imports successful\n")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}\n")
        return False

def test_config_files():
    """Test that all config JSON files exist and are valid"""
    print("2️⃣  Testing configuration files...")
    
    # Get parent directory (myDbAssistant)
    base_dir = Path(__file__).parent.parent
    config_dir = base_dir / 'ui' / 'config'
    required_files = ['llm.json', 'database.json', 'flask.json', 'chromadb.json', 'training.json']
    
    all_valid = True
    for filename in required_files:
        filepath = config_dir / filename
        if not filepath.exists():
            print(f"   ❌ Missing: {filename}")
            all_valid = False
        else:
            try:
                import json
                with open(filepath) as f:
                    json.load(f)
                print(f"   ✅ Valid: {filename}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON in {filename}: {e}")
                all_valid = False
    
    print()
    return all_valid

def test_data_files():
    """Test that training data files exist"""
    print("3️⃣  Testing training data files...")
    
    # Get parent directory (myDbAssistant)
    base_dir = Path(__file__).parent.parent
    
    checks = [
        (base_dir / 'trainingMyDb' / 'ddl', '*.sql', 'DDL scripts'),
        (base_dir / 'trainingMyDb' / 'documentation', '*.md', 'Documentation'),
        (base_dir / 'trainingMyDb' / 'trainingpairs', '*.json', 'Training pairs'),
    ]
    
    all_valid = True
    for dir_path, pattern, description in checks:
        if not dir_path.exists():
            print(f"   ❌ Missing directory: {dir_path.relative_to(base_dir)}")
            all_valid = False
            continue
        
        files = list(dir_path.glob(pattern))
        if not files:
            print(f"   ⚠️  No files in {dir_path.relative_to(base_dir)} matching {pattern}")
        else:
            print(f"   ✅ {description}: {len(files)} file(s)")
            for f in files:
                print(f"      - {f.name}")
    
    print()
    return all_valid

def test_config_loader():
    """Test ConfigLoader functionality"""
    print("4️⃣  Testing ConfigLoader...")
    
    try:
        from ui import ConfigLoader
        
        loader = ConfigLoader()
        
        # Test loading each config
        llm = loader.load_llm_config()
        db = loader.load_database_config()
        flask = loader.load_flask_config()
        chromadb = loader.load_chromadb_config()
        training = loader.load_training_config()
        
        print(f"   ✅ LLM config: {llm.get('api_type')}")
        print(f"   ✅ Database config: {db.get('type')}")
        print(f"   ✅ Flask config: port {flask.get('port')}")
        print(f"   ✅ ChromaDB config: path {chromadb.get('path')}")
        print(f"   ✅ Training config: auto_train_on_startup={training.get('auto_train_on_startup')}")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ ConfigLoader failed: {e}\n")
        return False

def test_data_loader():
    """Test DataLoader functionality"""
    print("5️⃣  Testing DataLoader...")
    
    try:
        from ui import DataLoader
        
        loader = DataLoader()
        
        # Test loading data
        ddl = loader.load_all_ddl()
        docs = loader.load_all_documentation()
        pairs = loader.load_all_training_pairs()
        
        print(f"   ✅ DDL loaded: {len(ddl)} characters")
        print(f"   ✅ Documentation loaded: {len(docs)} characters")
        print(f"   ✅ Training pairs loaded: {len(pairs)} pairs")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ DataLoader failed: {e}\n")
        return False

def test_helper_functions():
    """Test helper functions"""
    print("6️⃣  Testing helper functions...")
    
    try:
        from ui import (
            get_vanna_config,
            get_database_connection_params,
            get_flask_params,
        )
        
        vanna_config = get_vanna_config()
        db_params = get_database_connection_params()
        flask_params = get_flask_params()
        
        print(f"   ✅ get_vanna_config(): {len(vanna_config)} keys")
        print(f"      - model: {vanna_config.get('model')}")
        print(f"      - endpoint: {vanna_config.get('endpoint')}")
        
        print(f"   ✅ get_database_connection_params(): {len(db_params)} keys")
        print(f"      - type: {db_params.get('type')}")
        print(f"      - host: {db_params.get('host')}")
        
        print(f"   ✅ get_flask_params(): {len(flask_params)} keys")
        print(f"      - port: {flask_params.get('port')}")
        print(f"      - debug: {flask_params.get('debug')}")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Helper functions failed: {e}\n")
        return False

def test_training_control():
    """Test training control functions"""
    print("7️⃣  Testing training control functions...")
    
    try:
        from ui import should_auto_train
        
        # Test should_auto_train function
        auto_train = should_auto_train()
        print(f"   ✅ should_auto_train(): {auto_train}")
        
        # Note: We don't test train_from_files() here as it requires a Vanna instance
        print(f"   ℹ️  train_from_files() requires Vanna instance (tested in integration)")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Training control failed: {e}\n")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 UI Configuration Test Suite")
    print("="*60 + "\n")
    
    results = {
        'Imports': test_imports(),
        'Config Files': test_config_files(),
        'Data Files': test_data_files(),
        'ConfigLoader': test_config_loader(),
        'DataLoader': test_data_loader(),
        'Helper Functions': test_helper_functions(),
        'Training Control': test_training_control(),
    }
    
    # Summary
    print("="*60)
    print("📊 Test Results Summary")
    print("="*60 + "\n")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 All tests passed! UI configuration is ready to use.")
        print("\n   Next steps:")
        print("   1. Update credentials in ui/config/*.json")
        print("   2. Run: python quick_start_flask_ui.py")
        print()
        sys.exit(0)
    else:
        print("\n   ⚠️  Some tests failed. Fix the issues above.")
        print()
        sys.exit(1)

if __name__ == '__main__':
    main()
