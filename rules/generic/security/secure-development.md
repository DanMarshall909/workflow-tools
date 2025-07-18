# Security-First Development Principles

## Core Security Mindset

**Security is not a feature - it's a fundamental requirement.** Every line of code is a potential security boundary.

## The CIA Triad

### Confidentiality
- Data is only accessible to authorized users
- Encryption in transit and at rest
- Proper access controls

### Integrity
- Data cannot be modified without authorization
- Audit trails for all changes
- Input validation and output encoding

### Availability
- Systems remain accessible to legitimate users
- Protection against DoS attacks
- Graceful degradation under load

## OWASP Top 10 Prevention

### 1. Injection Prevention
```
❌ NEVER: String concatenation for queries
query = "SELECT * FROM users WHERE id = " + userId

✅ ALWAYS: Parameterized queries
query = "SELECT * FROM users WHERE id = ?"
execute(query, [userId])

✅ ALWAYS: Input validation
function validateUserId(id) {
    if (!isInteger(id) || id < 1) {
        throw new ValidationError("Invalid user ID")
    }
    return id
}
```

### 2. Broken Authentication
```
✅ SECURE: Password requirements
- Minimum 12 characters
- No common passwords (use haveibeenpwned API)
- Password strength meter
- Account lockout after failures
- Multi-factor authentication

✅ SECURE: Session management
- Secure, httpOnly, sameSite cookies
- Short session timeouts
- Regenerate session ID on login
- Proper logout (clear server session)
```

### 3. Sensitive Data Exposure
```
❌ NEVER: Log sensitive data
logger.info("User login: " + username + " password: " + password)

✅ ALWAYS: Mask sensitive information
logger.info("User login attempt for: " + username)

✅ ALWAYS: Encrypt sensitive data
- Use AES-256 for data at rest
- Use TLS 1.3 for data in transit
- Never store passwords (use bcrypt/argon2)
- Encrypt PII in databases
```

### 4. XML External Entities (XXE)
```
✅ SECURE: Disable external entities
// Disable DTDs entirely
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)

// Or disable external entities
factory.setFeature("http://xml.org/sax/features/external-general-entities", false)
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false)
```

### 5. Broken Access Control
```
✅ SECURE: Check permissions on every request
function getDocument(userId, documentId) {
    const user = authenticate(userId)
    const document = fetchDocument(documentId)
    
    if (!userCanAccess(user, document)) {
        throw new ForbiddenError("Access denied")
    }
    
    return document
}

❌ INSECURE: Client-side authorization only
// Never trust the client!
if (user.role === 'admin') {
    showAdminPanel() // Must verify server-side too!
}
```

### 6. Security Misconfiguration
```
✅ SECURE: Production configuration
- Remove default accounts
- Disable directory listing
- Custom error pages (no stack traces)
- Security headers configured
- Latest security patches applied

✅ SECURE: Headers checklist
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### 7. Cross-Site Scripting (XSS)
```
❌ VULNERABLE: Direct HTML insertion
element.innerHTML = userInput

✅ SECURE: Proper encoding
element.textContent = userInput

✅ SECURE: Template encoding
<div>{escapeHtml(userInput)}</div>

✅ SECURE: Content Security Policy
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'nonce-{random}';
    style-src 'self' 'nonce-{random}';
```

### 8. Insecure Deserialization
```
❌ NEVER: Deserialize untrusted data
const userData = JSON.parse(request.body)
eval(userData.code) // NEVER!

✅ ALWAYS: Validate after deserialization
const userData = JSON.parse(request.body)
const validated = validateUserSchema(userData)
```

### 9. Using Components with Known Vulnerabilities
```
✅ SECURE: Dependency management
- Regular dependency audits (npm audit, snyk)
- Automated security updates
- Monitor security advisories
- Remove unused dependencies

# Example: GitHub Dependabot configuration
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    security-updates-only: true
```

### 10. Insufficient Logging & Monitoring
```
✅ SECURE: Comprehensive logging
- Authentication attempts (success/failure)
- Authorization failures
- Input validation failures
- System errors
- Data modifications

