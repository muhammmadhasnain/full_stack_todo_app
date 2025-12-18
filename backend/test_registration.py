from src.api.auth import register
from src.models.user import UserRegister
from src.database.session import get_session
from src.database.database import engine
from sqlmodel import Session   

def test_registration():
    """
    Test the registration functionality to ensure it works properly
    """
    print("Testing registration functionality...")

    # Create a mock user registration object
    test_user = UserRegister(
        email="test@example.com",
        name="Test User",
        password="testpassword123",
        is_active=True
    )

    # Get a session and try to register the user
    with Session(engine) as session:
        try:
            # First, check if a user with this email already exists and delete it for testing
            from src.services.user_service import get_user_by_email
            existing_user = get_user_by_email(session, test_user.email)

            if existing_user:
                print(f"User with email {test_user.email} already exists, removing for test...")
                session.delete(existing_user)
                session.commit()

            # Now register the user
            result = register(test_user, session)
            print(f"[SUCCESS] User registered successfully: {result}")

        except Exception as e:
            print(f"[ERROR] Registration failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_registration()