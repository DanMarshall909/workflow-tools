# Development Rules and Standards

This directory contains targeted, platform-specific rules and standards designed to minimize context loading while maximizing code quality and consistency.

## 📁 Structure

```
rules/
├── typescript/          # TypeScript/JavaScript/React
│   ├── test-naming/     # Jest, React Testing Library patterns
│   ├── code-quality/    # ESLint rules, TypeScript standards
│   └── configs/         # Ready-to-use ESLint configurations
├── csharp/              # C#/.NET
│   ├── test-naming/     # xUnit, FluentAssertions patterns
│   ├── code-quality/    # .NET analyzers, clean architecture
│   └── configs/         # Ruleset files, analyzer configs
├── python/              # Python
│   ├── test-naming/     # pytest, unittest patterns
│   ├── code-quality/    # Type hints, async patterns
│   └── configs/         # (Pre-commit configs coming soon)
├── generic/             # Cross-platform principles
│   ├── test-naming/     # Universal test naming principles
│   ├── code-quality/    # Clean code, SOLID principles
│   └── security/        # Security-first development
└── git/                 # Version control workflows
    ├── commits/         # Conventional commit standards
    ├── branches/        # Branch naming conventions
    └── prs/            # Pull request guidelines
```

## 🎯 Purpose

These rules are designed to be:
- **Minimal Context**: Load only what you need for the current task
- **Practical**: Based on real-world patterns from production projects
- **Actionable**: Include examples and ready-to-use configurations
- **Universal**: Applicable across different project types

## 🧭 Navigation

- **[INDEX.md](INDEX.md)** - Find rules by scenario
- **[TAGS.md](TAGS.md)** - Browse by technology or topic
- **[Quick Reference Cards](quickref/)** - Cheat sheets for common tasks
- **[Decision Records](decisions/)** - Why we chose these standards

## 🚀 Quick Start

### For TypeScript/React Projects
```bash
# Test naming rules
cat rules/typescript/test-naming/jest-react-testing-library.md

# ESLint configuration
cp rules/typescript/configs/eslint.config.js .eslintrc.js
```

### For C#/.NET Projects
```bash
# Test naming patterns
cat rules/csharp/test-naming/xunit-fluent-assertions.md

# Code analysis ruleset
cp rules/csharp/configs/dotnet.ruleset .ruleset
```

### For Python Projects
```bash
# Test naming guidelines
cat rules/python/test-naming/pytest-unittest.md

# Code quality standards
cat rules/python/code-quality/general-standards.md
```

## 📚 Key Principles

### Test Naming (All Platforms)
- **Focus on business behavior**, not implementation
- **Ban "should" language** - describe what IS, not what SHOULD BE
- **Use domain language** that stakeholders understand
- Based on [Enterprise Craftsmanship](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)

### Code Quality
- **Privacy-first**: Never log sensitive data
- **ADHD-friendly**: Small functions, clear names, minimal complexity
- **Security by default**: Input validation, output encoding, principle of least privilege
- **Performance conscious**: Measure before optimizing

### Git Workflow
- **Conventional commits** for automated versioning
- **Meaningful branch names** for CI/CD automation
- **Comprehensive PRs** for knowledge sharing

## 🔧 Integration

### With Claude Code
```markdown
# In your project's CLAUDE.md, reference specific rules:
For test naming conventions, see:
- workflow-tools/rules/typescript/test-naming/jest-react-testing-library.md

For code quality standards, see:
- workflow-tools/rules/typescript/code-quality/general-standards.md
```

### With CI/CD
```yaml
# Use branch naming for automation
on:
  push:
    branches:
      - 'feature/**'  # Auto-deploy to staging
      - 'hotfix/**'   # Fast-track to production
```

### With Code Reviews
Reference specific rules in PR comments:
```
Per our TypeScript standards (rules/typescript/code-quality/general-standards.md#functions-should-be-small), 
this function exceeds our 50-line guideline. Consider breaking it into smaller, focused functions.
```

## 📋 Checklists

### Before Committing Code
- [ ] Tests follow business-focused naming patterns
- [ ] Functions are small and focused (< 50 lines)
- [ ] No sensitive data in logs or comments
- [ ] All inputs validated, outputs encoded
- [ ] Error messages don't leak system details

### Before Opening PR
- [ ] Branch name follows conventions
- [ ] Commit messages use conventional format
- [ ] PR description uses template
- [ ] Self-review completed
- [ ] Tests cover new functionality

## 🤝 Contributing

To add new rules or improve existing ones:

1. Keep rules focused and single-purpose
2. Include real-world examples
3. Provide both good and bad patterns
4. Link to authoritative sources
5. Consider ADHD-friendly formatting

## 🔄 Recent Additions

- **Navigation System**: INDEX.md and TAGS.md for easy rule discovery
- **Quick Reference Cards**: Cheat sheets for test naming, git workflow, clean code, and security
- **Decision Records**: Explanations for why we chose these standards
- **Cross-References**: "See Also" sections in all rule files

## 📖 References

- [Clean Code - Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Enterprise Craftsmanship Blog](https://enterprisecraftsmanship.com/)

---

> "Good rules liberate creativity by removing ambiguity." - Unknown

These rules are living documents. Update them as your team learns and grows!