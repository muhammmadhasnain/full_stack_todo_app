# UI Component Contracts: Modern Responsive ToDo Application

**Feature**: 001-todo-app-ui
**Created**: 2025-12-18

## Component API Contracts

### TaskCard Component Contract

**Interface**:
```typescript
interface TaskCardProps {
  task: Task;
  onStatusChange?: (taskId: string, newStatus: TaskStatus) => void;
  onPriorityChange?: (taskId: string, newPriority: TaskPriority) => void;
  onDueDateChange?: (taskId: string, newDueDate: Date) => void;
  onDelete?: (taskId: string) => void;
  onEdit?: (taskId: string) => void;
  className?: string;
  variant?: 'compact' | 'default' | 'expanded';
  showActions?: boolean;
  animationEnabled?: boolean;
}

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on-hold';
  priority: 'low' | 'medium' | 'high';
  dueDate?: Date;
  completedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

**Behavior Contract**:
- **Input Validation**: Accepts valid Task object with required fields
- **Event Handling**: Emits status/priority changes via callback props
- **Rendering**: Displays task information with appropriate visual indicators
- **Accessibility**: Provides keyboard navigation and screen reader support
- **Animation**: Smooth transitions when animationEnabled is true
- **Responsive**: Adapts layout based on variant and screen size

**Success Path**:
1. Component receives valid Task object
2. Renders task with appropriate status/priority indicators
3. Handles user interactions and emits events
4. Maintains visual consistency with theme

**Error Path**:
1. Component receives invalid Task object
2. Falls back to default rendering with error state
3. Logs error to console in development mode
4. Maintains basic functionality

### ThemeProvider Contract

**Interface**:
```typescript
interface ThemeProviderProps {
  children: React.ReactNode;
  defaultTheme?: 'light' | 'dark';
  storageKey?: string;
}

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  isDarkMode: boolean;
}
```

**Behavior Contract**:
- **Initialization**: Detects system preference or uses default theme
- **Persistence**: Stores theme preference in localStorage
- **Context Provision**: Provides theme state to child components
- **Theme Switching**: Smooth transition between themes
- **Event Handling**: Responds to system theme changes

**Success Path**:
1. Provider initializes with system or stored theme
2. Provides context to all child components
3. Handles theme changes with persistence
4. Updates CSS variables for theme application

**Error Path**:
1. Storage access fails
2. Falls back to default theme
3. Continues operation without persistence
4. Logs error for monitoring

### Input Component Contract

**Interface**:
```typescript
interface InputProps {
  label?: string;
  placeholder?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'success' | 'error' | 'warning';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  required?: boolean;
  type?: 'text' | 'email' | 'password' | 'date' | 'number';
  iconLeft?: React.ReactNode;
  iconRight?: React.ReactNode;
  className?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
  onFocus?: () => void;
}
```

**Behavior Contract**:
- **Validation**: Applies appropriate styling based on variant
- **Accessibility**: Proper labeling and ARIA attributes
- **Interaction**: Handles focus, blur, and change events
- **Visual Feedback**: Shows error/validation states
- **Keyboard Support**: Full keyboard navigation support

### Modal Component Contract

**Interface**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  className?: string;
}
```

**Behavior Contract**:
- **State Management**: Controls open/closed state
- **Focus Management**: Traps focus within modal
- **Keyboard Handling**: Closes on Escape key
- **Accessibility**: Proper ARIA roles and attributes
- **Animation**: Smooth enter/exit animations

## API Integration Contracts

### Task API Response Contract
```typescript
interface TaskApiResponse {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on-hold';
  priority: 'low' | 'medium' | 'high';
  due_date?: string; // ISO 8601 format
  completed_at?: string; // ISO 8601 format
  created_at: string; // ISO 8601 format
  updated_at: string; // ISO 8601 format
  recurrence_pattern?: RecurrencePattern;
}
```

**UI Handling Contract**:
- **Date Parsing**: Converts ISO strings to Date objects
- **Null Handling**: Properly handles optional fields
- **Error States**: Handles API errors gracefully
- **Loading States**: Shows appropriate loading indicators

### Theme API Contract (if applicable)
```typescript
interface ThemePreferences {
  theme: 'light' | 'dark' | 'system';
  updated_at: string;
}
```

## Animation Contracts

### Framer Motion Integration Contract
```typescript
interface AnimationProps {
  animate: object | string;
  initial: object | string;
  exit: object | string;
  transition: {
    duration: number;
    ease: string | number[];
    delay?: number;
  };
  layout?: boolean;
  layoutId?: string;
}
```

**Performance Contract**:
- **Frame Rate**: Maintains 60fps during animations
- **Reduced Motion**: Respects user's reduced motion preference
- **Duration**: Animation durations between 200-500ms
- **Easing**: Uses performance-optimized easing functions

## Accessibility Contracts

### ARIA Attributes Contract
```typescript
interface AriaAttributes {
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-labelledby'?: string;
  'aria-hidden'?: boolean;
  'aria-expanded'?: boolean;
  'aria-selected'?: boolean;
  'aria-current'?: boolean;
  role?: string;
}
```

**Compliance Contract**:
- **Screen Reader**: All content is accessible to screen readers
- **Keyboard Navigation**: Full keyboard operation support
- **Focus Management**: Proper focus handling for interactive elements
- **Color Independence**: Functionality doesn't rely solely on color

## Responsive Design Contracts

### Breakpoint Contract
```typescript
interface Breakpoints {
  sm: '640px';
  md: '768px';
  lg: '1024px';
  xl: '1280px';
  '2xl': '1536px';
}
```

**Layout Contract**:
- **Mobile-First**: Styles start from mobile and scale up
- **Adaptive**: Layout adjusts based on available space
- **Touch-Friendly**: Touch targets meet 44px minimum
- **Performance**: Responsive changes don't impact performance

## Error Handling Contracts

### Component Error Boundary Contract
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}
```

**Error Contract**:
- **Isolation**: Errors don't affect parent components
- **Fallback**: Provides graceful fallback UI
- **Logging**: Errors are logged for monitoring
- **Recovery**: Allows user to recover from errors

## Performance Contracts

### Rendering Performance
- **Component Render Time**: < 16ms for smooth 60fps
- **Bundle Size**: < 250KB for initial load
- **Memory Usage**: Efficient memory management
- **Animation Performance**: 60fps maintained during animations

### Loading Performance
- **LCP**: < 2.5 seconds
- **FID**: < 100ms
- **CLS**: < 0.1
- **TTFB**: < 600ms

## Testing Contracts

### Component Testing Contract
- **Unit Tests**: 100% of components have unit tests
- **Accessibility Tests**: All components pass accessibility tests
- **Responsive Tests**: Components tested at all breakpoints
- **Performance Tests**: Performance metrics validated
- **Cross-browser Tests**: Functionality verified across browsers

### Integration Testing Contract
- **API Integration**: All API contracts validated
- **State Management**: State flows tested end-to-end
- **User Flows**: Complete user journeys validated
- **Error Scenarios**: Error handling tested thoroughly