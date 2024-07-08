from model import POSInstanceModel, POSFeaturesModel
from sqlalchemy.orm import Session

class POSRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_pos_instance(self, token_id, tag, type_):
        pos_instance = POSInstanceModel(token_id=token_id, tag=tag, type_=type_)
        self.session.add(pos_instance)
        self.session.commit()
        self.session.flush()
        self.session.refresh(pos_instance)
        return pos_instance

    def add_pos_feature(self, pos_instance_id, feature, value):
        pos_feature = POSFeaturesModel(posinstance_id=pos_instance_id, feature=feature, value=value)
        self.session.add(pos_feature)
        self.session.commit()
        self.session.flush()

    def close(self):
        self.session.close()
