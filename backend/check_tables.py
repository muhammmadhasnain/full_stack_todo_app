from sqlmodel import select, Session
from src.database.database import engine
from src.models.user import User
from src.models.task import Task
from src.models.task_tag import TaskTag
from src.models.recurrence import RecurrencePattern
from sqlalchemy import inspect

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def list_all_tables():
    """List all tables in the database"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def check_data_exists():
    """Check if any data exists in the user table"""
    try:
        with Session(engine) as session:
            statement = select(User).limit(1)
            result = session.exec(statement).first()
            return result is not None
    except Exception as e:
        print(f"Error checking user data: {e}")
        return False

def main():
    print("Checking database tables...")
    print("=" * 40)

    tables_to_check = [
        ("user", User),
        ("task", Task),
        ("tasktag", TaskTag),
        ("recurrencepattern", RecurrencePattern)
    ]

    print("Tables to check:", [table[0] for table in tables_to_check])
    print()

    all_tables_exist = True
    for table_name, model_class in tables_to_check:
        exists = check_table_exists(table_name)
        status = "[EXISTS]" if exists else "[MISSING]"
        print(f"{status}: {table_name}")
        if not exists:
            all_tables_exist = False

    print()
    print("All tables in database:")
    all_db_tables = list_all_tables()
    for table in all_db_tables:
        print(f"  - {table}")

    print()
    if all_tables_exist:
        print("[SUCCESS] All required tables exist!")

        # Check if there's any user data
        has_users = check_data_exists()
        if has_users:
            print("[INFO] User table has data")
        else:
            print("[INFO] User table exists but is empty")
    else:
        print("[ERROR] Some tables are missing. Creating tables...")
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(bind=engine)
        print("[SUCCESS] Tables created successfully!")

if __name__ == "__main__":
    main()