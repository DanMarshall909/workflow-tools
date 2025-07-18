# Git Workflow Quick Reference

## 🔀 Branch Naming

### Format
```
<type>/<ticket>-<description>
<type>/<description>
```

### Types
- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `release/` - Release preparation
- `chore/` - Maintenance tasks

### Examples
```bash
feature/JIRA-123-user-authentication
bugfix/fix-login-redirect
hotfix/payment-processing-error
release/v2.1.0
chore/update-dependencies
```

## 📝 Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (no logic change)
- `refactor` - Code restructuring
- `perf` - Performance improvement
- `test` - Adding tests
- `chore` - Maintenance

### Examples
```bash
feat(auth): add OAuth2 integration
fix(api): resolve timeout on large queries
docs(readme): update installation steps
refactor(users): simplify validation logic
```

### Breaking Changes
```
feat(api): change authentication endpoint

BREAKING CHANGE: Auth endpoint moved from /auth to /api/v2/auth
```

## 🔃 Pull Request Title

Same as commit format:
```
feat(shopping-cart): implement persistent cart
fix(ui): correct mobile navigation menu
```

## ⚡ Quick Commands

### Start Feature
```bash
git checkout -b feature/JIRA-123-feature-name
```

### Commit with Convention
```bash
git commit -m "feat(scope): add new feature"
```

### Squash Commits
```bash
git rebase -i HEAD~3
```

### Update from Main
```bash
git checkout main
git pull
git checkout feature/branch
git rebase main
```

## 📋 PR Description Template
```markdown
## Description
[What this PR does]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change

## Testing
- [ ] Unit tests pass
- [ ] Manual testing done

## Checklist
- [ ] Follows code style
- [ ] Tests added
- [ ] Docs updated
```

---
[Full Guides: [Commits](../git/commits/conventional-commits.md) | [Branches](../git/branches/branch-naming.md) | [PRs](../git/prs/pull-request-standards.md)]