# Conventional Commit Guidelines

## Why Conventional Commits?

Conventional commits provide a structured way to write commit messages that:
- Enable automatic versioning (semantic release)
- Generate changelogs automatically
- Make commit history readable and searchable
- Communicate intent clearly to team members

## Basic Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required Elements
- **type**: The category of change
- **subject**: Brief description (50 chars max)

### Optional Elements
- **scope**: The area of code affected
- **body**: Detailed explanation
- **footer**: Breaking changes, issue references

## Commit Types

### Feature Development
```
feat: add user authentication via OAuth
feat(auth): implement Google OAuth integration
feat(api): add pagination to task endpoints
```

### Bug Fixes
```
fix: prevent crash when user email is null
fix(session): restore timer state after page refresh
fix(ui): correct button alignment on mobile devices
```

### Documentation
```
docs: update API authentication examples
docs(readme): add installation troubleshooting section
docs(api): clarify rate limiting behavior
```

### Code Style (No Production Changes)
```
style: format code according to new prettier config
style(components): apply consistent spacing
style: remove trailing whitespace
```

### Refactoring (No Feature Changes)
```
refactor: extract email validation to utility function
refactor(auth): simplify token refresh logic
refactor(database): optimize user query performance
```

### Performance Improvements
```
perf: lazy load images on dashboard
perf(api): add caching to frequently accessed endpoints
perf(search): implement database indexing
```

### Tests
```
test: add integration tests for payment flow
test(auth): verify OAuth error handling
test: increase coverage for user service
```

### Build/CI Changes
```
build: update webpack to version 5
build(docker): optimize container size
ci: add automated security scanning
```

### Chores (Maintenance)
```
chore: update dependencies
chore(deps): bump typescript to 5.0
chore: remove deprecated API endpoints
```

## Writing Good Commit Messages

### Subject Line Rules

**DO:**
- Use imperative mood ("add" not "added" or "adds")
- Capitalize first letter
- No period at the end
- Limit to 50 characters
- Be specific and meaningful

**DON'T:**
- Use past tense ("added feature")
- Be vague ("fix bug", "update code")
- Include issue numbers in subject (put in footer)

### Examples: Good vs Bad

```
❌ BAD:
- Fixed bug
- Updated stuff
- Changes
- fixing the login bug where users couldn't...

✅ GOOD:
- fix: prevent duplicate user registration
- feat: add password strength indicator
- refactor: simplify error handling logic
- perf: reduce bundle size by 30%
```

### Body Guidelines

Use the body to explain:
- **What** changed
- **Why** it changed
- **How** it affects users

```
feat(auth): add two-factor authentication

Implement TOTP-based 2FA to enhance account security. Users can now:
- Enable 2FA in account settings
- Use authenticator apps like Google Authenticator
- Generate backup codes for recovery

This addresses increasing security requirements and user requests
for additional account protection.
```

### Breaking Changes

Mark breaking changes clearly:

```
feat(api): restructure authentication endpoints

BREAKING CHANGE: Authentication endpoints have moved from /auth/* to /api/v2/auth/*.
Applications using the old endpoints must update their API calls.

Migration guide: docs/migration/v2-auth.md
```

## Scope Guidelines

Scope should indicate the area of code affected:

### Common Scopes by Project Type

**Frontend:**
- `ui`: Visual components
- `auth`: Authentication
- `routing`: Navigation
- `state`: State management
- `api`: API integration

**Backend:**
- `api`: REST/GraphQL endpoints
- `db`: Database changes
- `auth`: Authentication/authorization
- `queue`: Message queue
- `cache`: Caching layer

**Full-Stack:**
- `client`: Frontend changes
- `server`: Backend changes
- `shared`: Common code
- `config`: Configuration
- `docs`: Documentation

## Multi-Line Commits

For complex changes:

```
feat(shopping-cart): implement cart persistence across sessions

Previously, cart contents were lost on page refresh. This commit adds:
- LocalStorage integration for cart state
- Session recovery on app initialization  
- Automatic sync with backend every 30 seconds
- Cleanup of expired cart data after 7 days

Technical details:
- New CartPersistence service handles storage
- Added migration for existing users
- Backwards compatible with old cart format

Closes #234, Closes #189
```

## Commit Message Templates

### Feature with Tests
```
feat(<scope>): <what you added>

- Add <specific feature>
- Include unit tests for <components>
- Update documentation

Tested on: <browsers/platforms>
```

### Bug Fix with Root Cause
```
fix(<scope>): <what was broken>

Root cause: <explanation>
Solution: <what you did>

This prevents <issue> when <condition>.

Fixes #<issue-number>
```

### Performance Improvement
```
perf(<scope>): <what you optimized>

Benchmark results:
- Before: <metric>
- After: <metric>
- Improvement: <percentage>

Changes made:
- <optimization 1>
- <optimization 2>
```

## Automation Benefits

With conventional commits, you can:

### Generate Changelogs
```markdown
## [2.1.0] - 2024-01-20

### Features
- **auth**: add two-factor authentication
- **ui**: implement dark mode toggle

### Bug Fixes
- **api**: prevent null reference in user lookup
- **session**: fix timer persistence bug

### Performance
- **search**: optimize database queries (50% faster)
```

### Automatic Versioning
- `feat`: Minor version bump (1.0.0 → 1.1.0)
- `fix`: Patch version bump (1.0.0 → 1.0.1)
- `BREAKING CHANGE`: Major version bump (1.0.0 → 2.0.0)

### Trigger CI/CD Actions
```yaml
# Deploy only on feature commits
if: contains(github.event.head_commit.message, 'feat:')
```

## Team Agreements

### Commit Frequency
- Commit logical units of work
- Don't commit broken code
- Prefer smaller, focused commits
- Commit at least daily

### Co-authored Commits
```
feat: implement pair programming feature

Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

### Referencing Issues
```
feat: add CSV export functionality

Implements data export feature requested by accounting team.
Supports filtering by date range and account type.

Closes #456
See-also: #444, #445
```

## Quick Reference

| Type | Description | Version Bump |
|------|-------------|--------------|
| feat | New feature | Minor |
| fix | Bug fix | Patch |
| docs | Documentation only | None |
| style | Code style | None |
| refactor | Code change that neither fixes a bug nor adds a feature | None |
| perf | Performance improvement | Patch |
| test | Adding tests | None |
| build | Build system | None |
| ci | CI configuration | None |
| chore | Other changes | None |
| revert | Revert previous commit | Varies |

## Git Hooks

### Commit Message Validation
```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Expected: <type>(<scope>): <subject>"
    exit 1
fi
```

## Remember

> Good commit messages are a gift to your future self and your teammates.

Write commits as if the person reading them knows nothing about the context - because in 6 months, that person might be you!

## References
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)