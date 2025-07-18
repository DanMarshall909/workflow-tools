# Security Quick Reference

## 🔒 Golden Rules

1. **Never trust user input**
2. **Fail securely (closed)**
3. **Defense in depth**
4. **Principle of least privilege**
5. **Keep security simple**

## 🛡️ OWASP Top 10 Prevention

### 1. Injection
```javascript
// ❌ NEVER
query = "SELECT * FROM users WHERE id = " + userId

// ✅ ALWAYS
query = "SELECT * FROM users WHERE id = ?"
db.query(query, [userId])
```

### 2. Authentication
- Minimum 12 character passwords
- Account lockout after failures
- MFA/2FA required
- Session timeout
- Secure password reset

### 3. Sensitive Data
```javascript
// ❌ NEVER
console.log("Login attempt: " + password)
localStorage.setItem('token', authToken)

// ✅ ALWAYS
console.log("Login attempt for user: " + userId)
sessionStorage.setItem('token', authToken) // httpOnly cookie better
```

### 4. Access Control
```javascript
// ✅ ALWAYS verify server-side
function getDocument(userId, docId) {
  const user = authenticate(userId)
  const doc = fetchDocument(docId)
  
  if (!userCanAccess(user, doc)) {
    throw new ForbiddenError()
  }
  
  return doc
}
```

### 5. Security Headers
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000
```

## 🔐 Input Validation

### Whitelist Approach
```javascript
// Email validation
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
if (!emailRegex.test(email)) {
  throw new ValidationError('Invalid email')
}

// Number validation
const age = parseInt(userInput, 10)
if (isNaN(age) || age < 0 || age > 150) {
  throw new ValidationError('Invalid age')
}
```

### Sanitization
```javascript
// HTML encoding
function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// SQL safe strings
const safeName = name.replace(/[^a-zA-Z0-9\s]/g, '')
```

## 🔑 Authentication

### Password Hashing
```javascript
// ✅ Use bcrypt/argon2
const bcrypt = require('bcrypt')
const hash = await bcrypt.hash(password, 12)

// ❌ NEVER use MD5, SHA1, or plain text
```

### Session Management
- Regenerate session ID on login
- Use secure, httpOnly cookies
- Implement CSRF protection
- Short session timeouts
- Clear sessions on logout

## 🚨 Error Handling

### Safe Error Messages
```javascript
// ❌ BAD - Information leakage
catch (error) {
  return { error: error.stack }
}

// ✅ GOOD - Generic message
catch (error) {
  logger.error('Auth failed', error)
  return { error: 'Invalid credentials' }
}
```

## 📊 Logging & Monitoring

### What to Log
- ✅ Authentication attempts
- ✅ Authorization failures
- ✅ Input validation failures
- ✅ System errors
- ❌ Passwords or tokens
- ❌ Sensitive user data

### Log Format
```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "level": "WARN",
  "event": "LOGIN_FAILED",
  "userId": "user123",
  "ip": "192.168.1.1",
  "reason": "invalid_password"
}
```

## 🔍 Security Testing

### Quick Checks
- [ ] All inputs validated
- [ ] Outputs properly encoded
- [ ] Authentication on every request
- [ ] Sensitive data encrypted
- [ ] Error messages generic
- [ ] Security headers configured
- [ ] Dependencies up to date
- [ ] No hardcoded secrets

## 🚀 Quick Wins

1. **Use parameterized queries**
2. **Enable security headers**
3. **Implement rate limiting**
4. **Use HTTPS everywhere**
5. **Keep dependencies updated**
6. **Hash passwords properly**
7. **Validate all inputs**
8. **Log security events**

---
[Full Guide →](../generic/security/secure-development.md)