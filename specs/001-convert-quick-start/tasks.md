# Tasks: Convert Flask UI to Next.js Application

**Input**: Design documents from `/specs/001-convert-quick-start/`  
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅)

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are excluded. Focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Next.js project structure in `ui-nextjs/` with TypeScript, App Router, Tailwind CSS
- [ ] T002 Initialize package.json with dependencies: next@14, react@18, typescript@5, tailwindcss@3, axios, @tanstack/react-query, zod, react-hook-form, plotly.js, react-plotly.js, prismjs, next-themes
- [ ] T003 [P] Create Next.js configuration in `ui-nextjs/next.config.js` (configure API proxy, env vars, build settings)
- [ ] T004 [P] Create TypeScript configuration in `ui-nextjs/tsconfig.json` (strict mode, path aliases)
- [ ] T005 [P] Create Tailwind configuration in `ui-nextjs/tailwind.config.ts` (theme, colors, dark mode class strategy)
- [ ] T006 [P] Create PostCSS configuration in `ui-nextjs/postcss.config.js` for Tailwind processing
- [ ] T007 [P] Create ESLint configuration in `ui-nextjs/.eslintrc.json` (Next.js rules, TypeScript rules)
- [ ] T008 [P] Create Prettier configuration in `ui-nextjs/.prettierrc` (formatting rules)
- [ ] T009 [P] Create environment template in `ui-nextjs/.env.local.example` (NEXT_PUBLIC_FLASK_URL, etc.)
- [ ] T010 [P] Create README in `ui-nextjs/README.md` with setup instructions based on quickstart.md
- [ ] T011 Create project directory structure: `src/app/`, `src/components/`, `src/lib/`, `src/hooks/`, `src/styles/`, `public/`

**Checkpoint**: Project initialized - can run `npm install` and `npm run dev` successfully

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T012 Create TypeScript interfaces in `ui-nextjs/src/lib/types.ts` from data-model.md (Question, QueryResult, PlotlyFigure, QuestionAnswer, all Config interfaces, TrainingDataStats, UI state types, API request/response types)
- [ ] T013 Create Zod validation schemas in `ui-nextjs/src/lib/validation.ts` from data-model.md (databaseConfigSchema, llmConfigSchema, chromadbConfigSchema, flaskConfigSchema, trainingConfigSchema)
- [ ] T014 Create Axios API client in `ui-nextjs/src/lib/api-client.ts` (base configuration, interceptors, error handling, timeout: 30s)
- [ ] T015 Create utility functions in `ui-nextjs/src/lib/utils.ts` (cn helper for Tailwind, formatTimestamp, formatExecutionTime, getDefaultPort)
- [ ] T016 Initialize Shadcn/ui with `npx shadcn-ui@latest init` (Tailwind zinc theme, CSS variables)
- [ ] T017 [P] Add Shadcn Button component in `ui-nextjs/src/components/ui/button.tsx`
- [ ] T018 [P] Add Shadcn Input component in `ui-nextjs/src/components/ui/input.tsx`
- [ ] T019 [P] Add Shadcn Textarea component in `ui-nextjs/src/components/ui/textarea.tsx`
- [ ] T020 [P] Add Shadcn Select component in `ui-nextjs/src/components/ui/select.tsx`
- [ ] T021 [P] Add Shadcn Tabs component in `ui-nextjs/src/components/ui/tabs.tsx`
- [ ] T022 [P] Add Shadcn Card component in `ui-nextjs/src/components/ui/card.tsx`
- [ ] T023 [P] Add Shadcn Dialog component in `ui-nextjs/src/components/ui/dialog.tsx`
- [ ] T024 [P] Add Shadcn Toast component in `ui-nextjs/src/components/ui/toast.tsx` with useToast hook
- [ ] T025 [P] Add Shadcn Label component in `ui-nextjs/src/components/ui/label.tsx`
- [ ] T026 [P] Add Shadcn Badge component in `ui-nextjs/src/components/ui/badge.tsx`
- [ ] T027 [P] Add Shadcn Table component in `ui-nextjs/src/components/ui/table.tsx`
- [ ] T028 Create root layout in `ui-nextjs/src/app/layout.tsx` (HTML structure, font imports, ThemeProvider from next-themes, React Query provider, Toaster, metadata)
- [ ] T029 Create global styles in `ui-nextjs/src/styles/globals.css` (Tailwind directives, CSS variables for light/dark themes, Prism.js theme imports)
- [ ] T030 Create React Query provider wrapper in `ui-nextjs/src/lib/query-provider.tsx` (QueryClient with default options, QueryClientProvider)
- [ ] T031 Create React Query keys factory in `ui-nextjs/src/lib/query-keys.ts` (questions, config, training, plotly keys with type-safe factory functions)
- [ ] T032 Create custom hook for dark mode in `ui-nextjs/src/hooks/useDarkMode.ts` (useTheme wrapper, localStorage persistence)
- [ ] T033 Create DarkModeToggle component in `ui-nextjs/src/components/DarkModeToggle.tsx` (manual toggle button with sun/moon icons, uses useDarkMode hook)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Natural Language Questions (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with their database using natural language questions through a modern web interface, receiving SQL queries and visualizations without writing code.

**Independent Test**: Submit a question like "Show top 10 customers", verify SQL generation, execution, result display, and chart rendering.

### API Integration for User Story 1

- [ ] T034 [P] [US1] Implement askQuestion API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/ask with question, sessionId, returns QueryResult)
- [ ] T035 [P] [US1] Implement getPlotlyFigure API call in `ui-nextjs/src/lib/api-client.ts` (GET /api/v0/generate_plotly_figure?id={figureId}, returns PlotlyFigure)

