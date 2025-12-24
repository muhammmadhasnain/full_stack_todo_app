# Data Model: UI Components for Modern ToDo Application

**Feature**: 001-todo-app-ui
**Created**: 2025-12-18
**Status**: Draft

## Component Data Structures

### Task Card Data Model

```typescript
interface TaskCardData {
  // Basic task information
  id: string;
  title: string;
  description?: string;
  createdAt: Date;
  updatedAt: Date;

  // Status and priority
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on-hold';
  priority: 'low' | 'medium' | 'high';

  // Timing information
  dueDate?: Date;
  completedAt?: Date;

  // Recurrence pattern (if applicable)
  recurrencePattern?: {
    type: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';
    interval: number;
    endDate?: Date;
    daysOfWeek?: number[]; // 0 = Sunday, 1 = Monday, etc.
  };

  // UI-specific metadata
  isExpanded?: boolean;
  isSelected?: boolean;
  isDragging?: boolean;
}

interface TaskCardDisplayConfig {
  // Visual appearance
  showPriorityBadge: boolean;
  showDueDate: boolean;
  showStatusIndicator: boolean;
  showDescription: boolean;
  showActions: boolean;

  // Interaction behavior
  enableDragAndDrop: boolean;
  enableQuickActions: boolean;
  enableContextMenu: boolean;

  // Animation settings
  animationEnabled: boolean;
  animationDuration: number; // in ms
  animationType: 'slide' | 'fade' | 'scale';
}
```

### Theme Configuration Model

```typescript
interface ThemeConfig {
  // Theme identification
  id: string;
  name: string;
  type: 'light' | 'dark';

  // Color palette
  colors: {
    primary: ColorPalette;
    secondary: ColorPalette;
    success: ColorPalette;
    warning: ColorPalette;
    error: ColorPalette;
    neutral: ColorPalette;
    background: ColorPalette;
    text: ColorPalette;
    border: ColorPalette;
  };

  // Typography settings
  typography: {
    fontFamily: string;
    sizes: {
      xs: string; // 0.75rem
      sm: string; // 0.875rem
      base: string; // 1rem
      lg: string; // 1.125rem
      xl: string; // 1.25rem
      '2xl': string; // 1.5rem
      '3xl': string; // 1.875rem
      '4xl': string; // 2.25rem
      '5xl': string; // 3rem
      '6xl': string; // 3.75rem
    };
    weights: {
      thin: number;    // 100
      extralight: number; // 200
      light: number;   // 300
      normal: number;  // 400
      medium: number;  // 500
      semibold: number; // 600
      bold: number;    // 700
      extrabold: number; // 800
      black: number;   // 900
    };
    lineHeight: {
      none: number;    // 1
      tight: number;   // 1.25
      snug: number;    // 1.375
      normal: number;  // 1.5
      relaxed: number; // 1.625
      loose: number;   // 2
    };
  };

  // Spacing system
  spacing: {
    units: number[]; // [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 72, 80, 96];
    containerPadding: string;
    gridGap: string;
  };

  // Component-specific overrides
  components: {
    button: ButtonTheme;
    input: InputTheme;
    card: CardTheme;
    modal: ModalTheme;
  };
}

interface ColorPalette {
  50: string;   // Lightest
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;  // Base
  600: string;
  700: string;
  800: string;
  900: string;  // Darkest
}

interface ButtonTheme {
  primary: {
    bg: string;
    text: string;
    border: string;
    hoverBg: string;
    hoverText: string;
    activeBg: string;
    disabledBg: string;
    disabledText: string;
  };
  secondary: {
    bg: string;
    text: string;
    border: string;
    hoverBg: string;
    hoverText: string;
    activeBg: string;
    disabledBg: string;
    disabledText: string;
  };
  sizes: {
    sm: { padding: string; fontSize: string; height: string };
    md: { padding: string; fontSize: string; height: string };
    lg: { padding: string; fontSize: string; height: string };
  };
  radius: string;
  shadow: string;
}
```

### Animation Configuration Model

```typescript
interface AnimationConfig {
  // Global animation settings
  enabled: boolean;
  duration: {
    short: number;  // 150ms
    medium: number; // 300ms
    long: number;   // 500ms
  };
  easing: {
    easeIn: string;
    easeOut: string;
    easeInOut: string;
    linear: string;
  };

  // Component-specific animations
  components: {
    taskCard: TaskCardAnimation;
    modal: ModalAnimation;
    dropdown: DropdownAnimation;
    loading: LoadingAnimation;
  };

  // Performance settings
  performanceMode: 'smooth' | 'fast' | 'eco'; // Adjusts animation complexity based on device
  prefersReducedMotion: boolean; // Respects user's system preference
}

interface TaskCardAnimation {
  enter: {
    y: number;
    opacity: number;
    scale: number;
    duration: number;
    delay: number;
  };
  exit: {
    y: number;
    opacity: number;
    scale: number;
    duration: number;
  };
  drag: {
    scale: number;
    rotate: number;
    transition: {
      type: string;
      stiffness: number;
      damping: number;
    };
  };
  hover: {
    scale: number;
    y: number;
    transition: {
      type: string;
      duration: number;
    };
  };
}

interface ModalAnimation {
  enter: {
    scale: number;
    opacity: number;
    duration: number;
  };
  exit: {
    scale: number;
    opacity: number;
    duration: number;
  };
  backdrop: {
    opacity: number;
    duration: number;
  };
}
```

### Responsive Breakpoints Model

