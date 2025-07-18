# Decision Record: ADHD-Friendly Development Patterns

## Status
Accepted

## Context
Software development requires sustained focus, working memory, and executive function - areas that can be challenging for developers with ADHD. Traditional coding practices often create unnecessary cognitive load through:
- Large, complex functions
- Inconsistent patterns
- Poor visual organization
- Overwhelming files
- Context switching

Research shows that 4-5% of adults have ADHD, suggesting a significant portion of developers may benefit from ADHD-friendly practices.

## Decision
We adopt ADHD-friendly patterns as standard practice throughout our development guidelines.

## Rationale

### 1. Universal Benefit
ADHD-friendly patterns help everyone, not just those with ADHD:
- Reduced cognitive load benefits all developers
- Clearer code is easier to maintain
- Smaller functions are easier to test
- Consistent patterns reduce mental overhead

### 2. Specific ADHD Challenges Addressed

#### Working Memory
- **Problem**: Holding multiple concepts while coding
- **Solution**: Small functions that fit in working memory
- **Benefit**: Reduced mental juggling

#### Focus and Attention
- **Problem**: Getting distracted or overwhelmed
- **Solution**: Clear visual hierarchy and consistent patterns
- **Benefit**: Easier to maintain focus

#### Executive Function
- **Problem**: Planning and organizing complex tasks
- **Solution**: Breaking work into small, clear steps
- **Benefit**: Manageable chunks of work

### 3. Practical Patterns That Help

#### Small Functions (5-20 lines)
```javascript
// ❌ Overwhelming
function processUserData(users) {
  // 200 lines of mixed validation, transformation,
  // API calls, error handling, and logging
}

// ✅ Manageable
function validateUsers(users) { /* 10 lines */ }
function transformUsers(users) { /* 15 lines */ }
function saveUsers(users) { /* 12 lines */ }
```

#### Clear Visual Structure
```javascript
// ✅ Scannable structure
class UserService {
  // Public methods first
  async getUser(id) { }
  async createUser(data) { }
  
  // Private helpers below
  private validateId(id) { }
  private formatUser(user) { }
}
```

#### Consistent Patterns
Using the same patterns reduces decision fatigue and cognitive switching costs.

### 4. Research Support
Studies show that developers with ADHD perform better with:
- Structured environments
- Clear, consistent patterns
- Smaller units of work
- Visual organization
- Reduced context switching

## Consequences

### Positive
- More maintainable code for everyone
- Reduced cognitive load
- Better testability
- Improved readability
- Inclusive development environment
- Lower barrier to contribution

### Negative
- May require more files (but each is simpler)
- Initial resistance to "too many small functions"
- Some developers prefer longer functions

## Implementation Guidelines

### 1. Function Design
- Maximum 50 lines (prefer 5-20)
- Single responsibility
- Clear, descriptive names
- Limited parameters (max 3-4)

### 2. File Organization
- Consistent structure across files
- Clear sections with comments
- Imports → Types → Main → Helpers

### 3. Visual Clarity
```javascript
// ✅ One concept per line
const isActive = user.status === 'active'
const hasPermission = user.role === 'admin'
const canEdit = isActive && hasPermission

// ❌ Dense logic
const canEdit = user.status === 'active' && user.role === 'admin' && !user.suspended
```

### 4. Naming Conventions
- Self-documenting names
- Avoid abbreviations
- Use domain language
- Be consistent

### 5. Error Messages
Clear, actionable error messages reduce debugging cognitive load:
```javascript
// ❌ Vague
throw new Error('Invalid data')

// ✅ Clear
throw new Error('User email required for registration')
```

## Measurement

Track improvement through:
- Code review feedback
- Time to understand code
- Bug rates in complex functions
- Developer satisfaction surveys
- Onboarding time for new team members

## Examples in Our Standards

Every language guide incorporates these patterns:
- TypeScript: Small React components, clear hooks
- C#: Focused methods, clear async patterns  
- Python: Short functions, explicit type hints
- Git: Structured commits, clear PR templates

## Not Just for ADHD

These patterns help anyone who:
- Works on complex systems
- Switches between projects
- Reviews others' code
- Returns to code after time away
- Experiences fatigue or stress
- Values clarity and simplicity

## References
- [ADHD and Software Development](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3724232/)
- [Cognitive Load Theory in Software Development](https://www.nngroup.com/articles/minimize-cognitive-load/)
- [The Programmer's Brain](https://www.manning.com/books/the-programmers-brain)
- Community feedback from neurodiverse developers

## Review Date
July 2024 - Gather feedback on pattern effectiveness and adoption