### React Query Hooks for User Story 1

- [ ] T036 [US1] Create useAskQuestion mutation hook in `ui-nextjs/src/hooks/useQuery.ts` (useMutation for asking questions, manages loading/error states, optimistic updates)
- [ ] T037 [US1] Create usePlotlyFigure query hook in `ui-nextjs/src/hooks/useQuery.ts` (useQuery for fetching chart data by ID, enabled conditionally when hasChart=true)

### UI Components for User Story 1

- [ ] T038 [P] [US1] Create QuestionInput component in `ui-nextjs/src/components/QuestionInput.tsx` (Textarea for question, submit Button, loading spinner, session management)
- [ ] T039 [P] [US1] Create SQLHighlight component in `ui-nextjs/src/components/SQLHighlight.tsx` (Prism.js syntax highlighting for SQL, copy button, line numbers)
- [ ] T040 [P] [US1] Create ResultsDisplay component in `ui-nextjs/src/components/ResultsDisplay.tsx` (Table component displaying data/columns from QueryResult, pagination for large datasets)
- [ ] T041 [P] [US1] Create ChartRenderer component in `ui-nextjs/src/components/ChartRenderer.tsx` (react-plotly.js Plot wrapper, loads figure via usePlotlyFigure hook, responsive layout, dark mode support)
- [ ] T042 [US1] Create QuestionAnswerCard component in `ui-nextjs/src/components/QuestionAnswerCard.tsx` (Card combining SQLHighlight, ResultsDisplay, ChartRenderer, error display)

### Pages for User Story 1

- [ ] T043 [US1] Create home page in `ui-nextjs/src/app/page.tsx` (QuestionInput at top, list of QuestionAnswerCards below, uses useAskQuestion hook, manages session state)

### Error Handling for User Story 1

- [ ] T044 [US1] Implement error handling in QuestionInput component (display user-friendly messages for SQL generation failures, network errors, database errors)
- [ ] T045 [US1] Implement error handling in ChartRenderer component (fallback UI when chart fails to load, graceful degradation)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can ask questions, see SQL, view results, and see charts

---

## Phase 4: User Story 2 - Configure System Settings (Priority: P2)

**Goal**: Enable users to configure LLM provider, database connections, vector store settings, and training options through a web-based settings interface without editing configuration files.

**Independent Test**: Navigate to settings, update database credentials, test connection, verify changes persist.

### API Integration for User Story 2

