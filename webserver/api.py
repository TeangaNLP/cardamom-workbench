from urllib import request
from flask import Blueprint, request, render_template, jsonify 
import model
import config
import orm
import docx
import nltk

from fake_database import DbManager
nltk.download('punkt')
from Tokeniser import cardamom_tokenise
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import get_api_url

api = Blueprint('api', __name__,
                        template_folder='templates')

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    """
    User login
    """
    user_data = request.form.get("user")
    password_data = request.form.get("password")
    session = get_session()
    user = session.query(model.User).filter(model.User.email==user_data).one_or_none()

    if user:
        return jsonify({"user": user.id})
    else:
        return jsonify({"user": None})

@api.route('/file/', methods=["GET"])
def get_all_files() -> List[model.UploadedFile]:
    """
    Get all files of the user
    """
    user_id = request.args.get("user")
    
    session = get_session()
    files_ = session.query(model.UploadedFile).filter(model.UploadedFile.user_id == user_id).all()
    
    file_contents = [{"filename": file.name, "content": cardamom_tokenise(file.content, "english")} for file in files_]
    return  jsonify({"file_contents": file_contents})

@api.route('/fileUpload', methods = ['POST'])
def file_upload():

    session = get_session()
    
    if 'file' not in request.files:
        print('abort(400)') 

    uploaded_file = request.files["file"]
    name = uploaded_file.filename
    name, extension = name.split('.')
    user_id = 1
    if extension == 'txt':
        uploaded_file = uploaded_file.read()
        content = uploaded_file.decode("utf-8") 
        # the idea behind file_id needs to be implemented
        session = get_session()
        session.add(model.UploadedFile(1, name, content, user_id))

        content = cardamom_tokenise(content,"english")
        response_body = {
            "data": content
        }
    elif extension == 'docx':
        uploaded_file = docx.Document(uploaded_file)
        text = []
        content = ''
        for para in uploaded_file.paragraphs:
            text.append(para.text)
        content = '\n'.join(text)
        session = get_session()
        session.add(model.UploadedFile(1, name, content, user_id))
        print(content)
        response_body = {
            "data": content
        }
    return response_body

@api.route('/file/<file_id>', methods=["GET"])
def get_file(file_id) -> model.UploadedFile:
    session = get_session()
    file_ = session.query(model.UploadedFile).filter(model.UploadedFile.file_id==file_id).one()

    # TODO implement serializer for UploadedFile model
    data = {"name":file_.name,"file_id":file_.file_id,"content":file_.content}

    return jsonify(data) 

