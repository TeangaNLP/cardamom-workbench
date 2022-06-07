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

# orm.start_mappers()
# get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

db_manager = DbManager()
db_manager.insert_user("admin@cardamom.com", ("admin@cardamom.com", "Johnny Became", "admin@cardamom.com", "cardamom123"))
db_manager.insert_file("admin@cardamom.com", (1, "Lorem Ipsum the First", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu urna iaculis, consequat ex et, suscipit arcu. Duis laoreet consectetur viverra. Mauris odio mauris, tempus nec libero nec, commodo hendrerit eros. Nullam porta et elit eget fermentum. Fusce vehicula ac eros bibendum consectetur. Sed maximus, risus id vestibulum imperdiet, ligula mi accumsan tellus, eget blandit eros magna tincidunt dolor. Praesent lobortis non quam ac sodales. Donec a ligula eu leo consequat porta sit amet id mauris. Integer bibendum purus id orci posuere volutpat. In efficitur elit vitae mauris volutpat, non pellentesque quam consequat. Cras dui risus, condimentum a tortor quis, volutpat pellentesque diam. Vivamus feugiat posuere erat ut sollicitudin. Quisque sed ex ac turpis tincidunt porttitor id at lectus. Pellentesque feugiat magna ut elit bibendum faucibus.", "admin@cardamom.com"))
db_manager.insert_file("admin@cardamom.com", (2, "Lorem Ipsum the Second", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec eu urna iaculis, consequat ex et, suscipit arcu. Duis laoreet consectetur viverra. Mauris odio mauris, tempus nec libero nec, commodo hendrerit eros. Nullam porta et elit eget fermentum. Fusce vehicula ac eros bibendum consectetur. Sed maximus, risus id vestibulum imperdiet, ligula mi accumsan tellus, eget blandit eros magna tincidunt dolor. Praesent lobortis non quam ac sodales. Donec a ligula eu leo consequat porta sit amet id mauris. Integer bibendum purus id orci posuere volutpat. In efficitur elit vitae mauris volutpat, non pellentesque quam consequat. Cras dui risus, condimentum a tortor quis, volutpat pellentesque diam. Vivamus feugiat posuere erat ut sollicitudin. Quisque sed ex ac turpis tincidunt porttitor id at lectus. Pellentesque feugiat magna ut elit bibendum faucibus.", "admin@cardamom.com"))

@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    user = request.form.get("user")
    password = request.form.get("password")
    user = db_manager.get_user(user)
    if user.password == password:
        return jsonify({"accept": True})
    else:
        return jsonify({"accept": False})

@api.route('/file/', methods=["GET"])
def get_all_files() -> List[model.UploadedFile]:
    # session = get_session()
    # files_ = session.query(model.UploadedFile).all()

    user = request.args.get("user")
    files = db_manager.get_files(user)
    file_contents = [{"filename": file.name, "content": cardamom_tokenise(file.content, "english")} for file in files]
    return  jsonify({"file_contents": file_contents})

@api.route('/fileUpload', methods = ['POST'])
def file_upload():
    """
    Route to add a file to the database
    """
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

