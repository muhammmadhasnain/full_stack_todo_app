# API Versioning Strategy

This document outlines the API versioning strategy implemented during the frontend-backend consistency transition to maintain backward compatibility.

## Versioning Approach

The API uses a path-based versioning strategy with the following pattern:
- Base URL: `https://api.todoapp.com/v1/`
- Current version: `v1` (default if no version specified)

## Version Support Policy

- **Active Versions**: v1 (current)
- **Deprecated Versions**: None
- **End-of-Life Policy**: Deprecated versions will be maintained for 6 months after announcement

## Migration Timeline

### Phase 1: Introduction of v1 (Current)
- All new features and consistency fixes are available in v1
- Existing endpoints remain functional at the root path (backwards compatibility)
- Dual format support (integer IDs and UUIDs) available during transition

### Phase 2: Transition Period (Next 3 months)
- Encourage migration to v1 endpoints
- Deprecation notices added to root path endpoints
- Continued support for legacy integer IDs with migration utilities

### Phase 3: Full Migration (After 3 months)
- Root path endpoints will redirect to v1
- Legacy integer ID support maintained with warnings
- Complete UUID string ID enforcement planned for v2

## API Endpoints Version Mapping

### Current Endpoints (Root/Default)
- `/users/{user_id}/tasks` → `/v1/users/{user_id}/tasks`
- `/users/{user_id}/tasks/{task_id}` → `/v1/users/{user_id}/tasks/{task_id}`
- All other endpoints follow the same pattern

### New v1 Endpoints with Consistency Fixes
- All endpoints return UUID string IDs instead of integer IDs
- All datetime fields use ISO 8601 format consistently
- All endpoints support tags and recurrence patterns
- Proper server-side pagination with total count

## Response Format Changes

### Before (Legacy)
```json
{
  "id": 123,
  "user_id": 456,
  "title": "Sample Task",
  "created_at": "2023-10-05T14:48:00",
  "tags": null,
  "recurrence_pattern": null
}
```

### After (v1)
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "user_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "title": "Sample Task",
  "created_at": "2023-10-05T14:48:00Z",
  "tags": "work,important",
  "recurrence_pattern": {
    "type": "weekly",
    "interval": 1,
    "end_date": "2024-12-31T00:00:00Z"
  }
}
```

## Request Format Changes

### Before (Legacy)
```json
{
  "title": "New Task",
  "user_id": 456,
  "due_date": "2023-12-31 23:59:59"
}
```

### After (v1)
```json
{
  "title": "New Task",
  "user_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "due_date": "2023-12-31T23:59:59Z",
  "tags": "work,important",
  "recurrence_pattern": {
    "type": "daily",
    "interval": 1
  }
}
```

## Backward Compatibility Measures

1. **Dual Format Support**: During transition, APIs accept both integer and UUID user/task IDs
2. **Graceful Degradation**: Legacy endpoints continue to work but return deprecation warnings
3. **Migration Utilities**: Helper endpoints to convert integer IDs to UUIDs
4. **Documentation**: Clear migration guides for API consumers

## Deprecation Notices

All legacy endpoints return a `X-API-Deprecated` header indicating the replacement endpoint and timeline for removal.

## Client Migration Guide

### For Frontend Applications
1. Update API client to use v1 endpoints
2. Update TypeScript interfaces to handle UUID strings and ISO datetime formats
3. Implement proper tag and recurrence pattern support
4. Update pagination logic to use server-side pagination with total count

### For Third-Party Integrations
1. Update base API URL to include `/v1/` path
2. Update ID handling to work with UUID strings
3. Update datetime parsing to handle ISO 8601 format
4. Implement support for new fields (tags, recurrence patterns)

## Monitoring and Rollback

API performance and usage metrics are monitored during the transition period to ensure stability and guide migration decisions. A complete rollback plan is documented in `rollback_plan.md` in case of critical issues.