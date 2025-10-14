# Feature Specification: Convert Flask UI to Next.js Application

**Feature Branch**: `001-convert-quick-start`  
**Created**: October 13, 2025  
**Status**: Draft  
**Input**: User description: "Convert quick_start_flask_ui to Next.js page in new ui-nextjs folder"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Natural Language Questions (Priority: P1)

Users can interact with their database using natural language questions through a modern web interface, receiving SQL queries and visualizations without writing code.

**Why this priority**: Core feature that delivers immediate value - enables non-technical users to query databases.

**Independent Test**: Can be fully tested by submitting a question (e.g., "Show top 10 customers") and verifying SQL generation, execution, and result display.

**Acceptance Scenarios**:

1. **Given** user is on the home page, **When** they type "What are the top 10 customers by sales?" and click Ask, **Then** the system generates SQL, displays the query, shows results in a table, and renders a chart
2. **Given** user asks a question, **When** SQL generation fails, **Then** the system displays a user-friendly error message explaining what went wrong
3. **Given** user receives results, **When** they want to refine their question, **Then** they can submit a follow-up question using conversation context

---

### User Story 2 - Configure System Settings (Priority: P2)

Users can configure LLM provider, database connections, vector store settings, and training options through a web-based settings interface without editing configuration files.

**Why this priority**: Enables users to adapt the system to their environment without technical knowledge or server restarts.

**Independent Test**: Can be tested by navigating to settings, updating database credentials, testing connection, and verifying changes persist.

**Acceptance Scenarios**:

1. **Given** user is on settings page, **When** they update database credentials and click "Test Connection", **Then** system validates connection and shows success/failure status
2. **Given** user changes LLM model from gpt-5-mini to gpt-5, **When** they save settings, **Then** subsequent questions use the new model
3. **Given** user wants to switch databases, **When** they change database type (Oracle to PostgreSQL), **Then** default port auto-fills and schema options update accordingly

---

### User Story 3 - Manage Training Data (Priority: P2)

Users can view existing training data (DDL, documentation, question-SQL pairs) and load new training data to improve SQL generation accuracy.

**Why this priority**: Critical for customizing the system to specific database schemas and business terminology.

**Independent Test**: Can be tested by viewing training data count, clicking "Load Training Data", and verifying new items appear and improve question accuracy.

**Acceptance Scenarios**:

1. **Given** user is on settings page training tab, **When** they click "Load Training Data Now", **Then** system loads files from configured directory and shows count of items added
2. **Given** training data already exists, **When** user tries to load again, **Then** system detects duplicates and skips re-loading
3. **Given** user has custom DDL files, **When** they place files in trainingMyDb/ddl/, **Then** those schemas are automatically included in next load

---

### User Story 4 - View Query History (Priority: P3)

Users can review previously asked questions, their generated SQL, and results to learn SQL patterns or re-run queries.

**Why this priority**: Enhances learning and productivity but not essential for core functionality.

**Independent Test**: Can be tested by asking several questions, navigating to history view, and clicking to re-run a past query.

**Acceptance Scenarios**:

1. **Given** user has asked multiple questions, **When** they view history, **Then** they see chronological list with question text, SQL, and timestamp
2. **Given** user views a historical query, **When** they click "Re-run", **Then** system executes the SQL again and shows fresh results
3. **Given** user wants to modify a past query, **When** they click "Edit", **Then** the question text pre-fills in the input field for refinement

---

### Edge Cases

