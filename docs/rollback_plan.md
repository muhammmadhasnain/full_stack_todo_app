# Rollback Plan for Migration Issues (MIG-002)

This document outlines the rollback procedures for reverting the frontend-backend consistency changes in case of critical issues during or after the migration.

## Rollback Triggers

Rollback should be initiated if any of the following occur:
- Data integrity issues (corrupted or lost data)
- Critical system failures affecting >5% of users
- Performance degradation >50% from baseline
- Authentication/security issues
- >10% of API requests failing

## Rollback Timeline

- **Phase 1**: Immediate service preservation (0-15 minutes)
- **Phase 2**: Data rollback (15-60 minutes)
- **Phase 3**: System restoration (60-120 minutes)
- **Phase 4**: Validation and monitoring (2-4 hours)

## Pre-Migration Safeguards

### Database Backups
- Full database backup before migration starts
- Backup stored in secure, separate location
- Backup verification script executed before migration
- Point-in-time recovery snapshot created

### Feature Flags
- All new features controlled by feature flags
- Flags default to "off" state
- Gradual rollout with user segmentation
- Emergency disable capability

## Rollback Procedures

### 1. Service Preservation (Immediate)
1. **Disable new endpoints**: Return 503 for v1 API requests
2. **Activate maintenance mode**: Display maintenance page to users
3. **Scale down new services**: Reduce resources for new features
4. **Monitor alerts**: Track system health metrics

### 2. Database Rollback
1. **Stop all write operations**: Prevent data changes during rollback
2. **Restore from backup**: Use pre-migration backup to restore database
3. **Verify data integrity**: Run data validation scripts
4. **Update schema**: Revert to original integer ID schema if needed

### 3. Application Rollback
1. **Deploy previous version**: Roll back to last stable code version
2. **Update configuration**: Revert environment variables and settings
3. **Restart services**: Ensure clean state after rollback
4. **Verify functionality**: Test core features

### 4. Frontend Rollback
1. **Revert to stable build**: Deploy previous frontend version
2. **Update API endpoints**: Point to stable backend endpoints
3. **Clear user caches**: Invalidate browser caches and local storage
4. **Test user workflows**: Verify core functionality

## Rollback Scripts

### Database Rollback Script
```bash
#!/bin/bash
# rollback_database.sh

set -e

echo "Starting database rollback..."

# Stop application services
docker-compose scale api=0

# Restore from backup
pg_restore --verbose --clean --no-acl --no-owner -U todo_user -d todo_db /backups/pre_migration.backup

# Update sequences for integer IDs
psql -U todo_user -d todo_db -c "SELECT setval('user_id_seq', (SELECT MAX(id) FROM users));"
psql -U todo_user -d todo_db -c "SELECT setval('task_id_seq', (SELECT MAX(id) FROM tasks));"

echo "Database rollback completed."
```

### Application Rollback Script
```bash
#!/bin/bash
# rollback_application.sh

set -e

echo "Starting application rollback..."

# Pull previous stable version
git checkout main
git pull origin main
git checkout $(git describe --tags --abbrev=0 $(git describe --tags --abbrev=0)^)

# Build and deploy previous version
docker build -t todo-app:previous .
docker tag todo-app:previous todo-app:latest
docker-compose up -d --no-deps api

echo "Application rollback completed."
```

## Data Validation After Rollback

### User Data Verification
- Verify user accounts exist and are accessible
- Check that user profiles contain correct information
- Validate that user permissions are preserved

### Task Data Verification
- Confirm all tasks are accessible to correct users
- Verify task statuses, priorities, and metadata
- Check that task relationships (tags, recurrence) are intact

### Authentication Data Verification
- Test login functionality for various user accounts
- Verify session management works correctly
- Confirm password hashes are valid

## Communication Plan

### Internal Team
- **Alert system**: Automated notifications to #alerts channel
- **Incident commander**: Designated person to coordinate rollback
- **Engineering team**: On-call engineers to execute procedures
- **Product team**: To communicate with stakeholders

### External Communication
- **Status page**: Update status.todoapp.com with rollback status
- **Email notifications**: For registered users if needed
- **Social media**: For major incidents affecting many users
- **Support team**: Provide talking points for customer inquiries

## Rollback Testing

### Pre-Implementation Testing
- Test rollback procedures in staging environment
- Verify backup restoration process
- Test feature flag toggling
- Validate data integrity checks

### Post-Rollback Validation
- Execute smoke tests on core functionality
- Run performance tests to ensure baseline performance
- Verify user authentication and authorization
- Test API endpoints and data consistency

## Rollback Team Responsibilities

- **System Administrator**: Execute database rollback procedures
- **Backend Engineer**: Handle API rollback and data validation
- **Frontend Engineer**: Manage frontend rollback and user experience
- **DevOps Engineer**: Coordinate deployment and monitoring
- **Product Manager**: Communicate with stakeholders and users

## Success Criteria for Rollback

- All users can access their accounts and data
- Core functionality (create, read, update, delete tasks) works
- Performance metrics return to baseline levels
- Zero data loss or corruption
- User authentication and security intact

## Post-Rollback Actions

1. **Investigation**: Determine root cause of the issue that required rollback
2. **Fix Development**: Create fixes for the original problem
3. **Enhanced Testing**: Add tests to prevent similar issues
4. **Re-Migration Planning**: Plan next migration attempt with fixes
5. **Documentation Update**: Update this rollback plan based on lessons learned

## Contact Information

- **Primary On-Call**: [Phone Number]
- **DevOps Team**: [Email/Slack Channel]
- **Database Admin**: [Email/Slack Channel]
- **Security Contact**: [Email/Phone]