- [ ] T046 [P] [US2] Implement getConfig API call in `ui-nextjs/src/lib/api-client.ts` (GET /api/v0/get_config, returns AppConfig with all configurations)
- [ ] T047 [P] [US2] Implement updateLLMConfig API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/update_llm_config, accepts Partial<LLMConfig>)
- [ ] T048 [P] [US2] Implement updateDatabaseConfig API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/update_database_config, accepts DatabaseConfig)
- [ ] T049 [P] [US2] Implement updateChromaDBConfig API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/update_chromadb_config, accepts ChromaDBConfig)
- [ ] T050 [P] [US2] Implement updateFlaskConfig API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/update_flask_config, accepts FlaskConfig)
- [ ] T051 [P] [US2] Implement testDatabaseConnection API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/test_database_connection, returns ConnectionTestResult)
- [ ] T052 [P] [US2] Implement testLLMConnection API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/test_llm_connection, returns ConnectionTestResult)

### React Query Hooks for User Story 2

- [ ] T053 [US2] Create useConfig query hook in `ui-nextjs/src/hooks/useConfig.ts` (useQuery for fetching all configurations, caches result)
- [ ] T054 [US2] Create useUpdateConfig mutation hooks in `ui-nextjs/src/hooks/useConfig.ts` (separate useMutation hooks for each config type: LLM, Database, ChromaDB, Flask, optimistic updates, toast notifications)
- [ ] T055 [US2] Create useTestConnection mutation hooks in `ui-nextjs/src/hooks/useConfig.ts` (useMutation for testing database and LLM connections, loading states, result display)

### UI Components for User Story 2

- [ ] T056 [P] [US2] Create SettingsTabs component in `ui-nextjs/src/components/SettingsTabs.tsx` (Tabs component for LLM, Database, ChromaDB, Flask, Training tabs)
- [ ] T057 [P] [US2] Create LLMSettings component in `ui-nextjs/src/components/LLMSettings.tsx` (Form with Input fields for endpoint, api_key, model Select, temperature/max_tokens number inputs, save Button using useUpdateConfig, test connection Button using useTestConnection, uses react-hook-form + Zod validation)
- [ ] T058 [P] [US2] Create DatabaseSettings component in `ui-nextjs/src/components/DatabaseSettings.tsx` (Form with Select for type, Input for host/database/schema/user/password, number Input for port with auto-fill on type change via getDefaultPort, save Button, test connection Button, uses react-hook-form + Zod validation)
- [ ] T059 [P] [US2] Create ChromaDBSettings component in `ui-nextjs/src/components/ChromaDBSettings.tsx` (Form with number Inputs for n_results_sql/ddl/documentation, save Button, uses react-hook-form + Zod validation)
- [ ] T060 [P] [US2] Create FlaskSettings component in `ui-nextjs/src/components/FlaskSettings.tsx` (Form with Input fields for host/port/title/subtitle, toggle for debug/allow_llm_to_see_data, save Button, uses react-hook-form + Zod validation)

### Pages for User Story 2

- [ ] T061 [US2] Create settings page in `ui-nextjs/src/app/settings/page.tsx` (SettingsTabs component, fetches config via useConfig, displays all settings forms)

### Connection Testing for User Story 2

- [ ] T062 [US2] Implement connection test feedback in LLMSettings component (display success/failure Badge, response time, error details in Dialog)
- [ ] T063 [US2] Implement connection test feedback in DatabaseSettings component (display success/failure Badge, response time, error details in Dialog)

### Auto-fill Logic for User Story 2

- [ ] T064 [US2] Implement getDefaultPort utility in `ui-nextjs/src/lib/utils.ts` (returns default port based on database type: oracle=1521, postgres=5432, mysql=3306, mssql=1433)
- [ ] T065 [US2] Implement auto-fill logic in DatabaseSettings component (useEffect to update port when database type changes, calls getDefaultPort)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can ask questions AND configure all system settings with connection testing

---

## Phase 5: User Story 3 - Manage Training Data (Priority: P2)

**Goal**: Enable users to view existing training data (DDL, documentation, question-SQL pairs) and load new training data to improve SQL generation accuracy.

