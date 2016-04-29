# OS
import os

# Import send_file, abort
from flask import abort

# Import resource
from flask_restful import Resource

class Templates(Resource):
    """ REST: Templates resource """
    def get(self):
        templateFiles = []

        # iterate over content in folder scribus_templates
        for file in os.listdir("scribus_templates"):
            if file.endswith(".sla"):
                templateFiles.append(file)

        return templateFiles