✅ SECURE: Log format
{
    timestamp: "2024-01-20T10:30:00Z",
    level: "WARN",
    event: "LOGIN_FAILED",
    userId: "user123",
    ip: "192.168.1.1",
    userAgent: "Mozilla/5.0...",
    reason: "invalid_password"
}
```

## Secure Coding Patterns

### Input Validation
```
✅ SECURE: Whitelist validation
function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    if (!emailRegex.test(email) || email.length > 320) {
        throw new ValidationError("Invalid email format")
    }
    return email.toLowerCase()
}

✅ SECURE: Type and range validation
function validateAge(age) {
    const parsed = parseInt(age, 10)
    if (isNaN(parsed) || parsed < 0 || parsed > 150) {
        throw new ValidationError("Invalid age")
    }
    return parsed
}
```

### Output Encoding
```
✅ SECURE: Context-aware encoding
// HTML context
function escapeHtml(str) {
    const div = document.createElement('div')
    div.textContent = str
    return div.innerHTML
}

// URL context
function escapeUrl(str) {
    return encodeURIComponent(str)
}

// JavaScript context
function escapeJs(str) {
    return JSON.stringify(str)
}
```

### Cryptography
```
✅ SECURE: Password hashing
const bcrypt = require('bcrypt')
const saltRounds = 12

async function hashPassword(password) {
    return bcrypt.hash(password, saltRounds)
}

async function verifyPassword(password, hash) {
    return bcrypt.compare(password, hash)
}

❌ INSECURE: DIY crypto
function badHash(password) {
    return sha1(password + "mysalt") // NO!
}
```

### Error Handling
```
✅ SECURE: Safe error messages
try {
    authenticateUser(username, password)
} catch (error) {
    // Log full error internally
    logger.error("Authentication failed", error)
    
    // Return generic message to user
    return { error: "Invalid credentials" }
}

❌ INSECURE: Information leakage
catch (error) {
    return { error: error.stack } // Exposes internals!
}
```

## Privacy by Design

### Data Minimization
- Collect only necessary data
- Delete data when no longer needed
- Anonymize where possible

### Purpose Limitation
- Use data only for stated purpose
- Get consent for new uses
- Clear privacy policy

### Data Protection
```
✅ SECURE: PII handling
class UserData {
    constructor(data) {
        this.id = data.id
        this.email = encrypt(data.email)
        this.name = encrypt(data.name)
        this.preferences = data.preferences
    }
    
    getEmail() {
        return decrypt(this.email)
    }
    
    toJSON() {
        // Never include PII in JSON
        return {
            id: this.id,
            preferences: this.preferences
        }
    }
}
```

## Security Testing

### Static Analysis (SAST)
- Run on every commit
- Tools: SonarQube, Checkmarx, Fortify

### Dynamic Analysis (DAST)
- Run against running application
- Tools: OWASP ZAP, Burp Suite

### Dependency Scanning
- Check for vulnerable dependencies
- Tools: Snyk, WhiteSource, Black Duck

### Penetration Testing
- Regular third-party testing
- Fix findings promptly
- Retest after fixes

## Incident Response

### Preparation
1. Incident response plan
2. Contact list maintained
3. Backups tested regularly
4. Monitoring in place

### Detection & Analysis
1. Alert on anomalies
2. Investigate promptly
3. Determine scope
4. Preserve evidence

### Containment & Recovery
1. Isolate affected systems
2. Apply fixes
3. Restore from backups
4. Monitor for reoccurrence

### Post-Incident
1. Document timeline
2. Identify root cause
3. Update procedures
4. Share lessons learned

## Security Checklist

Before deploying:
- [ ] All inputs validated
- [ ] All outputs encoded
- [ ] Authentication implemented correctly
- [ ] Authorization checked on each request
- [ ] Sensitive data encrypted
- [ ] Security headers configured
- [ ] Logging implemented (without sensitive data)
- [ ] Error messages don't leak information
- [ ] Dependencies up to date
- [ ] Security testing completed

## Remember

> "Security is a process, not a product." - Bruce Schneier

> "The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room with armed guards." - Gene Spafford

**But we still try our best!**

## References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)