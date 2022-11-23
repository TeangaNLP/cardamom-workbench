import docx
import nltk
import config
import json
import orm
import model
from orm import Base
from typing import List, Dict
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker, class_mapper
# from flask import Blueprint, request, render_template, make_response, jsonify

from technologies import cardamom_tokenise, cardamom_space, cardamom_postag

orm.start_mappers()
engine = create_engine(config.get_postgres_uri())
Base.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)


def serialise(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


def serialise_data_model(model):
    return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}


def get_tokens(file_id, objectify=False):
    session = get_session()
    annots = session.query(model.TokenModel).filter(model.TokenModel.uploaded_file_id == file_id).all()
    if objectify:
        return annots
    annotations = [serialise(annot) for annot in annots]
    return sorted(annotations, key=lambda a: a['start_index'])


def get_replaced_tokens(start, end, annotations):
    # fetch the saved tokens
    i = 0
    replace_tokens = []

    while i < len(annotations):
        # if the new start is greater than annotations start
        new_set = set(range(start, end))
        overlap_set = set(range(annotations[i]["start_index"], annotations[i]["end_index"]))

        if len(new_set & overlap_set) > 0:
            while i < len(annotations) and end > annotations[i]["end_index"]:
                replace_tokens.append(annotations[i])
                i = i + 1
            replace_tokens.append(annotations[i])
            break
        i = i + 1
    return replace_tokens


def test_file_upload(uploaded_file_content, uploaded_file_name, user_id, iso_code):
    """
    Uploading a file
    """
    session = get_session()
    name, extension = uploaded_file_name.split('.')

    lang = session.query(model.LanguageModel).filter(model.LanguageModel.iso_code == iso_code).one_or_none()
    if extension == 'txt':
        # upload a txt file
        uploaded_file = uploaded_file_content.read()
        content = uploaded_file  #.decode("utf-8")
        new_file = model.UploadedFileModel(name=name, content=content, user_id=user_id, language_id=lang.id)
        session.add(new_file)
        session.commit()
        session.flush()
        content = cardamom_tokenise(content, iso_code=iso_code)
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
        session.add(model.UploadedFileModel(name, content, user_id, lang.id))
        session.commit()
        session.flush()
        content = cardamom_tokenise(content, iso_code=iso_code)
        response_body = {
            "data": content
        }
    return response_body


if __name__ == "__main__":

    file_content_object = open('test_file.txt')
    file_name = 'test_file.txt'
    user_id = 1
    iso_code = 'en'
    test_file_upload(file_content_object, file_name, user_id, iso_code)
