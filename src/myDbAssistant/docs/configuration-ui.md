# Configuration UI Guide

## Overview

The myDbAssistant configuration UI allows you to manage all application settings through a web interface instead of manually editing JSON files.

## Accessing the Configuration UI

1. **Start the application:**
   ```bash
   cd src/myDbAssistant
   python3 quick_start_flask_ui.py
   ```

2. **Open your browser:**
   - Main UI: http://localhost:8084
   - Configuration UI: http://localhost:8084/config

## Configuration Sections

### 🗄️ Database Configuration

Configure your database connection settings:

- **Database Type**: Select from Oracle, PostgreSQL, MySQL, or SQL Server
- **Host**: Database server hostname (e.g., localhost)
- **Port**: Database port (default: 1521 for Oracle, 5432 for PostgreSQL, 3306 for MySQL, 1433 for SQL Server)
- **Database**: Database name or SID
- **Schema**: Schema to use for queries
- **Username**: Database username
- **Password**: Database password

**Actions:**
- **Test Connection**: Verify settings work before saving
- **Save Database Config**: Save changes (requires app restart)

**Example Configurations:**

**Oracle:**
```
Type: oracle
Host: localhost
Port: 1521
Database: XEPDB1
Schema: hr
User: hr
Password: hr123
```

**PostgreSQL:**
```
Type: postgres
Host: localhost
Port: 5432
Database: mydb
Schema: public
User: postgres
Password: postgres
```

**MySQL:**
```
Type: mysql
Host: localhost
Port: 3306
Database: mydb
Schema: mydb
User: root
Password: root
```

**SQL Server:**
```
Type: mssql
Host: localhost
Port: 1433
Database: mydb
Schema: dbo
User: sa
Password: YourStrong!Passw0rd
```

### 🤖 LLM Configuration

Configure Umbrella Gateway (GitHub Copilot) settings:

