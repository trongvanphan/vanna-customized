# Phase 0: Research & Technology Decisions

**Feature**: Convert Flask UI to Next.js Application  
**Date**: October 13, 2025

## Overview

This document captures research findings and technology decisions for building a Next.js frontend that consumes the existing Flask backend API.

## Key Technology Decisions

### 1. Next.js Architecture: App Router vs Pages Router

**Decision**: Use **Next.js 14 App Router**

**Rationale**:
- Modern React Server Components support for better performance
- Improved routing with file-system based routing in `app/` directory
- Better TypeScript integration and type safety
- Native support for layouts and nested routing
- Streaming and Suspense built-in
- Future-proof choice (Pages Router in maintenance mode)

**Alternatives Considered**:
- **Pages Router**: More mature ecosystem but deprecated in favor of App Router
- **Remix**: Similar features but smaller ecosystem, less documentation

**Implementation Notes**:
- Use client components (`'use client'`) for interactive UI
- Server components for static layouts and data fetching where possible
- API routes in `app/api/` if we need to proxy Flask requests

---

### 2. State Management: React Query vs Redux vs Zustand

**Decision**: Use **React Query (TanStack Query v5)**

**Rationale**:
- Purpose-built for server state management (API calls)
- Automatic caching, refetching, and background updates
- Built-in loading and error states
- Optimistic updates for better UX
- Reduces boilerplate compared to Redux
- Perfect fit for API-driven application

**Alternatives Considered**:
- **Redux Toolkit**: Overcomplicated for this use case, adds unnecessary complexity
- **Zustand**: Good for client state but React Query handles server state better
- **Context API**: Too basic, would require building caching layer

**Implementation Notes**:
```typescript
// Example usage
const { data, isLoading, error } = useQuery({
  queryKey: ['ask-question', question],
  queryFn: () => apiClient.askQuestion(question)
});
```

---

### 3. UI Component Library: Shadcn/ui vs MUI vs Custom

**Decision**: Use **Shadcn/ui with Radix UI primitives**

**Rationale**:
- Copy-paste components (no npm dependency bloat)
- Built on Radix UI (accessible, unstyled primitives)
- Full control over styling and customization
- Excellent TypeScript support
- Works perfectly with TailwindCSS
- Modern, clean design system

**Alternatives Considered**:
- **Material-UI (MUI)**: Heavy bundle size, opinionated styling harder to customize
- **Ant Design**: Great for admin panels but less modern aesthetic
- **Custom components**: Would take longer, reinventing the wheel

**Implementation Notes**:
- Initialize with `npx shadcn-ui@latest init`
- Add components as needed: Button, Input, Tabs, Dialog, Toast
- Customize theme via `tailwind.config.ts`

---

### 4. API Client: Axios vs Fetch vs tRPC

**Decision**: Use **Axios with TypeScript**

**Rationale**:
- Automatic request/response transformations
- Interceptors for auth and error handling
- Better error handling than fetch
- Request cancellation built-in
- Widely used, well-documented

**Alternatives Considered**:
- **Native Fetch**: Requires polyfills for older browsers, less features
- **tRPC**: Overkill for REST API, would require backend changes
- **SWR**: Good but React Query is more feature-complete

**Implementation Notes**:
```typescript
// lib/api-client.ts
const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_FLASK_URL || 'http://localhost:8084',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
});
```

---

### 5. Form Validation: Zod vs Yup vs React Hook Form

**Decision**: Use **Zod with React Hook Form**

**Rationale**:
- TypeScript-first schema validation
- Infer TypeScript types from schemas
- Better error messages
- Smaller bundle size than Yup
- Integrates perfectly with React Hook Form

**Alternatives Considered**:
- **Yup**: Older, not TypeScript-native
- **Joi**: Server-side focused, larger bundle

**Implementation Notes**:
```typescript
import { z } from 'zod';

const databaseConfigSchema = z.object({
  type: z.enum(['oracle', 'postgres', 'mysql', 'mssql']),
  host: z.string().min(1),
  port: z.number().int().positive(),
  database: z.string().min(1),
  user: z.string().min(1),
  password: z.string().min(1)
});
```

---

### 6. Chart Rendering: Plotly.js vs Recharts vs Chart.js

**Decision**: Use **Plotly.js** (react-plotly.js wrapper)

**Rationale**:
- **REQUIRED** - Flask backend generates Plotly figure JSON
- Maintains consistency with existing Flask UI
- Interactive charts out of the box
- Supports complex visualizations
- Direct compatibility with backend response format

**Alternatives Considered**:
- None - backend already generates Plotly format, changing would require backend modifications