**Independent Test**: View training data count, click "Load Training Data", verify new items appear and improve question accuracy.

### API Integration for User Story 3

- [ ] T066 [P] [US3] Implement updateTrainingConfig API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/update_training_config, accepts TrainingConfig)
- [ ] T067 [P] [US3] Implement loadTrainingData API call in `ui-nextjs/src/lib/api-client.ts` (POST /api/v0/load_training_data, returns TrainingDataLoadResult)

### React Query Hooks for User Story 3

- [ ] T068 [US3] Create useUpdateTrainingConfig mutation hook in `ui-nextjs/src/hooks/useConfig.ts` (useMutation for updating training configuration, optimistic updates, toast notifications)
- [ ] T069 [US3] Create useLoadTrainingData mutation hook in `ui-nextjs/src/hooks/useConfig.ts` (useMutation for loading training data, loading states, result display, invalidates config query on success)

### UI Components for User Story 3

- [ ] T070 [P] [US3] Create TrainingSettings component in `ui-nextjs/src/components/TrainingSettings.tsx` (Form with toggle for auto_train_on_startup, Input for training_data_path, checkboxes for load_ddl/documentation/training_pairs/skip_if_exists/verbose, save Button using useUpdateTrainingConfig)
- [ ] T071 [US3] Create TrainingDataStats component in `ui-nextjs/src/components/TrainingDataStats.tsx` (Card displaying counts from TrainingConfig: DDL/docs/pairs counts, last updated timestamp, refresh Button)
- [ ] T072 [US3] Create LoadTrainingDataButton component in `ui-nextjs/src/components/LoadTrainingDataButton.tsx` (Button triggering useLoadTrainingData mutation, loading spinner, displays result in Dialog with ddl_loaded/docs_loaded/pairs_loaded counts, errors array)

### Integration into Settings Page

- [ ] T073 [US3] Add TrainingSettings component to settings page in `ui-nextjs/src/app/settings/page.tsx` (add training tab to SettingsTabs, display TrainingSettings, TrainingDataStats, LoadTrainingDataButton)

### Duplicate Detection Feedback

- [ ] T074 [US3] Implement duplicate detection feedback in LoadTrainingDataButton component (display message when skip_if_exists=true and items already exist, show Badge with "Duplicates Skipped" status)

**Checkpoint**: All User Stories 1, 2, and 3 should now be independently functional - users can ask questions, configure settings, AND manage training data

---

## Phase 6: User Story 4 - View Query History (Priority: P3)

**Goal**: Enable users to review previously asked questions, their generated SQL, and results to learn SQL patterns or re-run queries.

**Independent Test**: Ask several questions, navigate to history view, click to re-run a past query.

### State Management for User Story 4

- [ ] T075 [P] [US4] Create local storage utility in `ui-nextjs/src/lib/storage.ts` (functions for saving/loading question history to localStorage, max 100 items, JSON serialization)
- [ ] T076 [US4] Create useQueryHistory custom hook in `ui-nextjs/src/hooks/useQueryHistory.ts` (manages history state, adds new questions, retrieves history, re-runs queries, uses localStorage utility)

### UI Components for User Story 4

- [ ] T077 [P] [US4] Create HistoryItem component in `ui-nextjs/src/components/HistoryItem.tsx` (Card displaying question text, SQL snippet, timestamp, re-run Button, edit Button)
- [ ] T078 [P] [US4] Create HistoryList component in `ui-nextjs/src/components/HistoryList.tsx` (List of HistoryItem components, sorted chronologically, pagination, search filter)

### Pages for User Story 4

- [ ] T079 [US4] Create history page in `ui-nextjs/src/app/history/page.tsx` (HistoryList component, uses useQueryHistory hook)

### Integration with Home Page

- [ ] T080 [US4] Update home page in `ui-nextjs/src/app/page.tsx` to save questions to history (call useQueryHistory.addQuestion after successful query)
- [ ] T081 [US4] Implement re-run functionality in HistoryItem component (button triggers useAskQuestion mutation with historical question text)
- [ ] T082 [US4] Implement edit functionality in HistoryItem component (button navigates to home page with question text pre-filled in QuestionInput)

