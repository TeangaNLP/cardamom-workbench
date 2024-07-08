# services/user_service.py

from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from model import UserModel

class UserService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow
    
    def signup_user(self, username, email, password):
        
        
        with self.uow as uow:
            if uow.repo.get(email):
                return {"user": None, "message": "This email is already registered"}
            else:
                uow.repo.add(UserModel(name=username, email=email, password=password))
                uow.commit()
        
    def login_user(self, email_data, password_data):
        with self.uow as uow:
            user = uow.repo.get(email_data)
            if user is not None and user.password == password_data:
                response = {
                    "user": {
                        "id": user.id,"name": user.name,"email": user.email
                    },
                    "message": "Login successful"
                }
            else:
                response = {"user": None, "message": "Invalid username or password"}
            return response
