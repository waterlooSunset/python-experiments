# OS
import os

# Import send_file, abort
from flask import abort

# Import resource
from flask_restful import Resource

class PDFExists(Resource):
    """ REST: PDFDocument resource """
    def get(self, document_uid):
        # get path to pdf
        pdfFilename = document_uid + '.pdf'
        pdfPath = os.path.join('pdf', pdfFilename)

        # be sure that file exists
        if os.path.exists(pdfPath):
            return {'exists' : 1}
        else:
            abort(404)
