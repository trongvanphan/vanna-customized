# Quick Start Guide: Next.js UI for Vanna

## Overview

This guide will help you set up and run the Next.js frontend for Vanna's myDbAssistant. The Next.js app provides a modern web interface that communicates with the Flask backend for natural language database queries.

## Prerequisites

Before you begin, ensure you have:

- **Node.js 18+** installed ([Download](https://nodejs.org/))
- **npm** or **yarn** package manager
- **Flask backend running** on port 8084 (see Flask setup below)
- **Copilot Socket Core** extension active in VS Code
- **Database** (Oracle/PostgreSQL/MySQL/SQL Server) accessible

## Quick Start (Development)

### 1. Start Flask Backend

```bash
# Navigate to Flask backend
cd src/myDbAssistant

# Install Python dependencies (if not already done)
pip install -e '.[all]'

# Start Flask server
python3 quick_start_flask_ui.py
```

The Flask backend will start on `http://localhost:8084`.

### 2. Install Next.js Dependencies

```bash
# Navigate to Next.js app
cd ui-nextjs

# Install dependencies
npm install
# or
yarn install
```

### 3. Configure Environment

Create `.env.local` file in `ui-nextjs/` directory:

```bash
# Copy example environment file
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
# Flask Backend URL
NEXT_PUBLIC_FLASK_URL=http://localhost:8084

# Optional: Override default settings
NEXT_PUBLIC_APP_TITLE=MyDBAssistant
NEXT_PUBLIC_APP_SUBTITLE=Powered by Vanna AI
```

### 4. Start Development Server

```bash
# Start Next.js dev server
npm run dev
# or
yarn dev
```

The Next.js app will start on `http://localhost:3000`.

### 5. Open in Browser

Navigate to [http://localhost:3000](http://localhost:3000) to access the UI.

## Project Structure

```
ui-nextjs/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page (question asking)
│   │   └── settings/           # Settings page
│   ├── components/             # React components
│   │   ├── ui/                 # Base UI components (Button, Input, etc.)
│   │   ├── QuestionInput.tsx
│   │   ├── ResultsDisplay.tsx
│   │   ├── ChartRenderer.tsx
│   │   └── ...
│   ├── lib/                    # Utilities
│   │   ├── api-client.ts       # Flask API client
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Helper functions
│   └── hooks/                  # Custom React hooks
│       ├── useQuery.ts
│       └── useConfig.ts
├── public/                     # Static assets
├── tests/                      # Test files
├── .env.local                  # Environment variables (not in git)
├── next.config.js              # Next.js configuration
├── package.json                # Dependencies
└── tsconfig.json               # TypeScript configuration
```

## Available Scripts

### Development

```bash
# Start development server with hot reload
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Code formatting
npm run format
```

### Testing

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run component tests
npm run test:component

# Run E2E tests (requires Flask backend running)
npm run test:e2e

# Watch mode for development
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm run start

# Or build and start
npm run build && npm run start
```

## Configuration

### Flask Backend Configuration

The Next.js app reads configuration from Flask backend via `/api/v0/get_config` endpoint. To update settings:

1. Navigate to **Settings** page in UI
2. Update desired configuration (LLM, Database, ChromaDB, Flask, Training)
3. Click **Save** to persist changes to `ui/config/*.json` files

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_FLASK_URL` | Flask backend URL | `http://localhost:8084` |
| `NEXT_PUBLIC_APP_TITLE` | Application title | `MyDBAssistant` |
| `NEXT_PUBLIC_APP_SUBTITLE` | Application subtitle | `Powered by Vanna AI` |
| `NODE_ENV` | Environment mode | `development` |

## Usage Guide

### Asking Questions

1. Navigate to home page (`/`)
2. Type natural language question in input field
3. Click **Ask** or press Enter
4. View generated SQL, results table, and chart (if applicable)

**Example questions:**
- "What are the top 10 customers by sales?"
- "Show me sales by region for last quarter"
- "How many employees in each department?"

### Managing Settings

1. Click **Settings** icon in navigation
2. Select configuration tab (LLM, Database, ChromaDB, Flask, Training)
3. Update values in form
4. Click **Test Connection** to validate (Database and LLM tabs)
5. Click **Save** to persist changes

### Loading Training Data

1. Navigate to **Settings** → **Training** tab
2. View current training data statistics
3. Click **Load Training Data Now** button
4. Wait for load to complete (shows count of items loaded)

**Training data files location:**
- DDL: `trainingMyDb/ddl/*.sql`
- Documentation: `trainingMyDb/documentation/*.md`
- Q&A Pairs: `trainingMyDb/trainingpairs/*.json`

### Dark Mode

Toggle dark mode using the theme switcher in the navigation bar. Preference is saved to localStorage.

## Troubleshooting

### Flask Backend Not Running

**Error**: "Connection refused" or "Network error"

**Solution**:
1. Verify Flask backend is running: `curl http://localhost:8084/api/v0/get_config`
2. Check Flask logs for errors
3. Ensure Copilot Socket Core extension is active in VS Code

### CORS Issues

**Error**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**: Flask backend should have CORS enabled. Check `quick_start_flask_ui.py`:

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Chart Not Rendering

**Error**: Chart placeholder shows but no visualization

**Solution**:
1. Check browser console for Plotly.js errors
2. Verify query returns data (check table display)
3. Ensure `figure_id` is returned in query response
4. Try refreshing the page

### Type Errors

**Error**: TypeScript type errors during development

**Solution**:
1. Run type check: `npm run type-check`
2. Check `lib/types.ts` for correct type definitions
3. Ensure API responses match expected schema (use Zod validation)

### Build Errors

**Error**: Build fails with dependency errors

**Solution**:
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

## Development Tips

### API Testing

Use the Flask API directly for debugging:

```bash
# Test question endpoint
curl -X POST http://localhost:8084/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 10 customers?"}'

# Test configuration endpoint
curl http://localhost:8084/api/v0/get_config
```

### Component Development

Use Storybook (if configured) or create isolated test pages:

```typescript
// app/test/page.tsx
import QuestionInput from '@/components/QuestionInput';

export default function TestPage() {
  return <QuestionInput onSubmit={(q) => console.log(q)} />;
}
```

### Debugging React Query

Enable React Query DevTools in development:

```typescript
// app/layout.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

<ReactQueryDevtools initialIsOpen={false} />
```

### Hot Reload Issues

If hot reload stops working:

```bash
# Restart Next.js dev server
npm run dev

# Or clear .next directory
rm -rf .next && npm run dev
```

## Production Deployment

### Option 1: Vercel (Recommended for Next.js)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# NEXT_PUBLIC_FLASK_URL=https://your-flask-server.com
```

### Option 2: Docker

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Build and run
docker build -t vanna-nextjs .
docker run -p 3000:3000 -e NEXT_PUBLIC_FLASK_URL=http://flask:8084 vanna-nextjs
```

### Option 3: Static Export (if no API routes)

```bash
# Build static site
npm run build && npm run export

# Serve static files with any web server
# Files in out/ directory
```

## Performance Optimization

### Bundle Size

Check bundle size:

```bash
npm run build
# Look for "First Load JS" in output
```

Target: <500KB initial bundle

### Lighthouse Audit

```bash
npm install -g lighthouse

# Run audit
lighthouse http://localhost:3000 --view
```

Target scores:
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+

### Monitoring

Add analytics and error tracking:

```typescript
// lib/analytics.ts
export function trackEvent(name: string, properties?: object) {
  // Send to analytics service (e.g., Vercel Analytics, Plausible)
}

export function trackError(error: Error, context?: object) {
  // Send to error tracking service (e.g., Sentry)
}
```

## Security Checklist

- [ ] Environment variables not committed to git
- [ ] HTTPS in production
- [ ] CORS properly configured
- [ ] Input sanitization for user questions
- [ ] No sensitive data in client-side code
- [ ] Dependencies regularly updated
- [ ] Security headers configured

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Plotly.js Documentation](https://plotly.com/javascript/)
- [Vanna Documentation](https://vanna.ai/docs)

## Getting Help

- Check [Vanna GitHub Issues](https://github.com/vanna-ai/vanna/issues)
- Review Flask backend logs in `src/myDbAssistant/`
- Enable verbose logging: `DEBUG=true npm run dev`
- Check browser console for errors

---

**Happy Coding!** 🚀
