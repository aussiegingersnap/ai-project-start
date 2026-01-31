# AI Project Starter

A template for AI-assisted projects using Cursor's native skills discovery. Fork this to start new projects with structured rules, skills, and workflow.

## Quick Start

```bash
# Clone this template
git clone https://github.com/aussiegingersnap/ai-project-start.git my-project
cd my-project

# Install runtimes (requires mise)
mise install

# Open in Cursor and start a chat
# The /project-setup skill will guide you through configuration
```

When you open a fresh project, Cursor detects the unconfigured `project.mdc` and triggers the setup flow. Answer a few questions about your tech stack, and you're ready to build.

## What's Included

### Native Skills (Cursor 2.4+)

Skills live in `.cursor/skills/` and are automatically discovered by Cursor. No server setup required.

| Skill | Purpose |
|-------|---------|
| `project-setup` | Interactive onboarding for new projects |
| `feature-build` | Complete feature development lifecycle |

### Minimal Rules

| Rule | Purpose |
|------|---------|
| `main_rule.mdc` | Role detection + skills invocation |
| `project.mdc` | Project constraints (configured during setup) |

### Workflow Files

| File | Purpose |
|------|---------|
| `TASKS.md` | Sprint backlog → Cursor plans |
| `CHANGELOG.md` | Keep a Changelog format |
| `docs/architecture.md` | Technical patterns + decisions |

### Dev Environment

| File | Purpose |
|------|---------|
| `.mise.toml` | Pinned Node.js + Python versions |
| `.env.example` | Environment variable template |
| `lefthook.yml` | Git hooks for commit validation |

## Directory Structure

```
project/
├── .cursor/
│   ├── rules/
│   │   ├── main_rule.mdc      # Role detection + skills
│   │   └── project.mdc        # Project constraints (EDIT THIS)
│   └── skills/
│       ├── feature-build/     # Feature development workflow
│       └── project-setup/     # Onboarding flow
├── .env.example
├── .gitignore
├── .mise.toml
├── CHANGELOG.md
├── README.md
├── TASKS.md
├── lefthook.yml
└── docs/
    └── architecture.md
```

## Importing Skills

### From Cursor Settings (Recommended)

1. Open Cursor Settings (`Cmd+Shift+J`)
2. Go to the **Rules** tab
3. Click **Add Rule** → **Remote Rule (GitHub)**
4. Enter: `https://github.com/aussiegingersnap/cursor-skills`
5. Select the skills you want to import

Skills are copied to your `.cursor/skills/` directory and automatically discovered.

### Manual Copy

```bash
# Clone cursor-skills and copy what you need
git clone https://github.com/aussiegingersnap/cursor-skills /tmp/cursor-skills
cp -r /tmp/cursor-skills/skills/design-system .cursor/skills/
```

### Available Skills

Browse the [cursor-skills repo](https://github.com/aussiegingersnap/cursor-skills) for available skills:

| Skill | Description |
|-------|-------------|
| `design-system` | Linear/Notion-inspired UI patterns |
| `db-postgres` | PostgreSQL with Drizzle ORM |
| `db-prisma` | PostgreSQL with Prisma ORM |
| `nextjs-16` | Next.js 16 App Router patterns |
| `effector` | Effector state management |
| `docker-local` | Local Docker development |
| `linear` | Linear issue tracking |
| `api-rest` | REST API conventions |

## Project Setup Flow

When you open a fresh clone, the `/project-setup` skill guides you through:

1. **Project info** - Name and description
2. **Tech stack** - Framework, database, auth, deployment
3. **Skill recommendations** - Based on your choices
4. **Configuration** - Updates `project.mdc` with your answers

To manually trigger setup:
```
/project-setup
```

## Workflow

```
Task in TASKS.md → Create Cursor Plan → Execute → Update CHANGELOG.md
```

1. Add task to `TASKS.md` Current Sprint
2. Create Cursor plan for complex tasks (or use `/feature-build`)
3. Execute the work
4. Log changes in `CHANGELOG.md` under `[Unreleased]`
5. Check off task, move to Completed

### Using Feature Build

The `/feature-build` skill orchestrates the complete development lifecycle:

1. **Task Selection** - Define acceptance criteria
2. **Component Design** - Build components in style guide
3. **Build Loop** - Implement with browser testing
4. **Analytics** - Add tracking if needed
5. **Commit & Document** - Update docs and commit

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

- [Cursor](https://cursor.sh/) 2.4+ (native skills support)
- [mise](https://mise.jdx.dev/) for runtime management
- Node.js 20+ (for typical web projects)

## License

MIT
