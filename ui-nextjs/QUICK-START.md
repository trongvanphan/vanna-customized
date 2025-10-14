# Quick Start Guide - Db Assistant

## Summary of Changes

✅ **Completed Updates:**
1. Replaced "Vanna AI" with "Db Assistant" throughout the application
2. Changed keyboard shortcut from `Cmd+Enter` to `Enter` (use `Shift+Enter` for new lines)
3. Created Settings page at `/settings` to configure LLM, Database, ChromaDB, Flask, and Training
4. Created Training page at `/training` to load training data
5. Added navigation links in the header (Settings and Training buttons)

---

## How to Start the Application

### Step 1: Start Flask Backend

The Flask backend must be running first:

```bash
# Terminal 1: Start Flask backend
cd src/myDbAssistant
python3 quick_start_flask_ui.py
```

**Expected output:**
```
✅ Training data already exists (XXX items)
   Skipping training data load to avoid duplicates.
📊 Flask UI Settings:
   - Host: 0.0.0.0
   - Port: 8084
   - Debug: True
🌐 Flask app running on: http://0.0.0.0:8084
```

**Important:** Keep this terminal running! The Next.js app needs to connect to this Flask backend.

### Step 2: Start Next.js Frontend

In a separate terminal:

```bash
# Terminal 2: Start Next.js development server
cd ui-nextjs
npm run dev
```

**Expected output:**
```
▲ Next.js 14.2.33
- Local:        http://localhost:3000
✓ Ready in ~1.5s
```

### Step 3: Open the Application

Open your browser and navigate to:
```
http://localhost:3000
```

---

## Application Features

### 1. Home Page (http://localhost:3000)

**Ask Questions:**
- Type your question in the input field
- Press **Enter** to submit (or click the send button)
- Use **Shift+Enter** for new lines in multi-line questions

**View Results:**
- Generated SQL with syntax highlighting
- Copy SQL to clipboard
- Results table with pagination (50 rows per page)
- Interactive Plotly charts
- Execution time and status

### 2. Settings Page (http://localhost:3000/settings)

Configure all aspects of the application through a web interface:

