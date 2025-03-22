# Cursor AI Project Template

An opinionated template that combines structured rule systems with AI assistance to produce high-quality, consistent code faster.

## Overview

This template supercharges Cursor AI with domain-specific rule files that guide AI behavior across development disciplines:

- Domain-specific rule files in modular `.mdc` format
- Separate technical and business rules for cross-functional teams
- Pre-built tools for common operations
- Consistent file organization patterns

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

```
project-template/
├── .cursor/                # AI configuration
│   └── rules/              # Rule definition files
├── docs/                   # Documentation & guides
├── assets/                 # Media, images, resources
├── templates/              # Reusable document templates
├── reports/                # Generated reports & analysis
├── archive/               # Archived or completed work
├── README.md              # Developer documentation
└── START-HERE.md          # Non-technical guide
```

## Best Practices

1. **Follow patterns** - Maintain consistency with existing rules
2. **Document changes** - Comment modifications in rule files
3. **Test combinations** - Rules can interact in complex ways
4. **Be specific** - Avoid ambiguity between rules
5. **Consider all users** - Support both technical and non-technical teams

## For Non-developers

Direct non-technical team members to `START-HERE.md` for a simplified guide.

## License

[Insert your license here] 