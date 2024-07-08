# services/user_service.py

from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from model import UserModel

class UserService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow
    
    def signup_user(self, username, email, password):
        """
        Registers a new user in the database.

        Args:
            username (str): Username of the new user.
            email (str): Email address of the new user.
            password (str): Password of the new user.

        Returns:
            dict: Contains user information if registration is successful, or a message indicating the email is already registered.
        """
        with self.uow as uow:
            if uow.repo.get(email):
                return {"user": None, "message": "This email is already registered"}
            else:
                uow.repo.add(UserModel(name=username, email=email, password=password))
                uow.commit()
                return {"user": {"name": username, "email": email}, "message": "User registration successful"}

    def login_user(self, email_data, password_data):
        """
        Authenticates a user based on email and password.

        Args:
            email_data (str): Email address of the user attempting to log in.
            password_data (str): Password of the user attempting to log in.

        Returns:
            dict: Contains user information and success message if login is successful, or a message indicating invalid credentials.
        """
        with self.uow as uow:
            user = uow.repo.get(email_data)
            if user is not None and user.password == password_data:
                response = {
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email
                    },
                    "message": "Login successful"
                }
            else:
                response = {"user": None, "message": "Invalid username or password"}
            return response
