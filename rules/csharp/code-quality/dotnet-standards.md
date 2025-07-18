# C# .NET Code Quality Standards

## Core Principles

### Security & Privacy First
- Never log user input or sensitive information
- Use secure coding practices for authentication and data handling
- Implement proper input validation and sanitization
- Follow OWASP guidelines for web applications

### Clean Architecture
- Separation of concerns across layers
- Dependency inversion principle
- Domain-driven design patterns
- CQRS for complex business operations

### Performance & Scalability
- Async/await for I/O operations
- Proper memory management
- Efficient database queries
- Caching strategies

## Essential Rules

### 1. Class and Method Design
```csharp
// ✅ GOOD: Single responsibility, clear purpose
public class TaskAggregate : AggregateRoot
{
    private readonly List<TaskComment> _comments = new();
    
    public TaskId Id { get; private set; }
    public string Title { get; private set; }
    public TaskStatus Status { get; private set; }
    
    public Result Complete()
    {
        if (Status == TaskStatus.Completed)
            return Result.Failure("Task is already completed");
            
        Status = TaskStatus.Completed;
        CompletedAt = DateTime.UtcNow;
        
        AddDomainEvent(new TaskCompletedEvent(Id));
        return Result.Success();
    }
}

// ❌ BAD: Multiple responsibilities, unclear purpose
public class TaskManager
{
    public void ProcessTask(Task task, User user, string email) 
    {
        // Validates task, updates database, sends email, logs activity
        // Too many responsibilities in one method
    }
}
```

### 2. Error Handling & Result Pattern
```csharp
// ✅ GOOD: Explicit error handling with Result pattern
public class Result<T>
{
    public bool IsSuccess { get; private set; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; private set; }
    public string Error { get; private set; }
    
    private Result(bool isSuccess, T value, string error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }
    
    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(string error) => new(false, default, error);
}

// Usage in handlers
public async Task<Result<AuthResponse>> Handle(LoginCommand command)
{
    var userResult = await _userRepository.GetByEmailAsync(command.Email);
    if (userResult.IsFailure)
        return Result<AuthResponse>.Failure("Invalid credentials");
        
    if (!_passwordService.Verify(command.Password, userResult.Value.PasswordHash))
        return Result<AuthResponse>.Failure("Invalid credentials");
        
    var token = _jwtService.GenerateToken(userResult.Value);
    return Result<AuthResponse>.Success(new AuthResponse(token));
}

// ❌ BAD: Exception-based control flow
public AuthResponse Login(string email, string password)
{
    var user = _userRepository.GetByEmail(email); // Throws if not found
    if (!_passwordService.Verify(password, user.PasswordHash))
        throw new InvalidCredentialsException(); // Exception for business rule
        
    return new AuthResponse(_jwtService.GenerateToken(user));
}
```

### 3. Async/Await Best Practices
```csharp
// ✅ GOOD: Proper async patterns
public class UserService
{
    public async Task<Result<User>> CreateUserAsync(CreateUserCommand command, CancellationToken cancellationToken = default)
    {
        // Check if email already exists
        var existingUser = await _userRepository.GetByEmailAsync(command.Email, cancellationToken);
        if (existingUser.IsSuccess)
            return Result<User>.Failure("Email already registered");
            
        // Create new user
        var user = User.Create(command.Email, command.Name);
        await _userRepository.SaveAsync(user, cancellationToken);
        
        // Send welcome email (fire and forget)
        _ = Task.Run(async () => await _emailService.SendWelcomeEmailAsync(user.Email, cancellationToken), 
                    cancellationToken);
                    
        return Result<User>.Success(user);
    }
}

// ❌ BAD: Blocking async operations
public User CreateUser(CreateUserCommand command)
{
    var existingUser = _userRepository.GetByEmailAsync(command.Email).Result; // Blocking!
    if (existingUser.IsSuccess)
        throw new InvalidOperationException("Email exists");
        
    var user = User.Create(command.Email, command.Name);
    _userRepository.SaveAsync(user).Wait(); // Blocking!
    return user;
}
```

