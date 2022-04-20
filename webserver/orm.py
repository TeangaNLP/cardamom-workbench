from sqlalchemy import Table, MetaData, Column, Boolean, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
import model

metadata = MetaData()

uploaded_file = Table(
            'uploaded_files',metadata,
            Column("file_id", Integer, primary_key=True, autoincrement=True),
            Column("name", String(255), nullable=False),
            Column("content", String(), nullable=False),
        )

def start_mappers():
    pages_mapper = mapper(model.UploadedFile, uploaded_file)
