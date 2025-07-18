# Decision Record: Business-Focused Test Names

## Status
Accepted

## Context
Test naming conventions vary widely across teams and projects. Common patterns include:
- Technical naming: `testCalculateTotal()`, `shouldReturnUserWhenIdIsValid()`
- BDD style: `should_calculate_total_with_tax()`
- Given-When-Then: `givenValidUser_whenLogin_thenReturnToken()`

## Decision
We adopt business-focused test naming that describes behavior in plain English, avoiding technical implementation details.

## Rationale

### 1. Tests as Living Documentation
Tests serve as the most accurate documentation of system behavior. When named properly, they explain what the system does to anyone, regardless of technical expertise.

### 2. Stakeholder Communication
Product managers, designers, and business stakeholders can understand test reports when tests are named after business scenarios rather than technical implementation.

### 3. Behavior Focus vs Implementation Focus
Business-focused names survive refactoring better. When implementation changes but behavior remains the same, the test name stays valid.

**Example Evolution:**
```
// Implementation-focused (becomes invalid after refactoring)
test_redis_cache_stores_user_session()

// Behavior-focused (remains valid)
test_user_session_persists_between_requests()
```

### 4. Avoiding "Should" Language
"Should" implies intention rather than fact. Tests verify what IS, not what SHOULD BE.

```
// Intention (weak)
"should calculate tax correctly"

// Fact (strong)
"calculates sales tax for online orders"
```

### 5. Real-World Evidence
Based on the article ["You Naming Tests Wrong"](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/) and successful adoption in production systems, teams report:
- Faster onboarding of new developers
- Easier identification of broken functionality
- Better test coverage decisions
- Improved communication with non-technical stakeholders

## Consequences

### Positive
- Tests become self-documenting
- Business requirements are clearly verified
- Test reports are meaningful to all stakeholders
- Refactoring doesn't require test renaming
- New developers understand system behavior faster

### Negative
- Initial adjustment period for developers used to technical naming
- Slightly longer test names in some cases
- May require more thought when writing tests

## Examples

### Before (Technical Focus)
```javascript
test('userService.getUser returns user object when ID exists')
test('validateEmail throws ValidationError for invalid format')
test('calculateTotal applies discount when code is valid')
```

### After (Business Focus)
```javascript
test('registered users can view their profile')
test('registration requires valid email address')
test('discount codes reduce order total')
```

## Implementation Notes

1. Use language that a business analyst would understand
2. Focus on user outcomes, not technical processes
3. Write test names before implementation (TDD)
4. Review test names in PR reviews for clarity

## References
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- Real-world experience from Anchor project and other production systems

## Review Date
January 2025 - Reassess based on team feedback and adoption success