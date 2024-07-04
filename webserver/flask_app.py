from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from api import api
from orm import Base, start_mappers
from views import views
from unit_of_work.unitOfWork import SqlAlchemyUnitOfWork

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_postgres_uri()

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)  # Create tables, ensuring they exist
    Session = sessionmaker(bind=engine)
    
    # # Add session to the app context
    @app.before_request
    def before_request():
        print("Unit of work is being instantiated")
        g.uow = SqlAlchemyUnitOfWork(Session)

    # @app.teardown_appcontext
    # def teardown_db(exception=None):
    #     uow = getattr(g, 'uow', None)
    #     if uow is not None:
    #         uow.__exit__(exception)

    start_mappers()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80, debug=True)
