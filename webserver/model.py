from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UploadedFile():
    def __init__(self, id, name, content):
        self.file_id = id
        self.name = name
        self.content = content