### 4. Domain Events & CQRS
```csharp
// ✅ GOOD: Domain events for side effects
public abstract class AggregateRoot
{
    private readonly List<IDomainEvent> _domainEvents = new();
    
    public IReadOnlyCollection<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();
    
    protected void AddDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }
    
    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
}

// Domain event
public record SessionStartedEvent(
    SessionId SessionId, 
    UserId UserId, 
    DateTime StartTime) : IDomainEvent;

// Event handler
public class SessionStartedEventHandler : INotificationHandler<SessionStartedEvent>
{
    private readonly INotificationService _notificationService;
    
    public async Task Handle(SessionStartedEvent notification, CancellationToken cancellationToken)
    {
        await _notificationService.SendSessionStartNotification(
            notification.UserId, 
            notification.StartTime, 
            cancellationToken);
    }
}
```

### 5. Dependency Injection & Configuration
```csharp
// ✅ GOOD: Proper service registration
public static class ServiceExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        // MediatR for CQRS
        services.AddMediatR(cfg => cfg.RegisterServicesFromAssemblyContaining<CreateTaskCommand>());
        
        // Validation behavior
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        
        // Application services
        services.AddScoped<IUserRepository, UserRepository>();
        services.AddScoped<IPasswordHashingService, PasswordHashingService>();
        services.AddScoped<IJwtTokenService, JwtTokenService>();
        
        return services;
    }
    
    public static IServiceCollection AddAuthenticationServices(this IServiceCollection services, IConfiguration configuration)
    {
        var jwtOptions = configuration.GetSection("Jwt").Get<JwtOptions>();
        services.Configure<JwtOptions>(configuration.GetSection("Jwt"));
        
        services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
            .AddJwtBearer(options =>
            {
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidateLifetime = true,
                    ValidateIssuerSigningKey = true,
                    ValidIssuer = jwtOptions.Issuer,
                    ValidAudience = jwtOptions.Audience,
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtOptions.Key))
                };
            });
            
        return services;
    }
}
```

### 6. Input Validation & Security
```csharp
// ✅ GOOD: Comprehensive validation
public class CreateTaskCommandValidator : AbstractValidator<CreateTaskCommand>
{
    public CreateTaskCommandValidator()
    {
        RuleFor(x => x.Title)
            .NotEmpty().WithMessage("Task title is required")
            .MaximumLength(200).WithMessage("Task title cannot exceed 200 characters")
            .Must(NotContainMaliciousContent).WithMessage("Title contains invalid content");
            
        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("Description cannot exceed 2000 characters")
            .Must(NotContainMaliciousContent).WithMessage("Description contains invalid content")
            .When(x => !string.IsNullOrEmpty(x.Description));
            
        RuleFor(x => x.EstimatedDuration)
            .GreaterThan(TimeSpan.Zero).WithMessage("Estimated duration must be positive")
            .LessThanOrEqualTo(TimeSpan.FromHours(8)).WithMessage("Estimated duration cannot exceed 8 hours");
    }
    
    private bool NotContainMaliciousContent(string content)
    {
        if (string.IsNullOrEmpty(content)) return true;
        
        // Check for potential XSS or injection attempts
        var maliciousPatterns = new[] { "<script", "javascript:", "onload=", "onerror=" };
        return !maliciousPatterns.Any(pattern => 
            content.Contains(pattern, StringComparison.OrdinalIgnoreCase));
    }
}
```

