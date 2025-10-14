# Implementation Plan: Convert Flask UI to Next.js Application

**Branch**: `001-convert-quick-start` | **Date**: October 13, 2025 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-convert-quick-start/spec.md`

**Note**: This plan defines the technical approach for building a Next.js frontend that communicates with the existing Flask backend.

## Summary

Create a modern Next.js web application in `ui-nextjs/` folder that replicates all functionality from the Flask UI (`quick_start_flask_ui.py`). The Next.js app will act as an API client, communicating with the Flask backend via REST endpoints for question-answering, settings management, and training data operations. Key features include natural language database queries with SQL generation, interactive Plotly charts, comprehensive settings UI with connection testing, and manual dark mode toggle. The implementation maintains backward compatibility with existing Flask UI and JSON configuration system.

## Technical Context

**Language/Version**: TypeScript 5.0+ with Node.js 18+  
**Primary Dependencies**: Next.js 14 (App Router), React 18, TailwindCSS 3, Plotly.js, React Query (TanStack Query), Axios, Zod  
**Storage**: JSON configuration files (ui/config/*.json) accessed via Flask API  
**Testing**: Jest for unit tests, React Testing Library for component tests, Playwright for E2E tests  
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)  
**Project Type**: Web application (Next.js frontend + Flask backend)  
**Performance Goals**: <2s initial page load, <5s query response (95th percentile), <1s chart rendering  
**Constraints**: Flask backend must be running, no direct database access from frontend, CORS configuration required  
**Scale/Scope**: Single-tenant deployment, 50+ concurrent users, responsive design for 375px+ viewports

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Vanna Constitution Compliance

**✅ PASS - Multiple Inheritance Architecture**: N/A - This is a frontend implementation that consumes Flask API. Does not modify Vanna core architecture.

**✅ PASS - Method Naming Conventions**: N/A - Frontend does not add new methods to VannaBase.

**✅ PASS - Configuration Pattern**: The Next.js app will respect existing JSON configuration system (ui/config/*.json) accessed via Flask API endpoints.

**✅ PASS - Deterministic UUIDs**: N/A - Training data management remains in Flask backend.

**✅ PASS - Optional Dependencies**: All Next.js dependencies are isolated to ui-nextjs/ folder and do not affect Vanna core.

**✅ PASS - Testing Requirements**: Will include Jest unit tests, React Testing Library component tests, and Playwright E2E tests.

**✅ PASS - Code Quality**: Will use ESLint, Prettier, and TypeScript strict mode for code quality.

**✅ PASS - Security Standards**: No credentials in frontend code, all authentication handled by Flask backend, HTTPS-only in production.

**✅ PASS - Development Workflow**: Following spec-driven approach with proper Git workflow.

**No Violations** - All constitution principles respected or not applicable to frontend implementation.

## Project Structure

### Documentation (this feature)

```
specs/001-convert-quick-start/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 - technology decisions and best practices
├── data-model.md        # Phase 1 - TypeScript interfaces and API contracts
├── quickstart.md        # Phase 1 - setup and development guide
├── contracts/           # Phase 1 - API endpoint specifications
│   ├── flask-api.yaml   # OpenAPI spec for Flask backend endpoints
│   └── types.ts         # TypeScript type definitions
└── checklists/
    └── requirements.md  # Quality validation checklist (completed)
```

### Source Code (repository root)

```
ui-nextjs/                      # NEW - Next.js application
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout with dark mode provider
│   │   ├── page.tsx            # Home page - question asking interface
│   │   ├── settings/
│   │   │   └── page.tsx        # Settings page with tabbed configuration
│   │   └── api/                # Next.js API routes (if needed for proxying)
│   ├── components/             # React components
│   │   ├── ui/                 # Reusable UI components (buttons, inputs, tabs)
│   │   ├── QuestionInput.tsx   # Natural language question input
│   │   ├── ResultsDisplay.tsx  # SQL results table display
│   │   ├── ChartRenderer.tsx   # Plotly chart wrapper
│   │   ├── SQLHighlight.tsx    # Syntax-highlighted SQL display
│   │   ├── SettingsTabs.tsx    # Settings page navigation
│   │   ├── LLMSettings.tsx     # LLM configuration form
│   │   ├── DatabaseSettings.tsx # Database configuration form
│   │   ├── TrainingSettings.tsx # Training data management
│   │   └── DarkModeToggle.tsx  # Theme switcher
│   ├── lib/                    # Utilities and services
│   │   ├── api-client.ts       # Axios-based Flask API client
│   │   ├── types.ts            # TypeScript interfaces
│   │   ├── validation.ts       # Zod schemas
│   │   └── utils.ts            # Helper functions
│   ├── hooks/                  # Custom React hooks
│   │   ├── useQuery.ts         # React Query hooks for API calls
│   │   ├── useConfig.ts        # Configuration management
│   │   └── useDarkMode.ts      # Dark mode state management
│   └── styles/
│       └── globals.css         # Global styles with Tailwind
├── public/                     # Static assets
│   ├── favicon.ico
│   └── logo.png
├── tests/                      # Test files
│   ├── unit/                   # Jest unit tests
│   ├── integration/            # React Testing Library tests
│   └── e2e/                    # Playwright E2E tests
├── .env.local.example          # Environment variables template
├── .eslintrc.json              # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── jest.config.js              # Jest configuration
├── next.config.js              # Next.js configuration
├── package.json                # Dependencies
├── playwright.config.ts        # Playwright configuration
├── postcss.config.js           # PostCSS for Tailwind
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
└── README.md                   # Setup and usage guide

