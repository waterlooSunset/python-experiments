# Import Flask blueprint, render_remplate
from flask import Blueprint, render_template, url_for

backend = Blueprint('backend', __name__, template_folder='app/templates')

@backend.route('/', methods=['GET'])
def page():
    """
    Backend route
    """
    # render test.html
    return render_template("index.html")
