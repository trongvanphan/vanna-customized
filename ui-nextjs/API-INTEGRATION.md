# Next.js + Flask API Integration Guide

## Problem Fixed
Error: **"The rest of the API is not ported yet"**

## Root Cause
Next.js UI was calling `/api/v0/ask` which didn't exist in Flask. Flask had a catch-all route that returned this error for any unimplemented endpoints.

## Solutions Implemented

### 1. Added `/api/v0/ask` Endpoint to Flask ✅

**File**: `src/vanna/flask/__init__.py`

Added comprehensive endpoint that combines the full workflow:
- SQL generation (`vn.generate_sql()`)
- SQL validation (`vn.is_sql_valid()`)
- Query execution (`vn.run_sql()`)
- Chart generation (`vn.generate_plotly_code()`, `vn.get_plotly_figure()`)

**Request format:**
```json
POST /api/v0/ask
{
  "question": "Show me all employees",
  "sessionId": "optional-session-id"
}
```

**Response format (success):**
```json
{
  "sql": "SELECT * FROM employees",
  "data": [...],
  "columns": ["id", "name", "salary"],
  "dtypes": {"id": "int64", "name": "object", "salary": "float64"},
  "execution_time": 1.23,
  "figure_id": "abc123" // Optional, if chart was generated
}
```

**Response format (error):**
```json
{
  "sql": "INVALID SQL",
  "error": "Error message",
  "execution_time": 0.5
}
```

### 2. Fixed Config Endpoint Conflict ✅

**Problem**: Two routes for `/api/v0/get_config`:
- Flask base: Returns `{"type": "config", "config": {...}}`
- ConfigUI: Returns `{"llm": {...}, "database": {...}, ...}`

**Solution**: Renamed ConfigUI route to `/api/v0/get_all_config`

**Files changed:**
- `src/myDbAssistant/config_ui.py` - Route renamed
- `ui-nextjs/src/lib/api-client.ts` - Updated to use new route

### 3. Updated Next.js API Client ✅

**File**: `ui-nextjs/src/lib/api-client.ts`

Changes:
- `getConfig()` now calls `/api/v0/get_all_config`
- `askQuestion()` calls `/api/v0/ask` (now exists!)

## API Endpoints Available

### Question & Answer
| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v0/ask` | POST | Complete Q&A workflow | ✅ NEW |
| `/api/v0/generate_sql` | GET | SQL generation only | ✅ Existing |
| `/api/v0/run_sql` | GET | Execute SQL | ✅ Existing |
| `/api/v0/generate_plotly_figure` | GET | Get chart by ID | ✅ Existing |

### Configuration (from ConfigUI)
| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/v0/get_all_config` | GET | Get all configs | ✅ Fixed |
| `/api/v0/update_llm_config` | POST | Update LLM settings | ✅ Existing |
| `/api/v0/update_database_config` | POST | Update DB settings | ✅ Existing |
| `/api/v0/update_chromadb_config` | POST | Update vector store | ✅ Existing |
| `/api/v0/update_flask_config` | POST | Update Flask settings | ✅ Existing |
| `/api/v0/update_training_config` | POST | Update training settings | ✅ Existing |
| `/api/v0/test_database_connection` | POST | Test DB connection | ✅ Existing |
| `/api/v0/test_llm_connection` | POST | Test LLM connection | ✅ Existing |
| `/api/v0/load_training_data` | POST | Load training data | ✅ Existing |

## Testing

### 1. Restart Flask Server
```bash
cd src/myDbAssistant
lsof -ti:8084 | xargs kill -9
python3 quick_start_flask_ui.py
```

Look for:
```
✅ CORS enabled for Next.js frontend (localhost:3000)
✅ Configuration UI enabled at /settings
 * Running on http://0.0.0.0:8084
```

### 2. Restart Next.js
```bash
cd ui-nextjs
lsof -ti:3000 | xargs kill -9
npm run dev
```

Look for:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

### 3. Test End-to-End
1. Open http://localhost:3000
2. Type a question: "Show me all employees"
3. Submit
4. Should see:
   - ✅ SQL query displayed
   - ✅ Data table with results
   - ✅ Chart (if applicable)
   - ✅ No "The rest of the API is not ported yet" error

### 4. Test Settings Page
1. Navigate to http://localhost:3000/settings
2. Should see all configuration forms
3. Try updating LLM settings
4. Should see success message, no API errors

