from __future__ import annotations
import orm
import docx
import nltk
import config
from orm import Base
from typing import List, Dict
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, class_mapper
from flask import Blueprint, request, render_template, make_response, jsonify 

from Tokeniser import cardamom_tokenise

nltk.download('punkt')

api = Blueprint('api', __name__,
                        template_folder='templates')

# orm.start_mappers()
engine = create_engine(config.get_postgres_uri())
Base.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)


def serialise(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    """
    User login route
    """
    # for now we are just checking if the user name exist
    # we also need to check for password
    user_data = request.form.get("user")
    password_data = request.form.get("password")
    session = get_session()
    user = session.query(orm.User).filter(orm.User.email==user_data).one_or_none()
    if user:
        return jsonify({"user": user.id})
    else:
        return jsonify({"user": None})

@api.route('/get_files/', methods=["GET"])
def get_all_files() -> List[orm.UploadedFile]:
    """
    Get user files route
    """
    # for a user get all of their files
    user_id = request.args.get("user")
    session = get_session()
    user_data = session.query(orm.User).filter(orm.User.id == user_id).one_or_none()
    files_ = user_data.uploaded_files
    file_contents = [{"filename": file.name, "file_id": file.id, "content": file.content} for file in files_]
    return  jsonify({"file_contents": file_contents})

@api.route('/fileUpload', methods = ['POST'])
def file_upload():
    """
    Uploading a file
    """
    session = get_session()
    if 'file' not in request.files:
        print('abort(400)') 
    uploaded_file = request.files["file"]
    name = uploaded_file.filename
    name, extension = name.split('.')
    user_id = request.form['user_id']

    if extension == 'txt':
        # upload a txt file
        uploaded_file = uploaded_file.read()
        content = uploaded_file.decode("utf-8") 
        new_file = orm.UploadedFile(name = name, content = content, user_id = user_id)
        session.add(new_file)
        session.commit()
        session.flush()
        content = cardamom_tokenise(content,"english")
        response_body = {
            "data": content
        }
    elif extension == 'docx':
        # upload a docx file
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

def get_tokens(file_id):
    session = get_session()
    annots = session.query(orm.Annotation).filter(orm.Annotation.uploaded_file_id==file_id).all()
    # print('Inside get_tokens: ', annots)
    annotations = [serialise(annot) for annot in annots]
    return annotations

def get_replaced_tokens(start, end, annotations):
    # fetch the saved tokens
    i = 0
    replaceIndex, replaceTokens = None, []

    while(i < len(annotations)):
        # if the new start is greater than annotations start
        if((start >= annotations[i]["start_index"]) and not(annotations[i]["end_index"] <= start)):
            replaceIndex = i
            while(end > annotations[i]["end_index"]):
                replaceTokens.append(annotations[i])
                i = i + 1
            replaceTokens.append(annotations[i])
            break
        
        i = i + 1
    return replaceTokens


@api.route('/annotations/<file_id>', methods=["GET"])
def get_annotations(file_id) -> orm.UploadedFile:
    annotations = get_tokens(file_id)
    annotations = sorted(annotations, key=lambda a: a['start_index']) 
    return jsonify({"annotations": annotations})


@api.route('/annotations', methods = ["POST"])
def push_annotations():
    # assuming the annotations come as a list of dictionaries
    data = request.get_json()
    annotations, file_id = data.get('tokens'), data.get("file_id")
    session = get_session()
    
    # Check for tokens to be deleted
    extracted_annotations = get_tokens(file_id)
    for annotation in annotations:
        replaceTokens = get_replaced_tokens(annotation["start_index"], annotation["end_index"], extracted_annotations)
        for token in replaceTokens:
            session.query(orm.Annotation).filter(orm.Annotation.id == token["id"]).delete() 

        new_annotation = orm.Annotation(
            token = annotation["token"], 
            reserved_token = False, 
            start_index = annotation["start_index"],
            end_index = annotation["end_index"],
            token_language_id = 1, 
            type = annotation["type"],
            uploaded_file_id = file_id
        )
        session.add(new_annotation)
    session.commit()
    session.flush()
    response_body = {
            "response": "success"
        }
    return response_body


@api.route('/auto_tokenise', methods=["POST"])
def auto_tokenise():
    text = request.form.get("data")
    tokenised_text = cardamom_tokenise(text,"english")
    return { "annotations": tokenised_text }

    