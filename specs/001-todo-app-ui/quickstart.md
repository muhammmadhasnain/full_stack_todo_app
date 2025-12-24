# Quickstart Guide: Modern Responsive UI for ToDo Application

**Feature**: 001-todo-app-ui
**Created**: 2025-12-18
**Status**: Draft

## Getting Started

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- A modern browser for development

### Initial Setup

1. **Clone the repository** (if not already done):
```bash
git clone <repository-url>
cd <project-directory>
```

2. **Navigate to the frontend directory**:
```bash
cd frontend
```

3. **Install dependencies**:
```bash
npm install
# or
yarn install
```

4. **Start the development server**:
```bash
npm run dev
# or
yarn dev
```

5. **Open your browser** and navigate to `http://localhost:3000`

### Development Workflow

#### Running the Application
```bash
# Start development server with hot reloading
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run tests
npm run test
```

## Key Components Overview

### Core UI Components

#### TaskCard Component
The primary component for displaying individual tasks with visual indicators for status, priority, and due dates.

**Usage**:
```tsx
<TaskCard
  task={taskData}
  onStatusChange={handleStatusChange}
  variant="default"
/>
```

#### ThemeProvider
Context provider for managing light/dark theme preferences.

**Usage**:
```tsx
import { ThemeProvider } from '@/contexts/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      {/* Your application components */}
    </ThemeProvider>
  );
}
```

#### ResponsiveLayout
Component that adapts the layout based on screen size.

**Usage**:
```tsx
<ResponsiveLayout
  breakpoints={{
    sm: '640px',
    md: '768px',
    lg: '1024px'
  }}
>
  {/* Layout content */}
</ResponsiveLayout>
```

### Design System Configuration

#### Theme Configuration
The application uses a comprehensive theme system with light and dark modes:

```typescript
// Theme configuration is located in:
// frontend/src/styles/theme.ts

const theme = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      // ... more shades
    },
    // ... other color palettes
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  // ... more configuration
};
```

#### Animation Configuration
Smooth animations are implemented using Framer Motion:

```typescript
// Animation configuration is located in:
// frontend/src/lib/animations.ts

const animations = {
  taskCard: {
    enter: { y: 20, opacity: 0, duration: 0.3 },
    exit: { y: -20, opacity: 0, duration: 0.2 },
  },
  // ... more animation configs
};
```

## Development Guidelines

### Component Development

1. **Create new components** in the `frontend/src/components/ui/` directory
2. **Follow the naming convention**: `ComponentName.tsx`
3. **Use TypeScript interfaces** for props
4. **Include proper accessibility attributes**
5. **Implement responsive design** using Tailwind CSS

**Example component structure**:
```tsx
import { Button } from './Button';

interface CardProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function Card({ title, children, className }: CardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-md ${className}`}>
      <h3 className="text-lg font-semibold p-4 border-b">{title}</h3>
      <div className="p-4">{children}</div>
    </div>
  );
}
```

### Styling Guidelines

- Use **Tailwind CSS** utility classes for styling
- Follow the **7-1 pattern** for component organization:
  - `components/ui/` - Reusable UI components
  - `components/forms/` - Form-specific components
  - `components/layout/` - Layout components
- Use **consistent spacing** with the theme's spacing scale
- Ensure **accessibility** with proper contrast ratios

### Responsive Design

The application uses a mobile-first approach with the following breakpoints:

- `sm`: 640px (Mobile)
- `md`: 768px (Tablet)
- `lg`: 1024px (Desktop)
- `xl`: 1280px (Large Desktop)

**Example**:
```tsx
<div className="p-4 sm:p-6 md:p-8">
  {/* Content that adapts to screen size */}
</div>
```

## Theming System

### Light/Dark Mode

The application automatically detects system preference and allows manual override:

```tsx
// Access theme context
import { useTheme } from '@/contexts/ThemeContext';

function MyComponent() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button onClick={toggleTheme}>
      Switch to {theme === 'light' ? 'dark' : 'light'} mode
    </button>
  );
}
```

### Customizing Colors

To add custom colors to the theme:

1. Update `tailwind.config.ts` with new color definitions
2. Add color scales in the theme configuration
3. Test contrast ratios for accessibility

## Animation Guidelines

### Best Practices

- Use **subtle animations** that enhance UX without distracting
- Respect `prefers-reduced-motion` user preference
- Keep animation durations between **200-500ms**
- Use **easing functions** for natural motion

### Common Animation Patterns

```tsx
// Fade in animation
animate="fadeIn"
transition={{ duration: 0.3 }}

// Slide from left
animate={{ x: 0, opacity: 1 }}
initial={{ x: -20, opacity: 0 }}
transition={{ duration: 0.3 }}
```

## Accessibility Guidelines

### Keyboard Navigation

- All interactive elements must be **keyboard accessible**
- Implement proper **focus management**
- Use **logical tab order**
- Add **skip links** for main content

### Screen Reader Support

- Include proper **ARIA labels**
- Use **semantic HTML** elements
- Add **alternative text** for images
- Implement **live regions** for dynamic content

## Testing

### Component Testing

```bash
# Run component tests
npm run test:components

# Run accessibility tests
npm run test:accessibility

# Run visual regression tests
npm run test:visual
```

### Manual Testing Checklist

- [ ] Responsive layout on all target devices
- [ ] Keyboard navigation works properly
- [ ] Screen readers can interpret content correctly
- [ ] Color contrast meets WCAG 2.1 AA standards
- [ ] Animations respect user preferences
- [ ] All interactive elements are accessible

## Deployment

### Build Process

```bash
# Build for production
npm run build

# Verify build
npm run build && npm run start
```

### Environment Configuration

The application supports different environments through environment variables:

```bash
# Environment variables are in:
# .env.development
# .env.production
# .env.local (for local overrides)
```

### Performance Monitoring

- Core Web Vitals are monitored automatically
- Bundle size is checked during build
- Performance budgets are enforced

## Troubleshooting

### Common Issues

**Issue**: Theme not switching properly
**Solution**: Clear browser cache and check ThemeContext implementation

**Issue**: Animations not working
**Solution**: Verify Framer Motion installation and component implementation

**Issue**: Responsive layout breaking
**Solution**: Check Tailwind CSS configuration and responsive class usage

### Getting Help

- Check the **specification documents** in `specs/001-todo-app-ui/`
- Review the **component documentation** in Storybook (when available)
- Consult the **team's design system** documentation