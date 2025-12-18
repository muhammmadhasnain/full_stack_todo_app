#!/usr/bin/env python3
"""
Script to test Neon PostgreSQL database connection
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import psycopg2
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def test_raw_psycopg2_connection(database_url):
    """Test connection using raw psycopg2"""
    print("Testing connection with raw psycopg2...")
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        print(f"Connecting to host: {parsed.hostname}:{parsed.port}")
        print(f"Database: {parsed.path[1:]}")  # Remove leading '/'

        # Connect using psycopg2
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading '/'
            user=parsed.username,
            password=parsed.password
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"[SUCCESS] Successfully connected to PostgreSQL!")
        print(f"PostgreSQL version: {db_version[0]}")

        # Test with a simple query
        cursor.execute("SELECT NOW();")
        current_time = cursor.fetchone()
        print(f"Current server time: {current_time[0]}")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"[ERROR] psycopg2 connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error during psycopg2 connection: {e}")
        return False

def test_sqlalchemy_connection(database_url):
    """Test connection using SQLAlchemy"""
    print("\nTesting connection with SQLAlchemy...")
    try:
        # Create engine
        engine = create_engine(
            database_url,
            pool_size=1,
            max_overflow=0,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 10,
            }
        )

        # Test the connection
        with engine.connect() as connection:
            # Execute a simple query
            result = connection.execute(text("SELECT version();"))
            db_version = result.fetchone()[0]
            print(f"[SUCCESS] Successfully connected to PostgreSQL using SQLAlchemy!")
            print(f"PostgreSQL version: {db_version}")

            # Test with current timestamp
            result = connection.execute(text("SELECT NOW();"))
            current_time = result.fetchone()[0]
            print(f"Current server time: {current_time}")

            # Test with a basic table existence check
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                );
            """))
            tables_exist = result.fetchone()[0]
            print(f"Tables exist in public schema: {tables_exist}")

        return True

    except OperationalError as e:
        print(f"[ERROR] SQLAlchemy connection failed: {e}")
        if "Connection refused" in str(e):
            print("   This usually means the host/port is incorrect or the database is not accessible")
        elif "authentication failed" in str(e):
            print("   This usually means the username/password is incorrect")
        elif "database" in str(e) and "does not exist" in str(e):
            print("   This means the database name is incorrect")
        return False
    except SQLAlchemyError as e:
        print(f"[ERROR] SQLAlchemy error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error during SQLAlchemy connection: {e}")
        return False

def verify_database_url_format(database_url):
    """Verify the database URL format"""
    print(f"\nVerifying database URL format...")
    if not database_url:
        print("❌ Database URL is empty or not set")
        return False

    expected_prefixes = ['postgresql://', 'postgresql+psycopg2://', 'postgres://']
    valid_prefix = any(database_url.startswith(prefix) for prefix in expected_prefixes)

    if not valid_prefix:
        print(f"❌ Invalid database URL format. Expected prefixes: {expected_prefixes}")
        print(f"   Current URL: {database_url}")
        return False

    print(f"[SUCCESS] Database URL format appears valid")
    print(f"   URL: {database_url[:50]}..." if len(database_url) > 50 else f"   URL: {database_url}")
    return True

def main():
    """Main function to test database connection"""
    print("Neon PostgreSQL Database Connection Test")
    print("=" * 50)

    # Get the database URL from environment
    database_url = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] No database URL found in environment variables")
        print("   Please set either NEON_DATABASE_URL or DATABASE_URL in your .env file")
        sys.exit(1)

    print(f"Using database URL from environment variable")

    # Verify URL format
    if not verify_database_url_format(database_url):
        sys.exit(1)

    # Test raw psycopg2 connection
    psycopg2_success = test_raw_psycopg2_connection(database_url)

    # Test SQLAlchemy connection
    sqlalchemy_success = test_sqlalchemy_connection(database_url)

    print("\n" + "=" * 50)
    print("CONNECTION SUMMARY:")
    print(f"psycopg2 connection: {'[SUCCESS]' if psycopg2_success else '[FAILED]'}")
    print(f"SQLAlchemy connection: {'[SUCCESS]' if sqlalchemy_success else '[FAILED]'}")

    if psycopg2_success or sqlalchemy_success:
        print("\n[SUCCESS] Database connection successful!")
        print("Your Neon PostgreSQL database is accessible.")

        # Additional tips
        print("\nNext steps:")
        print("- You can now run your application with the configured database URL")
        print("- Remember to run database migrations if this is a new setup")
        print("- Consider using connection pooling for production applications")

    else:
        print("\n[ERROR] Database connection failed!")
        print("Please check your database credentials and network connectivity.")

        print("\nTroubleshooting tips:")
        print("- Verify your Neon database is active in the Neon dashboard")
        print("- Check that your IP address is allowed (if using IP restrictions)")
        print("- Ensure the connection string format is correct")
        print("- Verify username, password, and database name are correct")
        print("- Check your internet connection")
        print("- If using a firewall, ensure port 5432 is open")

        sys.exit(1)

if __name__ == "__main__":
    main()