# TypeScript Code Quality Standards

## Core Principles

### Privacy-First Development
- All data processing should be local-first when possible
- Never log user input or sensitive information
- Implement automatic PII detection and sanitization

### Performance & Memory
- Use React.memo for expensive components
- Implement proper dependency arrays in hooks
- Avoid unnecessary re-renders
- Consider virtualization for large lists

### Type Safety
- Prefer strict TypeScript configuration
- Use branded types for domain concepts
- Avoid `any` - use proper typing
- Implement proper error boundaries

## Essential Rules

### 1. Function & Component Design
```typescript
// ✅ GOOD: Pure, focused functions
const calculateSessionDuration = (startTime: Date, endTime: Date): number => {
  return endTime.getTime() - startTime.getTime();
};

// ✅ GOOD: Proper component typing
interface SessionTimerProps {
  duration: number;
  onComplete: () => void;
}

const SessionTimer: React.FC<SessionTimerProps> = ({ duration, onComplete }) => {
  // Implementation
};

// ❌ BAD: Impure functions with side effects
const calculateAndLogDuration = (start: Date, end: Date) => {
  const duration = end.getTime() - start.getTime();
  console.log('Duration:', duration); // Side effect
  return duration;
};
```

### 2. State Management
```typescript
// ✅ GOOD: Immutable state updates
const [tasks, setTasks] = useState<Task[]>([]);

const addTask = (newTask: Task) => {
  setTasks(prev => [...prev, newTask]);
};

// ✅ GOOD: Proper reducer for complex state
interface SessionState {
  status: 'idle' | 'running' | 'paused' | 'completed';
  remainingTime: number;
  taskId?: string;
}

const sessionReducer = (state: SessionState, action: SessionAction): SessionState => {
  switch (action.type) {
    case 'START_SESSION':
      return { ...state, status: 'running' };
    default:
      return state;
  }
};

// ❌ BAD: Direct state mutation
const addTaskBad = (newTask: Task) => {
  tasks.push(newTask); // Mutation!
  setTasks(tasks);
};
```

### 3. Error Handling
```typescript
// ✅ GOOD: Proper error boundaries and types
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

const fetchUserTasks = async (userId: string): Promise<Result<Task[]>> => {
  try {
    const response = await api.getTasks(userId);
    return { success: true, data: response.data };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error : new Error('Unknown error') 
    };
  }
};

// ✅ GOOD: Error boundary component
const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [hasError, setHasError] = useState(false);
  
  useEffect(() => {
    const handleError = () => setHasError(true);
    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);

  if (hasError) {
    return <ErrorFallback onReset={() => setHasError(false)} />;
  }

  return <>{children}</>;
};
```

### 4. Performance Optimization
```typescript
// ✅ GOOD: Memoized expensive calculations
const ExpensiveComponent: React.FC<{ data: LargeDataset }> = ({ data }) => {
  const processedData = useMemo(() => {
    return data.map(item => performExpensiveCalculation(item));
  }, [data]);

  return <div>{processedData.map(item => <Item key={item.id} data={item} />)}</div>;
};

// ✅ GOOD: Proper callback memoization
const TaskList: React.FC<{ tasks: Task[] }> = ({ tasks }) => {
  const handleTaskComplete = useCallback((taskId: string) => {
    // Handle completion
  }, []); // Empty deps - stable reference

  return (
    <div>
      {tasks.map(task => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onComplete={handleTaskComplete} 
        />
      ))}
    </div>
  );
};
```

### 5. Type Definitions
```typescript
// ✅ GOOD: Branded types for domain concepts
type UserId = string & { readonly brand: unique symbol };
type TaskId = string & { readonly brand: unique symbol };
type SessionId = string & { readonly brand: unique symbol };

// ✅ GOOD: Comprehensive interfaces
interface Task {
  readonly id: TaskId;
  readonly title: string;
  readonly description?: string;
  readonly priority: 'low' | 'medium' | 'high';
  readonly estimatedDuration: number; // milliseconds
  readonly createdAt: Date;
  readonly completedAt?: Date;
}

// ✅ GOOD: Union types for state
type SessionStatus = 'idle' | 'running' | 'paused' | 'completed';
type LoadingState<T> = 
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

## Code Organization

### File Structure
```
src/
├── components/          # Reusable UI components
│   ├── common/         # Generic components
│   └── feature/        # Feature-specific components
├── hooks/              # Custom React hooks
├── services/           # API and business logic
├── stores/             # State management
├── types/              # TypeScript type definitions
└── utils/              # Pure utility functions
```

### Import Organization
```typescript
// 1. External libraries
import React, { useState, useCallback } from 'react';
import { format } from 'date-fns';

// 2. Internal services
import { taskService } from '../services/taskService';

// 3. Internal components
import { TaskItem } from './TaskItem';
import { LoadingSpinner } from '../common/LoadingSpinner';

// 4. Types
import type { Task, TaskStatus } from '../types/task';
```

## ADHD-Friendly Patterns

### Keep Functions Small
```typescript
// ✅ GOOD: Single responsibility, easy to understand
const calculateSessionProgress = (elapsed: number, total: number): number => {
  return Math.min(elapsed / total, 1);
};

const formatSessionTime = (milliseconds: number): string => {
  const minutes = Math.floor(milliseconds / 60000);
  const seconds = Math.floor((milliseconds % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

// ❌ BAD: Too many responsibilities
const processSessionData = (session: Session) => {
  // 50+ lines of mixed concerns
};
```

### Clear Naming
```typescript
// ✅ GOOD: Self-documenting names
const isSessionActive = (status: SessionStatus): boolean => status === 'running';
const hasUserCompletedOnboarding = (user: User): boolean => user.onboardingCompleted;

// ❌ BAD: Unclear abbreviations
const isSessAct = (s: SessionStatus): boolean => s === 'running';
const hasUsrCompOnb = (u: User): boolean => u.onbCompleted;
```

## Quality Gates

### Required Before Commit
- [ ] TypeScript compilation passes with no errors
- [ ] ESLint passes with no violations
- [ ] Prettier formatting applied
- [ ] All tests pass
- [ ] No console.log statements in production code
- [ ] No unused imports or variables

### Performance Checklist
- [ ] Heavy components are memoized
- [ ] Large lists use virtualization
- [ ] API calls are properly cached
- [ ] Images are optimized and lazy-loaded
- [ ] Bundle size impact assessed