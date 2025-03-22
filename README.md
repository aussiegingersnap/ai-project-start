# Cursor AI Project Template

An opinionated template that combines structured rule systems with AI assistance to produce high-quality, consistent code faster.

## Overview

This template supercharges Cursor AI with domain-specific rule files that guide AI behavior across development disciplines:

- Domain-specific rule files in modular `.mdc` format
- Separate technical and business rules for cross-functional teams
- Pre-built tools for common operations
- Just-in-time file organization

## Quick Setup

```bash
# Clone this template
git clone https://github.com/aussiegingersnap/ai-project-start.git my-project

# Navigate to project
cd my-project

# Optional: Initialize package
npm init -y  # or yarn init -y
```

## Rule System Architecture

The template uses structured rule files in `.cursor/rules/`:

### Development Rules

- `development.mdc` - Core development principles and coding standards
- `backend.mdc` - Server architecture, security, middleware patterns
- `frontend.mdc` - UI components, state management, accessibility
- `database.mdc` - Data modeling, query optimization, migrations
- `api.mdc` - RESTful design, versioning, documentation
- `infrastructure.mdc` - Deployment, scaling, monitoring

### Business Rules

- `operations.mdc` - Project management, documentation, workflows
- `marketing.mdc` - Content creation, campaigns, analytics
- `data_analytics.mdc` - Reports, visualizations, insights
- `document_management.mdc` - File organization, versioning
- `business_tools.mdc` - CLI commands for non-technical users

## Usage

### Invoking Rules

Rules activate contextually based on your query or can be explicitly invoked:

```
Using the frontend rules, create a responsive navigation component.
```

### Extending the System

To customize rules:

1. Edit existing `.mdc` files in `.cursor/rules/`
2. Add new `.mdc` files for additional domains
3. Reference new rule files in `user-rules-v2`

### Business Tools

For non-developers, `business_tools.mdc` contains ready-to-use CLI commands implemented in the `/tools` directory.

To add new tools:

1. Implement in `/tools` directory
2. Document in `business_tools.mdc`
3. Follow established command patterns

## Directory Structure

The project starts minimal and grows as needed:

```
project-template/
├── .cursor/                # AI configuration
│   └── rules/              # Rule definition files
├── README.md              # Developer documentation
└── START-HERE.md          # Non-technical guide
```

### Just-in-Time Folders

Create these folders only when you need them:

- `docs/` - When you have documentation to maintain
- `assets/` - When you have media files to manage
- `templates/` - When you have reusable formats
- `archive/` - When you need to store old versions

This approach keeps your project lean and organized. Create folders when you have actual content for them, not before.

## Best Practices

1. **Start minimal** - Only create folders when you need them
2. **Stay organized** - Use clear, descriptive folder names
3. **Archive don't delete** - Move old work to archive instead of deleting
4. **Be consistent** - Once you create a folder, stick to its purpose
5. **Keep it flat** - Avoid deep folder nesting when possible

## For Non-developers

Direct non-technical team members to `START-HERE.md` for a simplified guide.

## License

[Insert your license here] 