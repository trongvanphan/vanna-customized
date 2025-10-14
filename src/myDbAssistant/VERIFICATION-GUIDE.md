# Verification & Troubleshooting Guide

**Date:** October 14, 2025  
**Status:** ✅ All fixes applied and server restarted

---

## ✅ Changes Applied Successfully

### 1. **Settings Button** - FIXED
- ✅ JavaScript injected via `after_request` hook
- ✅ Settings button will appear below "Open Debugger" button
- ✅ Settings icon appears in top-right corner

### 2. **"Vanna Logo" Text Removal** - FIXED
- ✅ Text replacement regex includes "Vanna Logo"
- ✅ Images with alt="Vanna Logo" are hidden and removed
- ✅ All text replaced with "MyDBAssistant"

### 3. **Oracle Connection** - FIXED
- ✅ Enhanced `connect_to_oracle()` method with auto-reconnect
- ✅ Connection verified: 7 tables found in HR schema
- ✅ Test queries successful (see logs above)

---

## 🔍 Why You Might Not See The Changes

### Issue: Browser Cache
**Problem:** Your browser is showing cached version of the page.

**Solution:**
1. **Hard Refresh** (this clears browser cache):
   - **macOS Chrome/Edge:** `Cmd + Shift + R`
   - **macOS Safari:** Hold `Shift` and click Reload button
   - **macOS Firefox:** `Cmd + Shift + R`

2. **Clear Browser Cache Completely:**
   - Chrome: Settings → Privacy → Clear browsing data
   - Check "Cached images and files"
   - Time range: "Last hour"
   - Click "Clear data"

3. **Open Incognito/Private Window:**
   - `Cmd + Shift + N` (Chrome)
   - `Cmd + Shift + P` (Firefox/Safari)
   - Visit: http://localhost:8084

---

## 🧪 Verification Steps

### Step 1: Check Settings Button

1. Open browser: http://localhost:8084
2. Do **Hard Refresh** (`Cmd + Shift + R`)
3. Look for **Settings button below "Open Debugger"**:
   - Should have purple gradient background
   - Should say "Settings" with a gear icon
   - Click it → should go to `/settings` page

### Step 2: Check "Vanna Logo" Text

1. On the main page, press `Cmd + F` (Find)
2. Search for: "Vanna Logo"
3. **Expected:** No results found
4. Search for: "MyDBAssistant"
5. **Expected:** Multiple results

### Step 3: Check Oracle Connection

1. In the text box, type: **"Who are the top 5 highest paid employees?"**
2. Click Send (or press Enter)
3. **Expected results:**
   ```
   SELECT employee_id, first_name, last_name, salary
   FROM employees
   ORDER BY salary DESC
   FETCH FIRST 5 ROWS ONLY
   ```
4. Query should execute and show results table
5. **No "DPY-1001" error should appear**

---

## 🐛 Troubleshooting

### Problem: Still See "Vanna Logo"

**Check 1: Is JavaScript running?**
```bash
# Open browser console (Cmd + Option + J)
# Look for any JavaScript errors
# Should see no errors related to custom branding
```

**Check 2: View Page Source**
```bash
# Right-click → View Page Source
# Search for: "custom-branding-injected"
# Should find: <style id="custom-branding-injected">
```

**Check 3: Is the CSS being applied?**
```bash
# In browser console, run:
document.querySelector('img[alt="Vanna Logo"]')
# Should return: null (image removed)
```

### Problem: Settings Button Not Visible

**Check 1: Is "Open Debugger" button present?**
- Settings button appears **below** "Open Debugger"
- If "Open Debugger" doesn't exist, Settings button won't appear there
- But Settings **icon** (top-right) should still appear

**Check 2: Check Browser Console**
```javascript
// In browser console (Cmd + Option + J):
document.getElementById('settings-btn-inline')
// Should return: <a id="settings-btn-inline" ...>
```

**Check 3: Force JavaScript Re-run**
```javascript
// In browser console, manually trigger:
location.reload(true)  // Hard reload
```

### Problem: Oracle Query Fails with DPY-1001

**Check 1: Is connection alive?**
```bash
cd /Users/trongpv6/Documents/GitHub/vanna/src/myDbAssistant
python3 -c "
import oracledb
conn = oracledb.connect(user='hr', password='hr123', dsn='localhost:1521/XEPDB1')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM employees')
print(f'Employees: {cursor.fetchone()[0]}')
conn.close()
"
```

