import nltk
import json
from services.posService import POSService
from services.fileService import FileService
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
    """
    Signup a new user.

    Extracts email, username, and password from the form data, validates them,
    and uses UserService to sign up the user.

    Returns:
        Dict: A JSON response containing user information and a message.
    """
    email_data = request.form.get("email")
    username_data = request.form.get("name")
    password_data = request.form.get("password")
    if any(v is None for v in [email_data, username_data, password_data]):
        return {"user": None, "message": "Please fill in all fields"}

    service = UserService(g.uows['user_uow'])
    return jsonify(service.signup_user(username_data, email_data, password_data))


@api.route('/login_user', methods=["POST"])
def login_user() -> Dict:
    """
    Login a user.

    Extracts email and password from the form data and uses UserService to log in the user.

    Returns:
        Dict: A JSON response containing the login result.
    """
    email_data = request.form.get("email")
    password_data = request.form.get("password")
    service = UserService(g.uows['user_uow'])

    response = service.login_user(email_data, password_data)
    return jsonify(response)


@api.route('/get_file/', methods=["GET"])
def get_file() -> List[model.UploadedFileModel]:
    """
    Get a file by its ID and user ID.

    Extracts file ID and user ID from the query parameters and uses FileService to retrieve the file.

    Returns:
        List[model.UploadedFileModel]: A JSON response containing the file data.
    """
    fileId = request.args.get("fileId")
    userId = request.args.get("userId")
    service = FileService(g.uows["file_uow"])
    return jsonify(service.get_file_by_id(userId, fileId))


@api.route('/get_files/', methods=["GET"])
def get_all_files() -> List[model.UploadedFileModel]:
    """
    Get all files for a user.

    Extracts user ID from the query parameters and uses FileService to retrieve all files for that user.

    Returns:
        List[model.UploadedFileModel]: A JSON response containing all file data for the user.
    """
    user_id = request.args.get("user")
    result = FileService(g.uows["file_uow"]).get_all_files(user_id)
    return jsonify({"file_contents": result})


@api.route('/fileUpload', methods=['POST'])
def file_upload():
    """
    Upload a file.

    Extracts the file, user ID, and ISO code from the form data and uses FileService to upload the file.

    Returns:
        Dict: A response body indicating the status of the file upload.
    """
    if 'file' not in request.files:
        print('abort(400)')
    uploaded_file = request.files["file"]
    user_id = request.form['user_id']
    iso_code = request.form['iso_code']
    file_service = FileService(g.uows["file_uow"])
    file_service.upload_file(uploaded_file, user_id, iso_code)
    response_body = {
        "status": "file uploaded"
    }
    return response_body


@api.route('/annotations/<file_id>', methods=["GET"])
def get_annotations(file_id) -> model.UploadedFileModel:
    """
    Get annotations for a file.

    Extracts the file ID from the URL and uses AnnotationService to retrieve the annotations.

    Returns:
        model.UploadedFileModel: A JSON response containing the annotations.
    """
    annotation_service = AnnotationService(g.uows["annotation_uow"])
    annotations = annotation_service.get_tokens(file_id)
    return jsonify({"annotations": annotations})


@api.route('/annotations', methods=["POST"])
def push_annotations():
    """
    Push annotations to the database.

    Extracts annotations and file ID from the request JSON data and uses AnnotationService to process the annotations.

    Returns:
        Dict: A response body indicating the success of the operation.
    """
    data = request.get_json()
    annotations, file_id = data.get('tokens'), data.get("file_id")
    annotation_service = AnnotationService(g.uows["annotation_uow"])
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
    """
    Automatically tokenise a file.

    Extracts file data and reserved tokens from the form data and uses AnnotationService to perform automatic tokenisation.

    Returns:
        Dict: A JSON response containing the annotations.
    """
    file_data = json.loads(request.form.get("file_data"))
    reserved_tokens = json.loads(request.form.get("reservedTokens"))
    return {"annotations": AnnotationService(g.uows["annotation_uow"]).auto_tokenise(file_data, reserved_tokens)}


@api.route('/pos_tag', methods=["POST"])
def push_postags():
    """
    Push part-of-speech tags to the database.

    Extracts POS tags from the request JSON data and uses POSService to add the POS tags.

    Returns:
        Tuple[Dict, int]: A JSON response indicating the success of the operation and the HTTP status code.
    """
    data = request.get_json()
    pos_tags = data.get('tags')
    pos_service = POSService(g.uows["pos_uow"])
    pos_service.add_pos_tags(pos_tags)
    return jsonify({"response": "success"}), 200


@api.route('pos_tag/<file_id>', methods=["GET"])
def get_postags(file_id):
    """
    Get part-of-speech tags for a file.

    Extracts the file ID from the URL and uses POSService to retrieve the POS tags.

    Returns:
        Dict: A JSON response containing the POS tags.
    """
    return jsonify(POSService(g.uows["pos_uow"]).get_postags(file_id))


@api.route('/auto_tag', methods=["POST"])
def auto_tag():
    """
    Automatically tag a file with part-of-speech tags.

    Extracts file data from the form data and uses POSService to perform automatic tagging.

    Returns:
        Dict: A JSON response containing the POS tags.
    """
    file_data = json.loads(request.form.get('file_data'))
    pos_tags = POSService(g.uows["pos_uow"]).auto_tag(file_data)
    return {"POS": pos_tags}


@api.route('/related_words/<word>', methods=["GET"])
def related_words(word):
    print(word, flush=True)
    related_words = [serialise_data_model(obj) for obj in cardamom_find_similar_words(word, "gle")]
    print(related_words, flush=True)
    return {"related_words": related_words}