- What happens when the database connection is lost during a query?
- How does system handle very large result sets (10,000+ rows)?
- What if LLM service (Copilot Socket Core) is unavailable?
- How to handle concurrent users asking questions simultaneously?
- What if training data files are corrupted or invalid JSON?
- How does system behave when JavaScript is disabled?
- What happens if user navigates away during a long-running query?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Next.js-based web interface that replicates all functionality from the Flask UI (question asking, settings management, training data loading)
- **FR-002**: System MUST communicate with the existing Vanna backend via REST API endpoints
- **FR-003**: System MUST render interactive Plotly charts from backend-generated figure data
- **FR-004**: System MUST support real-time question-answering with loading states and progress indicators
- **FR-005**: System MUST persist all user configurations (LLM, database, ChromaDB, Flask, training) to JSON files in ui/config/ directory
- **FR-006**: System MUST provide settings UI with tabbed interface for LLM, Database, ChromaDB, Flask, and Training configurations
- **FR-007**: System MUST validate database and LLM connections before saving settings
- **FR-008**: System MUST display SQL queries in syntax-highlighted format
- **FR-009**: System MUST show query results in both table and chart formats (when appropriate)
- **FR-010**: System MUST handle errors gracefully with user-friendly messages (database errors, LLM failures, network issues)
- **FR-011**: System MUST support automatic training data loading on startup (if configured) with duplicate detection
- **FR-012**: System MUST provide manual training data load button in settings
- **FR-013**: System MUST auto-fill default port numbers based on selected database type (Oracle: 1521, PostgreSQL: 5432, MySQL: 3306, SQL Server: 1433)
- **FR-014**: System MUST support multiple database types (Oracle, PostgreSQL, MySQL, Microsoft SQL Server)
- **FR-015**: System MUST display training data statistics (count of DDL, documentation, Q&A pairs)
- **FR-016**: System MUST maintain session context for follow-up questions via Copilot Socket Core session IDs
- **FR-017**: System MUST render custom branding (title, subtitle) from Flask configuration
- **FR-018**: System MUST provide manual dark mode toggle allowing users to switch between light and dark themes via UI control with preference persistence
- **FR-019**: System MUST work with the Flask backend running on configurable host/port from flask.json

### Key Entities

- **Question**: User's natural language query text, timestamp, associated SQL, results
- **Configuration**: LLM settings (model, temperature, tokens), database credentials, ChromaDB settings, Flask server settings, training settings
- **TrainingData**: DDL schemas, business documentation, question-SQL example pairs
- **QueryResult**: SQL query string, execution status, data rows, column metadata, chart figure JSON
- **Session**: Copilot Socket Core session ID for maintaining conversation context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully ask questions and receive SQL results in under 5 seconds for typical queries (95th percentile)
- **SC-002**: System handles at least 50 concurrent users without response time degradation
- **SC-003**: Configuration changes (database, LLM model) take effect within 2 seconds without requiring page refresh
- **SC-004**: Training data loads complete in under 10 seconds for typical datasets (100 DDL files, 50 documentation files, 200 Q&A pairs)
- **SC-005**: 90% of users can successfully configure database connection on first attempt using settings UI
- **SC-006**: Zero data loss when switching between Flask UI and Next.js UI (all configurations preserved)
- **SC-007**: Chart rendering completes within 1 second for datasets under 1000 rows
- **SC-008**: Error messages guide users to resolution in 95% of common failure scenarios (connection issues, invalid credentials)
- **SC-009**: Page load time under 2 seconds on standard broadband connection
- **SC-010**: Mobile viewport renders usably on devices with 375px width or larger

## Scope *(mandatory)*

### In Scope

