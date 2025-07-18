# Git Branch Naming Conventions

## Why Branch Naming Matters

Good branch names:
- Communicate intent and ownership
- Enable automation (CI/CD, auto-deployment)
- Make navigation easier in large projects
- Provide context in pull requests
- Help with project organization

## Branch Naming Format

### Basic Structure
```
<type>/<ticket-number>-<brief-description>
<type>/<brief-description>
```

### Examples
```
feature/JIRA-123-user-authentication
bugfix/PROJ-456-fix-login-redirect
hotfix/critical-payment-error
release/v2.1.0
```

## Branch Types

### Feature Branches
For new functionality
```
feature/add-password-reset
feature/JIRA-123-oauth-integration
feature/dark-mode-toggle
```

### Bugfix Branches
For fixing bugs in development
```
bugfix/fix-memory-leak
bugfix/PROJ-456-correct-timezone-handling
bugfix/resolve-mobile-layout-issue
```

### Hotfix Branches
For urgent production fixes
```
hotfix/critical-security-patch
hotfix/payment-processing-error
hotfix/v1.2.1
```

### Release Branches
For preparing releases
```
release/v2.0.0
release/2024-q1
release/march-features
```

### Other Types
```
chore/update-dependencies
docs/api-documentation
test/add-integration-tests
refactor/simplify-auth-logic
experiment/new-caching-strategy
```

## Naming Rules

### DO:
- Use lowercase letters
- Separate words with hyphens (-)
- Include ticket numbers when available
- Keep it concise but descriptive
- Use forward slashes for hierarchy

### DON'T:
- Use spaces or underscores
- Include personal names
- Make it too long (50 chars max)
- Use special characters
- Include sensitive information

## Good vs Bad Examples

```
❌ BAD:
- Feature_User_Login
- johns-branch
- fix
- NEW!!!FEATURE!!!
- my-work-on-the-thing-that-broke

✅ GOOD:
- feature/user-login
- bugfix/PROJ-123-validation-error
- hotfix/v1.2.1
- docs/update-readme
- test/auth-integration
```

## Integration with Issue Tracking

### JIRA Integration
```
feature/PROJ-123-shopping-cart
bugfix/PROJ-456-cart-calculation

# Automatically links to JIRA tickets
# Enables automatic status updates
```

### GitHub Issues
```
feature/123-add-export-function
bugfix/456-fix-date-format

# GitHub automatically links when PR is created
# Use: "Closes #123" in PR description
```

### GitLab Issues
```
feature/123-implement-search
bugfix/456-search-performance

# GitLab links issues automatically
# Updates issue status on merge
```

## Git Flow Strategy

### Main Branches
```
main        # Production-ready code
develop     # Integration branch for features
```

### Supporting Branches
```
feature/*   # New features (from develop)
release/*   # Release preparation (from develop)
hotfix/*    # Emergency fixes (from main)
```

### Flow Example
```
develop
  ├── feature/user-auth
  ├── feature/payment-integration
  └── feature/admin-dashboard
  
main
  └── hotfix/critical-security-fix
```

## GitHub Flow Strategy

Simpler approach with just main branch:

```
main
  ├── feature/add-search
  ├── bugfix/fix-search-filters
  └── hotfix/search-crash
```

All branches created from and merged to main.

## Environment-Based Naming

When branches deploy to specific environments:

```
deploy/staging
deploy/production
deploy/qa
env/demo-client-x
env/testing
```

## Personal Branch Strategies

### For Long-Running Personal Work
```
dev/username/feature-name
dev/john/experimental-cache
dev/jane/refactor-auth
```

### For Code Reviews
```
review/username/description
review/john/code-cleanup
review/jane/performance-fixes
```

## Automation with Branch Names

### CI/CD Pipeline Triggers
```yaml
# Deploy features to staging
on:
  push:
    branches:
      - 'feature/**'

# Deploy hotfixes immediately
on:
  push:
    branches:
      - 'hotfix/**'
```

