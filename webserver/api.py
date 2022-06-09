import orm
import docx
import nltk
import config
from orm import Base
from typing import List, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Tokeniser import cardamom_tokenise
from flask import Blueprint, request, render_template, jsonify 

nltk.download('punkt')

api = Blueprint('api', __name__,
                        template_folder='templates')

# orm.start_mappers()
engine = create_engine(config.get_postgres_uri())
Base.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)



@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    """
    User login
    """
    user_data = request.form.get("user")
    password_data = request.form.get("password")
    session = get_session()
    user = session.query(orm.User).filter(orm.User.email==user_data).one_or_none()
    if user:
        return jsonify({"user": user.id})
    else:
        return jsonify({"user": None})

@api.route('/file/', methods=["GET"])
def get_all_files() -> List[orm.UploadedFile]:
    """
    Get all files of the user
    """
    user_id = request.args.get("user")

    session = get_session()
    # files_ = session.query(orm.UploadedFile).filter(orm.UploadedFile.user_id == user_id).all()
    user_data = session.query(orm.User).filter(orm.User.id == user_id).one_or_none()
    files_ = user_data.uploaded_files
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
    user_id = request.form['user_id']
    print('TEST: ', user_id)
    if extension == 'txt':
        uploaded_file = uploaded_file.read()
        content = uploaded_file.decode("utf-8") 
        new_file = orm.UploadedFile(name = name, content = content, user_id = user_id)
        session.add(new_file)
        session.commit()
        session.flush()
        print(dir(new_file))
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
        session.add(orm.UploadedFile(name, content, user_id))
        session.commit()
        session.flush()
        content = cardamom_tokenise(content,"english")
        response_body = {
            "data": content
        }
    return response_body

@api.route('/file/<file_id>', methods=["GET"])
def get_file(file_id) -> orm.UploadedFile:
    session = get_session()
    file_ = session.query(orm.UploadedFile).filter(orm.UploadedFile.file_id==file_id).one()
    # TODO implement serializer for UploadedFile model
    data = {"name":file_.name,"file_id":file_.file_id,"content":file_.content}
    return jsonify(data) 

