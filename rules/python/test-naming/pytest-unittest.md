# Python pytest & unittest - Test Naming Rules

## Core Principle
Name tests as if explaining the scenario to someone who understands the business domain but not the code implementation.

## Essential Rules

### ❌ NEVER Use These Patterns
- `test_should_*` - describes intention, not behavior
- Method/function names in test names - ties to implementation
- Technical implementation details
- CamelCase for test functions (unless using unittest classes)

### ✅ ALWAYS Use These Patterns
- Snake_case with underscores for readability
- Plain English describing business behavior
- Behavior-focused descriptions
- Domain language that stakeholders understand

## Examples from Real Python Projects

### Authentication Tests
```python
# ❌ BAD: Technical focus
def test_login_should_return_token():
    pass

def test_password_hash_should_match():
    pass

# ✅ GOOD: Business behavior focus
def test_user_can_login_with_valid_credentials():
    """User receives authentication token after successful login"""
    pass

def test_user_sees_error_with_incorrect_password():
    """Failed login attempt shows appropriate error message"""
    pass

def test_account_locks_after_five_failed_attempts():
    """Security measure prevents brute force attacks"""
    pass
```

### API Endpoint Tests
```python
# ❌ BAD: Implementation details
class TestTaskAPI:
    def test_get_endpoint_returns_200(self):
        pass
    
    def test_post_validates_json_schema(self):
        pass

# ✅ GOOD: User journey focus
class TestTaskManagement:
    def test_user_can_retrieve_their_task_list(self):
        """Authenticated user sees all their assigned tasks"""
        pass
    
    def test_user_cannot_access_other_users_tasks(self):
        """Privacy: tasks are isolated between users"""
        pass
    
    def test_task_creation_requires_title(self):
        """Business rule: every task must have a descriptive title"""
        pass
```

### Data Processing Tests
```python
# ❌ BAD: Algorithm focus
def test_filter_function_removes_nulls():
    pass

def test_aggregation_calculates_sum():
    pass

# ✅ GOOD: Business value focus
def test_report_excludes_incomplete_data():
    """Reports only show validated, complete records"""
    pass

def test_daily_totals_include_all_transactions():
    """Financial accuracy: no transactions missed in daily summary"""
    pass
```

## pytest Specific Patterns

### Fixture Naming
```python
# Fixtures should describe business entities, not technical details
@pytest.fixture
def active_user():
    """A user with valid subscription and verified email"""
    return User(
        email="user@example.com",
        status="active",
        email_verified=True
    )

@pytest.fixture
def completed_task():
    """A task marked as done by the user"""
    return Task(
        title="Important work",
        status="completed",
        completed_at=datetime.now()
    )
```

### Parametrized Tests
```python
# ✅ GOOD: Business scenarios as parameters
@pytest.mark.parametrize("password,expected_strength", [
    ("abc123", "weak"),           # Common patterns are weak
    ("MyP@ssw0rd", "medium"),     # Mixed characters are better
    ("Tr0ub4dor&3", "strong"),    # Complex passwords are strong
    ("correct horse battery staple", "strong"),  # Passphrases are strong
], ids=[
    "common_pattern_rejected",
    "mixed_characters_acceptable", 
    "complex_password_preferred",
    "passphrase_recommended"
])
def test_password_strength_meets_security_requirements(password, expected_strength):
    """Security policy enforces minimum password complexity"""
    pass
```

### Class-Based Organization
```python
class TestUserRegistration:
    """User account creation and validation"""
    
    class TestSuccessfulRegistration:
        def test_user_receives_welcome_email(self):
            """New users get onboarding information via email"""
            pass
        
        def test_user_can_immediately_login(self):
            """Account is active right after registration"""
            pass
    
    class TestRegistrationValidation:
        def test_duplicate_email_prevents_registration(self):
            """Each email address can only have one account"""
            pass
        
        def test_weak_passwords_are_rejected(self):
            """Security standards require strong passwords"""
            pass
```

## unittest Patterns

