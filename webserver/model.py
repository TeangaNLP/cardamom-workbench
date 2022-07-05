from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User():
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UploadedFile():
    def __init__(self, name, content, user_id):
        self.name = name
        self.content = content
        self.user_id = user_id

class Annotation():
    def __init__(self, id, type, value, uploadedFile_id, user_id):
        self.id = id
        self.type = type
        self.value = value
        self.user_id = user_id
        self.uploadedFile_id = uploadedFile_id

