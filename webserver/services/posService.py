from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from sqlalchemy.inspection import inspect
from technologies import  cardamom_postag

class POSService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow
    
    def serialise_data_model(self, model):
        return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}

    def serialise(self, model):
        columns = [c.key for c in inspect(model).mapper.column_attrs]
        return {c: getattr(model, c) for c in columns}

    def get_tokens(self, file_id, objectify=False):
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
        
    def add_pos_tags(self, pos_tags):
        for token_id, tag_data in pos_tags.items():
            if tag_data["tag"] is None:
                continue
            else:
                with self.uow as uow:
                    pos_instance = uow.pos_repository.add_pos_instance(int(token_id), tag_data["tag"], tag_data["type_"])
                    if tag_data.get('features'):
                        for feature_data in tag_data['features']:
                            uow.pos_repository.add_pos_feature(pos_instance.id, feature_data["feature"], feature_data["value"])
    
    def get_postags(self, file_id):
        session, tokens = self.get_tokens(file_id, objectify=True)
        print(session)
        
        token_tags = {}
        for token in tokens:
            instances = token.pos_instance
            for instance in instances:
                features = instance.features
                tag_features = []
                for feature in features:
                    tag_features.append({"feature": feature.feature, "value": feature.value})
                token_tags[token.id] = {"tag": instance.tag, "features": tag_features, "start_index": token.start_index,
                                    "type_": token.type_, "token_id": token.id}
        annotations = self.get_tokens(file_id)
        annotations = [{"pos_tags": [self.serialise(posInstance) for posInstance in tokens[idx].pos_instance], **annotation} for idx, annotation in enumerate(annotations)]
        session.close()
        return   {"annotations": sorted(annotations, key=lambda a: a['start_index']), "tags": token_tags}
    
    def auto_tag(self, file_data):
        
        file_id = file_data["file_id"]
        lang_id = file_data["lang_id"]

        with self.uow as uow:
            file_obj = uow.annotation_repository.get_file_by_id(file_id)
            content = file_obj.content
            tokens = self.get_tokens(file_id)
            lang = uow.annotation_repository.get_language_by_id(lang_id)
            pos_tags = cardamom_postag(content, tokens, lang)
            pos_tags = [self.serialise_data_model(tags) for tags in pos_tags]
        return pos_tags