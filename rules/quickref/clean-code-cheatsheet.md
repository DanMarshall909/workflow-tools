# Clean Code Quick Reference

## 🎯 Core Principles

### SOLID
- **S**ingle Responsibility - One reason to change
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - Subtypes must be substitutable
- **I**nterface Segregation - Many specific interfaces
- **D**ependency Inversion - Depend on abstractions

### DRY vs WET
- **DRY**: Don't Repeat Yourself (but don't over-abstract)
- **WET**: Write Everything Twice (before abstracting)

## 📏 Size Guidelines

### Functions
- **Lines**: 5-20 (max 50)
- **Parameters**: Max 3-4
- **Indent levels**: Max 2-3
- **Do one thing well**

### Classes
- **Lines**: 100-200
- **Methods**: 5-10 public
- **Single purpose**

## 🏷️ Naming Rules

### Variables
```javascript
// ❌ BAD
const d = new Date()
const yrs = calcAge()

// ✅ GOOD
const currentDate = new Date()
const userAgeInYears = calculateAge()
```

### Functions
```javascript
// ❌ BAD
function calc(x, y) { }
function processData() { }

// ✅ GOOD
function calculateTotalPrice(items, taxRate) { }
function validateUserCredentials() { }
```

### Booleans
```javascript
// ❌ BAD
const flag = true
const status = checkUser()

// ✅ GOOD
const isLoggedIn = true
const hasActiveSubscription = checkUser()
```

## 🚫 Code Smells

### Long Parameter Lists
```javascript
// ❌ BAD
createUser(name, email, age, country, city, phone)

// ✅ GOOD
createUser({ name, email, age, address, phone })
```

### Magic Numbers
```javascript
// ❌ BAD
if (age >= 18) { }

// ✅ GOOD
const MINIMUM_AGE = 18
if (age >= MINIMUM_AGE) { }
```

### Deep Nesting
```javascript
// ❌ BAD
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      // do something
    }
  }
}

// ✅ GOOD
if (!user) return
if (!user.isActive) return
if (!user.hasPermission) return
// do something
```

## 💬 Comments

### When to Comment
- **WHY** not WHAT
- Complex business logic
- Workarounds with ticket reference
- Performance optimizations

### Examples
```javascript
// ❌ BAD: Obvious
// Increment i by 1
i++

// ✅ GOOD: Explains why
// Users get 3 free articles before paywall (JIRA-123)
const FREE_ARTICLE_LIMIT = 3
```

## 🔒 Error Handling

### Fail Fast
```javascript
// ✅ GOOD
function divide(a, b) {
  if (b === 0) {
    throw new Error('Division by zero')
  }
  return a / b
}
```

### Explicit Errors
```javascript
// ❌ BAD
catch (e) {
  console.log('Error occurred')
}

// ✅ GOOD
catch (error) {
  logger.error('Payment processing failed', {
    error,
    userId,
    amount
  })
  throw new PaymentError('Transaction failed')
}
```

## ⚡ Performance

### Common Optimizations
- Memoize expensive calculations
- Debounce user input
- Lazy load components
- Use pagination for lists

## 🧠 ADHD-Friendly

- **One concept per line**
- **Clear visual hierarchy**
- **Consistent patterns**
- **Small, focused functions**
- **Meaningful names**

---
[Full Guide →](../generic/code-quality/clean-code-principles.md)