- Complete Next.js application in new `ui-nextjs/` folder at project root
- API client to communicate with existing Flask backend
- Modern React components for question input, results display, settings management
- Responsive design supporting desktop and tablet viewports
- Integration with existing JSON configuration system (ui/config/*.json)
- Support for all existing features: question asking, SQL generation, chart rendering, settings management, training data loading
- Database connection testing from UI
- LLM connection testing from UI
- Syntax highlighting for SQL queries
- Interactive Plotly chart rendering
- Error handling and user feedback
- Loading states and progress indicators

### Out of Scope

- Authentication and authorization system (to be added in future iteration)
- Multi-user support with separate accounts (current single-tenant focus)
- Query result export to CSV/Excel (can be added later)
- SQL query editor for manual editing (future enhancement)
- Mobile-native applications (iOS/Android apps)
- Real-time collaborative features (multiple users seeing same queries)
- Custom chart type selection (uses backend-determined chart types)
- Database schema explorer UI (relies on training data for schema awareness)
- Embedded SQL execution without backend (requires Flask server running)

## Assumptions *(mandatory)*

1. **Backend Dependency**: Flask backend (quick_start_flask_ui.py) must be running for Next.js UI to function - this is an API client, not a standalone application
2. **Port Configuration**: Flask backend runs on port 8084 by default (configurable via flask.json)
3. **Same Host Deployment**: Next.js app and Flask backend deployed on same machine or with proper CORS configuration for cross-origin requests
4. **Node.js Environment**: Users have Node.js 18+ installed for Next.js development/deployment
5. **Browser Requirements**: Modern browsers with ES6+ support and JavaScript enabled
6. **Chart Library**: Plotly.js can render charts from JSON figure data generated by backend
7. **Session Management**: Copilot Socket Core extension maintains session state in backend
8. **Configuration Access**: Next.js app has filesystem access to ui/config/*.json files OR accesses configurations via Flask API endpoints
9. **Training Data Path**: Training data files remain in trainingMyDb/ directory accessible to Flask backend
10. **No Breaking Changes**: Existing Flask UI continues to work alongside Next.js UI during transition period

## Dependencies *(optional)*

### External Dependencies

- **Flask Backend**: quick_start_flask_ui.py must be running and accessible
- **Copilot Socket Core**: VS Code extension server on port 8765 for LLM functionality
- **Database Server**: Oracle/PostgreSQL/MySQL/SQL Server instance accessible from Flask backend
- **ChromaDB**: Vector storage for training data (embedded in Flask backend)

### Technical Dependencies

- **Next.js 14+**: App Router for routing and API routes
- **React 18+**: UI components and state management
- **TypeScript**: Type-safe development
- **Plotly.js**: Chart rendering library
- **TailwindCSS**: Utility-first styling (or alternative CSS framework)
- **React Query**: Server state management and caching
- **Zod**: Runtime type validation for API responses
- **Axios**: HTTP client for backend communication

## Non-Functional Requirements *(optional)*

### Performance

- Initial page load under 2 seconds
- Time to interactive under 3 seconds
- API response handling under 100ms (excluding backend processing time)
- Smooth animations at 60fps

### Accessibility

- WCAG 2.1 AA compliance for core functionality
- Keyboard navigation support for all interactive elements
- Screen reader friendly with ARIA labels
- Focus indicators clearly visible
- Color contrast ratios meet accessibility standards

### Usability

- Consistent design language matching modern web standards
- Clear visual feedback for all user actions
- Progress indicators for long-running operations
- Helpful error messages with actionable guidance
- Responsive layout adapting to different screen sizes

### Maintainability

- Component-based architecture for reusability
- TypeScript types for all API interfaces
- Comprehensive JSDoc comments for complex logic
- Separation of concerns (UI components, API client, utilities)
- Environment-based configuration (dev, production)

### Security

- No sensitive credentials stored in frontend code
- API keys and passwords managed by backend
- Input sanitization for user-provided text
- HTTPS-only in production deployment
- CORS properly configured between Next.js and Flask

## Technical Constraints *(optional)*

- **Backend Protocol**: Must use HTTP REST API (Flask backend does not support WebSocket for real-time updates)
- **Chart Format**: Must work with Plotly JSON figure format generated by backend get_plotly_figure()
- **Configuration Storage**: Configurations stored as JSON files, not in database
- **Session Persistence**: Sessions managed by Copilot Socket Core, not by Next.js frontend
- **Database Access**: No direct database connections from frontend - all queries proxied through Flask
- **Training Data**: Training data loading triggered via API call, files remain on server filesystem

## Open Questions for Planning Phase *(optional)*

These questions should be addressed during `/speckit.plan`:

1. Should Next.js app use App Router or Pages Router architecture?
2. State management: React Query vs Redux vs Zustand vs Context API?
3. UI component library: Shadcn/ui vs MUI vs Custom Tailwind components?
4. How to handle long-polling for query execution status updates?
5. Should settings changes require backend restart or hot-reload configuration?
6. Development setup: Separate Next.js dev server (port 3000) + Flask (port 8084) or integrated?
7. Production deployment: Separate services or Next.js API routes proxying to Flask?
8. Testing strategy: Unit tests (Jest), integration tests (Playwright), or both?
9. How to handle Flask backend downtime - show friendly error or queue requests?
10. Chart interactivity: Pass-through Plotly interactions or add custom controls?

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
