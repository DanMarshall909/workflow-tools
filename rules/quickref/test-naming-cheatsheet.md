# Test Naming Quick Reference

## The Golden Rule
**"Name tests as if explaining to a business stakeholder who doesn't code"**

## ❌ Never Use
- `should` - describes intention, not behavior
- Method names - `testCalculateTotal()`
- Technical jargon - `returnsTrue`, `throwsException`
- Vague names - `testHappyPath`, `testEdgeCase`

## ✅ Always Use
- Business behavior focus
- Natural language
- Present tense (what IS, not what SHOULD BE)
- Underscores for readability

## Quick Examples

### TypeScript/Jest
```typescript
// ❌ BAD
test('should return user data when API call succeeds')
test('handleClick calls onChange')

// ✅ GOOD
test('user can view their profile information')
test('search results appear after typing query')
```

### C#/xUnit
```csharp
// ❌ BAD
public void GetUser_ShouldReturnUser_WhenIdIsValid()
public void Validate_ThrowsException_WhenNull()

// ✅ GOOD
public void existing_user_profile_is_retrievable()
public void missing_required_fields_prevent_submission()
```

### Python/pytest
```python
# ❌ BAD
def test_calculate_returns_correct_sum():
def test_api_should_handle_errors():

# ✅ GOOD
def test_shopping_cart_calculates_total_with_tax():
def test_network_errors_show_retry_option():
```

## Common Patterns

| Scenario | Example Test Name |
|----------|-------------------|
| User actions | `user_can_reset_forgotten_password` |
| Business rules | `orders_over_100_dollars_qualify_for_free_shipping` |
| Error handling | `expired_session_redirects_to_login` |
| Validation | `email_must_be_unique_per_account` |
| Permissions | `only_admin_can_delete_users` |

## Remember
- Tests are documentation
- If a PM can't understand it, rewrite it
- Focus on WHAT, not HOW

---
[Full Guide →](../generic/test-naming/universal-principles.md)