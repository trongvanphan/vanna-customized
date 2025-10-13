# Spec-Kit Integration Guide for Vanna

## 🌱 What is Spec-Kit?

Spec-Kit is GitHub's toolkit for **Spec-Driven Development** - a methodology where specifications become executable, directly generating working implementations. Instead of writing code first, you define **what** you want to build, then the AI agent generates the implementation.

## ✅ Installation Status

Spec-kit has been successfully integrated into this Vanna project with:

- ✅ **CLI Tool Installed**: `specify` command available globally
- ✅ **GitHub Copilot Integration**: Slash commands configured for VS Code
- ✅ **Templates Added**: `.specify/templates/` directory
- ✅ **Scripts Ready**: `.specify/scripts/bash/` helper scripts
- ✅ **Prompts Configured**: `.github/prompts/` for all spec-kit commands
- ✅ **Security Settings**: `.gitignore` updated to prevent credential leakage

## 🚀 Available Slash Commands

Use these commands in GitHub Copilot chat (Cmd+I or Cmd+Shift+I):

### Core Workflow Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/speckit.constitution` | Establish project principles and guidelines | First step - define coding standards, testing requirements, etc. |
| `/speckit.specify` | Define requirements and user stories | Describe **what** you want to build (not **how**) |
| `/speckit.plan` | Create technical implementation plan | Choose tech stack, architecture, and approach |
| `/speckit.tasks` | Generate actionable task list | Break down plan into executable steps |
| `/speckit.implement` | Execute all tasks | Build the feature according to the plan |

### Enhancement Commands (Optional)

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/speckit.clarify` | Ask structured questions about ambiguous areas | Before `/speckit.plan` to de-risk assumptions |
| `/speckit.analyze` | Cross-artifact consistency check | After `/speckit.tasks`, before `/speckit.implement` |
| `/speckit.checklist` | Generate quality validation checklists | After `/speckit.plan` to validate completeness |

## 📋 Example Workflow for Vanna Project

### Scenario: Add Multi-Tenant Support to myDbAssistant

#### Step 1: Define Principles (One-time Setup)
```
/speckit.constitution Create principles for the Vanna project focusing on:
- Code quality and maintainability
- Multiple inheritance pattern for LLM/VectorStore combinations
- Security best practices for database credentials
- Comprehensive testing requirements
- Documentation standards
```

#### Step 2: Specify Requirements
```
/speckit.specify Add multi-tenant support to myDbAssistant where:
- Multiple organizations can use the same instance
- Each tenant has isolated training data and vector storage
- Database connections are tenant-specific
- UI shows only tenant-specific data
- Admin can manage tenant configurations
```

#### Step 3: Create Implementation Plan
```
/speckit.plan Use the existing Vanna architecture:
- Extend ChromaDB_VectorStore to support tenant collections
- Update config.json files to include tenant_id
- Modify Flask UI to include tenant selector
- Use existing multiple inheritance pattern
- Maintain backward compatibility with single-tenant mode
```

#### Step 4: Generate Tasks
```
/speckit.tasks
```

#### Step 5: Optional - Clarify Ambiguities
```
/speckit.clarify Focus on:
- How should tenant isolation work in ChromaDB?
- What authentication mechanism for tenant switching?
- Migration path for existing single-tenant deployments?
```

#### Step 6: Optional - Analyze Consistency
```
/speckit.analyze
```

#### Step 7: Implement
```
/speckit.implement
```

## 🔧 Using Spec-Kit CLI

### Check Installation
```bash
specify check
```

### Create New Feature Branch
The spec-kit workflow works best with Git feature branches:

```bash
# Spec-kit automatically detects your feature from branch name
git checkout -b feature/multi-tenant-support
```

### Manual Feature Creation (Non-Git)
If not using Git branches, set the feature environment variable:

```bash
export SPECIFY_FEATURE="001-multi-tenant-support"
```

## 📁 Directory Structure

After initialization, your project has:

```
vanna/
├── .github/
│   ├── prompts/                    # Spec-kit slash command definitions
│   │   ├── speckit.constitution.prompt.md
│   │   ├── speckit.specify.prompt.md
│   │   ├── speckit.plan.prompt.md
│   │   ├── speckit.tasks.prompt.md
│   │   ├── speckit.implement.prompt.md
│   │   ├── speckit.clarify.prompt.md
│   │   ├── speckit.analyze.prompt.md
│   │   └── speckit.checklist.prompt.md
│   └── copilot-instructions.md     # Your existing Vanna instructions
│
├── .specify/
│   ├── memory/                     # Persistent project memory
│   │   └── constitution.md         # Project principles (created by /speckit.constitution)
│   ├── templates/                  # Spec-kit templates
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   ├── checklist-template.md
│   │   └── agent-file-template.md
│   └── scripts/                    # Helper scripts
│       └── bash/
│           ├── create-new-feature.sh
│           ├── setup-plan.sh
│           ├── update-agent-context.sh
│           └── check-prerequisites.sh
│
└── specs/                          # Auto-created when you use spec-kit
    └── features/
        └── {feature-number}-{feature-name}/
            ├── spec.md             # Requirements (from /speckit.specify)
            ├── plan.md             # Implementation plan (from /speckit.plan)
            ├── tasks.md            # Task breakdown (from /speckit.tasks)
            ├── analysis.md         # Consistency analysis (from /speckit.analyze)
            └── checklist.md        # Quality checklist (from /speckit.checklist)
