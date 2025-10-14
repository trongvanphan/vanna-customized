# Testing Guide - Vanna Next.js UI

## Quick Start

### 1. Start Flask Backend
```bash
# Terminal 1: Start Flask backend
cd src/myDbAssistant
python3 quick_start_flask_ui.py

# Expected output:
# ✅ Training data already exists
# 📊 Flask UI Settings:
#    - Host: 0.0.0.0
#    - Port: 8084
#    - Debug: True
# 🌐 Flask app running on: http://0.0.0.0:8084
```

### 2. Start Next.js Dev Server
```bash
# Terminal 2: Start Next.js development server
cd ui-nextjs
npm run dev

# Expected output:
# ▲ Next.js 14.2.33
# - Local:        http://localhost:3000
# ✓ Ready in ~1.5s
```

### 3. Open Browser
Navigate to: **http://localhost:3000**

---

## Test Scenarios

### Test 1: Basic Question Submission
**Goal:** Verify end-to-end question-answering workflow

1. **Open the app** at http://localhost:3000
2. **Enter a test question** in the input field:
   ```
   What are the top 10 customers by sales?
   ```
3. **Submit** using either:
   - Click "Ask Question" button
   - Press `Cmd+Enter` (macOS) or `Ctrl+Enter` (Windows)
4. **Verify expected behavior:**
   - ✅ Loading spinner appears on button
   - ✅ Input field is disabled during submission
   - ✅ Toast notification appears: "Query executed successfully"
   - ✅ QuestionAnswerCard appears with:
     - Question text
     - Timestamp (e.g., "2 seconds ago")
     - Execution time badge
     - Status badge (success/error)
   - ✅ SQL section shows generated query with syntax highlighting
   - ✅ Results section shows data table
   - ✅ Chart section renders Plotly visualization (if applicable)

**Expected SQL output example:**
```sql
SELECT customer_name, SUM(sales) as total_sales
FROM customers
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10
```

---

### Test 2: SQL Syntax Highlighting
**Goal:** Verify Prism.js SQL highlighting works

1. **Submit a question** (use Test 1)
2. **Inspect the SQL display:**
   - ✅ Keywords highlighted (SELECT, FROM, WHERE, etc.)
   - ✅ Line numbers visible
   - ✅ Copy button present
3. **Click Copy button:**
   - ✅ Button shows checkmark icon
   - ✅ SQL copied to clipboard
   - ✅ Paste in text editor to verify
4. **Test in dark mode:**
   - ✅ Click dark mode toggle in header
   - ✅ SQL highlighting adapts to dark theme

---

### Test 3: Results Table Display
**Goal:** Verify data table rendering and pagination

1. **Submit a question** that returns multiple rows:
   ```
   Show me all customers with their total orders
   ```
2. **Verify table display:**
   - ✅ Column headers match data
   - ✅ Rows display correctly
   - ✅ Numbers formatted with commas (e.g., "1,234.56")
   - ✅ Booleans show as "true" or "false"
   - ✅ Null values show as "-"
3. **Test pagination** (if >50 rows):
   - ✅ "Previous" button disabled on first page
   - ✅ "Next" button enabled
   - ✅ Click "Next" to see next 50 rows
   - ✅ Page indicator shows "51 to 100 of X rows"
   - ✅ "Previous" button now enabled
4. **Test responsive overflow:**
   - ✅ Narrow browser window
   - ✅ Table scrolls horizontally
   - ✅ No layout breaking

---

### Test 4: Chart Visualization
**Goal:** Verify Plotly chart rendering

1. **Submit a question** that generates a chart:
   ```
   Show me the revenue trend for the last 12 months
   ```
2. **Verify chart display:**
   - ✅ Chart renders below results table
   - ✅ Interactive hover tooltips work
   - ✅ Chart is responsive (fits container)
   - ✅ Chart type appropriate for data (bar, line, scatter, etc.)
3. **Test dark mode:**
   - ✅ Toggle dark mode
   - ✅ Chart background transparent
   - ✅ Chart text color adapts to theme
   - ✅ Grid lines visible in both themes
4. **Test chart interactions:**
   - ✅ Hover over data points
   - ✅ Zoom in/out with Plotly controls
   - ✅ Pan across chart
   - ✅ Reset axes button works

---

### Test 5: Error Handling
**Goal:** Verify error states and notifications