**LLM Settings:**
- API Key (from VS Code Copilot Socket Core)
- Endpoint (default: http://127.0.0.1:8765)
- Model selection (gpt-5-mini, gpt-5, claude-sonnet-4, o1-mini)
- Temperature, max tokens
- Test connection button

**Database Settings:**
- Database type (Oracle, PostgreSQL, MySQL, SQL Server)
- Connection parameters (host, port, database, schema, user, password)
- Auto-fills default ports based on type
- Test connection button

**ChromaDB Settings:**
- Number of results to retrieve for SQL, DDL, and documentation
- Persist directory path

**Flask Settings:**
- Host and port (requires restart)
- UI title and subtitle
- Debug mode toggle
- Allow LLM to see data toggle

**Training Settings:**
- Auto-train on startup toggle
- Training data path
- Load options (DDL, documentation, training pairs)
- Skip if exists option

### 3. Training Page (http://localhost:3000/training)

**Load Training Data:**
- Click "Load Training Data" button to populate the vector store
- Loads DDL files (database schemas)
- Loads documentation (business rules)
- Loads training pairs (example Q&A)
- Displays statistics after loading

**Training Data Location:**
Default path: `src/myDbAssistant/trainingMyDb/`
```
trainingMyDb/
├── ddl/                    # .sql files with CREATE TABLE statements
├── documentation/          # .md files with business rules
└── trainingpairs/          # .json files with question-SQL pairs
```

**Training Pairs Format:**
```json
[
  {
    "question": "What are the top 10 customers by sales?",
    "sql": "SELECT customer_name, SUM(sales) as total FROM customers GROUP BY customer_name ORDER BY total DESC LIMIT 10"
  }
]
```

---

## Fixing the "No response from server" Error

This error appears when the Next.js frontend cannot connect to the Flask backend.

### Step 1: Verify Flask Backend is Running

```bash
# Check if Flask is running on port 8084
curl http://localhost:8084/health

# Or check if port is in use
lsof -i :8084  # macOS/Linux
```

**If Flask is not running:**
```bash
cd src/myDbAssistant
python3 quick_start_flask_ui.py
```

### Step 2: Verify Environment Variables

Check that `.env.local` exists in `ui-nextjs/` folder:

```bash
cat ui-nextjs/.env.local
```

**Should contain:**
```env
NEXT_PUBLIC_FLASK_URL=http://localhost:8084
```

**If file doesn't exist, create it:**
```bash
cd ui-nextjs
echo "NEXT_PUBLIC_FLASK_URL=http://localhost:8084" > .env.local
```

### Step 3: Restart Next.js Dev Server

After creating `.env.local`, you must restart the Next.js server:

```bash
# Press Ctrl+C to stop the server, then:
npm run dev
```

### Step 4: Check CORS Configuration

The Flask backend must allow requests from `http://localhost:3000`.

**In `quick_start_flask_ui.py`, verify CORS is enabled:**
```python
from flask_cors import CORS

# Should have CORS enabled
CORS(app)
```

### Step 5: Test the Connection

Open browser DevTools (F12) → Network tab, then:
1. Submit a question
2. Check the network request to `/api/v0/ask`
3. Look for the response status and any error messages

**Common Issues:**
- **ERR_CONNECTION_REFUSED**: Flask backend not running
- **404 Not Found**: Flask endpoint doesn't exist (check Flask routes)
- **CORS Error**: Flask CORS not configured properly
- **500 Internal Server Error**: Check Flask terminal for Python errors

---

## Configuration Guide

### Settings Page (http://localhost:3000/settings)

All configuration can now be done through the web interface! No need to edit JSON files manually.

**Changes take effect:**
- **LLM, ChromaDB, Training:** Immediately after saving
- **Database, Flask:** Requires Flask server restart

**To configure database:**
1. Go to Settings → Database tab
2. Select database type (Oracle, PostgreSQL, MySQL, SQL Server)
3. Fill in connection details
4. Click "Test Connection" to verify
5. Click "Save Configuration"
6. Restart Flask backend

**To configure LLM (Copilot Socket Core):**
1. Start Copilot Socket Core in VS Code:
   - `Cmd+Shift+P` → "Copilot Socket Core: Start Server"
2. Get auth token:
   ```bash
   cat .vscode/settings.json | grep authToken
   ```
3. Go to Settings → LLM tab
4. Paste auth token in "API Key" field
5. Verify endpoint is `http://127.0.0.1:8765`
6. Click "Test Connection"
7. Click "Save Configuration"

---

## Training Data Guide

### How Training Works (RAG Approach)

**1. Training Phase (One-Time Setup):**
- Load database schema (DDL) into vector store
- Load business documentation
- Load example Q&A pairs
- System creates embeddings for semantic search

**2. Query Phase (Every Question):**
- User asks question in natural language
- System searches vector store for relevant:
  - Database schemas (DDL)
  - Business documentation
  - Similar example queries
- Retrieves top N most relevant items (configured in ChromaDB settings)

**3. Generation Phase:**
- LLM receives:
  - User's question
  - Retrieved DDL schemas
  - Retrieved documentation
  - Retrieved example Q&A
- Generates SQL query specific to your database

### Loading Training Data

**Option 1: Via Training Page (Recommended)**
1. Go to http://localhost:3000/training
2. Click "Load Training Data" button
3. Wait for completion
4. View statistics (DDL loaded, docs loaded, pairs loaded)

**Option 2: Via Settings Page**
1. Go to Settings → Training tab
2. Configure training data path
3. Enable/disable what to load (DDL, docs, pairs)
4. Save configuration
5. Use Training page to load

**Option 3: Auto-load on Startup**
1. Go to Settings → Training tab
2. Enable "Auto-train on Startup"
3. Save configuration
4. Restart Flask backend
5. Training data loads automatically

### Adding Your Own Training Data

**DDL Files (.sql):**
```sql
-- File: trainingMyDb/ddl/customers.sql
CREATE TABLE customers (
  customer_id NUMBER PRIMARY KEY,
  customer_name VARCHAR2(100),
  email VARCHAR2(100),
  created_date DATE
);
```

**Documentation Files (.md):**
```markdown
<!-- File: trainingMyDb/documentation/business-rules.md -->
# Customer Business Rules

- Customers are considered "active" if they have made a purchase in the last 90 days
- Sales are calculated as the sum of order totals minus refunds
- Top customers are ranked by total lifetime value
```

**Training Pairs (.json):**
```json
// File: trainingMyDb/trainingpairs/customer-questions.json
[
  {
    "question": "Show me active customers",
    "sql": "SELECT * FROM customers WHERE created_date >= SYSDATE - 90"
  },
  {
    "question": "What are the top 10 customers by sales?",
    "sql": "SELECT c.customer_name, SUM(o.total) as sales FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_name ORDER BY sales DESC FETCH FIRST 10 ROWS ONLY"
  }
]
```

---

## Troubleshooting

### Issue: Cannot access settings page

**Solution:**
```bash
# Restart Next.js dev server
cd ui-nextjs
npm run dev
```

Settings page should be available at http://localhost:3000/settings

### Issue: Training data not loading

**Check:**
1. Training data path is correct (Settings → Training)
2. Files exist in the specified directory
3. Files have correct extensions (.sql, .md, .json)
4. JSON files are valid JSON
5. Check Flask terminal for error messages

### Issue: Questions return empty results

**Possible causes:**
1. Training data not loaded (go to Training page and load)
2. Database not connected (check Settings → Database)
3. LLM not configured (check Settings → LLM)

**Solution:**
1. Load training data first (Training page)
2. Configure database connection (Settings → Database)
3. Test connections (use Test buttons in Settings)

### Issue: Dark mode not working

**Solution:**
Click the dark mode toggle button (moon/sun icon) in the header.
Theme persists in localStorage.

### Issue: Charts not rendering

**Possible causes:**
1. Query returned no numeric data
2. Plotly not loaded properly

**Solution:**
1. Try asking a question that returns numeric data
2. Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
3. Check browser console (F12) for errors

---

## Development Notes

### Project Structure

```
ui-nextjs/
├── src/
│   ├── app/
│   │   ├── page.tsx            # Home page (ask questions)
│   │   ├── settings/
│   │   │   └── page.tsx        # Settings page
│   │   └── training/
│   │       └── page.tsx        # Training page
│   ├── components/
│   │   ├── QuestionInput.tsx   # Question input form
│   │   ├── SQLHighlight.tsx    # SQL syntax highlighting
│   │   ├── ResultsDisplay.tsx  # Results table
│   │   ├── ChartRenderer.tsx   # Plotly charts
│   │   └── ...                 # Other components
│   └── lib/
│       ├── api-client.ts       # Flask API calls
│       ├── types.ts            # TypeScript types
│       └── ...                 # Other utilities
└── ...
```

### API Endpoints

All Flask API endpoints are available via Next.js proxy:

**Questions:**
- `POST /api/v0/ask` - Submit question and get SQL + results

**Configuration:**
- `GET /api/v0/get_config` - Fetch all configurations
- `POST /api/v0/update_llm_config` - Update LLM settings
- `POST /api/v0/update_database_config` - Update database settings
- `POST /api/v0/update_chromadb_config` - Update ChromaDB settings
- `POST /api/v0/update_flask_config` - Update Flask settings
- `POST /api/v0/update_training_config` - Update training settings

**Testing:**
- `POST /api/v0/test_database_connection` - Test database connection
- `POST /api/v0/test_llm_connection` - Test LLM endpoint

**Training:**
- `POST /api/v0/load_training_data` - Load training data
- `GET /api/v0/generate_plotly_figure?id=<id>` - Get chart data

---

## Next Steps

1. ✅ Start Flask backend
2. ✅ Start Next.js frontend
3. ✅ Configure database (Settings → Database)
4. ✅ Configure LLM (Settings → LLM)
5. ✅ Load training data (Training page)
6. ✅ Ask your first question!

**Example questions to try:**
- "What are the top 10 customers by sales?"
- "Show me the revenue trend for the last 12 months"
- "Which products have the highest profit margin?"
- "List all employees in the sales department"

---

## Support

**Flask Backend Issues:**
Check the Flask terminal output for Python errors and stack traces.

**Next.js Frontend Issues:**
Check the browser console (F12) for JavaScript errors.

**Database Connection Issues:**
Use the "Test Connection" button in Settings → Database tab.

**LLM Connection Issues:**
Use the "Test Connection" button in Settings → LLM tab.

---

*Last Updated: 2025-01-14*  
*Version: 1.0*
