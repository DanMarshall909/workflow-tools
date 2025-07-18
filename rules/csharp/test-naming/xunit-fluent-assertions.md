# C# xUnit & FluentAssertions - Test Naming Rules

## Core Principle
Name tests as if explaining the business scenario to a domain expert who doesn't know the code implementation.

## Essential Rules

### ❌ NEVER Use These Patterns
- `Should` language - describes intention, not behavior
- Method names in test names - couples tests to implementation
- Technical details like "returns true/false"
- Rigid naming conventions like `MethodName_Scenario_ExpectedResult`

### ✅ ALWAYS Use These Patterns
- Plain English describing business outcomes
- Underscore separation for maximum readability
- Business behavior focus
- Domain language that stakeholders understand

## Examples from Real .NET Projects

### Authentication Tests
```csharp
// ❌ BAD: Technical implementation focus
public class LoginHandlerTests
{
    [Fact]
    public void Handle_ShouldReturnSuccess_WhenCredentialsAreValid() { }
    
    [Fact]
    public void Handle_ShouldReturnError_WhenPasswordIsIncorrect() { }
}

// ✅ GOOD: Business behavior focus
public class UserAuthenticationTests
{
    [Fact]
    public void user_can_login_with_valid_credentials() { }
    
    [Fact]
    public void user_sees_error_with_incorrect_password() { }
    
    [Fact]
    public void user_account_locks_after_multiple_failed_attempts() { }
}
```

### Domain Model Tests
```csharp
// ❌ BAD: Implementation details
public class TaskAggregateTests
{
    [Fact]
    public void CompleteTask_ShouldSetCompletedDate_WhenTaskIsActive() { }
    
    [Fact]
    public void AddComment_ShouldThrowException_WhenTaskIsCompleted() { }
}

// ✅ GOOD: Business rules focus
public class TaskManagementTests
{
    [Fact]
    public void completed_task_shows_completion_timestamp() { }
    
    [Fact]
    public void comments_cannot_be_added_to_completed_tasks() { }
    
    [Fact]
    public void task_priority_can_be_updated_while_in_progress() { }
}
```

### Validation Tests
```csharp
// ❌ BAD: Validator implementation focus
public class RegisterUserValidatorTests
{
    [Fact]
    public void Validate_ShouldReturnError_WhenEmailIsInvalid() { }
    
    [Fact]
    public void Validate_ShouldReturnError_WhenPasswordIsTooShort() { }
}

// ✅ GOOD: User experience focus
public class UserRegistrationTests
{
    [Fact]
    public void registration_requires_valid_email_address() { }
    
    [Fact]
    public void registration_requires_strong_password() { }
    
    [Fact]
    public void user_cannot_register_with_existing_email() { }
}
```

## FluentAssertions Best Practices

### Clear Assertion Messages
```csharp
// ✅ GOOD: Business context in assertions
[Fact]
public void user_can_create_task_with_estimated_duration()
{
    // Arrange
    var command = new CreateTaskCommand("Important Work", TimeSpan.FromHours(2));
    
    // Act
    var result = handler.Handle(command);
    
    // Assert
    result.IsSuccess.Should().BeTrue("because valid task creation should succeed");
    result.Value.EstimatedDuration.Should().Be(TimeSpan.FromHours(2), 
        "because user-specified duration should be preserved");
}

// ✅ GOOD: Domain-focused error messages
[Fact]
public void task_cannot_be_completed_twice()
{
    // Arrange
    var task = Task.Create("Work Item");
    task.Complete();
    
    // Act
    var result = task.Complete();
    
    // Assert
    result.IsFailure.Should().BeTrue("because completed tasks cannot be completed again");
    result.Error.Should().Contain("already completed", 
        "because error should explain the business rule violation");
}
```

### Testing Domain Events
```csharp
public class SessionEventTests
{
    [Fact]
    public void session_start_notifies_interested_parties()
    {
        // Arrange
        var session = new FocusSession(userId: "user123", duration: TimeSpan.FromMinutes(25));
        
        // Act
        session.Start();
        
        // Assert
        var startedEvent = session.DomainEvents.OfType<SessionStartedEvent>().Single();
        startedEvent.UserId.Should().Be("user123", "because event should identify the user");
        startedEvent.StartTime.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(1),
            "because start time should be recorded accurately");
    }
}
```

## Test Organization Patterns