**Test 5a: Invalid Question**
1. **Submit an unclear question:**
   ```
   asdfasdfasdf
   ```
2. **Verify error handling:**
   - ✅ Toast notification: "Failed to execute query"
   - ✅ QuestionAnswerCard shows error state
   - ✅ Error message displayed with AlertCircle icon
   - ✅ No SQL or results sections shown

**Test 5b: Backend Unreachable**
1. **Stop Flask backend** (Ctrl+C in Terminal 1)
2. **Submit a question**
3. **Verify error handling:**
   - ✅ Toast notification: "Network error: connect ECONNREFUSED"
   - ✅ Error card displayed

**Test 5c: Database Disconnected**
1. **Restart Flask backend** without database connection
2. **Submit a question**
3. **Verify error handling:**
   - ✅ Toast notification with database error message
   - ✅ Error card with helpful error text

---

### Test 6: Dark Mode
**Goal:** Verify theme switching

1. **Click dark mode toggle** in header (moon icon)
2. **Verify dark mode:**
   - ✅ Background changes to dark
   - ✅ Text color inverts
   - ✅ Cards have dark backgrounds
   - ✅ SQL highlighting uses dark theme
   - ✅ Charts adapt to dark theme
   - ✅ Buttons and inputs styled correctly
3. **Refresh page:**
   - ✅ Dark mode persists (localStorage)
4. **Toggle back to light mode:**
   - ✅ All elements return to light theme
   - ✅ Icon changes to sun

---

### Test 7: Multiple Questions
**Goal:** Verify question history management

1. **Submit first question:**
   ```
   What are the top 10 customers?
   ```
2. **Submit second question:**
   ```
   Show me total revenue by month
   ```
3. **Submit third question:**
   ```
   Which products have the highest margin?
   ```
4. **Verify history display:**
   - ✅ All 3 QuestionAnswerCards visible
   - ✅ Newest question at top
   - ✅ Each has unique timestamp
   - ✅ All results preserved
5. **Click "Clear All":**
   - ✅ All questions removed
   - ✅ Empty state shown with example questions

---

### Test 8: Keyboard Shortcuts
**Goal:** Verify keyboard interactions

1. **Focus on question input** (click textarea)
2. **Type a question**
3. **Press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows):**
   - ✅ Question submits
   - ✅ Same behavior as clicking button
4. **Type another question** while first is loading:
   - ✅ Input disabled during loading
   - ✅ Keyboard shortcut disabled

---

### Test 9: Session Management
**Goal:** Verify session ID generation

1. **Open browser DevTools** (F12)
2. **Go to Network tab**
3. **Submit a question**
4. **Inspect the API request** to `/api/v0/ask`:
   - ✅ Request includes `session_id` field
   - ✅ Session ID format: `vanna_session_<timestamp>`
5. **Submit another question:**
   - ✅ Same session ID used
6. **Refresh page:**
   - ✅ New session ID generated

---

### Test 10: Responsive Design
**Goal:** Verify mobile and tablet layouts

1. **Resize browser** to mobile width (375px)
2. **Verify mobile layout:**
   - ✅ Header stacks vertically (if needed)
   - ✅ Question input full width
   - ✅ Cards stack properly
   - ✅ Table scrolls horizontally
   - ✅ Charts resize to fit
   - ✅ Buttons touch-friendly (44px minimum)
3. **Test tablet width** (768px):
   - ✅ Layout adapts smoothly
   - ✅ No horizontal scroll (except tables)
4. **Test desktop width** (1280px+):
   - ✅ Content centered with max-width
   - ✅ Charts use available space

---

## Performance Tests

### Test 11: Large Result Sets
**Goal:** Verify performance with large data

1. **Submit a question** returning 1000+ rows:
   ```
   Show me all transactions from last year
   ```
2. **Verify performance:**
   - ✅ Table renders quickly (<1s)
   - ✅ Pagination works smoothly
   - ✅ No browser freezing
   - ✅ Scrolling is smooth
3. **Test pagination:**
   - ✅ Navigate through pages
   - ✅ Each page loads instantly (client-side pagination)

### Test 12: Complex Charts
**Goal:** Verify chart rendering performance

1. **Submit a question** with complex visualization:
   ```
   Show me sales by product category and region for the last 12 months
   ```