### Navigation

- [ ] T083 [US4] Add navigation link to history page in root layout `ui-nextjs/src/app/layout.tsx` (header with links to Home and History pages)

**Checkpoint**: All user stories should now be independently functional - complete feature set implemented

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Error Handling

- [ ] T084 [P] Create ErrorBoundary component in `ui-nextjs/src/components/ErrorBoundary.tsx` (catches React errors, displays fallback UI, error details in dev mode)
- [ ] T085 Update root layout in `ui-nextjs/src/app/layout.tsx` to wrap children with ErrorBoundary

### Loading States

- [ ] T086 [P] Create LoadingSpinner component in `ui-nextjs/src/components/LoadingSpinner.tsx` (animated spinner, optional message, size variants)
- [ ] T087 Update all async operations to display LoadingSpinner (QuestionInput, settings forms, LoadTrainingDataButton)

### Responsive Design

- [ ] T088 Test and fix responsive layout for mobile viewports (375px+) across all pages (home, settings, history)
- [ ] T089 Update QuestionInput component for mobile touch interactions (larger tap targets, better keyboard UX)

### Accessibility

- [ ] T090 [P] Add ARIA labels to all interactive elements (buttons, inputs, tabs)
- [ ] T091 [P] Implement keyboard navigation for SettingsTabs component (arrow keys, Tab/Shift+Tab)
- [ ] T092 [P] Add focus indicators to all focusable elements (outlines, ring styles)
- [ ] T093 Test with screen reader (VoiceOver/NVDA) and fix issues

### Performance Optimization

- [ ] T094 [P] Implement code splitting for settings page (dynamic imports for settings components)
- [ ] T095 [P] Optimize Plotly.js bundle size (use plotly.js-basic-dist instead of full plotly.js)
- [ ] T096 [P] Add React.memo to expensive components (ResultsDisplay, ChartRenderer, HistoryList)
- [ ] T097 Implement virtualization for large result sets in ResultsDisplay component (use react-window or similar)

### Documentation

- [ ] T098 [P] Update README in `ui-nextjs/README.md` with complete setup instructions (prerequisites, installation, configuration, development, deployment)
- [ ] T099 [P] Add JSDoc comments to all public API functions in `ui-nextjs/src/lib/api-client.ts`
- [ ] T100 [P] Add JSDoc comments to all custom hooks in `ui-nextjs/src/hooks/`
- [ ] T101 Create troubleshooting guide in `ui-nextjs/TROUBLESHOOTING.md` (common errors, Flask connection issues, CORS problems, chart rendering issues)

### Security

- [ ] T102 [P] Implement input sanitization for user questions (prevent XSS in QuestionInput component)
- [ ] T103 [P] Ensure no sensitive data logged to console in production (remove console.log, use proper logging)
- [ ] T104 Configure Content Security Policy headers in `ui-nextjs/next.config.js`

### Build & Deploy

- [ ] T105 Create production build script in `ui-nextjs/package.json` (npm run build)
- [ ] T106 Create Docker configuration in `ui-nextjs/Dockerfile` (multi-stage build, nginx or standalone output)
- [ ] T107 Create Docker Compose configuration in `ui-nextjs/docker-compose.yml` (Next.js + Flask backend orchestration)
- [ ] T108 Test production build locally (npm run build && npm run start)
- [ ] T109 Create deployment guide in `ui-nextjs/DEPLOYMENT.md` (Vercel, Docker, static export options)

### Final Validation

- [ ] T110 Run Lighthouse audit and optimize (target: Performance 90+, Accessibility 90+, Best Practices 90+, SEO 90+)
- [ ] T111 Validate all quickstart.md scenarios work end-to-end
- [ ] T112 Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] T113 Manual dark mode testing (toggle between light/dark, verify all components styled correctly)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion - can start after T033
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - can start after T033
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion - can start after T033
- **User Story 4 (Phase 6)**: Depends on User Story 1 (Phase 3) completion - needs useAskQuestion hook from T036
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (fully independent settings)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (settings tab, separate from US2)
- **User Story 4 (P3)**: Depends on User Story 1 completion - needs home page and question asking functionality (T043, T036)

