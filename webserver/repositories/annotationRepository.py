from model import TokenModel, UploadedFileModel, LanguageModel
from sqlalchemy.orm import Session

class AnnotationRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def get_language_by_id(self,  lang_id):
        return self.session.query(LanguageModel).filter(LanguageModel.id == lang_id).one_or_none()
    
    def get_tokens(self, file_id):
        return self.session.query(TokenModel).filter(TokenModel.uploaded_file_id == file_id).all()

    def get_file_by_id(self, file_id):
        return self.session.query(UploadedFileModel).filter(UploadedFileModel.id == file_id).one_or_none()

    def delete_token_by_id(self, token_id):
        self.session.query(TokenModel).filter(TokenModel.id == token_id).delete()

    def add_annotation(self, annotation_data, file, file_id):
        new_annotation = TokenModel(
            reserved_token=True if annotation_data["type_"] == "manual" else False,
            start_index=annotation_data["start_index"],
            end_index=annotation_data["end_index"],
            token_language_id=file.language_id,
            type_=annotation_data["type_"],
            uploaded_file_id=file_id
        )
        self.session.add(new_annotation)
        self.session.flush()
     

    def commit(self):
        self.session.commit()

    def flush(self):
        self.session.flush()

    def close(self):
        self.session.close()
