from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from api import api
from orm import Base, start_mappers
from views import views
from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork
from repositories import userRepository, fileRepository, posRepository, annotationRepository 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_postgres_uri()

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    @app.before_request
    def before_request():
        g.uows = {}
        concrete_uows = [
            ('user_uow', SqlAlchemyUnitOfWork(Session, userRepository.UserRepository)),
            ('file_uow', SqlAlchemyUnitOfWork(Session, fileRepository.FileRepository)),
            ('pos_uow', SqlAlchemyUnitOfWork(Session, posRepository.POSRepository)),
            ('annotation_uow', SqlAlchemyUnitOfWork(Session, annotationRepository.AnnotationRepository)),
            # Add other unit of work initializations here
        ]
        for name, concrete_uow in concrete_uows:
            g.uows[name] = concrete_uow

    start_mappers()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80, debug=True)