```

## 🎯 Best Practices for Vanna Development

### 1. Align with Vanna Architecture
When using `/speckit.plan`, always reference Vanna's patterns:
- Multiple inheritance (VectorStore first, then LLM)
- Method naming conventions (`get_`, `add_`, `generate_`, `run_`, `connect_`)
- Configuration via dict pattern
- Deterministic UUIDs for training data

### 2. Start with Constitution
Define project-specific principles once:
```
/speckit.constitution Focus on:
- Vanna's multiple inheritance architecture
- Method naming conventions from VannaBase
- Optional dependency handling
- Testing with tox
- Documentation in docstrings
```

### 3. Use Specs for Complex Features
Good candidates for spec-driven approach:
- New LLM provider implementations
- New vector store integrations
- Multi-database support enhancements
- UI/Flask improvements
- Training data management features

### 4. Keep Specs Version Controlled
The `.specify/memory/` directory contains project constitution - commit this:
```bash
git add .specify/memory/constitution.md
git commit -m "Add spec-kit constitution for Vanna project"
```

### 5. Review Generated Artifacts
Always review the generated specs before implementation:
- `specs/features/{feature}/spec.md` - Ensure requirements are complete
- `specs/features/{feature}/plan.md` - Verify architecture aligns with Vanna
- `specs/features/{feature}/tasks.md` - Check tasks are actionable

## 🔐 Security Considerations

### Protected Directories (Already in .gitignore)
- `.github/prompts/.env` - Don't commit environment secrets
- `.specify/memory/` - May contain sensitive project context

### API Keys and Credentials
Spec-kit commands don't require API keys, but your implementations might. Follow Vanna's pattern:
```python
def __init__(self, config=None):
    self.api_key = config.get('api_key', os.getenv('PROVIDER_API_KEY'))
```

## 📚 Advanced Usage

### Custom Checklist for Vanna
Create quality checklists specific to Vanna's requirements:

```
/speckit.checklist Generate checklist for adding new LLM provider:
- Inherits from VannaBase
- Implements all abstract methods (submit_prompt, system_message, user_message, assistant_message)
- Handles config dict properly
- Has optional dependency checking
- Includes test in tests/test_vanna.py
- Documented in README
- Exported in __init__.py
- Added to pyproject.toml optional-dependencies
```

### Parallel Implementation Exploration
Test multiple approaches using spec-kit:
```bash
# Branch 1: Approach A
git checkout -b feature/multi-tenant-chromadb
/speckit.plan Use ChromaDB collections for tenant isolation
/speckit.implement

# Branch 2: Approach B  
git checkout -b feature/multi-tenant-pgvector
/speckit.plan Use PgVector with tenant_id column for isolation
/speckit.implement

# Compare and choose best approach
```

### Integration with myDbAssistant
When working on myDbAssistant custom implementation:

```
/speckit.specify Enhance myDbAssistant settings UI to support:
- Multiple database profiles (dev/staging/prod)
- LLM model switching without restart
- Training data import/export
- ChromaDB backup/restore

/speckit.plan Use existing config_ui.py patterns:
- Add new tabs for profile management
- Extend ConfigLoader for profile support
- Update quick_start_flask_ui.py to load active profile
- Maintain backward compatibility with ui/config/*.json
```

## 🐛 Troubleshooting

### Slash Commands Not Working
1. Ensure GitHub Copilot is installed and active in VS Code
2. Check `.github/prompts/` directory exists with `.prompt.md` files
3. Restart VS Code to reload Copilot configuration

### "SPECIFY_FEATURE" Error
If you see errors about missing feature context:
```bash
# Option 1: Use Git branch (preferred)
git checkout -b feature/my-feature

# Option 2: Set environment variable
export SPECIFY_FEATURE="001-my-feature"
```

### Template Not Found
If templates are missing:
```bash
# Re-initialize (safe, uses --force)
specify init --here --ai copilot --force
```

### Conflicts with Existing Copilot Instructions
Spec-kit works alongside your existing `.github/copilot-instructions.md`. The slash commands are additive and won't interfere with Vanna-specific instructions.

## 📖 Learn More

- [Spec-Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Video Overview](https://www.youtube.com/watch?v=a9eR1xsfvHg)
- [Vanna Documentation](https://vanna.ai/docs)

## 🤝 Contributing with Spec-Kit

When contributing to Vanna using spec-kit:

1. Create feature branch: `git checkout -b feature/my-enhancement`
2. Use spec-kit workflow to develop feature
3. Include generated specs in PR: `specs/features/{feature}/`
4. Reference spec artifacts in PR description
5. Follow Vanna's PR guidelines in CONTRIBUTING.md

## 💡 Example: Adding Qdrant Integration

Complete example of using spec-kit to add a new vector store:

```bash
# 1. Create feature branch
git checkout -b feature/qdrant-vector-store

# 2. Define requirements
/speckit.specify Add Qdrant vector store integration to Vanna:
- Create src/vanna/qdrant/qdrant_vector.py
- Implement all VannaBase vector store methods
- Support Qdrant cloud and local deployment
- Use deterministic UUIDs for idempotent adds
- Handle embeddings as List[float]
- Support n_results configuration

# 3. Create plan
/speckit.plan Follow Vanna's patterns:
- Inherit from VannaBase
- Implement generate_embedding, add_*, get_*, remove_training_data
- Use qdrant-client library (optional dependency)
- Export in src/vanna/qdrant/__init__.py
- Add qdrant extra to pyproject.toml
- Create test in tests/test_vanna.py using multiple inheritance

# 4. Generate tasks
/speckit.tasks

# 5. Implement
/speckit.implement

# 6. Test
pytest tests/test_vanna.py::test_qdrant_integration
```

---

**Happy Spec-Driven Development!** 🚀

For questions or issues, open an issue on the [Vanna GitHub repository](https://github.com/vanna-ai/vanna).
