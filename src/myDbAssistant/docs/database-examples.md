# Database Configuration Examples

This document provides configuration examples for all supported database types.

## Oracle Database

**File:** `ui/config/database.json`

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

**Installation:**
```bash
pip install 'vanna[oracle]'
```

**Note:** Quotes are required in zsh (macOS default shell).

**Test Connection:**
```bash
sqlplus hr/hr123@localhost:1521/XEPDB1
```

**Verify Schema:**
```sql
SELECT COUNT(*) FROM all_tables WHERE owner = 'HR';
```

---

## PostgreSQL

**File:** `ui/config/database.json`

```json
{
  "type": "postgres",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "schema": "public",
  "user": "postgres",
  "password": "postgres"
}
```

**Installation:**
```bash
pip install 'vanna[postgres]'
```

**Test Connection:**
```bash
psql -h localhost -p 5432 -U postgres -d mydb
```

**Verify Schema:**
```sql
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';
```

---

## MySQL

**File:** `ui/config/database.json`

```json
{
  "type": "mysql",
  "host": "localhost",
  "port": 3306,
  "database": "mydb",
  "schema": "mydb",
  "user": "root",
  "password": "root"
}
```

**Installation:**
```bash
pip install 'vanna[mysql]'
```

**Test Connection:**
```bash
mysql -h localhost -P 3306 -u root -p mydb
```

**Verify Schema:**
```sql
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'mydb';
```

---

## Microsoft SQL Server

**File:** `ui/config/database.json`

```json
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

**Alternative type:** Can use `"sqlserver"` instead of `"mssql"`

**Installation:**
```bash
pip install 'vanna[mssql]'
```

**Test Connection:**
```bash
sqlcmd -S localhost,1433 -U sa -P 'YourStrong!Passw0rd' -d mydb
```

**Verify Schema:**
```sql
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'dbo';
```

---

## Switching Databases

To switch between databases:

### Option 1: Edit JSON File
Simply edit `ui/config/database.json` and change the `type` and connection parameters.

### Option 2: Programmatic Update
```python
from ui import ConfigLoader

loader = ConfigLoader()
loader.update_database_config({
    'type': 'postgres',
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'schema': 'public',
    'user': 'postgres',
    'password': 'postgres'
})
```

### Option 3: Multiple Configurations
Create separate config files for each database:
- `database-oracle.json`
- `database-postgres.json`
- `database-mysql.json`
- `database-mssql.json`

Then copy the desired one to `database.json` when needed.

---

## Default Ports Reference

| Database | Default Port |
|----------|-------------|
| Oracle | 1521 |
| PostgreSQL | 5432 |
| MySQL | 3306 |
| Microsoft SQL Server | 1433 |
| Snowflake | 443 (HTTPS) |

---

## Common Issues

### Oracle: "ORA-12154: TNS:could not resolve the connect identifier"
- Check DSN format: `host:port/database`
- Verify database is running: `lsnrctl status`

### PostgreSQL: "FATAL: password authentication failed"
- Check pg_hba.conf allows connections
- Verify user has access: `GRANT ALL ON DATABASE mydb TO postgres;`

### MySQL: "ERROR 1045: Access denied"
- Verify user has privileges: `GRANT ALL PRIVILEGES ON mydb.* TO 'root'@'localhost';`
- Check if password is correct

### SQL Server: "Login failed for user"
- Enable SQL Server authentication (not just Windows auth)
- Verify TCP/IP is enabled in SQL Server Configuration Manager
- Check firewall allows port 1433

---

## Security Best Practices

### For Production

**Never commit passwords to git!**

Use environment variables:

```python
import os
from ui import ConfigLoader

loader = ConfigLoader()
db_config = loader.load_database_config()

# Override with environment variables
db_config['password'] = os.getenv('DB_PASSWORD', db_config['password'])
db_config['user'] = os.getenv('DB_USER', db_config['user'])
```

Or use a `.env` file (add to `.gitignore`):

```bash
# .env
DB_HOST=production-db.example.com
DB_USER=prod_user
DB_PASSWORD=secure_password_here
DB_DATABASE=prod_db
```

Then load with python-dotenv:

```python
from dotenv import load_dotenv
load_dotenv()

loader.update_database_config({
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
})
```

---

## Testing Your Configuration

Before running the full application, test your database configuration:

```bash
cd src/myDbAssistant
python quick_start_flask_ui.py
```

Look for:
```
✅ Connected to [DATABASE_TYPE] database
✅ Using schema: [SCHEMA_NAME] ([N] tables found)
```

If you see errors, check:
1. Database is running
2. Credentials are correct
3. Required Python driver is installed
4. Firewall allows connection
5. User has proper privileges