### Within Each User Story

**User Story 1**:
1. API calls (T034, T035) [parallel]
2. React Query hooks (T036, T037) depend on API calls
3. UI components (T038-T042) [parallel after hooks]
4. Page (T043) depends on components
5. Error handling (T044, T045) depends on components

**User Story 2**:
1. API calls (T046-T052) [parallel]
2. React Query hooks (T053-T055) depend on API calls
3. UI components (T056-T060) [parallel after hooks]
4. Page (T061) depends on components
5. Connection testing (T062, T063) depends on components
6. Auto-fill logic (T064, T065) can run parallel with other components

**User Story 3**:
1. API calls (T066, T067) [parallel]
2. React Query hooks (T068, T069) depend on API calls
3. UI components (T070-T072) [parallel after hooks]
4. Integration (T073) depends on components
5. Duplicate detection (T074) depends on LoadTrainingDataButton

**User Story 4**:
1. Storage utility & hook (T075, T076) [parallel]
2. UI components (T077, T078) [parallel after hook]
3. Page (T079) depends on components
4. Integration (T080-T082) depends on page and User Story 1 completion
5. Navigation (T083) depends on page

### Parallel Opportunities

**Setup (Phase 1)**:
- T003, T004, T005, T006, T007, T008, T009, T010 can all run in parallel after T002

**Foundational (Phase 2)**:
- T017-T027 (Shadcn components) can all run in parallel after T016
- T029, T030, T031, T032, T033 can run in parallel after T028

**User Story 1**:
- T034, T035 (API calls) can run in parallel
- T038, T039, T040, T041 (UI components) can run in parallel after T037

**User Story 2**:
- T046-T052 (API calls) can run in parallel
- T056-T060 (settings components) can run in parallel after T055

**User Story 3**:
- T066, T067 (API calls) can run in parallel
- T070, T071 (components) can run in parallel after T069

**User Story 4**:
- T075, T076 (storage & hook) can run in parallel
- T077, T078 (components) can run in parallel after T076

**Polish (Phase 7)**:
- T084, T086, T090, T091, T092, T093, T094, T095, T096, T098, T099, T100, T102, T103 can all run in parallel

### Critical Path

The fastest path to MVP (User Story 1 only):
```
T001 → T002 → T011 (Setup)
↓
T012 → T013 → T014 → T015 (Core infrastructure)
↓
T016 → [T017-T027 parallel] (Shadcn components)
↓
T028 → T029 → T030 → T031 → T032 → T033 (Foundation complete)
↓
T034 → T036 (API & hooks)
↓
T038 → T042 (UI components)
↓
T043 (Home page)
↓
T044 → T045 (Error handling)
```

**Estimated MVP completion**: ~40 tasks (T001-T045)

---

## Parallel Example: User Story 1 (Ask Questions)

```bash
# After foundational phase is complete, launch API calls in parallel:
Task: "Implement askQuestion API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement getPlotlyFigure API call in ui-nextjs/src/lib/api-client.ts"

# After hooks are done, launch all UI components in parallel:
Task: "Create QuestionInput component in ui-nextjs/src/components/QuestionInput.tsx"
Task: "Create SQLHighlight component in ui-nextjs/src/components/SQLHighlight.tsx"
Task: "Create ResultsDisplay component in ui-nextjs/src/components/ResultsDisplay.tsx"
Task: "Create ChartRenderer component in ui-nextjs/src/components/ChartRenderer.tsx"
```

---

## Parallel Example: User Story 2 (Configure Settings)

