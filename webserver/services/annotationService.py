from sqlalchemy.inspection import inspect
from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from model import TokenModel
from technologies import cardamom_tokenise

class AnnotationService:
    """
    Service class for handling annotations on files using SQLAlchemy unit of work pattern.
    """

    def __init__(self, uow: SqlAlchemyUnitOfWork):
        """
        Initializes the AnnotationService with a SQLAlchemy unit of work instance.

        Args:
            uow (SqlAlchemyUnitOfWork): The SQLAlchemy unit of work instance.
        """
        self.uow = uow

    def get_replaced_tokens(self, start, end, annotations):
        """
        Retrieves tokens from annotations that overlap with a specified range.

        Args:
            start (int): Start index of the range.
            end (int): End index of the range.
            annotations (list): List of annotations.

        Returns:
            list: List of tokens that overlap with the specified range.
        """
        i = 0
        replace_tokens = []
        while i < len(annotations):
            new_set = set(range(start, end))
            overlap_set = set(range(annotations[i]["start_index"], annotations[i]["end_index"]))

            if len(new_set & overlap_set) > 0:
                while i < len(annotations) and end > annotations[i]["end_index"]:
                    replace_tokens.append(annotations[i])
                    i += 1
                replace_tokens.append(annotations[i])
                break
            i += 1
        return replace_tokens
    
    def serialise(self, model):
        """
        Serializes a SQLAlchemy model object into a dictionary.

        Args:
            model: SQLAlchemy model object.

        Returns:
            dict: Serialized representation of the model object.
        """
        columns = [c.key for c in inspect(model).mapper.column_attrs]
        return {c: getattr(model, c) for c in columns}

    def get_tokens(self, file_id, objectify=False):
        """
        Retrieves tokens (annotations) associated with a file.

        Args:
            file_id (int): ID of the file.
            objectify (bool, optional): If True, returns the SQLAlchemy session and tokens. Defaults to False.

        Returns:
            list or tuple: List of token annotations or tuple with session and annotations if objectify is True.
        """
        with self.uow as uow:
            annots = uow.repo.get_tokens(file_id)
            for idx, annotation in enumerate(annots):
                annotation.token_language
                annotation.pos_instance
            if objectify:
                return self.uow.session, annots
            annotations = [{
                **self.serialise(annot),
                "token_language_id": annot.token_language.iso_code
            } for annot in annots]
            return sorted(annotations, key=lambda a: a['start_index'])

    def process_annotations(self, annotations, file_id):
        """
        Processes annotations for a file, including replacing existing tokens and adding new annotations.

        Args:
            annotations (list): List of annotations to process.
            file_id (int): ID of the file associated with the annotations.

        Raises:
            ValueError: If the file associated with file_id is not found.
        """
        with self.uow as uow:
            file = uow.repo.get_file_by_id(file_id)
            if not file:
                raise ValueError("File not found")

            extracted_annotations = self.get_tokens(file_id, objectify=False)
            for annotation in annotations:
                replace_tokens = self.get_replaced_tokens(annotation["start_index"], annotation["end_index"], extracted_annotations)
                for token in replace_tokens:
                    uow.repo.delete_token_by_id(token["id"])
                uow.repo.add_annotation(annotation, file, file_id)
                uow.commit()

    def serialise_data_model(self, model):
        """
        Serializes a SQLAlchemy model object into a dictionary, excluding private attributes.

        Args:
            model: SQLAlchemy model object.

        Returns:
            dict: Serialized representation of the model object.
        """
        return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}

    def auto_tokenise(self, file_data, reserved_tokens):
        """
        Performs automatic tokenization on the content of a file using specified reserved tokens.

        Args:
            file_data (dict): Dictionary containing 'content', 'lang_id', and 'file_id'.
            reserved_tokens (list): List of reserved tokens.

        Returns:
            list: List of tokenized tokens with start_index, end_index, and token_language_id.
        """
        text = file_data['content']
        lang_id = file_data['lang_id']
        uploaded_file_id = file_data['file_id']
        resv_tks = []

        for token in reserved_tokens:
            tok_mod = TokenModel(reserved_token=True, start_index=token['start_index'],
                                    end_index=token['end_index'], token_language_id=lang_id, type_=token['type_'],
                                    uploaded_file_id=uploaded_file_id)
            resv_tks.append(self.serialise_data_model(tok_mod))
        with self.uow as uow:
            lang = uow.repo.get_language_by_id(lang_id)
            tokenised_text = cardamom_tokenise(text, iso_code=lang.iso_code, reserved_toks=resv_tks,
                                        uploaded_file_id=uploaded_file_id)
            tokenised_text = [self.serialise_data_model(token_model) for token_model in tokenised_text]
            tokenised_text = sorted(tokenised_text, key=lambda a: a['start_index'])
            return tokenised_text