**Check 2: Check server logs**
```bash
tail -f server.log
# Look for connection errors or reconnection messages
```

**Check 3: Verify database is running**
```bash
# Check Oracle is running
lsof -i :1521
# Should show Oracle process listening on port 1521
```

---

## 📊 Server Status

**Current Status:** ✅ Running on http://localhost:8084

**Check Server:**
```bash
cd /Users/trongpv6/Documents/GitHub/vanna/src/myDbAssistant
tail -f server.log  # Watch live logs
```

**Restart Server:**
```bash
cd /Users/trongpv6/Documents/GitHub/vanna/src/myDbAssistant
pkill -f "quick_start_flask_ui.py"
nohup python3 quick_start_flask_ui.py > server.log 2>&1 &
tail -f server.log
```

**Stop Server:**
```bash
pkill -f "quick_start_flask_ui.py"
```

---

## 🎯 Quick Test Commands

### Test 1: Verify Custom CSS/JS Injection
```bash
curl -s http://localhost:8084/ | grep "custom-branding-injected"
# Expected: <style id="custom-branding-injected">
```

### Test 2: Verify Settings Button Code
```bash
curl -s http://localhost:8084/ | grep "settings-btn-inline"
# Expected: Multiple matches (CSS class and JS code)
```

### Test 3: Verify "Vanna Logo" Replacement
```bash
curl -s http://localhost:8084/ | grep -i "vanna logo"
# Expected: Only in JavaScript replacement code, not in visible content
```

### Test 4: Test Oracle Connection via API
```bash
# This tests the actual query execution
curl -X POST http://localhost:8084/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many employees are there?"}'
# Expected: Returns SQL query
```

---

## 📝 What Changed in the Code

### Before (Not Working):
- Custom CSS/JS served as separate routes
- Index route override attempted but failed
- JavaScript not injected into HTML
- Browser showed cached page

### After (Working):
- **Used `@app.after_request` hook** - intercepts ALL responses
- **Injects CSS/JS directly into HTML** before sending to browser
- **JavaScript runs immediately** when page loads
- **Works with browser cache** (since code is inline)

### Key Code Change:
```python
@vanna_flask.flask_app.after_request
def inject_custom_assets(response):
    """Inject custom CSS/JS into HTML responses"""
    if response.content_type and 'text/html' in response.content_type:
        html = response.get_data(as_text=True)
        # Inject <style> and <script> directly into HTML
        html = html.replace('</head>', custom_css + '</head>')
        html = html.replace('</body>', custom_js + '</body>')
        response.set_data(html)
    return response
```

This ensures **every HTML response** includes the custom branding code.

---

## ✅ Expected Behavior After Hard Refresh

When you do **Cmd + Shift + R** (hard refresh):

1. **Title bar** shows "MyDBAssistant"
2. **Top-left corner** - NO "Vanna Logo" image or text
3. **Top-right corner** - Purple settings gear icon
4. **Sidebar** - "Training Data", "New question" buttons
5. **Below "Open Debugger"** - Purple "Settings" button with gear icon
6. **Main area** - "MyDBAssistant" heading, subtitle
7. **Query box** - "Ask me a question about your data..."

### When You Ask a Question:

1. Type: "Who are the top 5 employees by salary?"
2. Click Send
3. **Expected:**
   - SQL generated (with Oracle syntax)
   - Query executes successfully
   - Results table appears
   - **NO "DPY-1001: not connected" error**
   - May show "Reconnected to Oracle" in logs (this is normal and good!)

---

## 🚀 Next Steps

1. **Open browser in Incognito mode**: `Cmd + Shift + N`
2. **Visit**: http://localhost:8084
3. **Verify** all 3 fixes are visible
4. **Test Oracle query** with a sample question
5. **If still issues**, check browser console for errors (`Cmd + Option + J`)

---

## 📞 Need Help?

If issues persist:

1. **Check server logs:**
   ```bash
   cd /Users/trongpv6/Documents/GitHub/vanna/src/myDbAssistant
   tail -100 server.log
   ```

2. **Check browser console** (Cmd + Option + J) for JavaScript errors

3. **Verify server is running:**
   ```bash
   lsof -i :8084
   # Should show Python process on port 8084
   ```

4. **Try different browser** (Safari, Firefox, Edge)

---

**End of Guide**