src/myDbAssistant/              # EXISTING - Flask backend (unchanged)
├── quick_start_flask_ui.py     # Flask server with Copilot Socket Core
├── config_ui.py                # Settings API endpoints
└── ui/                         # JSON configuration system
    └── config/                 # Configuration files
        ├── llm.json
        ├── database.json
        ├── chromadb.json
        ├── flask.json
        └── training.json
```

**Structure Decision**: Web application pattern with separate frontend and backend. Next.js frontend in `ui-nextjs/` folder at repository root, Flask backend remains in `src/myDbAssistant/`. This separation allows independent development and deployment while maintaining clear API boundaries.

## Complexity Tracking

*No violations to track - all constitution principles respected.*

**Complexity Assessment**: LOW
- Frontend-only implementation
- Clear API boundaries with Flask backend
- Standard Next.js patterns and best practices
- No architectural changes to Vanna core

---

## Phase Completion Status

### ✅ Phase 0: Research & Outline (COMPLETE)

**Artifacts Created**:
- [research.md](./research.md) - All technology decisions documented
  - Next.js 14 App Router architecture
  - React Query for state management
  - Shadcn/ui component library
  - Axios API client with TypeScript
  - Zod for validation
  - Plotly.js for charts (required by backend)
  - Prism.js for syntax highlighting
  - next-themes for dark mode
  - Three-tier testing strategy (Jest + RTL + Playwright)

**Key Decisions**:
- ✅ App Router over Pages Router (future-proof)
- ✅ React Query over Redux (server state focus)
- ✅ Shadcn/ui over MUI (customization control)
- ✅ Axios over fetch (better features)
- ✅ Zod + React Hook Form (TypeScript-first)
- ✅ Plotly.js (backend compatibility requirement)
- ✅ Development proxy to avoid CORS issues

### ✅ Phase 1: Design & Contracts (COMPLETE)

**Artifacts Created**:
- [data-model.md](./data-model.md) - Complete TypeScript interfaces
  - Question & QueryResult entities
  - All configuration types (LLM, Database, ChromaDB, Flask, Training)
  - Training data entities
  - UI state management types
  - API request/response types
  - Zod validation schemas
  - Data transformation utilities
  - React Query keys factory

- [contracts/flask-api.yaml](./contracts/flask-api.yaml) - OpenAPI 3.0 specification
  - 11 endpoints documented
  - Request/response schemas
  - Error handling patterns
  - Authentication requirements
  - Example requests/responses

- [quickstart.md](./quickstart.md) - Comprehensive setup guide
  - Prerequisites and installation
  - Development workflow
  - Available scripts
  - Configuration guide
  - Usage instructions
  - Troubleshooting
  - Production deployment options
  - Performance optimization tips

**Agent Context Updated**:
- ✅ Updated `.github/copilot-instructions.md` with Next.js tech stack
- Added TypeScript, Next.js 14, React 18, TailwindCSS, Plotly.js, React Query, Axios, Zod

### 📋 Phase 2: Tasks (PENDING)

**Next Command**: `/speckit.tasks`

This will generate:
- `tasks.md` - Actionable task breakdown for implementation
- Priority-ordered tasks based on user stories
- Acceptance criteria for each task
- Dependencies between tasks

---

## Implementation Readiness

### Prerequisites Checklist

**Development Environment**:
- [x] Node.js 18+ available
- [x] Flask backend running on port 8084
- [x] Copilot Socket Core extension active
- [x] Database accessible from Flask
- [x] Git branch created (`001-convert-quick-start`)

**Planning Artifacts**:
- [x] Feature specification complete
- [x] Technology decisions made
- [x] Data model designed
- [x] API contracts defined
- [x] Quick start guide written
- [x] Constitution compliance verified

**Ready for Tasks Phase**: ✅ YES

---

## Risk Mitigation Summary

| Risk | Severity | Mitigation Strategy | Status |
|------|----------|---------------------|--------|
| Flask backend dependency | High | Health checks, clear error messages, retry logic | Planned |
| CORS configuration | Medium | Development proxy, Flask CORS config | Documented |
| Large result sets | Medium | Pagination, virtual scrolling | Designed |
| Chart performance | Medium | Dynamic import, code splitting | Planned |
| Type safety | Low | Zod validation, strict TypeScript | Implemented |

---

## Next Steps

1. **Run `/speckit.tasks`** to generate implementation tasks
2. **Review tasks.md** for completeness and ordering
3. **Run `/speckit.implement`** to begin implementation
4. **Follow quickstart.md** for setup instructions

---

## References

- Feature Spec: [spec.md](./spec.md)
- Research Document: [research.md](./research.md)
- Data Model: [data-model.md](./data-model.md)
- API Contracts: [contracts/flask-api.yaml](./contracts/flask-api.yaml)
- Quick Start: [quickstart.md](./quickstart.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)

---

**Plan Status**: ✅ COMPLETE - Ready for `/speckit.tasks`  
**Last Updated**: October 13, 2025
