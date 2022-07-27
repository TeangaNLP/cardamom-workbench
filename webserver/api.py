import docx
import nltk
import config
import json
import orm
from orm import Base
from typing import List, Dict
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, class_mapper
from flask import Blueprint, request, render_template, make_response, jsonify 

from Tokeniser import cardamom_tokenise
from POS_tag import cardamom_postag

api = Blueprint('api', __name__,
                        template_folder='templates')

# orm.start_mappers()
engine = create_engine(config.get_postgres_uri())
Base.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)


def serialise(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)

def get_tokens(file_id, objectify=False):
    session = get_session()
    annots = session.query(orm.Token).filter(orm.Token.uploaded_file_id==file_id).all()
    if objectify:
        return annots
    # print('Inside get_tokens: ', annots)
    annotations = [serialise(annot) for annot in annots]
    return sorted(annotations, key=lambda a: a['start_index'])

def get_replaced_tokens(start, end, annotations):
    # fetch the saved tokens
    i = 0
    replace_tokens = []

    while(i < len(annotations)):
        # if the new start is greater than annotations start
        new_set = set(range(start, end))
        overlap_set = set(range(annotations[i]["start_index"], annotations[i]["end_index"]))

        if(len(new_set & overlap_set) > 0):
            while(i < len(annotations) and end > annotations[i]["end_index"]):
                replace_tokens.append(annotations[i])
                i = i + 1
            replace_tokens.append(annotations[i])
            break
        i = i + 1
    return replace_tokens

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
    file_contents = [{"filename": file.name, "file_id": file.id, "content": file.content.replace("\\n", "\n")} for file in files_]
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

@api.route('/annotations/<file_id>', methods=["GET"])
def get_annotations(file_id) -> orm.UploadedFile:
    annotations = get_tokens(file_id)
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
        replace_tokens = get_replaced_tokens(annotation["start_index"], annotation["end_index"], extracted_annotations)
        for token in replace_tokens:
            session.query(orm.Token).filter(orm.Token.id == token["id"]).delete() 

        new_annotation = orm.Token(
            reserved_token = True if annotation["type"] == "manual" else False, 
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
    print(request.form)
    text = request.form.get("data").replace("\r", "")
    reserved_tokens = json.loads(request.form.get("reservedTokens"))
    print(reserved_tokens)
    tokenised_text = cardamom_tokenise(text, reserved_toks=reserved_tokens)
    sorted(tokenised_text, key=lambda a: a['start_index'])
    return { "annotations": tokenised_text }
    
@api.route('/pos_tag', methods=["POST"])
def push_postags():
    data = request.get_json()
    pos_tags = data.get('tags')

    session = get_session()

    print(pos_tags)

    for token_id in pos_tags:
        print(token_id)
        pos_instance = orm.POSInstance(token_id = int(token_id), tag = pos_tags[token_id]["tag"], type=pos_tags[token_id]["type"])
        session.add(pos_instance)
        session.commit()
        session.flush()
        session.refresh(pos_instance)
        print(pos_instance.id)
        if pos_tags[token_id]['features']:
            for f_key_val in pos_tags[token_id]['features']:
                f_key = f_key_val["feature"]
                f_val = f_key_val["value"]
                session.add(orm.POSFeatures(posinstance_id = pos_instance.id, feature = f_key, value = f_val))
            session.commit()
            session.flush()
    response_body = {
            "response": "success"
        }
    return response_body

@api.route('pos_tag/<file_id>', methods = ["GET"])
def get_postags(file_id):
    tokens = get_tokens(file_id, objectify=True)
    token_tags = {}
    for token in tokens:
        instances = token.pos_instance
        for instance in instances:
            features = instance.features
            tag_features = []
            for feature in features:
                tag_features.append({"feature": feature.feature, "value": feature.value})
            token_tags[token.id] = {"tag": instance.tag, "features": tag_features, "start_index": token.start_index}
    annotations = [serialise(annot) for annot in tokens]
    return jsonify({"annotations": sorted(annotations, key=lambda a: a['start_index']), "tags": token_tags})


@api.route('/auto_tag', methods=["POST"])
def auto_tag():
    print(request.form)
    # extract the text
    content = request.form.get('content')
    tokens = json.loads(request.form.get('tokens'))
    print(tokens)
    pos_text = cardamom_postag(content, tokens, 2, 'en')
    print(pos_text)
    return { "POS": pos_text }