- **API Endpoint**: Umbrella Gateway URL (default: http://localhost:8765)
- **API Key / Auth Token**: Get from `.vscode/settings.json`
- **Model**: Choose from available models:
  - `copilot/gpt-5-mini` - Fast, efficient
  - `copilot/gpt-5` - Balanced performance
  - `copilot/claude-sonnet-4` - Most powerful
  - `copilot/o1-mini` - Reasoning-focused
- **Temperature**: 0.0 (deterministic) to 2.0 (creative)
- **Max Tokens**: Maximum response length (default: 4096)
- **Timeout**: Request timeout in seconds (default: 60)

**Actions:**
- **Test LLM**: Verify connection to Umbrella Gateway
- **Save LLM Config**: Save changes (requires app restart)

**Getting Your Auth Token:**
```bash
cat .vscode/settings.json | grep authToken
```

### 📚 Training Configuration

Control how and when training data is loaded:

- **Auto-train on startup**: Automatically load training data when app starts
- **Training Data Path**: Path to training data directory (default: ../trainingMyDb)
- **Load DDL**: Load SQL schema files from `ddl/` directory
- **Load Documentation**: Load business rules from `documentation/` directory
- **Load Training Pairs**: Load Q&A examples from `trainingpairs/` directory
- **Skip if exists**: Don't re-add training data that already exists
- **Verbose output**: Show detailed training progress

**Actions:**
- **Run Training Now**: Manually trigger training data load
- **Save Training Config**: Save settings

**Recommended Settings:**
```
✓ Auto-train on startup (for first-time setup)
✓ Load DDL
✓ Load Documentation
✓ Load Training Pairs
✓ Skip if exists (prevents duplicates)
✓ Verbose output (see what's happening)
```

**After Initial Training:**
```
☐ Auto-train on startup (faster restarts)
✓ Skip if exists
```

### 🌐 Flask Configuration

Configure the web server:

- **Host**: 
  - `0.0.0.0` - Accessible from network
  - `127.0.0.1` - Localhost only (more secure)
- **Port**: Server port (default: 8084)
- **Debug Mode**: Enable Flask debugger (⚠️ disable in production)

**UI Settings:**
- **Title**: Main page title
- **Subtitle**: Main page subtitle
- **Allow LLM to see data**: Enable intermediate SQL pattern for data introspection

**Actions:**
- **Save Flask Config**: Save changes (requires app restart)

### 💾 ChromaDB Configuration

Configure vector database settings:

- **Persist Directory**: Where ChromaDB stores data (default: ./chromadb)
- **Collection Name**: ChromaDB collection name (default: vanna_vectors)
- **Embedding Model**: Sentence transformer model (default: all-MiniLM-L6-v2)
- **SQL Results Count**: Number of similar Q&A pairs to retrieve (default: 10)
- **DDL Results Count**: Number of related schemas to retrieve (default: 10)
- **Documentation Results Count**: Number of related docs to retrieve (default: 10)

**Actions:**
- **Clear ChromaDB**: ⚠️ Delete ALL training data (cannot be undone!)
- **Save ChromaDB Config**: Save changes (requires app restart)

## Workflow Examples

### First-Time Setup

1. **Configure Database**
   - Go to 🗄️ Database tab
   - Select your database type
   - Enter connection details
   - Click "Test Connection"
   - Click "Save Database Config"

2. **Configure LLM**
   - Go to 🤖 LLM tab
   - Get auth token: `cat .vscode/settings.json | grep authToken`
   - Paste token in "API Key" field
   - Select your preferred model
   - Click "Test LLM"
   - Click "Save LLM Config"

3. **Configure Training**
   - Go to 📚 Training tab
   - Enable "Auto-train on startup"
   - Enable all "Load" options
   - Enable "Skip if exists" and "Verbose"
   - Click "Save Training Config"

4. **Restart Application**
   ```bash
   # Stop with Ctrl+C
   python3 quick_start_flask_ui.py
   ```

5. **Verify**
   - Training data loads automatically
   - Ask a question in main UI
   - Generate and run SQL

### Switching Databases

**Method 1: Use Configuration UI**
1. Go to http://localhost:8084/config
2. Click 🗄️ Database tab
3. Change "Database Type" dropdown
4. Update host, port, database, schema, credentials
5. Click "Test Connection"
6. Click "Save Database Config"
7. Restart application

**Method 2: Edit JSON Directly**
1. Edit `ui/config/database.json`
2. Change `"type": "oracle"` to `"type": "postgres"`
3. Update other fields
4. Restart application

### Changing LLM Model

1. Go to http://localhost:8084/config
2. Click 🤖 LLM tab
3. Select new model from dropdown
4. Optionally adjust temperature/tokens
5. Click "Test LLM" to verify
6. Click "Save LLM Config"
7. Restart application

### Managing Training Data

**Add Training Data:**
1. Add files to `trainingMyDb/` directories:
   - `ddl/*.sql` - Schema definitions
   - `documentation/*.md` - Business rules
   - `trainingpairs/*.json` - Q&A examples

2. Go to http://localhost:8084/config
3. Click 📚 Training tab
4. Click "Run Training Now"
5. Wait for completion message

**Clear and Retrain:**
1. Go to http://localhost:8084/config
2. Click 💾 ChromaDB tab
3. Click "Clear ChromaDB"
4. Confirm deletion
5. Restart application (training data reloads)

## API Endpoints

The configuration UI also exposes REST API endpoints:

### Get Configuration
```bash
# Get database config
curl http://localhost:8084/api/config/database

# Get LLM config
curl http://localhost:8084/api/config/llm

# Get training config
curl http://localhost:8084/api/config/training

# Get Flask config
curl http://localhost:8084/api/config/flask

# Get ChromaDB config
curl http://localhost:8084/api/config/chromadb
```

### Update Configuration
```bash
# Update database config
curl -X POST http://localhost:8084/api/config/database \
  -H "Content-Type: application/json" \
  -d '{"type": "postgres", "host": "localhost", "port": 5432, ...}'

# Update LLM config
curl -X POST http://localhost:8084/api/config/llm \
  -H "Content-Type: application/json" \
  -d '{"model": "copilot/gpt-5", "temperature": 0.7, ...}'
```

### Test Connections
```bash
# Test database connection
curl http://localhost:8084/api/test/database

# Test LLM connection
curl http://localhost:8084/api/test/llm
```

### Training Operations
```bash
# Run training manually
curl -X POST http://localhost:8084/api/train

# Clear ChromaDB
curl -X POST http://localhost:8084/api/chromadb/clear
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Passwords in Browser**: The UI shows passwords. Only use on trusted networks.

2. **Network Access**: Default host `0.0.0.0` allows network access. For production:
   ```
   Host: 127.0.0.1  (localhost only)
   Debug: disabled
   ```

3. **HTTPS**: Consider using HTTPS proxy (nginx, Apache) for production

4. **Authentication**: The configuration UI has no authentication. Consider:
   - Firewall rules
   - VPN access only
   - Reverse proxy with auth

5. **API Endpoints**: All `/api/config/*` endpoints are unauthenticated

## Troubleshooting

### "Config file not found"
**Solution:** Ensure all JSON files exist in `ui/config/`:
```bash
ls -la ui/config/
# Should show: database.json, llm.json, flask.json, chromadb.json, training.json
```

### "Connection test failed"
**Database:**
- Verify database is running
- Check credentials
- Test connection manually: `psql -h localhost -U postgres -d mydb`

**LLM:**
- Ensure VS Code is open
- Start Umbrella Gateway: `Cmd+Shift+P` → "Umbrella Gateway: Start Server"
- Verify token is current: `cat .vscode/settings.json | grep authToken`

### "Training failed"
**Solutions:**
- Check training data exists: `ls -la trainingMyDb/`
- Verify JSON format: `python -m json.tool < trainingMyDb/trainingpairs/hr_questions.json`
- Check verbose output for specific errors

### "Changes not taking effect"
**Solution:** Always restart the application after configuration changes:
```bash
# Stop with Ctrl+C
python3 quick_start_flask_ui.py
```

### "Port already in use"
**Solution:** Change port in Flask config:
```
Port: 8085 (or any available port)
```

## Best Practices

1. **Test Before Saving**: Always use "Test Connection" before saving database/LLM configs

2. **Backup Configurations**: Copy `ui/config/*.json` before major changes

3. **Incremental Changes**: Change one thing at a time, test, then save

4. **Version Control**: Use git to track configuration changes:
   ```bash
   git add ui/config/*.json
   git commit -m "Updated database to PostgreSQL"
   ```

5. **Documentation**: Add notes to JSON files (use `"_comment"` fields)

6. **Environment Variables**: For production, use environment variables instead of hardcoded credentials

## Related Documentation

- **Multi-Database Setup**: See `docs/database-examples.md`
- **Training Data Format**: See `docs/TRAINING_DATA_FORMAT.md`
- **Umbrella Gateway**: See `.github/copilot-instructions.md`
- **JSON Configuration System**: See `ui/README.md`

## Support

For issues:
- Configuration UI bugs: Report in GitHub issues
- Database connection: See `docs/database-examples.md`
- LLM connection: See Umbrella Gateway documentation
- Training: See `docs/TRAINING_DATA_FORMAT.md`
