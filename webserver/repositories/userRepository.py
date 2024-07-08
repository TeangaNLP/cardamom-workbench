from sqlalchemy.orm import Session
from model import UserModel

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: UserModel):
        self.session.add(user)
        self.session.flush()  

    def get(self, email: str):
        print(email)
        return self.session.query(UserModel).filter(UserModel.email == email).one_or_none()

    def user_to_dict(self, user: UserModel) -> dict:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            # Add other fields as necessary
        }
