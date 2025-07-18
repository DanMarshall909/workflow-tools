# TypeScript Jest & React Testing Library - Test Naming Rules

## Core Principle
Name tests as if explaining the scenario to a business stakeholder unfamiliar with the code implementation.

## Essential Rules

### ❌ NEVER Use These Patterns
- `should` language - describes intention, not behavior
- Method names in test names - ties tests to implementation
- Technical implementation details in names
- Rigid naming formulas

### ✅ ALWAYS Use These Patterns
- Plain English describing business behavior
- Underscore separation for readability
- Behavior-focused descriptions
- Domain language that non-programmers understand

## Examples from Real Projects

### Authentication Tests
```typescript
// ❌ BAD: Technical focus
describe('LoginForm', () => {
  it('should call onSubmit when form is valid', () => {})
  it('should show error when validation fails', () => {})
})

// ✅ GOOD: Business behavior focus
describe('User Login', () => {
  it('user can login with valid credentials', () => {})
  it('user sees error message with invalid credentials', () => {})
})
```

### Component Behavior Tests
```typescript
// ❌ BAD: Implementation details
describe('SessionTimer', () => {
  it('should update state every second', () => {})
  it('should call onComplete when timer reaches zero', () => {})
})

// ✅ GOOD: User experience focus
describe('Session Timer', () => {
  it('user sees countdown during active session', () => {})
  it('user receives notification when session completes', () => {})
})
```

### Error Handling Tests
```typescript
// ❌ BAD: Technical exceptions
describe('API Service', () => {
  it('should handle 404 errors gracefully', () => {})
  it('should retry on network failure', () => {})
})

// ✅ GOOD: User impact focus
describe('Task Loading', () => {
  it('user sees empty state when no tasks available', () => {})
  it('user sees retry option when connection fails', () => {})
})
```

## React Testing Library Specific Patterns

### User Interaction Tests
```typescript
// Focus on user actions and outcomes
describe('Task Creation', () => {
  it('user can create task with title and description', () => {})
  it('user cannot create task without required title', () => {})
  it('user sees confirmation after task creation', () => {})
})
```

### Hook Testing
```typescript
// ❌ BAD: Hook implementation focus
describe('useSessionPersistence', () => {
  it('should save to localStorage on state change', () => {})
  it('should handle corrupted localStorage data', () => {})
})

// ✅ GOOD: Business value focus
describe('Session Persistence', () => {
  it('user session continues after browser refresh', () => {})
  it('user starts fresh when session data corrupted', () => {})
})
```

## Test Organization

### Group by Business Scenarios
```typescript
describe('User Registration', () => {
  describe('successful registration', () => {
    it('user receives welcome email', () => {})
    it('user can immediately login', () => {})
  })
  
  describe('registration validation', () => {
    it('user cannot register with existing email', () => {})
    it('user must provide strong password', () => {})
  })
})
```

## Quick Reference

| Bad Pattern | Good Pattern |
|-------------|--------------|
| `should return user data` | `user can view their profile` |
| `should handle API errors` | `user sees helpful error message` |
| `should debounce input` | `rapid typing saves without data loss` |
| `should validate form` | `user cannot submit incomplete form` |
| `should call useEffect` | `data loads when component appears` |

## Integration with Jest

### File Naming
- `UserLogin.test.tsx` - Component behavior tests
- `SessionPersistence.test.ts` - Hook behavior tests
- `TaskService.test.ts` - Service behavior tests

### Test Structure
```typescript
describe('Business Feature', () => {
  beforeEach(() => {
    // Setup business context
  })

  it('business_scenario_in_plain_english', () => {
    // Arrange: Set up business state
    // Act: Perform user action
    // Assert: Verify business outcome
  })
})
```

## References
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)
- [React Testing Library Philosophy](https://testing-library.com/docs/guiding-principles/)