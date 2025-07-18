# Python Code Quality Standards

## Core Principles

### Privacy & Security First
- Never log sensitive user data or PII
- Use type hints for better security analysis
- Implement input validation and sanitization
- Follow OWASP guidelines for web applications

### Clean, Pythonic Code
- Follow PEP 8 style guide
- Use descriptive variable names
- Prefer composition over inheritance
- Write functions that do one thing well

### Performance & Scalability
- Use generators for large datasets
- Implement proper caching strategies
- Profile before optimizing
- Consider memory usage in data structures

## Essential Rules

### 1. Function Design
```python
# ✅ GOOD: Pure, focused functions with type hints
from typing import List, Optional, Dict
from datetime import datetime, timedelta

def calculate_session_duration(start_time: datetime, end_time: datetime) -> timedelta:
    """Calculate the duration of a focus session."""
    return end_time - start_time

def filter_active_tasks(tasks: List[Task]) -> List[Task]:
    """Return only tasks that are not completed or archived."""
    return [task for task in tasks if task.status in ('pending', 'in_progress')]

# ✅ GOOD: Clear error handling
def parse_user_input(raw_input: str) -> Optional[Dict[str, str]]:
    """Parse user input safely, returning None if invalid."""
    try:
        # Validate input first
        if not raw_input or len(raw_input) > 1000:
            return None
        
        # Parse and validate structure
        data = json.loads(raw_input)
        if not isinstance(data, dict):
            return None
            
        # Sanitize values
        return {
            key: str(value)[:100]  # Limit string length
            for key, value in data.items()
            if isinstance(key, str) and key.isidentifier()
        }
    except (json.JSONDecodeError, ValueError):
        return None

# ❌ BAD: Side effects, unclear purpose, no type hints
def process_data(data):
    # Modifies global state
    global user_cache
    # Logs sensitive data
    print(f"Processing: {data}")  
    # Multiple responsibilities
    validated = validate(data)
    save_to_db(validated)
    send_email(validated['email'])
    user_cache[data['id']] = validated
    return True
```

### 2. Class Design
```python
# ✅ GOOD: Clear interfaces with dataclasses
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class Task:
    """Represents a user's task with ADHD-friendly features."""
    title: str
    description: str = ""
    priority: str = "medium"  # low, medium, high
    estimated_duration: Optional[timedelta] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        # Validate priority
        if self.priority not in ('low', 'medium', 'high'):
            raise ValueError(f"Invalid priority: {self.priority}")
        
        # Validate title length for focus
        if len(self.title) > 100:
            raise ValueError("Title too long - keep it concise for clarity")
    
    def complete(self) -> None:
        """Mark task as completed with timestamp."""
        if self.completed_at:
            raise ValueError("Task already completed")
        self.completed_at = datetime.utcnow()
    
    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.completed_at is not None

# ✅ GOOD: Context managers for resource handling
class DatabaseConnection:
    """Safe database connection handling."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._connection = None
    
    def __enter__(self):
        self._connection = create_connection(self.connection_string)
        return self._connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            self._connection.close()
        # Don't suppress exceptions
        return False
```

### 3. Error Handling
```python
# ✅ GOOD: Custom exceptions with context
class TaskError(Exception):
    """Base exception for task-related errors."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task not found: {task_id}")

class TaskValidationError(TaskError):
    """Raised when task data is invalid."""
    def __init__(self, field: str, value: Any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid {field}: {reason}")

# ✅ GOOD: Result type pattern
from typing import Union, TypeVar, Generic

T = TypeVar('T')

@dataclass
class Success(Generic[T]):
    value: T

@dataclass
class Failure:
    error: str
    
Result = Union[Success[T], Failure]

def create_task(title: str, user_id: str) -> Result[Task]:
    """Create a new task with validation."""
    # Validate input
    if not title or len(title.strip()) == 0:
        return Failure("Title cannot be empty")
    
    if len(title) > 100:
        return Failure("Title too long - maximum 100 characters")
    
    try:
        task = Task(title=title.strip())
        # Save to database...
        return Success(task)
    except Exception as e:
        logger.error(f"Task creation failed for user {user_id}", exc_info=True)
        return Failure("Failed to create task")

# ❌ BAD: Generic exception handling
def bad_error_handling(data):
    try:
        # Do everything
        process_data(data)
    except:  # Never catch all exceptions blindly
        pass  # Never suppress errors silently
```

### 4. Async Patterns
```python
# ✅ GOOD: Proper async/await usage
import asyncio
from typing import List, Optional
import aiohttp

async def fetch_user_tasks(user_id: str, session: aiohttp.ClientSession) -> List[Task]:
    """Fetch user's tasks from API asynchronously."""
    async with session.get(f"/api/users/{user_id}/tasks") as response:
        if response.status != 200:
            raise TaskError(f"Failed to fetch tasks: {response.status}")
        
        data = await response.json()
        return [Task(**task_data) for task_data in data]

async def notify_task_complete(task: Task, user_id: str) -> None:
    """Send async notification when task completes."""
    async with aiohttp.ClientSession() as session:
        payload = {
            "user_id": user_id,
            "task_id": task.id,
            "message": f"Task '{task.title}' completed!"
        }
        
        async with session.post("/api/notifications", json=payload) as response:
            if response.status != 201:
                # Log but don't fail the main operation
                logger.warning(f"Notification failed for task {task.id}")

# ✅ GOOD: Concurrent operations with proper error handling
async def process_multiple_tasks(task_ids: List[str]) -> List[Result[Task]]:
    """Process multiple tasks concurrently."""
    async def process_single_task(task_id: str) -> Result[Task]:
        try:
            # Simulate async processing
            await asyncio.sleep(0.1)
            return Success(Task(title=f"Processed {task_id}"))
        except Exception as e:
            return Failure(f"Failed to process {task_id}: {str(e)}")
    
    # Process all tasks concurrently
    results = await asyncio.gather(
        *[process_single_task(task_id) for task_id in task_ids],
        return_exceptions=False
    )
    
    return results
```

