from flask import Blueprint, render_template, abort

views = Blueprint('views', __name__, template_folder='templates')
@views.route('/', defaults={'path': ''})
@views.route('/<path:path>')
def index(path):
    return render_template("index.html") 
