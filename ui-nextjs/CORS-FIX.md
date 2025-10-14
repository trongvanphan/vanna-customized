# CORS Fix for Next.js + Flask Integration

## Problem
Next.js UI was showing "No response from server" error even though Flask backend was running correctly on port 8084.

## Root Cause
**Cross-Origin Resource Sharing (CORS)** blocking:
- Next.js dev server runs on `http://localhost:3000`
- Flask backend runs on `http://localhost:8084`
- Different ports = different origins → Browser blocks requests by default

## Solutions Implemented

### Solution 1: Enable CORS in Flask Backend ✅

Added `flask-cors` to Flask backend:

```python
# In src/myDbAssistant/quick_start_flask_ui.py
from flask_cors import CORS

# After creating Flask app:
CORS(vanna_flask.flask_app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     supports_credentials=True)
```

**To install:**
```bash
pip3 install flask-cors
```

**Restart Flask after adding CORS:**
```bash
# Kill existing Flask process
lsof -ti:8084 | xargs kill -9

# Start Flask with CORS enabled
cd src/myDbAssistant
python3 quick_start_flask_ui.py
```

### Solution 2: Use Next.js API Proxy (Recommended) ✅

Modified `ui-nextjs/src/lib/api-client.ts` to use **relative URLs** in development mode, allowing Next.js to proxy requests to Flask:

```typescript
// Old: Direct calls to Flask (CORS issues)
const FLASK_URL = 'http://localhost:8084';

// New: Use Next.js proxy in development
const FLASK_URL = 
  typeof window !== 'undefined' && process.env.NODE_ENV === 'development'
    ? '' // Relative URLs → Next.js proxies to Flask
    : process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084';
```

**How it works:**
1. Next.js dev server receives request: `http://localhost:3000/api/v0/ask`
2. `next.config.js` rewrites rule matches: `/api/v0/:path*`
3. Next.js forwards to Flask: `http://localhost:8084/api/v0/ask`
4. Response returned to browser via Next.js (same origin)

**Configuration in `next.config.js`:**
```javascript
async rewrites() {
  return [
    {
      source: '/api/v0/:path*',
      destination: `${process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084'}/api/v0/:path*`,
    },
  ];
}
```

## Why Use Both Solutions?

1. **Development**: Next.js proxy handles CORS automatically (cleaner, no CORS preflight)
2. **Production**: Direct Flask calls with CORS enabled (simpler deployment, no proxy needed)
3. **Flexibility**: Works in both scenarios

## Testing

### 1. Verify Flask is running with CORS:
```bash
curl -s -X GET "http://localhost:8084/api/v0/get_config" \
  -H "Origin: http://localhost:3000" \
  -v 2>&1 | grep -i "access-control"
```

Should see: `Access-Control-Allow-Origin: http://localhost:3000`

### 2. Test Next.js proxy:
```bash
# Start Next.js dev server
cd ui-nextjs
npm run dev

# Open browser console at http://localhost:3000
# Submit a question
# Check Network tab: requests should go to localhost:3000/api/v0/...
```

### 3. Verify end-to-end:
1. Start Flask: `cd src/myDbAssistant && python3 quick_start_flask_ui.py`
2. Start Next.js: `cd ui-nextjs && npm run dev`
3. Open http://localhost:3000
4. Ask a question: "Show me all employees"
5. Should see SQL results without errors

## Common Issues

### Issue: "No response from server"
**Check:**
- Flask is running: `curl http://localhost:8084/api/v0/get_config`
- Next.js is running: `lsof -ti:3000`
- CORS enabled: Look for "✅ CORS enabled" in Flask logs
- Browser console: Check for actual error message

### Issue: CORS errors in browser console
**Solutions:**
1. Restart Flask after adding CORS
2. Clear browser cache
3. Verify Flask logs show CORS setup
4. Check `.env.local` has correct Flask URL

### Issue: 404 on API calls
**Check:**
- Flask endpoints exist: `curl http://localhost:8084/api/v0/ask -X POST`
- Next.js rewrites config matches your endpoint path
- No typos in API client function calls

## Files Modified

1. **Flask Backend**: `src/myDbAssistant/quick_start_flask_ui.py`
   - Added `from flask_cors import CORS`
   - Added CORS configuration after Flask app creation

2. **Next.js API Client**: `ui-nextjs/src/lib/api-client.ts`
   - Modified `FLASK_URL` to use relative URLs in development
   - Enables automatic proxying via Next.js

3. **Next.js Config**: `ui-nextjs/next.config.js` (already configured)
   - Rewrites API calls from `/api/v0/*` to Flask backend

## Production Deployment

For production, you have two options:

### Option A: Keep both services separate (recommended)
- Deploy Flask on: `https://api.yourdomain.com`
- Deploy Next.js on: `https://yourdomain.com`
- Set `NEXT_PUBLIC_FLASK_URL=https://api.yourdomain.com`
- Flask CORS must be enabled with your production domain

### Option B: Deploy as single service
- Deploy Flask + serve Next.js static build from Flask
- No CORS needed (same origin)
- Use Flask to serve `ui-nextjs/out/` directory

## Additional Resources

- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Next.js Rewrites](https://nextjs.org/docs/app/api-reference/next-config-js/rewrites)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## Summary

✅ **Problem solved**: Next.js can now communicate with Flask backend without CORS errors

✅ **Development mode**: Uses Next.js proxy (no CORS issues)

✅ **Production mode**: Uses direct calls with CORS enabled

✅ **Flexible**: Works in both scenarios seamlessly
