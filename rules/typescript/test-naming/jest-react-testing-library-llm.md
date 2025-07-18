---
rule_id: typescript-test-naming
category: test-naming
language: typescript
frameworks: [jest, react-testing-library]
severity: required
tags: [testing, naming, business-focused, jest, react]
prerequisites: [universal-test-naming]
related_rules: [typescript-code-quality, eslint-config]
version: 1.0.0
last_updated: 2024-01-20
---

# TypeScript Jest & React Testing Library - Test Naming Rules

## RULE_SUMMARY
Name tests as business scenarios using plain English, avoiding technical implementation details and 'should' language.

## APPLIES_TO
- **Languages**: TypeScript, JavaScript
- **Frameworks**: Jest, React Testing Library, Vitest
- **File Patterns**: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`
- **Development Phase**: Testing

## REQUIREMENTS

### MUST_FOLLOW
<!-- EXTRACT:requirements:start -->
1. **[REQ001]** Use plain English describing business behavior
   - Rationale: Tests serve as living documentation for all stakeholders
   - Impact: Poor names reduce test value as documentation

2. **[REQ002]** Use underscores for readability in test names
   - Rationale: Improves readability of longer test descriptions
   - Impact: Harder to quickly understand test purpose

3. **[REQ003]** Focus on user actions and outcomes, not implementation
   - Rationale: Tests should survive refactoring
   - Impact: Tests become brittle and misleading after code changes

4. **[REQ004]** Group tests by business scenarios using describe blocks
   - Rationale: Creates logical organization matching user workflows
   - Impact: Difficult to find related tests
<!-- EXTRACT:requirements:end -->

### MUST_NOT_DO
<!-- EXTRACT:antipatterns:start -->
1. **[ANT001]** Never use "should" in test names
   - Why: Describes intention rather than fact
   - Instead: State what IS, not what SHOULD BE

2. **[ANT002]** Never include method or function names
   - Why: Ties tests to implementation details
   - Instead: Describe the business outcome

3. **[ANT003]** Never use technical jargon or implementation details
   - Why: Not understandable by non-developers
   - Instead: Use domain language

4. **[ANT004]** Never use vague names like "works correctly"
   - Why: Provides no information about expected behavior
   - Instead: Be specific about the scenario and outcome
<!-- EXTRACT:antipatterns:end -->

## EXAMPLES

### GOOD_EXAMPLE_001: Authentication Tests
```typescript
// Context: User login functionality
describe('User Login', () => {
  it('user_can_login_with_valid_credentials', () => {
    // Test implementation
  })
  
  it('user_sees_error_message_with_invalid_credentials', () => {
    // Test implementation
  })
  
  it('user_account_locks_after_five_failed_attempts', () => {
    // Test implementation
  })
})
```
**Why this is good**: Describes user experience and business rules clearly

### GOOD_EXAMPLE_002: React Component Tests
```typescript
// Context: Shopping cart component
describe('Shopping Cart', () => {
  it('displays_total_price_including_tax', () => {
    render(<ShoppingCart items={items} />)
    expect(screen.getByText('Total: $107.50')).toBeInTheDocument()
  })
  
  it('user_can_remove_items_from_cart', () => {
    render(<ShoppingCart items={items} />)
    fireEvent.click(screen.getByLabelText('Remove iPhone'))
    expect(screen.queryByText('iPhone')).not.toBeInTheDocument()
  })
})
```
**Why this is good**: Focuses on what users see and can do

### BAD_EXAMPLE_001: Technical Implementation Focus
```typescript
// Anti-pattern: Method names and technical details
describe('LoginForm', () => {
  it('should call onSubmit when form is valid', () => {})
  it('should update state when input changes', () => {})
  it('handleSubmit processes credentials correctly', () => {})
})
```
**Why this is bad**: Tied to implementation, uses "should", not business-focused
**Better approach**: See GOOD_EXAMPLE_001

### BAD_EXAMPLE_002: Vague and Technical
```typescript
// Anti-pattern: Unclear purpose
describe('API Service', () => {
  it('should work properly', () => {})
  it('returns data', () => {})
  it('handles errors', () => {})
})
```
**Why this is bad**: Provides no information about actual behavior
**Better approach**: Be specific about scenarios and outcomes

## PATTERNS

### Pattern Recognition
<!-- EXTRACT:patterns:start -->
- **PATTERN_GOOD_001**: `user_[action]_[outcome]`
  - Example: `user_can_*`, `user_sees_*`, `user_receives_*`
  - Matches: `user_can_reset_password`, `user_sees_error_message`

- **PATTERN_GOOD_002**: `[business_rule]_is_enforced`
  - Example: `*_is_required`, `*_is_validated`
  - Matches: `email_uniqueness_is_enforced`, `password_strength_is_required`

- **PATTERN_BAD_001**: `should_[anything]`
  - Example: `should_*`
  - Avoid because: Uses "should" language

- **PATTERN_BAD_002**: `test[MethodName]` or `[methodName]_*`
  - Example: `testLogin`, `handleClick_*`
  - Avoid because: Tied to implementation
<!-- EXTRACT:patterns:end -->

## AUTOMATED_CHECKS

### ESLint Configuration
```javascript
// Tool: ESLint with custom rule
{
  "rules": {
    "jest/valid-title": ["error", {
      "mustNotMatch": {
        "it": ["^should", "^test", "^returns", "^calls", "^handles"],
        "describe": ["^Test", "Component$", "Service$", "Function$"]
      }
    }]
  }
}
```

### Validation Commands
```bash
# Check for "should" in test names
grep -r "it\(['\"]should" --include="*.test.ts*" src/

