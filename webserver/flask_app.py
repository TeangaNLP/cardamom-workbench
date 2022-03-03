from flask import Flask
from api import api
from views import views

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)

app.run(host="0.0.0.0",port=80)
