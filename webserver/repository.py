'''
 Repository pattern for abstracting persisting data
'''
import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod 
    def add(self, batch: model.Batch):
        raise NotImplementedError  #(2)

    @abc.abstractmethod``
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def get_all(self, user):
        annots = session.query(model.TokenModel).filter(model.TokenModel.uploaded_file_id == file_id).all()
        for idx, annotation in enumerate(annots):
            annotation.token_language
            annotation.pos_instance
        if objectify:
            return session, annots
        annotations = [{**serialise(annot),"token_language_id": annot.token_language.iso_code}\
                                        for annot in annots]
        session.close()
    def list(self):
        return self.session.query(model.Batch).all()


