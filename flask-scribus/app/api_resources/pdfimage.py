# OS
import os

# Import send_file, abort
from flask import send_file, abort

# Import resource
from flask_restful import Resource

class PDFImage(Resource):
    """ REST: PDFDocument resource """
    def get(self, document_uid):
        # get path to image
        imgFileName = document_uid + '.jpg'
        imgPath = os.path.join('pdf', imgFileName)

        # be sure that file exists
        if os.path.exists(imgPath):
            return send_file(os.path.join('../pdf/', imgFileName))
        else:
            # if not found return 404
            abort(404)