## How It Works Now

### Question Flow
```
User enters question in Next.js UI
    ↓
POST /api/v0/ask {"question": "..."}
    ↓
Next.js proxy forwards to Flask
    ↓
Flask: Generate SQL
    ↓
Flask: Execute SQL
    ↓
Flask: Generate chart (if applicable)
    ↓
Response with SQL + data + chart ID
    ↓
Next.js renders results
```

### Settings Flow
```
User visits /settings page
    ↓
GET /api/v0/get_all_config
    ↓
Returns all config sections
    ↓
User updates settings
    ↓
POST /api/v0/update_*_config
    ↓
JSON files in ui/config/ updated
    ↓
Success confirmation
```

## Key Implementation Details

### Cache Integration
The `/api/v0/ask` endpoint integrates with Flask's cache system:
```python
id = self.cache.generate_id(question=question)
self.cache.set(id=id, field="question", value=question)
self.cache.set(id=id, field="sql", value=sql)
self.cache.set(id=id, field="df", value=df)
self.cache.set(id=id, field="fig", value=fig)
```

This allows:
- Chart retrieval via `/api/v0/generate_plotly_figure?id={id}`
- Question history tracking
- Result caching for performance

### Error Handling
Comprehensive error handling at multiple levels:
1. **Request validation**: Missing question → 400 error
2. **SQL validation**: Invalid SQL → Returns SQL with error message
3. **Execution errors**: SQL fails → Returns SQL + error message
4. **Chart errors**: Chart generation fails → Query still succeeds, no chart ID

### Chart Generation Logic
Charts only generated when appropriate:
```python
if df is not None and not df.empty and vn.should_generate_chart(df):
    # Generate chart
```

`should_generate_chart()` checks:
- DataFrame not empty
- Has numeric columns for visualization
- Result set appropriate size

## Remaining Work

### Optional Enhancements
These are **not required** for basic functionality but could improve UX:

1. **Streaming responses**: Add Server-Sent Events for real-time SQL generation
2. **Query history**: Implement `/api/v0/get_question_history` integration
3. **SQL editing**: Allow users to edit generated SQL before execution
4. **Export options**: CSV download, SQL export

### Production Considerations
Before deploying to production:

1. **Authentication**: Currently using `@self.requires_auth` but may need real auth
2. **Rate limiting**: Add rate limiting to prevent abuse
3. **Caching strategy**: Configure cache TTL and size limits
4. **Error logging**: Add structured logging for errors
5. **Monitoring**: Add metrics for query performance

## Troubleshooting

### Issue: "The rest of the API is not ported yet"
**Cause**: Old Flask version without `/api/v0/ask`
**Fix**: Restart Flask server after pulling latest changes

### Issue: 404 on `/api/v0/ask`
**Check**:
```bash
curl -X POST http://localhost:8084/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"test"}'
```
Should return JSON response, not 404.

### Issue: CORS errors still happening
**Check**: Flask logs show "✅ CORS enabled"
**Fix**: Restart both Flask and Next.js

### Issue: Config endpoint returns wrong format
**Old format** (Flask base):
```json
{"type": "config", "config": {...}}
```

**New format** (ConfigUI):
```json
{"llm": {...}, "database": {...}, ...}
```

Make sure Next.js is calling `/api/v0/get_all_config`, not `/api/v0/get_config`.

## Files Modified

### Flask Backend
1. **`src/vanna/flask/__init__.py`**
   - Added `/api/v0/ask` endpoint (156 lines)
   - Handles complete Q&A workflow

2. **`src/myDbAssistant/config_ui.py`**
   - Renamed `/api/v0/get_config` → `/api/v0/get_all_config`
   - Avoids conflict with Flask base route

### Next.js Frontend
3. **`ui-nextjs/src/lib/api-client.ts`**
   - Updated `getConfig()` to call `/api/v0/get_all_config`
   - Uses relative URLs in development (CORS fix)

## Summary

✅ **Problem solved**: "The rest of the API is not ported yet" error eliminated

✅ **New endpoint**: `/api/v0/ask` provides complete Q&A workflow

✅ **Config fixed**: Settings page now works correctly

✅ **Ready for use**: Next.js UI fully functional with Flask backend

The Next.js UI now has full API integration with the Flask backend! 🎉