```typescript
interface ResponsiveConfig {
  breakpoints: {
    sm: string;  // 640px
    md: string;  // 768px
    lg: string;  // 1024px
    xl: string;  // 1280px
    '2xl': string; // 1536px
  };

  componentVariants: {
    taskCard: {
      sm: TaskCardDisplayConfig;
      md: TaskCardDisplayConfig;
      lg: TaskCardDisplayConfig;
      xl: TaskCardDisplayConfig;
    };
    taskList: {
      sm: TaskListDisplayConfig;
      md: TaskListDisplayConfig;
      lg: TaskListDisplayConfig;
      xl: TaskListDisplayConfig;
    };
    navigation: {
      sm: NavigationDisplayConfig;
      md: NavigationDisplayConfig;
      lg: NavigationDisplayConfig;
      xl: NavigationDisplayConfig;
    };
  };
}

interface TaskListDisplayConfig {
  columns: number;           // Number of columns to display
  cardSize: 'compact' | 'normal' | 'expanded';
  showFilters: boolean;
  showSortOptions: boolean;
  showSearch: boolean;
  itemsPerPage: number;
}

interface NavigationDisplayConfig {
  orientation: 'vertical' | 'horizontal';
  collapsible: boolean;
  showLabels: boolean;
  compactOnMobile: boolean;
}
```

### Accessibility Configuration Model

```typescript
interface AccessibilityConfig {
  // Screen reader settings
  screenReader: {
    enabled: boolean;
    announcementDelay: number; // Time to wait before announcing changes
  };

  // Keyboard navigation
  keyboard: {
    shortcuts: {
      global: {
        'Escape': string;    // Close modal/dialog
        'Ctrl+K': string;    // Open search
        'Ctrl+N': string;    // Create new task
        'Ctrl+Shift+N': string; // Navigate to next section
      };
      taskCard: {
        'Space': string;     // Toggle completion
        'Enter': string;     // Edit task
        'Delete': string;    // Delete task
        'ArrowUp': string;   // Move to previous task
        'ArrowDown': string; // Move to next task
      };
    };
    focusOrder: string[];    // Custom focus order for complex components
    focusIndicator: {
      width: string;
      style: string;
      color: string;
      offset: string;
    };
  };

  // Visual adjustments
  visual: {
    highContrastMode: boolean;
    reduceMotion: boolean;
    largeTextMode: boolean;
  };

  // ARIA attributes configuration
  aria: {
    liveRegions: {
      polite: string[];      // Elements that should announce updates politely
      assertive: string[];   // Elements that should announce updates assertively
    };
    landmarks: {
      banner: boolean;
      navigation: boolean;
      main: boolean;
      complementary: boolean;
      contentinfo: boolean;
    };
  };
}
```

### User Preference Model

```typescript
interface UserPreferences {
  // Theme preferences
  theme: {
    current: 'light' | 'dark' | 'system';
    systemPreference: 'light' | 'dark';
    lastManualSelection?: 'light' | 'dark';
    timestamp: Date;
  };

  // Display preferences
  display: {
    compactView: boolean;
    showCompletedTasks: boolean;
    defaultTaskView: 'list' | 'grid' | 'kanban';
    itemsPerPage: number;
  };

  // Notification preferences
  notifications: {
    email: boolean;
    push: boolean;
    sound: boolean;
    dueDateReminders: {
      enabled: boolean;
      timeBefore: '1h' | '24h' | '1w';
    };
  };

  // Privacy settings
  privacy: {
    analytics: boolean;
    performanceTracking: boolean;
    errorReporting: boolean;
  };

  // Accessibility preferences
  accessibility: {
    reducedMotion: boolean;
    highContrast: boolean;
    largeText: boolean;
    screenReader: boolean;
  };
}
```

## Data Relationships

### Component Hierarchy Relationships
```
Layout
├── Header (depends on ThemeConfig)
│   ├── Navigation (depends on UserPreferences.display)
│   └── UserMenu (depends on UserPreferences.theme)
├── MainContent (depends on ResponsiveConfig)
│   ├── TaskFilterBar (depends on ThemeConfig, UserPreferences.display)
│   ├── TaskList (depends on TaskCardData[], AnimationConfig)
│   │   └── TaskCard (depends on TaskCardData, TaskCardDisplayConfig)
│   └── TaskCreationForm (depends on ThemeConfig, AccessibilityConfig)
└── Footer (depends on ThemeConfig)
```

### Theme Inheritance Chain
```
BaseTheme (default values)
├── LightTheme (overrides for light mode)
├── DarkTheme (overrides for dark mode)
└── UserCustomTheme (user-specific overrides)
```

### Animation Dependency Chain
```
GlobalAnimationConfig
├── ComponentAnimationConfig
│   ├── TaskCardAnimation
│   ├── ModalAnimation
│   └── ButtonAnimation
└── ReducedMotionOverride (when user prefers reduced motion)
```

## Validation Rules

### Theme Configuration Validation
- All color values must be valid CSS color formats (hex, rgb, hsl)
- Contrast ratios must meet WCAG 2.1 AA standards (minimum 4.5:1)
- Font sizes must be within reasonable ranges (12px to 72px)
- Spacing values must be positive numbers or valid CSS units

### Animation Configuration Validation
- Duration values must be positive numbers (in milliseconds)
- Easing functions must be valid CSS easing functions
- Performance mode must be one of: 'smooth', 'fast', 'eco'
- Animation settings must respect user's prefers-reduced-motion preference

### Responsive Configuration Validation
- Breakpoint values must be valid CSS media query values
- Component variants must be defined for all breakpoints
- Column counts must be positive integers
- Mobile-first approach must be maintained (smallest to largest)

### Accessibility Configuration Validation
- Keyboard shortcuts must not conflict with system shortcuts
- Focus indicators must be visible (minimum 2px width)
- ARIA attributes must follow WAI-ARIA specifications
- Screen reader announcements must be concise and informative