2. **Verify chart performance:**
   - ✅ Chart loads within 2 seconds
   - ✅ Interactive hover is responsive
   - ✅ No lag when zooming/panning

---

## Browser Compatibility

### Test 13: Cross-Browser Testing
**Browsers to test:**
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (macOS/iOS)

**For each browser:**
1. Open http://localhost:3000
2. Submit a question
3. Verify all features work:
   - Question submission
   - SQL highlighting
   - Results table
   - Chart rendering
   - Dark mode toggle
   - Copy to clipboard

---

## Accessibility Tests

### Test 14: Keyboard Navigation
**Goal:** Verify keyboard-only navigation

1. **Tab through interface:**
   - ✅ Focus visible on all interactive elements
   - ✅ Tab order logical (top to bottom)
   - ✅ Skip to main content available
2. **Test form submission:**
   - ✅ Enter key submits question (when focused on button)
   - ✅ Cmd/Ctrl+Enter works from textarea
3. **Test buttons:**
   - ✅ Space/Enter activates buttons
   - ✅ Focus indicates interactive state

### Test 15: Screen Reader (Optional)
**Goal:** Verify screen reader compatibility

1. **Enable screen reader** (VoiceOver on Mac, NVDA on Windows)
2. **Navigate through page:**
   - ✅ Headings announced correctly
   - ✅ Form labels read aloud
   - ✅ Button purposes clear
   - ✅ Error messages announced
   - ✅ Toast notifications announced

---

## Troubleshooting

### Issue: "Network error: connect ECONNREFUSED"
**Cause:** Flask backend not running  
**Solution:**
```bash
cd src/myDbAssistant
python3 quick_start_flask_ui.py
```

### Issue: "Module not found" errors
**Cause:** Dependencies not installed  
**Solution:**
```bash
cd ui-nextjs
npm install
```

### Issue: Charts not rendering
**Cause:** Dynamic import issue or Plotly not loaded  
**Solution:**
1. Check browser console for errors
2. Verify `react-plotly.js` installed: `npm list react-plotly.js`
3. Try hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

### Issue: SQL highlighting not working
**Cause:** Prism.js not loaded  
**Solution:**
1. Check `globals.css` includes Prism themes
2. Verify `prismjs` installed: `npm list prismjs`
3. Clear `.next` cache: `rm -rf .next && npm run dev`

### Issue: Dark mode not persisting
**Cause:** localStorage blocked or cleared  
**Solution:**
1. Check browser allows localStorage
2. Check browser DevTools → Application → Local Storage
3. Verify `theme` key exists

### Issue: API proxy not working
**Cause:** `next.config.js` proxy misconfigured  
**Solution:**
1. Verify `rewrites` in `next.config.js` points to correct Flask URL
2. Check Flask is on port 8084
3. Restart Next.js dev server

---

## Test Checklist

### Core Functionality
- [ ] Question submission works
- [ ] SQL generation displays correctly
- [ ] Results table renders data
- [ ] Charts visualize data
- [ ] Error handling works
- [ ] Toast notifications appear
- [ ] Copy SQL to clipboard works

### User Interface
- [ ] Dark mode toggle works
- [ ] Theme persists on refresh
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Loading states show during async operations
- [ ] Empty state displays when no questions

### Performance
- [ ] Production build compiles
- [ ] Development server starts quickly
- [ ] Large result sets render smoothly
- [ ] Charts load without lag
- [ ] Pagination is instant

### Accessibility
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Keyboard shortcuts functional
- [ ] Screen reader compatible (optional)

### Browser Compatibility
- [ ] Chrome/Edge works
- [ ] Firefox works
- [ ] Safari works (macOS/iOS)

---

## Reporting Issues

If you encounter issues during testing:

1. **Check browser console** (F12 → Console tab)
2. **Check Network tab** (F12 → Network tab)
3. **Document steps to reproduce**
4. **Note environment:**
   - Browser and version
   - Operating system
   - Node.js version (`node --version`)
   - npm version (`npm --version`)
5. **Create GitHub issue** with details

---

## Next Testing Phase

After MVP validation, test:
- **Settings UI** (User Story 2)
- **Training Management** (User Story 3)
- **History Page** (User Story 4)
- **Production deployment**
- **E2E tests with Playwright**
- **Lighthouse performance audit**

---

*Last Updated: 2025-01-14*  
*Version: MVP 0.1.0*
