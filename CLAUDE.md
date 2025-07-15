# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository provides a comprehensive collection of workflow automation tools and utilities designed for global use across development projects. While initially extracted from patterns developed in the Anchor project, these tools are built to be universally applicable for any development team seeking robust automation, quality gates, and productivity workflows.

**Key Goals:**
- **Universal Applicability**: Works with any tech stack and project structure
- **Quality-First Development**: Enforces TDD, coverage, and quality standards
- **Developer Productivity**: Automates repetitive tasks and ensures consistency
- **Open Source Community**: Shareable patterns and best practices

## Development Guidelines

Based on proven patterns from the Anchor project, these guidelines ensure quality and consistency:

### Test-Driven Development (MANDATORY)
- **Red-Green-Refactor-Cover-Commit cycle**: Write failing test, implement minimal code, refactor, ensure coverage, commit
- **ONE TEST AT A TIME**: Never write multiple tests simultaneously
- **95% branch coverage** required for all commits
- **Business-focused test naming**: Focus on scenarios, not technical implementation
  - ❌ BAD: "should return data when API succeeds"
  - ✅ GOOD: "user can view their data"

### Code Quality Standards
- **Privacy-first**: All data processing should be local-first when possible
- **Clean Architecture**: SOLID principles, separation of concerns
- **Functional Programming**: Pure functions, immutable state where applicable
- **Performance**: Consider optimization for production use

### Git Workflow
- Work on feature branches for new tools
- Use descriptive commit messages following conventional commits
- All commits must pass quality gates (tests, linting, coverage)
- Create PRs for all changes, no direct commits to main

## Project Structure

This repository will be integrated as a submodule and should contain:

- `/scripts/` - Core development workflow scripts (TDD, CI, quality gates)
- `/tools/` - Standalone automation utilities 
- `/templates/` - Project templates and boilerplate generators
- `/docs/` - Documentation for tools and workflows
- `/config/` - Shared configuration files and standards

### Design Principles
- Each tool should be self-contained and language-agnostic where possible
- Focus on maximum reusability across different projects and tech stacks
- Provide sensible defaults with easy customization options
- Clear documentation and examples for adoption by other teams

## GitHub Integration

- Repository: https://github.com/DanMarshall909/workflow-tools.git
- Project Board: https://github.com/users/DanMarshall909/projects/3/views/1
- Create issues for new tools with clear acceptance criteria
- Link commits to project board issues for tracking

## Common Development Commands

Since this is a multi-language repository, commands will vary by technology:

### Node.js Tools
```bash
npm install          # Install dependencies
npm test            # Run tests
npm run lint        # Code quality check
npm run format      # Code formatting
```

### Python Tools
```bash
pip install -r requirements.txt  # Install dependencies
pytest                           # Run tests
black .                         # Code formatting
flake8                          # Linting
```

### Shell Scripts
```bash
shellcheck script.sh   # Shell script linting
```

## Tool Development Guidelines

### New Tool Checklist
- [ ] Clear purpose and usage documentation
- [ ] Comprehensive test coverage (95%+)
- [ ] Error handling and user feedback
- [ ] Configuration validation
- [ ] Privacy considerations addressed
- [ ] Performance impact assessed

### Documentation Requirements
- README.md for each tool explaining purpose, usage, examples
- Inline code comments for complex logic
- Configuration schema documentation
- Troubleshooting section for common issues

## Submodule Integration

### Usage as Submodule
This repository is designed to be included as a git submodule in other projects:

```bash
# Add as submodule
git submodule add https://github.com/DanMarshall909/workflow-tools.git workflow-tools

# Use scripts from parent project
./workflow-tools/scripts/tdd-cycle.sh

# Use tools from parent project
./workflow-tools/tools/quality-gate/run.sh
```

### Integration Requirements
- All scripts must work regardless of parent project structure
- Use relative paths and environment detection
- Provide configuration override mechanisms
- Support multiple integration patterns (submodule, direct clone, package manager)
- Comprehensive documentation for setup and customization