**Implementation Notes**:
```typescript
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

<Plot data={figureData.data} layout={figureData.layout} />
```

---

### 7. Syntax Highlighting: Prism vs Highlight.js vs Monaco

**Decision**: Use **Prism.js with react-syntax-highlighter**

**Rationale**:
- Lightweight (~2KB gzipped with SQL theme)
- Easy React integration
- Excellent SQL syntax support
- Customizable themes
- No heavy editor features needed

**Alternatives Considered**:
- **Monaco Editor**: Overkill (full VSCode editor), 1.7MB bundle
- **Highlight.js**: Good but Prism has better React integration
- **CodeMirror**: Too complex for read-only display

**Implementation Notes**:
```typescript
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';

<SyntaxHighlighter language="sql" style={tomorrow}>
  {sqlQuery}
</SyntaxHighlighter>
```

---

### 8. Dark Mode Implementation: next-themes vs Manual

**Decision**: Use **next-themes**

**Rationale**:
- Handles SSR/hydration issues automatically
- Provides useTheme hook
- Integrates with TailwindCSS dark mode
- Zero-flash dark mode on page load
- localStorage persistence built-in

**Implementation Notes**:
```typescript
// app/layout.tsx
import { ThemeProvider } from 'next-themes';

<ThemeProvider attribute="class" defaultTheme="light">
  {children}
</ThemeProvider>

// components/DarkModeToggle.tsx
const { theme, setTheme } = useTheme();
```

---

### 9. Testing Strategy: Jest + RTL + Playwright

**Decision**: Use **three-tier testing approach**

**Rationale**:
- **Jest**: Unit tests for utilities, hooks, pure logic
- **React Testing Library**: Component integration tests
- **Playwright**: E2E tests for critical user journeys

**Coverage Goals**:
- Unit tests: 80% coverage for lib/, hooks/
- Component tests: All interactive components
- E2E tests: P1 user stories from spec

**Implementation Notes**:
```bash
# Unit test
npm run test:unit

# Component test
npm run test:component

# E2E test (requires Flask backend running)
npm run test:e2e
```

---

### 10. Development Environment Setup

**Decision**: Separate development servers with proxy configuration

**Rationale**:
- Next.js dev server on port 3000
- Flask backend on port 8084
- Next.js rewrites to proxy `/api/v0/*` to Flask
- Avoids CORS issues in development

**Implementation Notes**:
```javascript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/v0/:path*',
        destination: 'http://localhost:8084/api/v0/:path*'
      }
    ];
  }
};
```

---

### 11. Production Deployment Considerations

**Decision**: Deploy as separate services with reverse proxy

**Options**:
1. **Vercel (Next.js) + Separate Flask server**
   - Next.js on Vercel
   - Flask on cloud VM or container
   - Environment variable for Flask API URL

2. **Docker Compose (both services)**
   - Nginx reverse proxy
   - Next.js container
   - Flask container
   - Shared network

3. **Single server with Nginx**
   - Nginx serves Next.js static export
   - Proxy `/api/v0/*` to Flask

**Recommendation**: Option 2 (Docker Compose) for simplicity and portability

---

## Best Practices Research

### Next.js 14 App Router Best Practices

1. **Server vs Client Components**:
   - Use Server Components by default
   - Add `'use client'` only when needed (interactivity, hooks, browser APIs)
   - Keep client components small and focused

2. **Data Fetching**:
   - Use React Query for client-side data fetching
   - Avoid fetching in Server Components for this use case (all data from Flask)

3. **Performance**:
   - Use `next/image` for optimized images
   - Dynamic imports for heavy libraries (Plotly)
   - Code splitting by route automatically

4. **Error Handling**:
   - Use error.tsx for route-level error boundaries
   - loading.tsx for Suspense boundaries
   - Global error handling in root layout

### TypeScript Best Practices

1. **Strict Mode**: Enable `strict: true` in tsconfig.json
2. **Type Safety**:
   - Define interfaces for all API responses
   - Use Zod for runtime validation + type inference
   - No `any` types

3. **Organization**:
   - Colocate types with usage
   - Shared types in `lib/types.ts`
   - Generate types from API contracts

### API Integration Patterns

1. **Error Handling**:
   ```typescript
   try {
     const response = await apiClient.post('/api/v0/ask', { question });
     return response.data;
   } catch (error) {
     if (axios.isAxiosError(error)) {
       // Handle API errors
       throw new Error(error.response?.data?.error || 'Request failed');
     }
     throw error;
   }
   ```

2. **Loading States**:
   - Use React Query's `isLoading`, `isFetching` states
   - Show skeleton loaders for better UX
   - Disable buttons during mutations

