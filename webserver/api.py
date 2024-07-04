import nltk
import json
from services.posService import POSService
from services.fileservice import FileService
from services.annotationService import AnnotationService
from services.userService import UserService
import model
from typing import List, Dict
from sqlalchemy.pool import NullPool
from flask import g, Blueprint, request, render_template, make_response, jsonify
from technologies import  cardamom_find_similar_words #cardamom_space, cardamom_postag

api = Blueprint('api', __name__, template_folder='templates')

# def serialise_data_model(model):
#     return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}
#   
@api.route('/signup_user', methods=["POST"])
def signup_user() -> Dict:

    email_data = request.form.get("email")
    username_data = request.form.get("name")
    password_data = request.form.get("password")

    service = UserService(g.uow)

    return jsonify(service.signup_user(username_data, email_data, password_data))

@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    email_data = request.form.get("email")
    password_data = request.form.get("password")
    service = UserService(g.uow)
    response = service.login_user(email_data, password_data)
    return jsonify(response)

@api.route('/get_file/', methods=["GET"])
def get_file() -> List[model.UploadedFileModel]:
    fileId = request.args.get("fileId")
    userId = request.args.get("userId") 
    service = FileService(g.uow)
    return jsonify(service.get_file_by_id(userId, fileId))


@api.route('/get_files/', methods=["GET"])
def get_all_files() -> List[model.UploadedFileModel]:
    user_id = request.args.get("user")
    result = FileService(g.uow).get_all_files(user_id)
    return jsonify({"file_contents": result})


@api.route('/fileUpload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        print('abort(400)')
    uploaded_file = request.files["file"]
    user_id = request.form['user_id']
    iso_code = request.form['iso_code']
    file_service = FileService(g.uow)
    file_service.upload_file(uploaded_file, user_id, iso_code)
    response_body = {
        "status": "file uploaded" 
    }
    return response_body


@api.route('/annotations/<file_id>', methods=["GET"])
def get_annotations(file_id) -> model.UploadedFileModel:
    annotation_service = AnnotationService(g.uow)
    annotations = annotation_service.get_tokens(file_id)
    return jsonify({"annotations": annotations})


@api.route('/annotations', methods=["POST"])
def push_annotations():
    data = request.get_json()
    annotations, file_id = data.get('tokens'), data.get("file_id")
    annotation_service = AnnotationService(g.uow)
    annotation_service.process_annotations(annotations, file_id)
    '''
    for space in spaces:
        new_space = model.SpaceModel(
            space_index=space["space_index"],
            space_type=space["space_type"],
            uploaded_file_id=file_id
        )
        session.add(new_space)
    '''
    ''' #todo 
        # implement the gaps in the backend, 
        # we need to think how to replace the existing gaps with the new created gaps
    extracted_annotations = get_gaps(file_id)
    for gap in gaps:
        replace_tokens = get_replaced_tokens(annotation["start_index"], annotation["end_index"], extracted_annotations)
        for token in replace_tokens:
            session.query(model.TokenModel).filter(model.TokenModel.id == token["id"]).delete() 

        new_annotation = model.TokenModel(
            reserved_token=True if annotation["type_"] == "manual" else False,
            start_index=annotation["start_index"],
            end_index=annotation["end_index"],
            token_language_id=file.language_id,
            type_=annotation["type_"],
            uploaded_file_id=file_id
        )
        session.add(new_annotation)
    session.commit()
    session.flush()
    '''
    response_body = {
        "response": "success"
    }
    return response_body


@api.route('/auto_tokenise', methods=["POST"])
def auto_tokenise():
    file_data = json.loads(request.form.get("file_data"))
    reserved_tokens = json.loads(request.form.get("reservedTokens"))
    return {"annotations": AnnotationService(g.uow).auto_tokenise(file_data, reserved_tokens)}

@api.route('/pos_tag', methods=["POST"])
def push_postags():
    data = request.get_json()
    pos_tags = data.get('tags')
    pos_service = POSService(g.uow)
    pos_service.add_pos_tags(pos_tags)
    return jsonify({"response": "success"}), 200

@api.route('pos_tag/<file_id>', methods=["GET"])
def get_postags(file_id):
    return jsonify(POSService(g.uow).get_postags(file_id))
    
@api.route('/auto_tag', methods=["POST"])
def auto_tag():
    file_data = json.loads(request.form.get('file_data'))
    return {"POS": POSService(g.uow).auto_tag(file_data)}

@api.route('/related_words/<word>', methods=["GET"])
def related_words(word):
    print(word,flush=True)
    related_words =  [serialise_data_model(obj) for obj in cardamom_find_similar_words(word, "gle")]
    print(related_words,flush=True)
    return {"related_words": related_words}