# Changelog

All notable changes to myDbAssistant will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-XX

### 🎉 Major Changes

#### Migrated from Umbrella Gateway to Copilot Socket Core v3.2.5

Complete LLM API migration with enhanced features and improved architecture.

**Migration Benefits:**
- ✅ **No authentication required** for localhost (was: Bearer token)
- ✅ **Built-in session management** (no manual session creation)
- ✅ **Tool calling support** (1-200 rounds, configurable)
- ✅ **Multimodal support** (text + images)
- ✅ **Better error handling** and logging
- ✅ **Standardized endpoints** (/health, /models, /tools)
- ✅ **Improved performance** (faster response times)

### Added

- **Settings UI** - Complete web-based configuration management
  - Modern single-page interface at `/settings`
  - Tab-based navigation (LLM, Database, ChromaDB, Flask, Training)
  - Real-time validation and testing
  - Test connection buttons for LLM and database
  - Shows available models dynamically
  - Saves to JSON files automatically
  
- **Tool Calling Support** - New `max_tool_rounds` configuration
  - Configure in Settings UI or `llm.json`
  - Range: 1-200 rounds
  - Default: 5 rounds
  - Logs tool call usage automatically

- **Session Management** - Automatic session handling
  - Auto-creates sessions on first request
  - Maintains conversation context
  - Session IDs logged for debugging

- **Enhanced Testing** - Comprehensive test suite
  - `test_copilot_socket_core.py` - 7 automated tests
  - `quick_test.py` - Quick smoke test
  - `compare_apis.py` - Compare old vs new API
  - `TESTING_MIGRATION.md` - Complete testing guide

- **New Configuration Fields** in `llm.json`:
  - `api_type`: "copilot-socket-core" (identifies API version)
  - `max_tool_rounds`: 5 (tool calling iterations)
  - `timeout`: 60 (request timeout in seconds)

- **Documentation** - Comprehensive guides
  - `TESTING_MIGRATION.md` - Testing procedures
  - `docs/MIGRATION_TO_COPILOT_SOCKET_CORE.md` - Migration guide (600+ lines)
  - `docs/LLM_API_MIGRATION_SUMMARY.md` - Change summary (500+ lines)
  - `docs/TECHNICAL_SPEC.md` - API specification
  - `docs/settings-ui-guide.md` - Settings UI guide

### Changed

- **LLM Integration** (`quick_start_flask_ui.py`)
  - Complete rewrite of `MyCustomLLM` class (~120 lines)
  - New method: `_ensure_session()` for auto session creation
  - Request format: messages array → single message string
  - Response parsing: `data.get('text')` → `data.get('reply')`
  - Added tool calls logging
  - Enhanced error messages

- **API Configuration** (`ui/config/llm.json`)
  - `endpoint`: "http://localhost:8765" → "http://localhost:8080"
  - `model`: "copilot/gpt-5-mini" → "copilot/gpt-4o"
  - `api_key`: Required → Empty/removed (not needed for localhost)
  - Added `max_tool_rounds` field

- **Settings UI** (`config_ui.py`)
  - Updated LLM section HTML for new fields
  - Added max_tool_rounds input field
  - Enhanced LLM connection test (shows available models)
  - Updated JavaScript config loading/saving

- **Documentation** (`README.md`)
  - Updated prerequisites (Copilot Socket Core, not Umbrella Gateway)
  - Updated setup instructions (port 8080, not 8765)
  - Removed auth token requirements
  - Added testing section
  - Updated troubleshooting section
  - Added configuration files section

### Removed

- **Authentication Requirements** - No longer need API key for localhost
- **Manual Session Creation** - Now automatic
- **Old Error Messages** - Replaced with Copilot Socket Core specific messages

### Fixed

- Authentication issues (no longer required)
- Session management complexity (now automatic)
- Error messages referencing wrong API/port

### Migration Notes

**Breaking Changes:**
- Configuration format changed (see `llm.json`)
- API endpoint changed (port 8765 → 8080)
- Request/response format changed
- Authentication no longer required for localhost

**Upgrade Path:**
1. Install Copilot Socket Core extension in VSCode
2. Update `ui/config/llm.json` (see migration guide)
3. Start Copilot Socket Core server
4. Test: `python3 test_copilot_socket_core.py`
5. Run: `python3 quick_start_flask_ui.py`

**Rollback Plan:**
See `docs/LLM_API_MIGRATION_SUMMARY.md` for rollback instructions.

**Compatibility:**
- Python: 3.11+ (unchanged)
- VSCode: Latest recommended
- Copilot Socket Core: v3.2.5+
- Database drivers: No changes

### Security

- Removed API key from localhost configuration (not required)
- Settings UI has no built-in authentication (⚠️ add for production)
- Configuration files in `.gitignore` (prevents credential commits)

### Performance

- Response times improved with Copilot Socket Core
- Session reuse reduces overhead
- Tool calling enables more accurate queries
- Reduced authentication overhead (no token validation)

---

## [1.0.0] - 2024-XX-XX

### Added

- Initial release of myDbAssistant
- Umbrella Gateway integration
- Multi-database support (Oracle, PostgreSQL, MySQL, SQL Server)
- ChromaDB vector store
- Flask web UI
- JSON configuration system
- Training control system
- Auto-learning from Q&A pairs

### Features

- Natural language to SQL conversion
- RAG-based query generation
- Training data management
- Plotly visualizations
- Flask REST API

---

## Versioning

- **Major version (X.0.0)**: Breaking changes (API changes, config format changes)
- **Minor version (0.X.0)**: New features (backward compatible)
- **Patch version (0.0.X)**: Bug fixes (backward compatible)

## Links

- [Migration Guide](docs/MIGRATION_TO_COPILOT_SOCKET_CORE.md)
- [Testing Guide](TESTING_MIGRATION.md)
- [Settings UI Guide](docs/settings-ui-guide.md)
- [Technical Spec](docs/TECHNICAL_SPEC.md)
- [Vanna AI](https://github.com/vanna-ai/vanna)