### TestCase Classes
```python
# ✅ GOOD: Behavior-focused test methods
class SessionManagementTests(unittest.TestCase):
    """Focus session tracking and management"""
    
    def test_session_starts_with_25_minute_default(self):
        """Pomodoro technique: standard focus session is 25 minutes"""
        session = FocusSession()
        self.assertEqual(session.duration, timedelta(minutes=25))
    
    def test_user_receives_break_reminder_after_session(self):
        """Healthy work habits: system suggests breaks between sessions"""
        session = FocusSession()
        session.complete()
        self.assertTrue(session.break_reminder_sent)
    
    def test_session_pauses_when_user_switches_tasks(self):
        """Accurate time tracking: only active work time is counted"""
        session = FocusSession()
        session.start()
        session.switch_task()
        self.assertEqual(session.status, "paused")
```

### Test Docstrings
```python
def test_data_export_respects_privacy_settings():
    """
    User data exports honor privacy preferences.
    
    Given: User has marked certain fields as private
    When: Data export is requested
    Then: Private fields are excluded from export
    """
    user = User(privacy_settings={"phone": "private"})
    export_data = user.export_data()
    assert "phone" not in export_data
```

## Integration Test Patterns

### Database Tests
```python
# ✅ GOOD: Business operation focus
@pytest.mark.integration
class TestDataPersistence:
    def test_completed_tasks_are_archived_after_30_days(self, db):
        """Data lifecycle: old completed tasks move to archive"""
        pass
    
    def test_user_data_survives_service_restart(self, db):
        """Reliability: user data persists across system updates"""
        pass
    
    def test_concurrent_updates_maintain_data_integrity(self, db):
        """Consistency: multiple users can safely update shared data"""
        pass
```

### API Integration Tests
```python
@pytest.mark.integration
def test_third_party_calendar_sync():
    """User's tasks appear in their external calendar"""
    pass

@pytest.mark.integration  
def test_notification_delivery_to_mobile_app():
    """Users receive timely alerts on their mobile devices"""
    pass
```

## Mock and Stub Naming

```python
# ✅ GOOD: Mocks describe business behavior
@patch('services.email.send')
def test_password_reset_sends_secure_link(mock_email_send):
    """Password reset process sends time-limited secure link"""
    user = User(email="user@example.com")
    user.request_password_reset()
    
    mock_email_send.assert_called_once()
    email_content = mock_email_send.call_args[0][1]
    assert "expires in 1 hour" in email_content

# Name mocks after business concepts, not technical details
mock_payment_processor = Mock(spec=PaymentService)
mock_inventory_system = Mock(spec=InventoryService)
```

## Quick Reference

| Bad Pattern | Good Pattern |
|-------------|--------------|
| `test_should_return_user_list` | `test_admin_can_view_all_users` |
| `test_validation_fails` | `test_form_rejects_incomplete_data` |
| `test_api_returns_404` | `test_deleted_items_are_not_accessible` |
| `test_cache_hit_improves_performance` | `test_frequently_accessed_data_loads_quickly` |

## File Organization

### Directory Structure
```
tests/
├── unit/
│   ├── test_user_registration.py
│   ├── test_task_management.py
│   └── test_session_tracking.py
├── integration/
│   ├── test_data_persistence.py
│   ├── test_external_services.py
│   └── test_api_endpoints.py
└── e2e/
    ├── test_user_workflows.py
    └── test_complete_scenarios.py
```

### Test Module Naming
- `test_business_feature.py` - Groups related business scenarios
- Avoid technical names like `test_utils.py` or `test_helpers.py`
- Prefer `test_user_authentication.py` over `test_auth_module.py`

## Performance Test Naming

```python
@pytest.mark.performance
def test_search_returns_within_one_second():
    """Users experience fast search results"""
    pass

@pytest.mark.performance
def test_bulk_import_handles_10000_records():
    """System can process large data imports efficiently"""
    pass
```

## Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=200))
def test_task_title_always_displays_correctly(title):
    """Any valid title renders properly in the UI"""
    task = Task(title=title)
    rendered = render_task(task)
    assert task.title in rendered

@given(st.integers(min_value=1, max_value=480))
def test_session_duration_stays_within_workday(minutes):
    """Sessions cannot exceed 8-hour workday limit"""
    session = FocusSession(duration_minutes=minutes)
    assert session.is_valid_duration()
```

## References
- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)