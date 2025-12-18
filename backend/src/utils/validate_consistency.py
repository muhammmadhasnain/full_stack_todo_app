"""
Consistency validation script for CI/CD pipeline.
Validates consistency requirements FR-001, FR-002, FR-003.
"""
import ast
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


def validate_uuid_consistency() -> Tuple[bool, List[str]]:
    """
    Validate FR-001: System MUST use consistent data types (UUID strings) for all entity IDs across frontend and backend
    """
    errors = []

    # Check backend models
    model_files = Path('backend/src/models').glob('*.py')
    for model_file in model_files:
        with open(model_file, 'r') as f:
            content = f.read()
            if 'id: UUID' not in content and 'id: UUID =' not in content:
                errors.append(f"ERROR: {model_file} - ID field should use UUID type")

    # Check backend schemas
    schema_files = Path('backend/src/schemas').glob('*.py')
    for schema_file in schema_files:
        with open(schema_file, 'r') as f:
            content = f.read()
            if 'id: str' not in content:
                errors.append(f"ERROR: {schema_file} - Schema ID field should be str type")

    # Check frontend types
    frontend_task_file = Path('frontend/src/types/task.ts')
    if frontend_task_file.exists():
        with open(frontend_task_file, 'r') as f:
            content = f.read()
            if not re.search(r'id:\s*string', content):
                errors.append(f"ERROR: {frontend_task_file} - Task interface should have id as string type")
            if not re.search(r'userId:\s*string', content):
                errors.append(f"ERROR: {frontend_task_file} - Task interface should have userId as string type")

    frontend_user_file = Path('frontend/src/types/user.ts')
    if frontend_user_file.exists():
        with open(frontend_user_file, 'r') as f:
            content = f.read()
            if not re.search(r'id:\s*string', content):
                errors.append(f"ERROR: {frontend_user_file} - User interface should have id as string type")

    return len(errors) == 0, errors


def validate_datetime_format_consistency() -> Tuple[bool, List[str]]:
    """
    Validate FR-002: System MUST use ISO 8601 format for all date/time values exchanged between frontend and backend
    """
    errors = []

    # Check backend models for datetime fields
    model_files = Path('backend/src/models').glob('*.py')
    for model_file in model_files:
        with open(model_file, 'r') as f:
            content = f.read()
            # Check for required datetime fields
            required_fields = ['created_at', 'updated_at', 'completed_at', 'due_date']
            for field in required_fields:
                if field in content:
                    if 'datetime' not in content:
                        errors.append(f"ERROR: {model_file} - {field} field should use datetime type")

    # Check frontend types for ISO 8601 format
    frontend_task_file = Path('frontend/src/types/task.ts')
    if frontend_task_file.exists():
        with open(frontend_task_file, 'r') as f:
            content = f.read()
            # Check for ISO datetime field types (should be string in frontend)
            if not re.search(r'createdAt:\s*string', content):
                errors.append(f"ERROR: {frontend_task_file} - createdAt should be string type for ISO format")
            if not re.search(r'updatedAt:\s*string', content):
                errors.append(f"ERROR: {frontend_task_file} - updatedAt should be string type for ISO format")
            if not re.search(r'completedAt:\s*string', content):
                errors.append(f"ERROR: {frontend_task_file} - completedAt should be string type for ISO format")

    return len(errors) == 0, errors


def validate_missing_fields_consistency() -> Tuple[bool, List[str]]:
    """
    Validate FR-003: System MUST support all task fields (created_at, updated_at, completed_at) in both frontend and backend
    """
    errors = []

    # Check backend models for required fields
    model_files = Path('backend/src/models').glob('*.py')
    for model_file in model_files:
        with open(model_file, 'r') as f:
            content = f.read()
            required_fields = ['created_at', 'updated_at', 'completed_at']
            for field in required_fields:
                if field not in content:
                    errors.append(f"ERROR: {model_file} - Missing required field: {field}")

    # Check backend schemas for required fields
    schema_files = Path('backend/src/schemas').glob('*.py')
    for schema_file in schema_files:
        with open(schema_file, 'r') as f:
            content = f.read()
            required_fields = ['created_at', 'updated_at', 'completed_at']
            for field in required_fields:
                if field not in content:
                    errors.append(f"ERROR: {schema_file} - Missing required field: {field}")

    # Check frontend types for required fields
    frontend_task_file = Path('frontend/src/types/task.ts')
    if frontend_task_file.exists():
        with open(frontend_task_file, 'r') as f:
            content = f.read()
            required_fields = ['createdAt', 'updatedAt', 'completedAt']
            for field in required_fields:
                if not re.search(f'{field}:\\s*string', content):
                    errors.append(f"ERROR: {frontend_task_file} - Missing required field: {field}")

    return len(errors) == 0, errors


def validate_api_endpoint_consistency() -> Tuple[bool, List[str]]:
    """
    Validate API endpoints use consistent UUID string parameters
    """
    errors = []

    # Check API files for UUID string parameter handling
    api_files = Path('backend/src/api').glob('*.py')
    for api_file in api_files:
        with open(api_file, 'r') as f:
            content = f.read()
            # Check for proper UUID string handling in path parameters
            if 'user_id: str' not in content and 'task_id: str' not in content:
                errors.append(f"WARNING: {api_file} - Check that path parameters use str type for UUIDs")

    return len(errors) == 0, errors


def main():
    """
    Main validation function for CI/CD pipeline
    """
    print("Running consistency validation checks...")

    # Validate FR-001: UUID consistency
    print("\n1. Validating UUID string consistency (FR-001)...")
    uuid_valid, uuid_errors = validate_uuid_consistency()
    for error in uuid_errors:
        print(error)
    if uuid_valid:
        print("[PASS] UUID consistency validation passed")
    else:
        print("[FAIL] UUID consistency validation failed")

    # Validate FR-002: DateTime format consistency
    print("\n2. Validating ISO 8601 datetime format consistency (FR-002)...")
    datetime_valid, datetime_errors = validate_datetime_format_consistency()
    for error in datetime_errors:
        print(error)
    if datetime_valid:
        print("[PASS] DateTime format consistency validation passed")
    else:
        print("[FAIL] DateTime format consistency validation failed")

    # Validate FR-003: Missing fields consistency
    print("\n3. Validating missing fields consistency (FR-003)...")
    fields_valid, fields_errors = validate_missing_fields_consistency()
    for error in fields_errors:
        print(error)
    if fields_valid:
        print("[PASS] Missing fields consistency validation passed")
    else:
        print("[FAIL] Missing fields consistency validation failed")

    # Validate API endpoint consistency
    print("\n4. Validating API endpoint consistency...")
    api_valid, api_errors = validate_api_endpoint_consistency()
    for error in api_errors:
        print(error)
    if api_valid:
        print("[PASS] API endpoint consistency validation passed")
    else:
        print("[FAIL] API endpoint consistency validation failed")

    # Overall result
    all_valid = uuid_valid and datetime_valid and fields_valid
    print(f"\nOverall consistency validation: {'PASSED' if all_valid else 'FAILED'}")

    if not all_valid:
        print("\nConsistency validation failed. Please fix the above issues before merging.")
        exit(1)
    else:
        print("\nAll consistency requirements validated successfully!")
        exit(0)


if __name__ == "__main__":
    main()