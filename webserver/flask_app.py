from flask import Flask
from api import api
from views import views
from flask_cors import CORS
from werkzeug.middleware.profiler import ProfilerMiddleware

app = Flask(__name__)
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=('/app/webserver/api.py') )
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

app.run(host="0.0.0.0", port=80,debug=True)
