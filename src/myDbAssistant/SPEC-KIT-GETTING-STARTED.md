# 🚀 Getting Started with Spec-Kit

## Your First Spec-Kit Command

Open GitHub Copilot chat in VS Code and try:

```
/speckit.constitution
```

This will show you the Vanna development principles that have been established.

## Quick Example: Add a Simple Feature

Let's walk through adding a new utility function to Vanna:

### 1. Specify What You Want
```
/speckit.specify Add a utility function to vanna/utils.py that validates SQL query complexity:
- Count the number of JOINs, subqueries, and WHERE conditions
- Return a complexity score (1-10)
- Provide recommendations for simplification if score > 7
- Include docstring with examples
```

### 2. Create Implementation Plan
```
/speckit.plan Implementation approach:
- Add validate_sql_complexity() function to src/vanna/utils.py
- Use sqlparse library (already a dependency)
- Parse SQL to extract complexity metrics
- Return dict with: {score, joins, subqueries, conditions, recommendations}
- Follow existing Vanna code style
- Add unit tests in tests/test_vanna.py
```

### 3. Generate Tasks
```
/speckit.tasks
```

### 4. Review & Implement
After reviewing the generated tasks:
```
/speckit.implement
```

## Available Commands

### Core Workflow
| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | View/update Vanna development principles |
| `/speckit.specify` | Describe what you want to build |
| `/speckit.plan` | Create technical implementation plan |
| `/speckit.tasks` | Break down into actionable tasks |
| `/speckit.implement` | Execute implementation |

### Enhancement Commands
| Command | Purpose |
|---------|---------|
| `/speckit.clarify` | Ask questions about unclear requirements |
| `/speckit.analyze` | Check cross-artifact consistency |
| `/speckit.checklist` | Generate quality validation checklist |

## Common Patterns for Vanna

### Adding a New LLM Provider

```
/speckit.specify Add Anthropic Claude integration:
- Create src/vanna/anthropic/anthropic_chat.py
- Implement VannaBase abstract methods
- Support Claude 3 models (Opus, Sonnet, Haiku)
- Handle streaming responses
- Add optional dependency: anthropic>=0.18.0

/speckit.plan Follow Vanna's multiple inheritance pattern:
- Inherit from VannaBase
- Implement submit_prompt(), system_message(), user_message(), assistant_message()
- Config dict with api_key, model, temperature
- Export in __init__.py
- Add to pyproject.toml optional-dependencies
- Create test in tests/test_vanna.py

/speckit.tasks
/speckit.implement
```

### Adding a New Vector Store

```
/speckit.specify Add Pinecone vector store integration:
- Create src/vanna/pinecone/pinecone_vector.py
- Support Pinecone serverless and pod-based indexes
- Implement all VannaBase vector methods
- Use deterministic UUIDs for training data
- Support metadata filtering

/speckit.plan Implementation details:
- Use pinecone-client library (optional dependency)
- Follow ChromaDB implementation pattern
- Implement: generate_embedding, add_*, get_*, remove_training_data
- Store Q&A pairs as JSON in metadata
- Support n_results_sql, n_results_ddl, n_results_documentation config
- Add tests with mocked Pinecone client

/speckit.tasks
/speckit.implement
```

### Enhancing myDbAssistant

```
/speckit.specify Add training data import/export to myDbAssistant:
- Export current training data to JSON/CSV
- Import training data from files
- Validate imported data format
- Add UI buttons in settings page
- Show import/export status

/speckit.plan Using existing architecture:
- Extend config_ui.py with new endpoints
- Add /api/v0/export_training_data endpoint
- Add /api/v0/import_training_data endpoint
- Use vn.get_training_data() and vn.train()
- Add new "Training Data" tab in settings UI
- Follow existing Flask patterns

/speckit.tasks
/speckit.implement
```

## Tips for Success

### 1. Be Specific in Specs
❌ **Bad**: "Add database support"
✅ **Good**: "Add PostgreSQL connection support with connection pooling, SSL/TLS, and schema selection"

### 2. Reference Vanna Patterns
Always mention in `/speckit.plan`:
- Multiple inheritance pattern
- Configuration dict pattern
- Method naming conventions
- Deterministic UUID usage
- Optional dependency handling

### 3. Review Before Implementing
Always check the generated files before `/speckit.implement`:
```bash
cat specs/features/your-feature/spec.md
cat specs/features/your-feature/plan.md
cat specs/features/your-feature/tasks.md
```

### 4. Use Clarify for Complex Features
If your feature has ambiguities:
```
/speckit.clarify Focus on:
- How should error handling work?
- What configuration options are needed?
- Should this be backward compatible?
```

### 5. Use Analyze for Quality
After tasks are generated:
```
/speckit.analyze
```
This checks consistency between spec, plan, and tasks.

## Workflow with Git

```bash
# 1. Create feature branch
git checkout -b feature/my-new-feature

# 2. Use spec-kit in VS Code
/speckit.specify ...
/speckit.plan ...
/speckit.tasks ...
/speckit.implement

# 3. Review generated code
git status
git diff

# 4. Commit with specs
git add .
git commit -m "Add feature via spec-kit

Generated specs:
- specs/features/feature-my-new-feature/spec.md
- specs/features/feature-my-new-feature/plan.md
- specs/features/feature-my-new-feature/tasks.md
"

# 5. Push and create PR
git push origin feature/my-new-feature
```

## Troubleshooting

### Slash Commands Not Appearing
1. Restart VS Code
2. Ensure GitHub Copilot is active (check status bar)
3. Type `/spec` to see if autocomplete shows commands

### Feature Not Detected
```bash
# Make sure you're on a feature branch
git checkout -b feature/your-feature

# Or set manually
export SPECIFY_FEATURE="001-your-feature"
```

### Template Errors
```bash
# Reinitialize (safe operation)
specify init --here --ai copilot --force
```

## Next Steps

1. **Read the full guide**: `SPEC-KIT-GUIDE.md`
2. **Review the constitution**: `.specify/memory/constitution.md`
3. **Try a simple feature**: Use spec-kit to add something small
4. **Experiment**: Try different combinations of commands

## Documentation Index

- **SPEC-KIT-SETUP.md** - Integration summary (what was installed)
- **SPEC-KIT-GUIDE.md** - Comprehensive guide (how to use)
- **.specify/QUICK-REFERENCE.md** - Command cheat sheet
- **.specify/memory/constitution.md** - Vanna development principles
- **README.md** - Project overview (updated with spec-kit section)

## Help & Support

- **Spec-Kit GitHub**: https://github.com/github/spec-kit
- **Spec-Kit Video**: https://www.youtube.com/watch?v=a9eR1xsfvHg
- **Vanna Discord**: https://discord.gg/qUZYKHremx
- **Vanna Docs**: https://vanna.ai/docs/

---

**Ready?** Open GitHub Copilot chat and type: `/speckit.constitution`

Happy coding! 🎉
