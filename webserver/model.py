from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserModel():
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UploadedFileModel():
    def __init__(self, name, content, user_id, language_id):
        self.name = name
        self.content = content
        self.user_id = user_id
        self.language_id = language_id


class LanguageModel():
    def __init__(self, language_name, iso_code, requested):
        self.language_name = language_name
        self.iso_code = iso_code
        self.requested = requested


class ProvenanceModel():
    def __init__(self, timestamp, reference_id):
        self.timestamp = timestamp
        self.reference_id = reference_id


class POSInstanceModel():
    def __init__(self, token_id, tag, type_):
        self.token_id = token_id
        self.tag = tag
        self.type_ = type_


class POSFeaturesModel():
    def __init__(self, posinstance_id, feature, value):
        self.posinstance_id = posinstance_id
        self.feature = feature
        self.value = value


class TokenModel():
    def __init__(self, reserved_token, start_index, end_index, token_language_id, type_, uploaded_file_id):
        self.reserved_token = reserved_token
        self.start_index = start_index
        self.end_index = end_index
        self.token_language_id = token_language_id
        self.type_ = type_
        self.uploaded_file_id = uploaded_file_id