### 5. Data Validation
```python
# ✅ GOOD: Pydantic for data validation
from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class CreateTaskRequest(BaseModel):
    """Validated request for task creation."""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field("medium", regex="^(low|medium|high)$")
    estimated_minutes: Optional[int] = Field(None, ge=1, le=480)  # 1-480 minutes
    
    @validator('title')
    def title_must_be_meaningful(cls, v):
        """Ensure title contains actual content."""
        if v.strip() != v:
            raise ValueError('Title cannot start or end with whitespace')
        if len(v.split()) < 2:
            raise ValueError('Title should be descriptive (at least 2 words)')
        return v
    
    @validator('description')
    def sanitize_description(cls, v):
        """Remove any potential harmful content."""
        if v:
            # Simple sanitization - in production use proper library
            forbidden = ['<script', 'javascript:', 'onload=']
            for pattern in forbidden:
                if pattern in v.lower():
                    raise ValueError('Description contains forbidden content')
        return v

# ✅ GOOD: Type-safe configuration
class AppConfig(BaseModel):
    """Application configuration with validation."""
    database_url: str
    redis_url: Optional[str] = None
    max_tasks_per_user: int = Field(100, ge=1, le=1000)
    session_timeout_minutes: int = Field(30, ge=5, le=120)
    enable_notifications: bool = True
    
    class Config:
        env_prefix = 'APP_'  # Read from APP_DATABASE_URL, etc.
```

### 6. Testing Helpers
```python
# ✅ GOOD: Test fixtures and factories
import pytest
from datetime import datetime, timedelta
from typing import List

class TaskFactory:
    """Factory for creating test tasks with sensible defaults."""
    
    @staticmethod
    def create_task(
        title: str = "Test Task",
        priority: str = "medium",
        completed: bool = False,
        **kwargs
    ) -> Task:
        """Create a task with test defaults."""
        task = Task(title=title, priority=priority, **kwargs)
        if completed:
            task.complete()
        return task
    
    @staticmethod
    def create_batch(count: int, **kwargs) -> List[Task]:
        """Create multiple tasks for testing."""
        return [
            TaskFactory.create_task(
                title=f"Task {i+1}",
                **kwargs
            )
            for i in range(count)
        ]

@pytest.fixture
def active_user():
    """Fixture for an active user with valid session."""
    return User(
        id="test_user_123",
        email="test@example.com",
        is_active=True,
        created_at=datetime.utcnow() - timedelta(days=30)
    )
```

## ADHD-Friendly Patterns

### Keep Functions Small
```python
# ✅ GOOD: Small, focused functions
def is_task_overdue(task: Task, current_time: datetime) -> bool:
    """Check if task is past its due date."""
    if not task.due_date:
        return False
    return current_time > task.due_date

def format_duration(minutes: int) -> str:
    """Format minutes into human-readable duration."""
    if minutes < 60:
        return f"{minutes} minutes"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes:
        return f"{hours}h {remaining_minutes}m"
    return f"{hours} hours"

# ❌ BAD: Too many responsibilities
def process_and_validate_and_save_task(data, user, db, cache, notifications):
    # 100+ lines doing too many things
    pass
```

### Clear Variable Names
```python
# ✅ GOOD: Descriptive names
tasks_completed_today = filter_tasks_by_date(tasks, today)
minutes_until_break = calculate_remaining_time(session_start, break_duration)
high_priority_tasks = [t for t in tasks if t.priority == "high"]

# ❌ BAD: Unclear abbreviations
tct = filter_t_by_d(t, td)
mub = calc_rem_t(s_s, b_d)
hpt = [x for x in t if x.p == "h"]
```

## Quality Gates

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ["--max-line-length=88", "--extend-ignore=E203"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "src/"]
```

### Required Before Commit
- [ ] All tests pass (pytest)
- [ ] Type checking passes (mypy)
- [ ] Code formatted (black)
- [ ] Imports sorted (isort)
- [ ] Linting passes (flake8/ruff)
- [ ] Security scan passes (bandit)
- [ ] No hardcoded secrets (detect-secrets)
- [ ] Test coverage > 95%

### Performance Checklist
- [ ] Large datasets use generators or pagination
- [ ] Database queries are optimized (use select_related/prefetch_related)
- [ ] Caching implemented where appropriate
- [ ] Async used for I/O-bound operations
- [ ] Memory profiling done for data-heavy operations
- [ ] API responses are paginated

## Code Organization

### Project Structure
```
project/
├── src/
│   ├── api/           # API endpoints
│   ├── core/          # Core business logic
│   ├── models/        # Data models
│   ├── services/      # External service integrations
│   └── utils/         # Utility functions
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/           # Maintenance scripts
└── config/           # Configuration files
```

### Import Organization
```python
# Standard library imports
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict

# Third-party imports
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

# Local application imports
from src.models import Task, User
from src.services.notification import NotificationService
from src.core.validation import validate_task_data
```

## References
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints - PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Python Security Best Practices](https://python.security/)