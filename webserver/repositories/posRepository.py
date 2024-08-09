from model import POSInstanceModel, POSFeaturesModel, TokenModel, UploadedFileModel, LanguageModel
from sqlalchemy.orm import Session

class POSRepository:
    """
    Repository class for handling POS-related database operations.
    """
    def __init__(self, session: Session):
        """
        Initialize the POSRepository with a SQLAlchemy session.

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
    def get_file_by_id(self, file_id: int) -> UploadedFileModel:
        """
        Retrieve a file by its ID from the database.

        Args:
            file_id (int): The ID of the file to be retrieved.

        Returns:
            UploadedFileModel: The file model if found, otherwise None.
        """
        return self.session.query(UploadedFileModel).filter(UploadedFileModel.id == file_id).one_or_none()
    def get_tokens(self, file_id: int):
        """
        Retrieve all tokens associated with a file ID from the database.

        Args:
            file_id (int): The ID of the file whose tokens are to be retrieved.

        Returns:
            list[TokenModel]: A list of token models associated with the file.
        """
        return self.session.query(TokenModel).filter(TokenModel.uploaded_file_id == file_id).all()
    
    def add_pos_instance(self, token_id: int, tag: str, type_: str) -> POSInstanceModel:
        """
        Add a new POS instance to the database.

        Args:
            token_id (int): The ID of the token.
            tag (str): The POS tag.
            type_ (str): The type of POS instance.

        Returns:
            POSInstanceModel: The added POS instance model.
        """
        pos_instance = POSInstanceModel(token_id=token_id, tag=tag, type_=type_)
        self.session.add(pos_instance)
        self.session.commit()
        self.session.flush()
        self.session.refresh(pos_instance)
        return pos_instance

    def add_pos_feature(self, pos_instance_id: int, feature: str, value: str):
        """
        Add a new POS feature to the database.

        Args:
            pos_instance_id (int): The ID of the POS instance.
            feature (str): The name of the feature.
            value (str): The value of the feature.
        """
        pos_feature = POSFeaturesModel(posinstance_id=pos_instance_id, feature=feature, value=value)
        self.session.add(pos_feature)
        self.session.commit()
        self.session.flush()
        self.session.refresh(pos_feature)

    def close(self):
        """
        Close the SQLAlchemy session.
        """
        self.session.close()
