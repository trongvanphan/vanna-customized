#!/usr/bin/env python3
"""
Test script to verify Umbrella Gateway connection
Run this before starting Vanna to ensure everything is configured correctly
"""

import requests
import sys
import config

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_health():
    """Test if Umbrella Gateway server is running"""
    print_header("1. Testing Umbrella Gateway Health")
    
    endpoint = config.LLM_CONFIG['endpoint']
    print(f"   Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{endpoint}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to {endpoint}")
        print("\n   Solutions:")
        print("   1. Open VS Code with this workspace")
        print("   2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)")
        print("   3. Run: 'Umbrella Gateway: Start Server'")
        print("   4. Wait for 'Server started on port 8765' notification")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_auth():
    """Test authentication with auth token"""
    print_header("2. Testing Authentication")
    
    endpoint = config.LLM_CONFIG['endpoint']
    token = config.LLM_CONFIG['api_key']
    
    print(f"   Token: {token[:20]}..." if len(token) > 20 else f"   Token: {token}")
    
    if token == 'your-auth-token-here':
        print("   ❌ Placeholder token detected!")
        print("\n   Steps to get your token:")
        print("   1. Check .vscode/settings.json in your workspace")
        print("   2. Look for 'umbrella-gateway.authToken'")
        print("   3. Copy the token to config.py LLM_CONFIG['api_key']")
        print("\n   Example:")
        print("   cat .vscode/settings.json | grep authToken")
        return False
    
    try:
        response = requests.get(
            f"{endpoint}/models",
            headers={'Authorization': f'Bearer {token}'},
            timeout=5
        )
        
        if response.status_code == 200:
            print("   ✅ Authentication successful!")
            return True
        elif response.status_code == 401:
            print("   ❌ Unauthorized - Invalid token")
            print("\n   Solutions:")
            print("   1. Verify token in .vscode/settings.json")
            print("   2. Regenerate token: Cmd+Shift+P -> 'Regenerate Auth Token'")
            print("   3. Copy exact token to config.py")
            return False
        elif response.status_code == 403:
            print("   ❌ Forbidden - Access not granted")
            print("\n   Solution:")
            print("   1. Press Cmd+Shift+P")
            print("   2. Run: 'Umbrella Gateway: Grant Access'")
            print("   3. Restart the server")
            return False
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_models():
    """Test fetching available models"""
    print_header("3. Testing Available Models")
    
    endpoint = config.LLM_CONFIG['endpoint']
    token = config.LLM_CONFIG['api_key']
    
    try:
        response = requests.get(
            f"{endpoint}/models",
            headers={'Authorization': f'Bearer {token}'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            print(f"   ✅ Found {len(models)} models:")
            for model in models:
                model_id = model.get('id', 'unknown')
                provider = model.get('provider', 'unknown')
                print(f"      • {model_id} ({provider})")
            
            # Check if configured model is available
            configured_model = config.LLM_CONFIG['model']
            model_ids = [m.get('id') for m in models]
            
            if configured_model in model_ids:
                print(f"\n   ✅ Configured model '{configured_model}' is available!")
                return True
            else:
                print(f"\n   ⚠️  Configured model '{configured_model}' not found")
                print(f"   Available models: {', '.join(model_ids)}")
                return True  # Still pass, just a warning
        else:
            print(f"   ❌ Failed to fetch models: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_chat():
    """Test a simple chat request"""
    print_header("4. Testing Chat Endpoint")
    
    endpoint = config.LLM_CONFIG['endpoint']
    token = config.LLM_CONFIG['api_key']
    model = config.LLM_CONFIG['model']
    
    print(f"   Model: {model}")
    print(f"   Sending test message...")
    
    try:
        response = requests.post(
            f"{endpoint}/chat",
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json={
                'message': 'Say "Hello from Vanna!" and nothing else.',
                'sessionId': 'test_session',
                'model': model,
                'stream': False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            text = data.get('text', data.get('response', ''))
            print(f"   ✅ Chat successful!")
            print(f"   Response: {text[:100]}...")
            return True
        elif response.status_code == 503:
            print(f"   ❌ Service Unavailable - Model may be down")
            print(f"   Try a different model in config.py")
            return False
        else:
            print(f"   ❌ Chat failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timeout - Model took too long to respond")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_pgvector():
    """Test PgVector database connection"""
    print_header("5. Testing PgVector Database")
    
    try:
        import psycopg2
    except ImportError:
        print("   ⚠️  psycopg2 not installed")
        print("   Install with: pip install psycopg2-binary")
        return False
    
    pg_config = config.PGVECTOR_CONFIG
    print(f"   Host: {pg_config['host']}")
    print(f"   Port: {pg_config['port']}")
    print(f"   Database: {pg_config['database']}")
    print(f"   User: {pg_config['user']}")
    
    try:
        conn = psycopg2.connect(
            host=pg_config['host'],
            port=pg_config['port'],
            database=pg_config['database'],
            user=pg_config['user'],
            password=pg_config['password'],
            connect_timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"   ✅ PostgreSQL connected!")
        print(f"   Version: {version[:50]}...")
        
        # Check for pgvector extension
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        if cursor.fetchone():
            print(f"   ✅ pgvector extension installed!")
        else:
            print(f"   ⚠️  pgvector extension not found (optional)")
            print(f"   Note: Vanna will create tables automatically if needed")
            print(f"   To install pgvector manually:")
            print(f"   1. Install pgvector on your PostgreSQL server")
            print(f"   2. Then run: CREATE EXTENSION vector;")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n   Solutions:")
        print("   1. Ensure PostgreSQL is running")
        print("   2. Check credentials in config.py")
        print("   3. Verify database exists:")
        print(f"      psql -U {pg_config['user']} -d {pg_config['database']}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_oracle():
    """Test Oracle database connection"""
    print_header("6. Testing Oracle Database")
    
    try:
        import oracledb
    except ImportError:
        print("   ⚠️  oracledb not installed")
        print("   Install with: pip install vanna[oracle]")
        return False
    
    db_config = config.DATA_DB_CONFIG
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   Schema: {db_config['schema']}")
    print(f"   User: {db_config['user']}")
    
    try:
        dsn = oracledb.makedsn(
            db_config['host'],
            db_config['port'],
            service_name=db_config['database']
        )
        
        conn = oracledb.connect(
            user=db_config['user'],
            password=db_config['password'],
            dsn=dsn
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM v$version WHERE ROWNUM = 1")
        version = cursor.fetchone()[0]
        
        print(f"   ✅ Oracle connected!")
        print(f"   Version: {version[:50]}...")
        
        # Test schema access
        cursor.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {db_config['schema']}")
        cursor.execute("SELECT COUNT(*) FROM user_tables")
        table_count = cursor.fetchone()[0]
        
        print(f"   ✅ Schema '{db_config['schema']}' accessible")
        print(f"   Tables found: {table_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n   Solutions:")
        print("   1. Ensure Oracle is running")
        print("   2. Check credentials in config.py")
        print("   3. Verify listener is up: lsnrctl status")
        return False

def main():
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*10 + "UMBRELLA GATEWAY CONNECTION TEST" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {
        'health': test_health(),
        'auth': test_auth(),
        'models': test_models(),
        'chat': test_chat(),
        'pgvector': test_pgvector(),
        'oracle': test_oracle(),
    }
    
    print_header("Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {status} - {test_name.title()}")
    
    print(f"\n   Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n   🎉 All tests passed! Ready to run Vanna.")
        print("\n   Next step:")
        print("   $ python quick_start_flask.py")
        sys.exit(0)
    else:
        print("\n   ⚠️  Some tests failed. Fix the issues above before running Vanna.")
        print("\n   See UMBRELLA_GATEWAY_SETUP.md for detailed troubleshooting.")
        sys.exit(1)

if __name__ == '__main__':
    main()