```bash
# Launch all API calls in parallel:
Task: "Implement getConfig API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement updateLLMConfig API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement updateDatabaseConfig API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement updateChromaDBConfig API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement updateFlaskConfig API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement testDatabaseConnection API call in ui-nextjs/src/lib/api-client.ts"
Task: "Implement testLLMConnection API call in ui-nextjs/src/lib/api-client.ts"

# Launch all settings forms in parallel after hooks:
Task: "Create LLMSettings component in ui-nextjs/src/components/LLMSettings.tsx"
Task: "Create DatabaseSettings component in ui-nextjs/src/components/DatabaseSettings.tsx"
Task: "Create ChromaDBSettings component in ui-nextjs/src/components/ChromaDBSettings.tsx"
Task: "Create FlaskSettings component in ui-nextjs/src/components/FlaskSettings.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T011)
2. Complete Phase 2: Foundational (T012-T033) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T034-T045)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Ask questions: "Show top 10 customers"
   - Verify SQL generation works
   - Verify results display correctly
   - Verify charts render
   - Verify error handling
5. Deploy/demo if ready

**MVP Task Count**: 45 tasks (T001-T045)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T033)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! T034-T045)
3. Add User Story 2 → Test independently → Deploy/Demo (T046-T065)
4. Add User Story 3 → Test independently → Deploy/Demo (T066-T074)
5. Add User Story 4 → Test independently → Deploy/Demo (T075-T083)
6. Polish & optimize → Final production release (T084-T113)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T033)
2. **Once Foundational is done (after T033)**:
   - **Developer A**: User Story 1 - Ask Questions (T034-T045)
   - **Developer B**: User Story 2 - Configure Settings (T046-T065)
   - **Developer C**: User Story 3 - Manage Training (T066-T074)
3. **After US1 completes**:
   - **Developer D**: User Story 4 - View History (T075-T083, depends on US1)
4. **All developers**: Polish & Cross-Cutting (T084-T113)

Stories complete and integrate independently.

---

## Task Count Summary

- **Phase 1 (Setup)**: 11 tasks (T001-T011)
- **Phase 2 (Foundational)**: 22 tasks (T012-T033) - **BLOCKS ALL STORIES**
- **Phase 3 (User Story 1 - P1)**: 12 tasks (T034-T045) - **MVP**
- **Phase 4 (User Story 2 - P2)**: 20 tasks (T046-T065)
- **Phase 5 (User Story 3 - P2)**: 9 tasks (T066-T074)
- **Phase 6 (User Story 4 - P3)**: 9 tasks (T075-T083)
- **Phase 7 (Polish)**: 30 tasks (T084-T113)

**Total**: 113 tasks

**MVP (User Story 1 only)**: 45 tasks (40% of total)  
**MVP + Settings (US1 + US2)**: 65 tasks (58% of total)  
**MVP + Settings + Training (US1 + US2 + US3)**: 74 tasks (65% of total)  
**All User Stories (US1-4)**: 83 tasks (73% of total)

### Parallel Opportunities Identified

- **Setup**: 8 parallel tasks
- **Foundational**: 15 parallel tasks  
- **User Story 1**: 6 parallel tasks
- **User Story 2**: 12 parallel tasks
- **User Story 3**: 4 parallel tasks
- **User Story 4**: 4 parallel tasks
- **Polish**: 18 parallel tasks

**Total Parallel Tasks**: 67 (59% of all tasks can run in parallel with proper planning)

### Independent Test Criteria

- **User Story 1**: Submit question "Show top 10 customers" → Verify SQL + results + chart render
- **User Story 2**: Navigate to /settings → Update database port → Test connection → Verify success
- **User Story 3**: Navigate to /settings training tab → Click "Load Training Data" → Verify counts increase
- **User Story 4**: Navigate to /history → See previous questions → Click re-run → Verify executes

### Suggested MVP Scope

**Recommendation**: Implement **User Story 1 only** (45 tasks) for initial MVP.

**Rationale**:
- Delivers core value: natural language database queries
- Demonstrates full workflow: question → SQL → results → charts
- Provides immediate user feedback and validation
- Settings can be configured via Flask backend initially
- Reduces risk and time to market

**Next Iteration**: Add User Story 2 (settings UI) for self-service configuration.

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Foundational phase (T012-T033) MUST complete before ANY user story work begins**
- Tests are NOT included per feature specification - focus on implementation
- Accessibility tasks (T090-T093) are critical for production readiness
- Performance optimization (T094-T097) can be done after MVP if needed
