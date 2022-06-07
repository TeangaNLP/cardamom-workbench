from sqlalchemy import Table, MetaData, Column, Boolean, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
import model

metadata = MetaData()

uploaded_file = Table(
            'uploaded_files',metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String(255), nullable=False),
            Column("content", String(), nullable=False),
            Column("user_id", Integer, nullable=False),
        )

users = Table(
            'users',metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String(255), nullable=False),
            Column("email", String(255), nullable=False),
            Column("password", String(), nullable=False),
        )

def start_mappers():
    pages_mapper = mapper(model.UploadedFile, uploaded_file)
    users_mapper = mapper(model.User, users)
