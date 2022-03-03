from flask import Blueprint, render_template, jsonify 
import model
import config
import orm
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

api = Blueprint('api', __name__,
                        template_folder='templates')

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


@api.route('/file/', methods=["GET"])
def get_all_files() -> List[model.UploadedFile]:
    session = get_session()
    files_ = session.query(model.UploadedFile).all()

    # TODO implement serializer for UploadedFile model
    data = [{"name":f.name,"file_id":f.file_id,"content":f.content} for f in files_]

    return  jsonify(data)

@api.route('/file/<file_id>', methods=["GET"])
def get_file(file_id) -> model.UploadedFile:
    session = get_session()
    file_ = session.query(model.UploadedFile).filter(model.UploadedFile.file_id==file_id).one()

    # TODO implement serializer for UploadedFile model
    data = {"name":file_.name,"file_id":file_.file_id,"content":file_.content}

    return jsonify(data) 

