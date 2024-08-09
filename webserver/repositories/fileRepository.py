from model import UploadedFileModel, LanguageModel, UserModel
from sqlalchemy.orm import Session

class FileRepository:
    """
    Repository class for handling file-related database operations.
    """
    def __init__(self, session: Session):
        """
        Initialize the FileRepository with a SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object.
        """
        self.session = session

    def get(self, file_id: int) -> UploadedFileModel:
        """
        Retrieve a file by its ID from the database.

        Args:
            file_id (int): The ID of the file to be retrieved.

        Returns:
            UploadedFileModel: The file model if found, otherwise None.
        """
        return self.session.query(UploadedFileModel).filter(UploadedFileModel.id == file_id).one_or_none()

    def get_all(self, user_id: int)-> list[UploadedFileModel]:
        """
        Retrieve all files associated with a specific user ID.

        Args:
            user_id (int): The ID of the user whose files are to be retrieved.

        Returns:
            list[UploadedFileModel]: A list of file models associated with the user.
        """
        return self.session.query(UserModel).filter(UserModel.id == user_id).one_or_none()

    def get_language_by_iso_code(self, iso_code: str) -> LanguageModel:
        """
        Retrieve a language by its ISO code from the database.

        Args:
            iso_code (str): The ISO code of the language to be retrieved.

        Returns:
            LanguageModel: The language model if found, otherwise None.
        """
        return self.session.query(LanguageModel).filter(LanguageModel.iso_code == iso_code).one_or_none()

    def add(self, name: str, content: str, user_id: int, language_id: int) -> UploadedFileModel:
        """
        Add a new file to the database.

        Args:
            name (str): The name of the file.
            content (str): The content of the file.
            user_id (int): The ID of the user who uploaded the file.
            language_id (int): The ID of the language associated with the file.

        Returns:
            UploadedFileModel: The newly added file model.
        """
        new_file = UploadedFileModel(name=name, content=content, user_id=user_id, language_id=language_id)
        self.session.add(new_file)
        self.session.flush()
        self.session.commit()
        return new_file
