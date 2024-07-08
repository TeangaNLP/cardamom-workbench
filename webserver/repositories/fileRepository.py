from model import UploadedFileModel, UserModel, LanguageModel
from sqlalchemy.orm import Session

class FileRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, file_id):
            return self.session.query(UploadedFileModel).filter(UploadedFileModel.id == file_id).one_or_none()
        

    def get_all_files(self, user_id):
            return self.session.query(UploadedFileModel).filter(UploadedFileModel.user_id == user_id).all()

    def get_language_by_iso_code(self, iso_code):
            return self.session.query(LanguageModel).filter(LanguageModel.iso_code == iso_code).one_or_none()

    def add(self, name, content, user_id, language_id):
            new_file = UploadedFileModel(name=name, content=content, user_id=user_id, language_id=language_id)
            self.session.add(new_file)
            self.session.flush()
            return new_file