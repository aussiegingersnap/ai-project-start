# AI Project Starter

A boilerplate for AI-assisted projects using the skills framework pattern. Fork this to start new projects with structured rules, skills, and workflow.

## Quick Start

```bash
# Clone this template
git clone https://github.com/aussiegingersnap/ai-project-start.git my-project
cd my-project

# Install runtimes (requires mise)
mise install

# Update project.mdc with your project details
# Then start building!
```

## What's Included

### Skills Framework
- **MCP Server** (`mcp/skills_mcp.py`) - Enables Cursor to discover and invoke specialized skills
- **Skills Directory** (`skills/`) - Add project-specific or reusable skills here
- **Orchestrator Pattern** - AI checks for relevant skills before solving tasks directly

### Minimal Rules
- `main_rule.mdc` - Skills orchestrator + pair programmer roles
- `project.mdc` - Project-specific constraints (customize this!)

### Workflow
- `TASKS.md` - Sprint backlog → Cursor plans
- `CHANGELOG.md` - Keep a Changelog format
- `lefthook.yml` - Git hooks for commit validation + secret detection

### Dev Environment
- `.mise.toml` - Pinned Node.js + Python versions
- `.env.example` - Environment variable template
- `.gitignore` - Comprehensive ignore patterns

## Directory Structure

```
project/
├── .cursor/
│   ├── mcp.json           # Skills server config
│   └── rules/
│       ├── main_rule.mdc  # Orchestrator roles
│       └── project.mdc    # Project constraints (EDIT THIS)
├── .env.example           # Env template
├── .gitignore
├── .mise.toml             # Runtime versions
├── CHANGELOG.md           # Progress log
├── README.md
├── TASKS.md               # Sprint + backlog
├── lefthook.yml           # Git hooks
├── docs/
│   └── architecture.md    # Technical patterns (add as needed)
├── mcp/
│   └── skills_mcp.py      # Skills MCP server
└── skills/                # Add skills here
    └── .gitkeep
```

## Setup Cursor MCP

1. Open `.cursor/mcp.json`
2. Update the path to your project's `mcp/skills_mcp.py`
3. In Cursor: Settings → Tools and MCP → Verify "cursor-skills" shows 4 tools

## Customizing

### 1. Update `project.mdc`

Replace the template content with your project's:
- Name and description
- Tech stack
- Core constraints
- Documentation links

### 2. Add Skills

Create skills in `skills/` directory:
```
skills/
└── my-skill/
    ├── SKILL.md           # Instructions (required)
    └── scripts/           # Helper scripts (optional)
```

### 3. Import Community Skills

Use the MCP tools to import skills:
```
import_skill("https://github.com/anthropics/skills/tree/main/skill-name")
```

## Workflow

```
Task in TASKS.md → Create Cursor Plan → Execute → Update CHANGELOG.md
```

1. Add task to `TASKS.md` Current Sprint
2. Create Cursor plan for complex tasks
3. Execute the work
4. Log changes in `CHANGELOG.md` under `[Unreleased]`
5. Check off task, move to Completed

## Git Standards

**Conventional Commits**: `<type>(<scope>): <subject>`

```bash
# After completing work, Cursor provides commands like:
gaa && gcmsg "feat(api): add user endpoints"
gp
```

Lefthook validates:
- ✅ Conventional commit format
- ✅ No secrets in commits
- ✅ No .env files committed

## Requirements

- [Cursor](https://cursor.sh/) with MCP enabled
- [mise](https://mise.jdx.dev/) for runtime management
- [uv](https://github.com/astral-sh/uv) for Python (skills server)
- Node.js 20+ (for typical web projects)
- Python 3.10+ (for skills MCP server)

## License

MIT
