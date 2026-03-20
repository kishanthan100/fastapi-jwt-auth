from sqlalchemy.orm import Session
from app.models.user_model import  UserDetails



def get_user_details_by_email(db: Session,  email: str):
    """
    Retrieve a user's details from the UserDetails table by their email address.
    
    Args:
        db (Session): SQLAlchemy database session
        email (str): Email address of the user to look up
    
    Returns:
        Optional[UserDetails]: UserDetails object if found, None otherwise
    
    Example:
        user_details = get_user_details_by_email(db, "john@example.com")
        if user_details:
            print(f"Found user: {user_details.name}")
    """
    return db.query(UserDetails).filter(
        UserDetails.email == email
    ).first()



def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the users table by their email address.
    
    Args:
        db (Session): SQLAlchemy database session
        email (str): Email address of the user to look up
    
    Returns:
        Optional[User]: User object if found, None otherwise
    
    Raises:
        NoResultFound: If email is empty or invalid format (optional)
    
    Example:
        user = get_user_by_email(db, "john@example.com")
        if user:
            print(f"User ID: {user.id}")
    """

    response = db.query(UserDetails).filter(UserDetails.email == email).first()
    return response



def create_user(db: Session, user_data: dict):

    """
    Create a new user in the database.
    
    Args:
        db (Session): SQLAlchemy database session
        user_data (dict): Dictionary containing user information.
            Expected keys: name, email, phone (and any other required fields)
    
    Returns:
        User: The newly created User object
    
    Raises:
        IntegrityError: If a user with the same email already exists
        ValueError: If required fields are missing in user_data
    
    Example:
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890"
        }
        new_user = create_user(db, user_data)
        print(f"Created user with ID: {new_user.id}")
    
    Note:
        This function does not commit the transaction. The caller is responsible
        for calling db.commit() and db.refresh() if needed.
    """

    user = UserDetails(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user