# Pull Request Standards

## Why PR Standards Matter

Good pull requests:
- Facilitate effective code reviews
- Document changes for future reference
- Ensure quality and consistency
- Enable knowledge sharing
- Create audit trails

## PR Title Format

### Follow Conventional Commits
```
<type>(<scope>): <description>

feat(auth): add OAuth2 integration
fix(api): resolve timeout on large queries
docs(readme): update installation steps
```

### Include Ticket References
```
feat(payment): implement Stripe integration [JIRA-123]
fix(ui): correct button alignment on mobile (#456)
```

## PR Description Template

```markdown
## Description
Brief summary of what this PR does and why it's needed.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
- Closes #123
- Relates to #456
- Fixes JIRA-789

## Changes Made
- Added user authentication via OAuth
- Updated login UI components
- Added integration tests for auth flow
- Updated API documentation

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Tested on: [browsers/devices]

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] I have updated documentation accordingly
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged
```

## PR Size Guidelines

### Ideal PR Characteristics
- **Lines changed**: < 400
- **Files changed**: < 20
- **Single purpose**: One feature/fix per PR
- **Review time**: < 1 hour

### When to Split PRs
```
❌ TOO LARGE:
- feat: add user management system (2000+ lines)

✅ BETTER:
- feat(auth): add user model and migrations
- feat(auth): implement registration endpoint  
- feat(auth): add login and session handling
- feat(ui): create user management interface
```

## Code Review Readiness

### Before Opening PR

1. **Self-Review Checklist**
   - [ ] Code compiles without warnings
   - [ ] All tests pass
   - [ ] No debugging code left
   - [ ] No commented-out code
   - [ ] Sensitive data removed

2. **Code Quality**
   - [ ] Follows project conventions
   - [ ] Functions are focused
   - [ ] Complex logic is commented
   - [ ] No code duplication
   - [ ] Error handling complete

3. **Testing**
   - [ ] Unit tests for new code
   - [ ] Integration tests updated
   - [ ] Edge cases covered
   - [ ] Performance impact assessed

## Writing PR Descriptions

### Good Description Example
```markdown
## Description
This PR adds two-factor authentication to improve account security.

Users were requesting additional security measures, especially those in 
financial services. This implements TOTP-based 2FA that works with 
standard authenticator apps.

## Changes Made
- Added 2FA setup flow in account settings
- Implemented TOTP token generation and validation
- Created backup codes for account recovery
- Added database migrations for 2FA fields
- Updated authentication middleware

## Testing
- Unit tests for TOTP generation/validation
- Integration tests for full 2FA flow
- Manual testing with Google Authenticator and Authy
- Tested account recovery with backup codes
- Verified backward compatibility for existing users

## Breaking Changes
None - 2FA is optional and doesn't affect existing auth flow

## Performance Impact
- Additional database query on login (cached after first check)
- Negligible impact on authentication time (<50ms added)
```

### Poor Description Example
```markdown
❌ BAD:
Fixed stuff

Added 2FA
```

## Review Response Etiquette

### Responding to Feedback

**DO:**
```
✅ "Good catch! I've updated the error handling in commit abc123"
✅ "I see your point. I've refactored this to be more readable"
✅ "You're right about the performance concern. I've added caching"
```

**DON'T:**
```
❌ "It works fine on my machine"
❌ "That's how it's always been done"
❌ "This is just your opinion"
```

### Addressing Review Comments

1. **Acknowledge all comments**
   - ✅ Fixed in commit abc123
   - 💭 Let's discuss in the thread
   - 📝 Created issue #123 for follow-up
   - ❓ Could you clarify what you mean?

2. **Update PR systematically**
   - Address feedback in new commits
   - Don't force-push during review
   - Mark conversations as resolved
   - Request re-review when ready

## PR Review Guidelines

### For Reviewers

**Focus Areas:**
1. **Correctness**: Does it work as intended?
2. **Design**: Is the approach sound?
3. **Readability**: Can others understand it?
4. **Testing**: Is it properly tested?
5. **Performance**: Any concerns?
6. **Security**: Any vulnerabilities?

**Comment Types:**
```
🚨 MUST: Security issue - blocks merge
🐛 MUST: Bug - blocks merge  
💡 SHOULD: Important improvement
💭 CONSIDER: Suggestion for discussion
📝 NITPICK: Minor style issue
✨ PRAISE: Highlight good code
```