### Auto-labeling PRs
```yaml
# .github/labeler.yml
feature:
  - feature/**
  
bugfix:
  - bugfix/**
  - hotfix/**
  
documentation:
  - docs/**
```

### Branch Protection Rules
```
Pattern: main
- Require PR reviews
- Require status checks
- Require up-to-date branches

Pattern: release/*
- Require PR reviews
- Restrict who can push
- Require signed commits
```

## Team Conventions

### Ticket Number Requirements
```
# Always required
feature/JIRA-123-description

# Optional for small fixes
bugfix/typo-in-readme

# Required for client work
feature/CLIENT-789-custom-feature
```

### Description Standards
```
# Use clear action words
feature/add-user-export
feature/implement-caching
feature/create-admin-panel

# Not vague descriptions
feature/fix-stuff    ❌
feature/updates      ❌
feature/changes      ❌
```

## Branch Lifecycle

### Creation
```bash
# Create from latest develop
git checkout develop
git pull origin develop
git checkout -b feature/JIRA-123-new-feature

# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix
```

### Working
```bash
# Regular commits while working
git add .
git commit -m "feat: implement user authentication"

# Keep branch updated
git checkout develop
git pull origin develop
git checkout feature/JIRA-123-new-feature
git merge develop
```

### Completion
```bash
# Clean up before PR
git rebase -i develop  # Squash if needed

# Push for review
git push origin feature/JIRA-123-new-feature

# After merge, delete local
git branch -d feature/JIRA-123-new-feature

# Delete remote
git push origin --delete feature/JIRA-123-new-feature
```

## Special Cases

### Dependent Features
```
feature/base-authentication
  └── feature/oauth-integration
      └── feature/social-login
```

### Version-Specific Fixes
```
support/v1.x
  └── bugfix/v1-compatibility-fix

support/v2.x
  └── bugfix/v2-performance-fix
```

### Experimental Branches
```
experiment/new-architecture
spike/performance-testing
poc/blockchain-integration
```

## Quick Reference

| Type | Purpose | Created From | Merged To |
|------|---------|--------------|-----------|
| feature/* | New features | develop | develop |
| bugfix/* | Bug fixes | develop | develop |
| hotfix/* | Urgent fixes | main | main & develop |
| release/* | Release prep | develop | main & develop |
| docs/* | Documentation | develop | develop |
| test/* | Test additions | develop | develop |
| chore/* | Maintenance | develop | develop |

## Branch Naming Cheatsheet

```bash
# Feature with ticket
git checkout -b feature/JIRA-123-shopping-cart

# Bugfix without ticket  
git checkout -b bugfix/fix-login-redirect

# Hotfix for production
git checkout -b hotfix/v1.2.1

# Documentation update
git checkout -b docs/update-api-guide

# Dependency update
git checkout -b chore/update-react-18
```

## Common Pitfalls to Avoid

1. **Too Generic**: `feature/update`, `bugfix/fix`
2. **Too Long**: `feature/implement-new-user-authentication-system-with-oauth`
3. **Personal Names**: `feature/johns-work`
4. **Unclear Purpose**: `feature/stuff`, `bugfix/thing`
5. **Wrong Type**: Using `feature/` for a bugfix

## Tools and Scripts

### Branch Name Validation Hook
```bash
#!/bin/bash
# .git/hooks/pre-push

branch=$(git rev-parse --abbrev-ref HEAD)
valid_pattern="^(feature|bugfix|hotfix|release|docs|test|chore)\/[a-z0-9-]+$"

if ! [[ "$branch" =~ $valid_pattern ]]; then
  echo "Branch name '$branch' does not follow naming convention"
  echo "Expected format: <type>/<description>"
  exit 1
fi
```

### Automatic Branch Creation
```bash
# Create branch from JIRA ticket
function create-feature() {
  ticket=$1
  description=$2
  git checkout -b "feature/${ticket}-${description}"
}

# Usage
create-feature "JIRA-123" "user-authentication"
```

## Remember

> Branch names are communication tools. Make them work for your team, not against it.

Good branch names make everyone's life easier - from developers to CI/CD systems to project managers.

## References
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)