---
id: 0001
title: Frontend Backend Consistency Spec
stage: spec
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-frontend-backend-consistency
branch: 001-frontend-backend-consistency
user: Hasnain
command: /sp.phr
labels: ["spec", "frontend", "backend", "consistency", "api", "schema"]
links:
  spec: "../specs/001-frontend-backend-consistency/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - C:/Users/Hasnain/Desktop/full_stack todo app/specs/001-frontend-backend-consistency/spec.md
  - C:/Users/Hasnain/Desktop/full_stack todo app/specs/001-frontend-backend-consistency/checklists/requirements.md
  - C:/Users/Hasnain/Desktop/full_stack todo app/docs/frontend_backend_consistency_spec.md
tests:
  - none
---

## Prompt

  build a specification                                                    # Frontend-Backend Consistency Specification

## Overview
This document outlines the required changes to ensure consistency between the frontend and backend of the full-stack todo app. It addresses type/schema mismatches, API endpoint inconsistencies, and missing functionality to create a unified experience.

## Identified Issues

### 1. Type/Schema Inconsistencies

**Current State:**
- Backend uses integer IDs (`id: int`, `user_id: int`)
- Frontend expects string IDs (`id: string`, `userId: string`)
- Backend uses datetime objects, frontend expects ISO date strings
- Missing fields in frontend that exist in backend (`created_at`, `updated_at`, `completed_at`)
- Additional fields in frontend not supported by backend (`tags`, `recurrencePattern`)

**Required Changes:**
- Standardize on string UUIDs for all IDs to ensure consistency
- Ensure all datetime fields use ISO 8601 format
- 'medium', 'high'
    due_date: Optional[datetime] = None
    tags: Optional[str] = None  # Comma-separated tags
    is_recurring: bool = False
    recurrence_pattern: Optional[dict] = None

class TaskCreate(TaskBase):
    title: str
    priority: strAdd missing backend fields to frontend types
- Implement missing backend support for frontend features

### 2. API Endpoint Inconsistencies

**Current State:**
- Backend uses integer user_id/task_id in path parameters
- Frontend passes string userId/taskId parameters
- Frontend implements client-side pagination while backend supports server-side pagination

**Required Changes:**
- Align parameter types between frontend and backend
- Implement proper server-side pagination in frontend
- Standardize endpoint contracts

### 3. Authentication Inconsistencies

**Current State:**
- Backend returns UserProfile with integer id
- Frontend expects User with string id

**Required Changes:**
- Standardize user object structure between frontend and backend

## Detailed Specifications

### Backend Changes Required

#### 1. Update Task Model and Schema
```python
# In backend/src/schemas/task.py
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TaskBas
    user_id: str  # Changed from int to str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[dict] = None

class TaskResponse(TaskBase):
    id: str  # Changed from int to str (UUID)
    user_id: str  # Changed from int to str (UUID)
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
```

#### 2. Update User Model and Schema
```python
# In backend/src/schemas/user.py
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class UserProfile(BaseModel):
    id: str  # Changed from int to str (UUID)
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
```

#### 3. Update API Endpoints
- Change all user_id and task_id path parameters from int to str
- Ensure consistent response formats
- Add support for tags and recurrence patterns

### Frontend Changes Required

#### 1. Update Task Type Definitions
```typescript
// In frontend/src/types/task.ts
export interface Task {
  id: string;  // Ensure consistent with backend
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority: 'low' | 'medium' | 'high';
  tags?: string;  // Comma-separated string
  dueDate?: string; // ISO date string
  completed: boolean;
  completedAt?: string; // ISO date string - ADD TO FRONTEND
  recurrencePattern?: RecurrencePattern;
  userId: string;  // Ensure consistent with backend
  createdAt: string; // ISO date string - ADD TO FRONTEND
  updatedAt: string; // ISO date string - ADD TO FRONTEND
}
```

#### 2. Update User Type Definitions
```typescript
// In frontend/src/types/task.ts
export interface User {
  id: string;  // Ensure consistent with backend
  email: string;
  name: string;
  createdAt: string; // ISO date string - ADD TO FRONTEND
  updatedAt: string; // ISO date string - ADD TO FRONTEND
  is_active?: boolean;
}
```