### Review Checklist
- [ ] Changes match PR description
- [ ] No obvious bugs
- [ ] Tests cover new code
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Follows conventions

## Specialized PR Types

### Hotfix PRs
```markdown
## 🚨 HOTFIX: [Brief description]

**Severity**: Critical/High/Medium
**Affected Users**: All/Subset/Specific
**Workaround**: Available/None

## Root Cause
[Brief explanation of what caused the issue]

## Fix
[What this PR does to fix it]

## Testing
- [ ] Reproduced issue locally
- [ ] Verified fix resolves issue
- [ ] Regression tests added
- [ ] Tested in staging environment

## Rollback Plan
[How to rollback if this makes things worse]
```

### Refactoring PRs
```markdown
## Refactoring: [What you're refactoring]

## Motivation
[Why this refactoring is needed]

## Changes
- No functional changes
- [List structural changes]

## Testing
- All existing tests pass
- No new tests needed (no behavior change)
- Manual smoke testing completed

## Risk Assessment
Low - No functional changes, all tests passing
```

### Documentation PRs
```markdown
## Documentation: [What you're documenting]

## Changes
- [ ] Added [new documentation]
- [ ] Updated [existing docs]
- [ ] Fixed [errors/typos]

## Review Focus
- Technical accuracy
- Clarity and readability
- Completeness
- Examples correctness
```

## Merge Strategies

### Squash and Merge (Preferred)
- Single commit on main branch
- Clean history
- Good for feature branches

### Merge Commit
- Preserves branch history
- Good for release branches
- Shows full context

### Rebase and Merge
- Linear history
- No merge commits
- Good for small fixes

## PR Automation

### Auto-labeling
```yaml
# .github/labeler.yml
documentation:
  - docs/**/*
  - '*.md'

frontend:
  - src/components/**
  - src/pages/**

backend:
  - api/**
  - server/**

tests:
  - '**/*.test.js'
  - '**/*.spec.ts'
```

### Required Checks
```yaml
# .github/branch-protection.yml
protection_rules:
  - name: main
    required_status_checks:
      - continuous-integration
      - tests-pass
      - code-coverage
      - security-scan
    required_reviews: 2
    dismiss_stale_reviews: true
```

### PR Templates
```markdown
<!-- .github/pull_request_template.md -->
## What does this PR do?
[Replace with description]

## How to test
[Replace with testing steps]

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.logs or debugging code
- [ ] Follows code style guidelines
```

## Common PR Mistakes

### 1. Too Large
**Problem**: 50+ files changed
**Solution**: Break into smaller PRs

### 2. Mixed Concerns
**Problem**: Bug fix + feature + refactoring
**Solution**: Separate PRs for each

### 3. Poor Testing
**Problem**: "Tested manually"
**Solution**: Add automated tests

### 4. No Context
**Problem**: "Fix bug"
**Solution**: Explain what, why, how

### 5. Ignoring Feedback
**Problem**: Resolving without addressing
**Solution**: Respond to every comment

## PR Communication

### Status Updates
```
🚧 WIP - Still working on tests
✅ Ready for review
🔄 Addressing feedback
⏸️ On hold - waiting for dependency
✨ Ready to merge
```

### Blocking Issues
```
⚠️ BLOCKED: Waiting on #123 to merge first
⚠️ BLOCKED: Need design approval
⚠️ BLOCKED: Requires database migration
```

## Quick Reference

### PR Lifecycle
1. Create feature branch
2. Make changes
3. Self-review
4. Open PR
5. Address feedback
6. Get approvals
7. Merge
8. Delete branch

### Review Priorities
1. 🚨 Security issues
2. 🐛 Bugs
3. 🏗️ Architecture concerns
4. 🎯 Business logic
5. 📝 Code style
6. ✨ Nice-to-haves

### Merge Checklist
- [ ] All CI checks pass
- [ ] Required approvals obtained
- [ ] Feedback addressed
- [ ] No merge conflicts
- [ ] Up to date with base branch
- [ ] Documentation updated
- [ ] Ready for production

## Remember

> "The goal of a PR is not just to merge code, but to share knowledge and maintain quality."

Take time to write good PRs - your future self and teammates will thank you!

## References
- [Google Engineering Practices](https://google.github.io/eng-practices/review/)
- [Best Practices for Code Review](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/)
- [Conventional Comments](https://conventionalcomments.org/)