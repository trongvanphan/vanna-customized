#!/usr/bin/env python3
"""
Quick test to verify Oracle connection works in Flask app
"""

import requests
import json

# Test SQL generation
print("🧪 Testing Oracle Query Generation...\n")

url = "http://localhost:8084/api/v0/generate_sql"
headers = {"Content-Type": "application/json"}
data = {"question": "How many employees are there in total?"}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    
    if 'sql' in result:
        print(f"✅ SQL Generated Successfully:")
        print(f"   {result['sql']}\n")
    else:
        print(f"❌ No SQL returned")
        print(f"   Response: {result}\n")
        
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test SQL execution
print("🧪 Testing Oracle Query Execution...\n")

sql_query = "SELECT COUNT(*) as employee_count FROM employees"

url2 = "http://localhost:8084/api/v0/run_sql"
data2 = {"sql": sql_query}

try:
    response2 = requests.post(url2, headers=headers, json=data2, timeout=30)
    response2.raise_for_status()
    
    result2 = response2.json()
    
    if 'df' in result2:
        print(f"✅ Query Executed Successfully:")
        print(f"   Result: {result2['df']}\n")
    else:
        print(f"❌ No results returned")
        print(f"   Response: {result2}\n")
        
except Exception as e:
    print(f"❌ Error: {e}\n")

print("✅ Oracle connection tests complete!")