### 7. Database & Entity Framework
```csharp
// ✅ GOOD: Proper Entity Framework configuration
public class AnchorDbContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<Task> Tasks { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // User configuration
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasConversion(id => id.Value, value => new UserId(value));
            entity.Property(e => e.Email).HasMaxLength(320).IsRequired();
            entity.Property(e => e.PasswordHash).HasMaxLength(256).IsRequired();
            entity.HasIndex(e => e.Email).IsUnique();
        });
        
        // Task configuration
        modelBuilder.Entity<Task>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Id).HasConversion(id => id.Value, value => new TaskId(value));
            entity.Property(e => e.Title).HasMaxLength(200).IsRequired();
            entity.Property(e => e.Description).HasMaxLength(2000);
            entity.Property(e => e.Status).HasConversion<string>();
            entity.Property(e => e.Priority).HasConversion<string>();
            
            // Soft delete
            entity.HasQueryFilter(e => !e.IsDeleted);
        });
    }
}

// Repository pattern
public class UserRepository : IUserRepository
{
    private readonly AnchorDbContext _context;
    
    public async Task<Result<User>> GetByEmailAsync(string email, CancellationToken cancellationToken = default)
    {
        var user = await _context.Users
            .AsNoTracking()
            .FirstOrDefaultAsync(u => u.Email == email, cancellationToken);
            
        return user == null 
            ? Result<User>.Failure("User not found")
            : Result<User>.Success(user);
    }
    
    public async Task<Result> SaveAsync(User user, CancellationToken cancellationToken = default)
    {
        try
        {
            _context.Users.Add(user);
            await _context.SaveChangesAsync(cancellationToken);
            return Result.Success();
        }
        catch (DbUpdateException ex) when (ex.InnerException?.Message.Contains("duplicate key") == true)
        {
            return Result.Failure("Email already exists");
        }
    }
}
```

## ADHD-Friendly Patterns

### Keep Methods Focused
```csharp
// ✅ GOOD: Single responsibility methods
public class SessionService
{
    public async Task<Result<Session>> StartSessionAsync(StartSessionCommand command)
    {
        var validationResult = ValidateSessionRequest(command);
        if (validationResult.IsFailure)
            return Result<Session>.Failure(validationResult.Error);
            
        var session = CreateSession(command);
        var saveResult = await SaveSessionAsync(session);
        
        if (saveResult.IsSuccess)
            await NotifySessionStartedAsync(session);
            
        return saveResult;
    }
    
    private Result ValidateSessionRequest(StartSessionCommand command) { /* focused validation */ }
    private Session CreateSession(StartSessionCommand command) { /* focused creation */ }
    private async Task<Result<Session>> SaveSessionAsync(Session session) { /* focused persistence */ }
    private async Task NotifySessionStartedAsync(Session session) { /* focused notification */ }
}

// ❌ BAD: Too many responsibilities
public async Task<Session> ProcessSessionStart(StartSessionCommand command)
{
    // 100+ lines mixing validation, creation, persistence, notification, logging, etc.
}
```

### Clear Naming Conventions
```csharp
// ✅ GOOD: Self-documenting names
public class UserAccountService
{
    public async Task<bool> IsUserAccountActiveAsync(UserId userId) { }
    public async Task<Result> DeactivateUserAccountAsync(UserId userId, string reason) { }
    public async Task<TimeSpan> GetTimeSinceLastLoginAsync(UserId userId) { }
}

// ❌ BAD: Unclear abbreviations
public class UsrAccSvc
{
    public async Task<bool> IsActvAsync(UserId uid) { }
    public async Task<Result> DeactAsync(UserId uid, string rsn) { }
    public async Task<TimeSpan> GetTmSncLstLgnAsync(UserId uid) { }
}
```

## Quality Gates

### Static Analysis Rules (EditorConfig)
```ini
# .editorconfig
root = true

[*.cs]
# Indentation
indent_style = space
indent_size = 4

# New line preferences
end_of_line = crlf
insert_final_newline = true

# Code style rules
dotnet_style_qualification_for_field = false
dotnet_style_qualification_for_property = false
dotnet_style_qualification_for_method = false
dotnet_style_qualification_for_event = false

# Expression-level preferences
dotnet_style_object_initializer = true
dotnet_style_collection_initializer = true
dotnet_style_explicit_tuple_names = true
dotnet_style_null_propagation = true
dotnet_style_coalesce_expression = true

# C# Code style rules
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true

# Organize usings
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false
```

### Required Before Commit
- [ ] All compiler warnings resolved
- [ ] No SonarQube critical or major issues
- [ ] Security scan passes
- [ ] Unit test coverage above 95%
- [ ] Integration tests pass
- [ ] No hardcoded secrets or credentials
- [ ] Proper logging levels (no Debug in production code)

### Performance Checklist
- [ ] Database queries are efficient and indexed
- [ ] Async operations don't block threads
- [ ] Large datasets use pagination
- [ ] Caching implemented where appropriate
- [ ] Memory allocations minimized in hot paths
- [ ] Disposal patterns implemented for resources