# Workflow-Tools Rules Index

Quick navigation to find the right rules for your scenario.

## 🚀 Quick Start by Project Type

### Starting a New TypeScript/React Project
1. [TypeScript Code Quality Standards](typescript/code-quality/general-standards.md)
2. [ESLint Configuration](typescript/configs/eslint.config.js)
3. [Jest Test Naming](typescript/test-naming/jest-react-testing-library.md)
4. [Git Commit Standards](git/commits/conventional-commits.md)

### Starting a New C#/.NET Project
1. [.NET Code Quality Standards](csharp/code-quality/dotnet-standards.md)
2. [Code Analysis Ruleset](csharp/configs/dotnet.ruleset)
3. [xUnit Test Naming](csharp/test-naming/xunit-fluent-assertions.md)
4. [Branch Naming](git/branches/branch-naming.md)

### Starting a New Python Project
1. [Python Code Quality Standards](python/code-quality/general-standards.md)
2. [Pytest Test Naming](python/test-naming/pytest-unittest.md)
3. [Security Guidelines](generic/security/secure-development.md)
4. [PR Standards](git/prs/pull-request-standards.md)

## 📚 By Topic

### Test Naming Conventions
- **Universal Principles**: [Generic Test Naming](generic/test-naming/universal-principles.md)
- **TypeScript/Jest**: [Jest & React Testing Library](typescript/test-naming/jest-react-testing-library.md)
- **C#/xUnit**: [xUnit & FluentAssertions](csharp/test-naming/xunit-fluent-assertions.md)
- **Python/pytest**: [pytest & unittest](python/test-naming/pytest-unittest.md)

### Code Quality Standards
- **Clean Code**: [Universal Clean Code Principles](generic/code-quality/clean-code-principles.md)
- **TypeScript**: [TypeScript Standards](typescript/code-quality/general-standards.md)
- **C#/.NET**: [.NET Standards](csharp/code-quality/dotnet-standards.md)
- **Python**: [Python Standards](python/code-quality/general-standards.md)

### Security & Privacy
- **Security First**: [Secure Development](generic/security/secure-development.md)
- **OWASP Guidelines**: See security rules for OWASP Top 10 coverage
- **Privacy Patterns**: Integrated in all language-specific rules

### Git Workflow
- **Commits**: [Conventional Commits](git/commits/conventional-commits.md)
- **Branches**: [Branch Naming](git/branches/branch-naming.md)
- **Pull Requests**: [PR Standards](git/prs/pull-request-standards.md)

### Configuration Files
- **TypeScript**: [ESLint Config](typescript/configs/eslint.config.js)
- **C#**: [.NET Ruleset](csharp/configs/dotnet.ruleset)
- **Python**: Configuration files coming soon (#30)

## 🎯 By Goal

### "I want to improve test quality"
1. Start with [Universal Test Naming Principles](generic/test-naming/universal-principles.md)
2. Then see your language-specific guide:
   - [TypeScript](typescript/test-naming/jest-react-testing-library.md)
   - [C#](csharp/test-naming/xunit-fluent-assertions.md)
   - [Python](python/test-naming/pytest-unittest.md)

### "I need to set up code quality tools"
1. Check language-specific configurations:
   - TypeScript: [ESLint](typescript/configs/eslint.config.js)
   - C#: [Ruleset](csharp/configs/dotnet.ruleset)
2. Review [Clean Code Principles](generic/code-quality/clean-code-principles.md)

### "I want consistent git practices"
1. [Conventional Commits](git/commits/conventional-commits.md) for commit messages
2. [Branch Naming](git/branches/branch-naming.md) for branch organization
3. [PR Standards](git/prs/pull-request-standards.md) for code reviews

### "I need to improve security"
1. Read [Secure Development](generic/security/secure-development.md)
2. Apply language-specific security rules from code quality guides
3. Use security-focused linting configurations

## 🏷️ Tags

### By Language
- `#typescript` `#javascript` `#react` `#node`
- `#csharp` `#dotnet` `#aspnet`
- `#python` `#django` `#fastapi`
- `#generic` `#language-agnostic`

### By Topic
- `#testing` `#test-naming` `#tdd`
- `#code-quality` `#clean-code` `#solid`
- `#security` `#owasp` `#privacy`
- `#git` `#version-control` `#ci-cd`

### By Experience Level
- `#beginner-friendly`
- `#intermediate`
- `#advanced`
- `#team-lead`

## 🔄 Cross-References

### TypeScript Ecosystem
```
TypeScript Code Quality
    ├── Uses: Generic Clean Code Principles
    ├── Pairs with: ESLint Configuration
    ├── Tested by: Jest Test Naming
    └── Committed with: Conventional Commits
```

### C# Ecosystem
```
C# Code Quality
    ├── Based on: Generic Clean Code + SOLID
    ├── Enforced by: .NET Ruleset
    ├── Tested with: xUnit Patterns
    └── Reviewed via: PR Standards
```

### Python Ecosystem
```
Python Code Quality
    ├── Follows: Generic Security Principles
    ├── Will use: Pre-commit configs (#30)
    ├── Tests with: pytest Patterns
    └── Deployed via: CI/CD Templates (#34)
```

## 🎓 Learning Paths

### Junior Developer Path
1. [Universal Test Naming](generic/test-naming/universal-principles.md)
2. [Clean Code Principles](generic/code-quality/clean-code-principles.md)
3. Language-specific code quality guide
4. [Conventional Commits](git/commits/conventional-commits.md)

### Senior Developer Path
1. [Security-First Development](generic/security/secure-development.md)
2. Advanced patterns in language guides
3. [PR Standards](git/prs/pull-request-standards.md) for mentoring
4. Configuration tuning guides

### Team Lead Path
1. All git workflow standards
2. Security and privacy guidelines
3. Configuration templates for team standards
4. PR review best practices

## 🔍 Search Helper

Looking for rules about...

- **Naming things?** → Check test naming and code quality guides
- **Git workflows?** → See git/ directory
- **Security?** → Start with generic/security/
- **Testing?** → See test-naming/ in your language
- **Code style?** → Check code-quality/ guides
- **Tool configuration?** → Look in configs/ directories

## 📈 Adoption Checklist

For teams adopting workflow-tools:

- [ ] Choose your primary language guides
- [ ] Install recommended configurations
- [ ] Read and share test naming principles
- [ ] Adopt git workflow standards
- [ ] Review security guidelines
- [ ] Set up PR templates
- [ ] Configure IDE/editor
- [ ] Run team training session

## 🚧 Coming Soon

- Go language support (#31)
- API design standards (#32)
- Database guidelines (#33)
- CI/CD templates (#34)
- Quickstart guides (#35)
- IDE integrations (#36)

---

> 💡 **Tip**: Use Ctrl+F (Cmd+F on Mac) to search this page for specific topics or technologies.