# Check for method names in tests
grep -r "it\(['\"].*handle\|process\|render\|update" --include="*.test.ts*" src/
```

### CI Integration
```yaml
# GitHub Actions example
- name: Validate Test Naming
  run: |
    # Fail if "should" found in test names
    ! grep -r "it\(['\"]should" --include="*.test.ts*" src/
    
    # Fail if technical patterns found
    ! grep -r "it\(['\"]test\|returns\|calls" --include="*.test.ts*" src/
```

## METRICS

### Measuring Compliance
<!-- EXTRACT:metrics:start -->
- **Metric**: Business-focused test names
  - **Target**: 100% compliance
  - **Query**: `grep -r "it\(" --include="*.test.ts*" src/ | grep -v "should\|test\|return\|call" | wc -l`
  
- **Metric**: Average test name clarity
  - **Target**: Understandable without seeing code
  - **Query**: Manual review during PR
<!-- EXTRACT:metrics:end -->

### Success Indicators
- Product managers can understand test output
- Test names don't change during refactoring
- New developers understand system behavior from tests

## MIGRATION_GUIDE

### Adopting in Existing Code
1. **Step 1**: Identify non-compliant tests
   ```bash
   grep -r "it\(['\"]should" --include="*.test.ts*" src/ > tests-to-fix.txt
   ```

2. **Step 2**: Rename during regular development
   - When fixing a bug, rename the related test
   - When adding features, improve nearby test names

### Common Challenges
- **Challenge**: "Test names are too long"
  - **Solution**: Long names are fine if they're clear. Clarity > brevity

- **Challenge**: "Hard to describe without technical terms"
  - **Solution**: Think about how you'd explain to a product manager

## CONTEXT_AND_RATIONALE

### Why This Rule Exists
Tests are the only documentation that never lies. When named properly, they explain system behavior to anyone, regardless of technical expertise.

### Evidence and Research
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)
- Teams report 40% faster onboarding when tests use business language

### Trade-offs
- **Benefits**: Living documentation, survives refactoring, accessible to all stakeholders
- **Costs**: Initial learning curve, slightly longer test names

## ENFORCEMENT_LEVEL

### When to Apply
- **Always**: All new tests must follow these patterns
- **Usually**: Existing tests renamed when touched
- **Sometimes**: Legacy test suites can be migrated gradually

### Exceptions
- Low-level utility function tests (rare)
- Performance benchmark tests
- Infrastructure tests

## LLM_METADATA
```json
{
  "rule_relationships": {
    "depends_on": ["universal-test-naming"],
    "enhances": ["typescript-code-quality"],
    "conflicts_with": [],
    "supersedes": ["old-jest-patterns"]
  },
  "extraction_hints": {
    "key_concept": "business-focused test naming",
    "problem_solved": "tests as documentation",
    "applicable_contexts": ["frontend-testing", "react-testing", "jest-tests"]
  },
  "query_patterns": [
    "How do I name tests in TypeScript?",
    "What are good Jest test names?",
    "React Testing Library naming conventions"
  ]
}
```

---
<!-- LLM_INSTRUCTION: This rule can be summarized as: Use business-focused test names that describe user behavior without 'should' or technical details -->