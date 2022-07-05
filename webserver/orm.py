
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(), nullable=False)


class UploadedFile(Base):
    __tablename__ = 'uploaded_files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    content = Column( String(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 

    user = relationship("User", backref = backref('uploaded_files'))

class Annotation(Base):
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False)
    text_language = Column(String(255), nullable=False)
    token_language = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    reserved_token = Column(Boolean, nullable=False)
    start_index = Column(Integer, nullable=False)
    end_index = Column(Integer, nullable=False)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable=False)

    file = relationship("UploadedFile", backref = backref('annotations'))




