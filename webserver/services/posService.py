from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from utilities import serialise
from technologies import cardamom_postag

class POSService:
    """
    Service class for handling Part-Of-Speech (POS) tagging operations using the SQLAlchemy unit of work pattern.
    """

    def __init__(self, uow: SqlAlchemyUnitOfWork):
        """
        Initializes the POSService with a SQLAlchemy unit of work instance.

        Args:
            uow (SqlAlchemyUnitOfWork): The SQLAlchemy unit of work instance.
        """
        self.uow = uow

    def serialise_data_model(self, model):
        """
        Serializes a SQLAlchemy model object into a dictionary, excluding private attributes.

        Args:
            model: SQLAlchemy model object.

        Returns:
            dict: Serialized representation of the model object.
        """
        return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}

    def get_postags(self, file_id):
        """
        Retrieves POS tags associated with a file.

        Args:
            file_id (int): ID of the file.

        Returns:
            dict: Dictionary containing annotations and POS tags.
        """
        with self.uow as uow:
            tokens = uow.repo.get_tokens(file_id)
            for idx, token in enumerate(tokens):
                token.token_language  
                token.pos_instance

            token_tags = {}
            for token in tokens:
                instances = token.pos_instance
                for instance in instances:
                    features = instance.features
                    tag_features = []
                    for feature in features:
                        tag_features.append({"feature": feature.feature, "value": feature.value})
                    token_tags[token.id] = {
                        "tag": instance.tag,
                        "features": tag_features,
                        "start_index": token.start_index,
                        "type_": token.type_,
                        "token_id": token.id
                    }

            annotations = sorted([{
                **serialise(token),
                "token_language_id": token.token_language.iso_code} for token in tokens], key=lambda a: a['start_index'])
            annotations = [{"pos_tags": [serialise(posInstance) for posInstance in tokens[idx].pos_instance], **annotation} for idx, annotation in enumerate(annotations)]

            return {
                "annotations": sorted(annotations, key=lambda a: a['start_index']),
                "tags": token_tags
            }

    def auto_tag(self, file_data):
        """
        Automatically tags a file's content with POS tags.

        Args:
            file_data (dict): Dictionary containing 'file_id' and 'lang_id'.

        Returns:
            list: List of serialized POS tags.
        """
        with self.uow as uow:
            file_id = file_data["file_id"]
            lang_id = file_data["lang_id"]
            file_obj = uow.repo.get_file_by_id(file_id)
            content = file_obj.content
            session = uow.session
            annots = uow.repo.get_tokens(file_id)
            for idx, annotation in enumerate(annots):
                annotation.token_language
                annotation.pos_instance
            annotations = [{
                **serialise(annot),
                "token_language_id": annot.token_language.iso_code
            } for annot in annots]
            tokens = sorted(annotations, key=lambda a: a['start_index'])
            lang = uow.repo.get_language_by_id(lang_id)
            pos_tags = cardamom_postag(content, tokens, lang)
            pos_tags = [self.serialise_data_model(tags) for tags in pos_tags]
            print(pos_tags)
            return pos_tags

    def add_pos_tags(self, pos_tags):
        """
        Adds POS tags to the database.

        Args:
            pos_tags (dict): Dictionary of POS tags to add.

        Returns:
            None
        """
        with self.uow as uow:
            for token_id, tag_data in pos_tags.items():
                if tag_data["tag"] is None:
                    continue
                pos_instance = uow.repo.add_pos_instance(int(token_id), tag_data["tag"], tag_data["type_"])
                if tag_data.get('features'):
                    for feature_data in tag_data['features']:
                        uow.repo.add_pos_feature(pos_instance.id, feature_data["feature"], feature_data["value"])
