
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
    language_id = Column(Integer, ForeignKey("languages.id"))

    user = relationship("User", backref = backref('uploaded_files'))
    file_language = relationship("Language", back_populates = "uploaded_files")

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_name = Column(String(255), nullable=False)
    iso_code = Column(String(255))
    requested = Column(Boolean, nullable=False)

    uploaded_files = relationship("UploadedFile", back_populates = "file_language")
    annotations = relationship("Annotation", back_populates = "annotation_language")

class Provenance(Base):
    __tablename__ = 'provenances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(255), nullable=False)
    reference_id = Column(Integer)

class Annotation(Base):
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False)
    reserved_token = Column(Boolean, nullable=False)
    start_index = Column(Integer, nullable=False)
    end_index = Column(Integer, nullable=False)
    token_language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    type = Column(String(255), nullable=False)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"), nullable = False)
    
    file = relationship("UploadedFile", backref = backref('annotations'))
    annotation_language = relationship("Language", back_populates = "annotations")





