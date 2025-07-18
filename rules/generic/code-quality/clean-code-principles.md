# Universal Clean Code Principles

## Core Philosophy
Code is written once but read many times. Optimize for readability, maintainability, and understanding.

## The SOLID Principles

### Single Responsibility Principle (SRP)
Every module, class, or function should have one reason to change.

```
❌ BAD: Multiple responsibilities
class UserManager {
    createUser()      // User creation
    sendEmail()       // Email sending
    validateInput()   // Input validation
    saveToDatabase()  // Persistence
    generateReport()  // Reporting
}

✅ GOOD: Separated concerns
class UserService { createUser() }
class EmailService { sendEmail() }
class ValidationService { validateInput() }
class UserRepository { save() }
class ReportGenerator { generateUserReport() }
```

### Open/Closed Principle (OCP)
Software entities should be open for extension but closed for modification.

### Liskov Substitution Principle (LSP)
Derived classes must be substitutable for their base classes.

### Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they don't use.

### Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions.

## Universal Code Quality Rules

### 1. Naming is Documentation

**Variables**: Use descriptive names that explain purpose
```
❌ BAD:  d = calculate(x, y)
✅ GOOD: daysSinceLastLogin = calculateDaysBetween(lastLogin, today)
```

**Functions**: Name should describe what it does
```
❌ BAD:  process()
✅ GOOD: validateUserCredentials()
```

**Classes**: Nouns that represent domain concepts
```
❌ BAD:  Manager, Helper, Utility
✅ GOOD: UserAccount, PaymentProcessor, NotificationService
```

### 2. Functions Should Be Small

**Ideal characteristics:**
- Do one thing well
- 5-20 lines (language dependent)
- No more than 2-3 levels of indentation
- Clear input/output

```
❌ BAD: Kitchen sink function
function processUserData(data) {
    // validate data
    // transform data
    // save to database
    // send email
    // update cache
    // log activity
    // 200+ lines...
}

✅ GOOD: Focused functions
function validateUserData(data) { }
function transformUserData(data) { }
function saveUser(user) { }
function notifyUserCreated(user) { }
```

### 3. Comments Explain Why, Not What

```
❌ BAD: Redundant comment
// Increment counter by 1
counter++

✅ GOOD: Explains business logic
// Users get 3 free trial days after registration
const trialDays = 3

✅ GOOD: Explains workaround
// Using legacy API endpoint until v2 migration complete (ticket: PROJ-1234)
const endpoint = '/api/v1/users'
```

### 4. Avoid Deep Nesting

**Maximum nesting: 2-3 levels**

```
❌ BAD: Arrow anti-pattern
if (user) {
    if (user.isActive) {
        if (user.hasPermission) {
            if (user.email) {
                // Do something
            }
        }
    }
}

✅ GOOD: Early returns
if (!user) return
if (!user.isActive) return
if (!user.hasPermission) return
if (!user.email) return
// Do something
```

### 5. Don't Repeat Yourself (DRY)

But remember: **Duplication is cheaper than the wrong abstraction**

```
✅ GOOD: Extract common logic
function calculatePrice(items) {
    const subtotal = items.reduce((sum, item) => sum + item.price, 0)
    const tax = calculateTax(subtotal)
    const shipping = calculateShipping(items)
    return subtotal + tax + shipping
}

⚠️ CAREFUL: Don't over-abstract
// These might look similar but serve different purposes
function validateUserEmail(email) { }
function validateSystemEmail(email) { }
```

### 6. Fail Fast and Explicitly

```
✅ GOOD: Clear error handling
function divideNumbers(a, b) {
    if (b === 0) {
        throw new Error('Division by zero is not allowed')
    }
    return a / b
}

❌ BAD: Silent failures
function divideNumbers(a, b) {
    if (b === 0) {
        return null  // What does null mean here?
    }
    return a / b
}
```

## ADHD-Friendly Development Patterns

### 1. Cognitive Load Reduction
- **One concept per line**
- **Clear visual hierarchy**
- **Consistent patterns**
- **Minimal context switching**

### 2. Predictable Structure
```
Every file follows same pattern:
1. Imports/Dependencies
2. Constants/Configuration
3. Types/Interfaces
4. Main logic
5. Helper functions
6. Exports
```

### 3. Visual Clarity
```
✅ GOOD: Visually scannable
const isUserActive = user.status === 'active'
const hasValidSubscription = user.subscription?.isValid
const canAccessFeature = isUserActive && hasValidSubscription

❌ BAD: Dense logic
const canAccess = user.status === 'active' && user.subscription?.isValid && user.role !== 'guest' && !user.isBanned
```

## Security-First Patterns

### 1. Input Validation
**Never trust external input**
- Validate type, length, format
- Sanitize before processing
- Use allowlists, not denylists

### 2. Principle of Least Privilege
- Functions access only what they need
- Users see only their own data
- Services have minimal permissions

### 3. Secure by Default
- Encryption for sensitive data
- HTTPS for all communications
- Strong authentication required

## Code Smells to Avoid

### 1. Long Parameter Lists
```
❌ BAD:
createUser(name, email, password, age, country, city, phone, newsletter)

✅ GOOD:
createUser(userDetails: UserCreationRequest)
```

### 2. Magic Numbers/Strings
```
❌ BAD:
if (user.age >= 18) { }
if (status === 'active') { }

✅ GOOD:
const MINIMUM_AGE = 18
const USER_STATUS_ACTIVE = 'active'

if (user.age >= MINIMUM_AGE) { }
if (status === USER_STATUS_ACTIVE) { }
```

### 3. God Objects/Classes
Classes that know too much or do too much

### 4. Primitive Obsession
Using primitives instead of domain objects
```
❌ BAD:
function chargeCard(amount: number, currency: string)

✅ GOOD:
function chargeCard(payment: PaymentAmount)
```

## Refactoring Triggers

**Refactor when you:**
1. Add a feature and code is hard to understand
2. Fix a bug and see improvement opportunity
3. Do a code review and spot duplication
4. See performance issues in profiling

**Don't refactor when:**
1. Close to deadline
2. Code works and won't be touched
3. You don't have tests

## The Boy Scout Rule

> "Leave the code better than you found it"

- Fix one small thing each time
- Update outdated comments
- Improve one variable name
- Extract one small function

## Testing as Quality Gate

**No code without tests:**
- Unit tests for business logic
- Integration tests for workflows
- Performance tests for critical paths

**Test quality indicators:**
- Tests fail when code is broken
- Tests are fast and reliable
- Tests document behavior
- Tests are maintainable

## Code Review Checklist

Before submitting code:
- [ ] Would a new team member understand this?
- [ ] Are all names meaningful?
- [ ] Is there duplicated logic?
- [ ] Are errors handled properly?
- [ ] Is it testable?
- [ ] Does it follow team conventions?
- [ ] Is it secure?
- [ ] Will it perform at scale?

## Quotes to Remember

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler

> "Programs must be written for people to read, and only incidentally for machines to execute." - Abelson & Sussman

> "Clean code always looks like it was written by someone who cares." - Robert C. Martin

## References
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Refactoring by Martin Fowler](https://martinfowler.com/books/refactoring.html)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)