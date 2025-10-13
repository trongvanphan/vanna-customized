# Spec-Kit Quick Reference

## 🚀 Quick Command Reference

### Core Workflow (Use in Order)
```
/speckit.constitution → /speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement
```

### Optional Enhancement Commands
```
/speckit.clarify   # Before /speckit.plan - ask questions about unclear areas
/speckit.analyze   # After /speckit.tasks - check consistency
/speckit.checklist # After /speckit.plan - generate quality checks
```

## 📝 Example: Add New Vector Store to Vanna

### 1. Constitution (One-time)
```
/speckit.constitution Create principles for Vanna development:
- Follow multiple inheritance pattern (VectorStore first, LLM second)
- Use deterministic_uuid for all training data IDs
- Method names: get_*, add_*, generate_*, run_*, remove_*, connect_*
- All new dependencies must be optional
- Include tests in tests/test_vanna.py
- Export in __init__.py
- Document in README
```

### 2. Specify Requirements
```
/speckit.specify Add Weaviate vector store integration:
- Create src/vanna/weaviate/weaviate_vector.py
- Inherit from VannaBase
- Implement all vector store abstract methods
- Support both cloud and local Weaviate instances
- Use weaviate-client library as optional dependency
- Support Weaviate's hybrid search capabilities
- Handle embeddings as List[float]
```

### 3. Create Plan
```
/speckit.plan Implementation approach:
- Use weaviate-client v4.x
- Create Weaviate class "VannaTrainingData" with properties: content, embedding, type (sql/ddl/doc)
- Implement deterministic UUID generation for idempotent adds
- Support n_results configuration
- Add weaviate extra to pyproject.toml: weaviate[all]>=4.0.0
- Follow ChromaDB implementation pattern
- Handle connection errors gracefully
```

### 4. Generate Tasks
```
/speckit.tasks
```

### 5. Clarify (Optional)
```
/speckit.clarify Focus on:
- How to handle Weaviate schema versioning?
- Should we support multi-tenancy in Weaviate?
- What's the migration path from other vector stores?
```

### 6. Implement
```
/speckit.implement
```

## 🔧 CLI Commands

### Check Installation
```bash
specify check
```

### Initialize New Project
```bash
# For new projects
specify init my-project --ai copilot

# For existing project (already done)
specify init --here --ai copilot --force
```

### Update Spec-Kit
```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git
```

## 📁 Generated Artifacts Location

All spec artifacts are created in:
```
specs/
└── features/
    └── {branch-name-or-feature-id}/
        ├── spec.md        # From /speckit.specify
        ├── plan.md        # From /speckit.plan  
        ├── tasks.md       # From /speckit.tasks
        ├── analysis.md    # From /speckit.analyze
        └── checklist.md   # From /speckit.checklist
```

## 🎯 Best Practices for Vanna

### When to Use Spec-Kit
✅ **Good for:**
- Adding new LLM providers
- Adding new vector stores
- Complex feature development
- Architecture changes
- Multi-step implementations

❌ **Not needed for:**
- Bug fixes
- Documentation updates
- Simple refactoring
- Single-file changes

### Vanna-Specific Patterns to Include in Specs

**Multiple Inheritance:**
```python
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)
```

**Config Pattern:**
```python
def __init__(self, config=None):
    VannaBase.__init__(self, config=config)
    if config is None:
        config = {}
    self.api_key = config.get('api_key', os.getenv('PROVIDER_API_KEY'))
```

**Deterministic IDs:**
```python
from vanna.utils import deterministic_uuid
id = deterministic_uuid(content) + "-sql"
```

**Optional Dependencies:**
```python
try:
    import optional_lib
except ImportError:
    raise DependencyError("Install via: pip install vanna[provider]")
```

## 🔄 Workflow with Git

```bash
# 1. Create feature branch (spec-kit detects this automatically)
git checkout -b feature/add-qdrant-support

# 2. Use spec-kit commands
/speckit.specify ...
/speckit.plan ...
/speckit.tasks ...
/speckit.implement

# 3. Review generated specs
cat specs/features/feature-add-qdrant-support/spec.md

# 4. Commit everything including specs
git add .
git commit -m "Add Qdrant vector store support"

# 5. Push and create PR
git push origin feature/add-qdrant-support
```

## 🧪 Testing Generated Code

After `/speckit.implement`:

```bash
# Run tests
pytest tests/test_vanna.py

# Check linting
tox -e flake8

# Test in notebook
jupyter notebook
```

## 📚 Documentation Links

- **Spec-Kit Guide:** [SPEC-KIT-GUIDE.md](SPEC-KIT-GUIDE.md)
- **Spec-Kit Repo:** https://github.com/github/spec-kit
- **Vanna Copilot Instructions:** [.github/copilot-instructions.md](.github/copilot-instructions.md)
- **Vanna Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

## 💡 Tips

1. **Start with constitution** - Define Vanna patterns once, reference in all specs
2. **Be specific in specs** - "Add Qdrant support" → "Add Qdrant vector store with hybrid search"
3. **Review before implement** - Always check `plan.md` and `tasks.md` before `/speckit.implement`
4. **Use clarify liberally** - Better to ask questions than make wrong assumptions
5. **Commit specs to git** - They're valuable documentation for PRs

## 🚨 Troubleshooting

**Slash commands not working:**
- Restart VS Code
- Check GitHub Copilot is active
- Verify `.github/prompts/*.prompt.md` files exist

**Feature detection issues:**
```bash
# Make sure you're on a feature branch
git checkout -b feature/my-feature

# Or set manually (not recommended)
export SPECIFY_FEATURE="001-my-feature"
```

**Template errors:**
```bash
# Reinitialize (safe operation)
specify init --here --ai copilot --force
```
