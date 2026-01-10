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
```

**Import skills you need:**
```
Browse available skills from trusted sources
Import design-principles and skill-creator
```

This template starts minimal - no skills baked in. Import what you need from trusted sources.

## What's Included

### Skills Framework
- **MCP Server** (`mcp/skills_mcp.py`) - Enables Cursor to discover and invoke specialized skills
- **Skills Directory** (`skills/`) - Add project-specific or reusable skills here
- **Orchestrator Pattern** - AI checks for relevant skills before solving tasks directly
- **Trusted Sources** (`skill_sources.yaml`) - Browse and import skills from curated repos

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
├── skill_sources.yaml     # Trusted skill repos
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
3. In Cursor: Settings → Tools and MCP → Verify "cursor-skills" shows 7 tools

## Importing Skills

### From Trusted Sources (Recommended)

The `skill_sources.yaml` file defines trusted repositories for browsing and importing skills.

**1. Browse available skills:**
```
Show me available skills from my trusted sources
```

This calls `browse_skills()` and shows all skills organized by source with author attribution:

```
# Available Skills from Trusted Sources

## cursor-skills (by @aussiegingersnap)
_Jason's curated skills collection_
  - design-principles: Enforce minimal design system...
  - repo-review: GitHub repository analysis...
  
## anthropic-skills (by @anthropic)
_Official Anthropic skills from Claude team_
  - artifacts-builder: Build HTML artifacts with React...
  - skill-creator: Tools for creating new skills...
```

**2. Import specific skills:**
```
Import the design-principles and skill-creator skills
```

This calls `import_skills(["design-principles", "skill-creator"])` and downloads only what you need.

**3. Browse a specific source:**
```
Show me skills from anthropic-skills
```

### From Any GitHub URL

For one-off imports from untrusted sources:
```
import_skill("https://github.com/someone/repo/tree/main/my-skill")
```

### Adding Trusted Sources

Edit `skill_sources.yaml` to add your own trusted repos:

```yaml
sources:
  my-team-skills:
    url: https://github.com/my-org/cursor-skills
    description: "Team-specific skills"
    author: my-org
    path: skills  # subdirectory containing skills
```

## MCP Tools Reference

| Tool | Description |
|------|-------------|
| `list_skills()` | List locally installed skills |
| `invoke_skill(name)` | Load a skill's full instructions |
| `list_skill_sources()` | Show configured trusted sources |
| `browse_skills(source?)` | Browse available skills from sources (with author info) |
| `import_skills(names, source?)` | Import specific skills from trusted sources |
| `import_skill(url)` | Import from any GitHub URL |
| `find_skill()` | Browse community skills directory |

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

### 3. Configure Trusted Sources

Edit `skill_sources.yaml` with repositories you trust.

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