3. **Optimistic Updates**:
   - Update UI immediately for settings changes
   - Revert on error
   - Use React Query's `useMutation` with optimistic updates

### Accessibility Patterns

1. **Keyboard Navigation**:
   - All interactive elements tabbable
   - Logical tab order
   - Escape key to close modals

2. **Screen Readers**:
   - ARIA labels for icon buttons
   - Live regions for dynamic updates
   - Semantic HTML (button, nav, main, aside)

3. **Focus Management**:
   - Focus trap in modals
   - Focus return after modal close
   - Visible focus indicators

---

## Integration Points with Flask Backend

### Required Flask API Endpoints

Based on `config_ui.py` and `quick_start_flask_ui.py`:

1. **Question Asking**:
   - `POST /api/v0/ask` - Ask natural language question
   - `GET /api/v0/generate_plotly_figure` - Get chart for result

2. **Configuration Management**:
   - `GET /api/v0/get_config` - Get all configurations
   - `POST /api/v0/update_llm_config` - Update LLM settings
   - `POST /api/v0/update_database_config` - Update database settings
   - `POST /api/v0/update_chromadb_config` - Update ChromaDB settings
   - `POST /api/v0/update_flask_config` - Update Flask settings
   - `POST /api/v0/update_training_config` - Update training settings

3. **Connection Testing**:
   - `POST /api/v0/test_database_connection` - Test database connectivity
   - `POST /api/v0/test_llm_connection` - Test LLM endpoint health

4. **Training Data**:
   - `POST /api/v0/load_training_data` - Load training data from files
   - `GET /api/v0/get_training_data` - Get training data statistics (if available)

### Authentication/Authorization

**Current State**: No authentication in Flask backend

**Implementation**: 
- Not implemented in this phase (out of scope per spec)
- Future: Add JWT or session-based auth
- For now: Assume trusted local/internal network

---

## Risk Assessment

### Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Flask backend not running | High | Clear error messages, health check endpoint, connection retry logic |
| CORS issues | Medium | Proper CORS configuration in Flask, development proxy in Next.js |
| Large result sets crashing UI | Medium | Pagination, virtualized tables, streaming responses |
| Chart rendering performance | Medium | Dynamic import of Plotly, Web Workers for large datasets |
| TypeScript complexity | Low | Good documentation, examples, leverage Zod for validation |

### Dependency Risks

| Dependency | Risk | Mitigation |
|------------|------|------------|
| Next.js 14 | Low | Stable release, large community, good documentation |
| React Query | Low | Battle-tested, v5 is stable |
| Plotly.js | Medium | Large bundle size (~3MB), use dynamic import |
| Shadcn/ui | Low | Copy-paste model, no version lock-in |

---

## Performance Optimization Strategy

1. **Bundle Size**:
   - Dynamic import for Plotly.js (~3MB)
   - Tree-shaking with ES modules
   - Code splitting by route (automatic)
   - Target: <500KB initial bundle

2. **Rendering**:
   - Virtual scrolling for large tables
   - Debounce user input
   - Memoize expensive computations
   - Target: 60fps interactions

3. **Network**:
   - Request deduplication via React Query
   - Stale-while-revalidate caching
   - Abort in-flight requests on navigation
   - Target: <5s end-to-end query time

---

## Open Questions for Phase 1

1. ✅ **RESOLVED**: Should we use Server Actions or client-side API calls?
   - **Answer**: Client-side API calls with React Query (better for API-driven app)

2. ✅ **RESOLVED**: How to handle query history persistence?
   - **Answer**: Not in scope for MVP (P3 user story), implement in future iteration

3. ✅ **RESOLVED**: Should we implement real-time updates?
   - **Answer**: No, Flask doesn't support WebSocket. Use polling if needed.

4. ✅ **RESOLVED**: How to handle Flask backend restarts?
   - **Answer**: Detect connection loss, show reconnection UI, auto-retry

---

## Phase 0 Completion Checklist

- [x] Next.js architecture decision documented
- [x] State management approach defined
- [x] UI component library selected
- [x] API client strategy determined
- [x] Form validation approach chosen
- [x] Chart rendering library confirmed
- [x] Syntax highlighting solution selected
- [x] Dark mode implementation planned
- [x] Testing strategy defined
- [x] Development environment approach documented
- [x] Flask API integration points identified
- [x] Risk assessment completed
- [x] Performance optimization strategy outlined
- [x] All open questions resolved

**Status**: ✅ Phase 0 Complete - Ready for Phase 1 (Design & Contracts)