### Arrange-Act-Assert with Business Context
```csharp
public class OAuth_Authentication_Tests
{
    [Fact]
    public void user_can_login_with_google_account()
    {
        // Arrange: User has valid Google OAuth token
        var oauthToken = "valid_google_token";
        var mockOAuthService = new Mock<IGoogleOAuthService>();
        mockOAuthService.Setup(s => s.GetUserInfo(oauthToken))
                       .ReturnsAsync(new GoogleUserInfo { Email = "user@example.com" });
        
        // Act: User attempts login
        var result = await handler.Handle(new OAuthLoginCommand(oauthToken, "google"));
        
        // Assert: User is successfully authenticated
        result.IsSuccess.Should().BeTrue("because valid OAuth token should authenticate user");
        result.Value.User.Email.Should().Be("user@example.com", 
            "because user email should match OAuth provider data");
    }
}
```

### Grouping Related Scenarios
```csharp
public class Password_Security_Tests
{
    public class when_user_sets_new_password
    {
        [Fact]
        public void password_must_meet_minimum_length_requirement() { }
        
        [Fact]
        public void password_must_contain_special_characters() { }
        
        [Fact]
        public void password_cannot_be_recently_used_password() { }
    }
    
    public class when_user_enters_incorrect_password
    {
        [Fact]
        public void failed_attempt_is_recorded_for_security_monitoring() { }
        
        [Fact]
        public void account_locks_after_five_consecutive_failures() { }
        
        [Fact]
        public void user_receives_account_lockout_notification() { }
    }
}
```

## Integration Test Naming

### API Endpoint Tests
```csharp
public class Task_API_Integration_Tests : IClassFixture<WebApplicationFactory<Program>>
{
    [Fact]
    public async Task user_can_retrieve_their_task_list()
    {
        // Test implementation focuses on user journey
    }
    
    [Fact]
    public async Task unauthorized_user_cannot_access_tasks()
    {
        // Test implementation focuses on security boundary
    }
}
```

### Database Integration Tests
```csharp
public class Task_Persistence_Tests : IClassFixture<DatabaseFixture>
{
    [Fact]
    public void completed_tasks_are_archived_after_thirty_days()
    {
        // Test business rule about data lifecycle
    }
    
    [Fact]
    public void user_data_is_properly_isolated_between_tenants()
    {
        // Test privacy and security requirements
    }
}
```

## Quick Reference

| Bad Pattern | Good Pattern |
|-------------|--------------|
| `ShouldReturnUser_WhenIdIsValid` | `user_profile_loads_with_valid_id` |
| `ShouldThrowException_WhenEmailExists` | `registration_fails_with_duplicate_email` |
| `ShouldUpdatePassword_WhenTokenIsValid` | `user_can_reset_password_with_valid_token` |
| `ShouldReturnFalse_WhenValidationFails` | `invalid_input_prevents_form_submission` |

## File and Class Organization

### File Naming
- `UserAuthenticationTests.cs` - Business feature tests
- `TaskManagementTests.cs` - Domain behavior tests
- `EmailNotificationTests.cs` - Service behavior tests

### Class Structure
```csharp
/// <summary>
/// Tests for user session management business rules
/// Covers focus sessions, breaks, and productivity tracking
/// </summary>
public class Session_Management_Tests
{
    private readonly SessionHandler _handler;
    private readonly Mock<INotificationService> _mockNotifications;
    
    public Session_Management_Tests()
    {
        // Setup test dependencies
    }
    
    [Fact]
    public void user_receives_reminder_when_session_ends()
    {
        // Business scenario test
    }
}
```

## Test Data Builders

### Business-Focused Test Data
```csharp
public class TaskTestDataBuilder
{
    public static Task CreateHighPriorityTask(string title = "Important Work")
        => Task.Create(title, priority: TaskPriority.High);
    
    public static Task CreateCompletedTask(string title = "Finished Work")
    {
        var task = Task.Create(title);
        task.Complete();
        return task;
    }
}

// Usage in tests
[Fact]
public void high_priority_tasks_appear_first_in_user_list()
{
    var highPriorityTask = TaskTestDataBuilder.CreateHighPriorityTask("Critical Bug Fix");
    var normalTask = TaskTestDataBuilder.CreateNormalTask("Documentation Update");
    
    // Test business rule implementation
}
```

## References
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)
- [xUnit Documentation](https://xunit.net/)
- [FluentAssertions Documentation](https://fluentassertions.com/)