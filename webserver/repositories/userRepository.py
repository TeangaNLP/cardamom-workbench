from sqlalchemy.orm import Session
from model import UserModel

class UserRepository:
    """
    Repository class for handling user-related database operations.
    """
    def __init__(self, session: Session):
        """
        Initialize the UserRepository with a SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object.
        """
        self.session = session

    def add(self, user: UserModel):
        """
        Add a new user to the database.

        Args:
            user (UserModel): The user model to be added to the database.
        """
        self.session.add(user)
        self.session.flush()

    def get(self, email: str):
        """
        Retrieve a user by email from the database.

        Args:
            email (str): The email of the user to be retrieved.

        Returns:
            UserModel: The user model if found, otherwise None.
        """
        print(email)
        return self.session.query(UserModel).filter(UserModel.email == email).one_or_none()

    def user_to_dict(self, user: UserModel) -> dict:
        """
        Convert a user model to a dictionary.

        Args:
            user (UserModel): The user model to be converted.

        Returns:
            dict: A dictionary representation of the user model.
        """
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
