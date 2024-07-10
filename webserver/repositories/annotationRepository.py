from model import TokenModel, UploadedFileModel, LanguageModel
from sqlalchemy.orm import Session

class AnnotationRepository:
    """
    Repository class for handling annotation-related database operations.
    """
    def __init__(self, session: Session):
        """
        Initialize the AnnotationRepository with a SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object.
        """
        self.session = session
        
    def get_language_by_id(self, lang_id: int) -> LanguageModel:
        """
        Retrieve a language by its ID from the database.

        Args:
            lang_id (int): The ID of the language to be retrieved.

        Returns:
            LanguageModel: The language model if found, otherwise None.
        """
        return self.session.query(LanguageModel).filter(LanguageModel.id == lang_id).one_or_none()
    
    def get(self, file_id: int) -> list[TokenModel]:
        """
        Retrieve all tokens associated with a file ID from the database.

        Args:
            file_id (int): The ID of the file whose tokens are to be retrieved.

        Returns:
            list[TokenModel]: A list of token models associated with the file.
        """
        return self.session.query(TokenModel).filter(TokenModel.uploaded_file_id == file_id).all()

    def get_file_by_id(self, file_id: int) -> UploadedFileModel:
        """
        Retrieve a file by its ID from the database.

        Args:
            file_id (int): The ID of the file to be retrieved.

        Returns:
            UploadedFileModel: The file model if found, otherwise None.
        """
        return self.session.query(UploadedFileModel).filter(UploadedFileModel.id == file_id).one_or_none()

    def delete(self, token_id: int):
        """
        Delete a token by its ID from the database.

        Args:
            token_id (int): The ID of the token to be deleted.
        """
        self.session.query(TokenModel).filter(TokenModel.id == token_id).delete()
        self.session.commit()

    def add(self, annotation_data: dict, file: UploadedFileModel, file_id: int):
        """
        Add a new annotation to the database.

        Args:
            annotation_data (dict): The data of the annotation to be added.
            file (UploadedFileModel): The file model associated with the annotation.
            file_id (int): The ID of the file associated with the annotation.
        """
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

    