# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a collection of workflow automation tools and utilities designed to streamline development and operational processes.

## Development Guidelines

Following development standards from DanMarshall909/Anchor:

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

- `/tools/` - Individual workflow automation tools
- `/scripts/` - Shared utility scripts
- `/docs/` - Documentation for tools and workflows
- Each tool should be self-contained with clear documentation

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