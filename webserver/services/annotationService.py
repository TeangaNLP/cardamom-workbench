from sqlalchemy.inspection import inspect
from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from model import TokenModel
from technologies import cardamom_tokenise

class AnnotationService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow

    def get_replaced_tokens(self, start, end, annotations):
        # fetch the saved tokens
        i = 0
        replace_tokens = []
        while i < len(annotations):
            # if the new start is greater than annotations start
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

    def process_annotations(self, annotations, file_id):
        with self.uow as uow:
            file = uow.repo.get_file_by_id(file_id)
            if not file:
                raise ValueError("File not found")

            extracted_annotations = self.get_tokens(file_id, objectify=False)
            print(extracted_annotations)
            for annotation in annotations:
                replace_tokens = self.get_replaced_tokens(annotation["start_index"], annotation["end_index"], extracted_annotations)
                for token in replace_tokens:
                    print(token["id"])
                    uow.repo.delete_token_by_id(token["id"])
                uow.repo.add_annotation(annotation, file, file_id)
                uow.commit()
    def serialise_data_model(self,model):
        return {k: v for k, v in model.__dict__.items() if not k.startswith("_")}

    def auto_tokenise(self,file_data,reserved_tokens ):
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
            print(repr(text),flush=True)
            print([(text[t['start_index']:t['end_index']],t['start_index'],t['end_index']) for t in tokenised_text],flush=True)
            return tokenised_text