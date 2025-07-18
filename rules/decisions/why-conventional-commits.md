# Decision Record: Conventional Commits

## Status
Accepted

## Context
Git commit messages are often inconsistent across projects and developers, making it difficult to:
- Understand change history
- Generate automated changelogs
- Trigger automated workflows
- Determine version bumps

Common anti-patterns include:
- Vague messages: "fix bug", "update code", "changes"
- Inconsistent format across team members
- No connection between commit type and version impact
- Difficulty searching commit history

## Decision
We adopt the Conventional Commits specification for all commit messages.

## Rationale

### 1. Automation Enablement
Conventional commits enable powerful automation:
- **Semantic versioning**: `feat` → minor, `fix` → patch, `BREAKING CHANGE` → major
- **Changelog generation**: Automated, categorized changelogs
- **CI/CD triggers**: Deploy features vs fixes differently
- **Release notes**: Automatic generation for stakeholders

### 2. Improved Communication
Structured commits communicate intent clearly:
```
feat(auth): add two-factor authentication
^    ^       ^
|    |       |__ Clear, imperative description
|    |__ Scope for context
|__ Type indicates impact
```

### 3. Searchable History
Finding specific changes becomes trivial:
```bash
# Find all security-related features
git log --grep="^feat.*auth"

# Find all performance improvements
git log --grep="^perf"

# Find all breaking changes
git log --grep="BREAKING CHANGE"
```

### 4. Team Consistency
A standard format ensures everyone communicates changes the same way, reducing cognitive load when reviewing history.

### 5. Tool Ecosystem
Wide tool support:
- Commitizen for guided commit creation
- Husky for commit validation
- Standard-version for versioning
- Semantic-release for automated releases

## Consequences

### Positive
- Automated versioning and changelog generation
- Clear communication of change impact
- Searchable, parseable commit history
- Improved release management
- Better integration with CI/CD
- Forced thought about change categorization

### Negative
- Learning curve for developers
- Slightly more time per commit
- Requires discipline and enforcement
- Some commits hard to categorize

## Implementation

### Commit Types
- `feat`: New feature (minor version)
- `fix`: Bug fix (patch version)
- `docs`: Documentation only
- `style`: Code style (no logic change)
- `refactor`: Code change that neither fixes nor adds feature
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

#### Feature with Scope
```
feat(shopping-cart): add item quantity adjustment

Users can now increase/decrease item quantities directly
in the cart without removing and re-adding items.
```

#### Breaking Change
```
feat(api): restructure authentication endpoints

BREAKING CHANGE: Authentication endpoints have moved from 
/auth/* to /api/v2/auth/*. Update your API calls accordingly.

Migration guide: docs/migration/v2-auth.md
```

#### Fix with Issue Reference
```
fix(payment): prevent duplicate charge on network timeout

Implements idempotency key to prevent charging users multiple
times when network timeouts occur during payment processing.

Fixes #234
```

### Enforcement

1. **Git hooks** (recommended):
```bash
# .gitmessage
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
```

2. **CI validation**:
```yaml
- name: Validate commits
  uses: wagoid/commitlint-github-action@v4
```

3. **Team agreement**: Include in onboarding and PR reviews

## Alternatives Considered

1. **Free-form with guidelines**: Too inconsistent
2. **Ticket-ID only**: Loses context without external system
3. **Detailed templates**: Too heavyweight for small changes

## References
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)

## Review Date
June 2024 - Assess automation benefits and team adoption