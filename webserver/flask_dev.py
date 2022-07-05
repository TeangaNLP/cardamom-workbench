from distutils.log import debug
from flask import Flask
from flask_cors import CORS
from api import api
from views import views

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

app.run(host="0.0.0.0",port=80, debug=True)