#### 3. Update API Service
- Modify all API calls to use string IDs
- Update pagination to use server-side pagination from backend
- Add support for missing fields in responses

## Migration Strategy

### Phase 1: Backend Schema Updates (Week 1)
1. Update database models to use UUIDs instead of integers
2. Update Pydantic schemas to use string IDs
3. Add missing fields to backend models
4. Update API endpoints to use consistent string parameters
5. Implement tags and recurrence pattern support in backend

### Phase 2: API Contract Alignment (Week 2)
1. Update all endpoint contracts to match new schemas
2. Ensure proper response formats
3. Implement proper server-side pagination
4. Add comprehensive filtering support

### Phase 3: Frontend Updates (Week 3)
1. Update TypeScript interfaces to match backend schemas
2. Modify API service to use new endpoint contracts
3. Update components to handle new fields and data structures
4. Implement proper server-side pagination

### Phase 4: Testing and Validation (Week 4)
1. Comprehensive integration testing
2. Data migration testing
3. End-to-end functionality testing
4. Performance testing with new data structures

## Implementation Priorities

### High Priority (Must Implement)
1. ID type consistency (integer → string/UUID)
2. Date format standardization (datetime → ISO 8601)
3. Missing field support (created_at, updated_at, completed_at)

### Medium Priority (Should Implement)
1. Tags support in backend
2. Recurrence pattern support in backend
3. Server-side pagination implementation

### Low Priority (Nice to Have)
1. Advanced filtering options
2. Enhanced recurrence pattern features
3. Performance optimizations

## Testing Requirements

### Unit Tests
- Test all updated schema validations
- Test API endpoint parameter handling
- Test data conversion functions

### Integration Tests
- Test frontend-backend communication with new schemas
- Test pagination functionality
- Test authentication flow with updated user models

### End-to-End Tests
- Test complete user workflows
- Test data consistency across frontend and backend
- Test error handling with new schemas

## Risk Analysis and Mitigation

### Risk 1: Data Migration Issues
- **Impact**: High - Could cause data loss or corruption
- **Mitigation**: Implement comprehensive backup strategy and phased migration with rollback capability

### Risk 2: API Breaking Changes
- **Impact**: High - Could break existing frontend functionality
- **Mitigation**: Maintain backward compatibility during transition or coordinate simultaneous frontend/backend deployment

### Risk 3: Performance Degradation
- **Impact**: Medium - UUIDs may impact database performance
- **Mitigation**: Optimize database indexes and monitor performance metrics

## Acceptance Criteria

### Backend Acceptance Criteria
1. All API endpoints accept and return string IDs consistently
2. All datetime fields use ISO 8601 format
3. Task responses include all missing fields (created_at, updated_at, completed_at)
4. API properly supports tags and recurrence patterns
5. Server-side pagination works correctly

### Frontend Acceptance Criteria
1. All components work with string IDs consistently
2. All date displays use proper formatting
3. Missing fields are properly displayed in UI
4. Tags and recurrence patterns are supported in UI
5. Pagination uses server-side implementation

### Integration Acceptance Criteria
1. Frontend and backend communicate without type conversion errors
2. All existing functionality continues to work
3. New features (tags, recurrence) work end-to-end
4. Performance meets or exceeds current levels
5. All tests pass successfully

## Deployment Considerations

1. Plan for coordinated deployment of frontend and backend
2. Prepare database migration scripts for ID type changes
3. Schedule maintenance window if needed for data migration
4. Prepare rollback procedures in case of issues
5. Monitor application metrics after deployment

## Response snapshot

Created comprehensive specification for frontend-backend consistency, including feature branch 001-frontend-backend-consistency with proper spec file and quality checklist.

## Outcome

- ✅ Impact: Created complete feature specification addressing all frontend-backend inconsistencies
- 🧪 Tests: none
- 📁 Files: specs/001-frontend-backend-consistency/spec.md, checklists/requirements.md, docs/frontend_backend_consistency_spec.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Proper specification ensures consistent data handling between frontend and backend systems

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
