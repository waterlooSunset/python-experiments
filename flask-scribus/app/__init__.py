# Import flask and template operators
from flask import Flask, render_template

# Import flask-rest
from flask_restful import Api

# Import flask-rest resources
from api_resources.scribusjob import ScribusJob
from api_resources.pdfdocument import PDFDocument
from api_resources.pdfexists import PDFExists
from api_resources.pdfimage import PDFImage
from api_resources.templates import Templates

# Import flask blueprint resources
from blueprint_resources.backend import backend as Backend

# Define the WSGI application object
app = Flask(__name__)

# Enable/disable debugging
app.debug = True

# Register blueprints
app.register_blueprint(Backend)

# Init API
api = Api(app, prefix='/api/v1')

# Setup api resources
api.add_resource(ScribusJob, '/jobs')
api.add_resource(Templates, '/templates')
api.add_resource(PDFDocument, '/document/<string:document_uid>')
api.add_resource(PDFImage, '/document/<string:document_uid>/image')
api.add_resource(PDFExists, '/document/<string:document_uid>/exists')
