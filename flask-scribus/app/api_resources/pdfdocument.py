# OS
import os

# Import send_file, abort
from flask import send_file, abort

# Import resource
from flask_restful import Resource

class PDFDocument(Resource):
    """ REST: PDFDocument resource """
    def get(self, document_uid):
        # get path to pdf
        pdfFilename = document_uid + '.pdf'
        pdfPath = os.path.join('pdf', pdfFilename)

        # be sure that file exists
        if os.path.exists(pdfPath):
            return send_file(os.path.join('../pdf/', pdfFilename))
        else:
            # if not found return 404
            abort(404)
