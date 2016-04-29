# Import os, json, UUD
import uuid, os, json

# Import jsonify
from flask import jsonify, request

# Import resource
from flask_restful import Resource

# Import Redis
from redis import Redis

# Import rq
from rq import Worker, Queue, Connection

# Import buildPDF method which we will pass to our redis queue
from app.modules.scribus import buildPDF

# setup redis & queue
redis_conn = Redis()
q = Queue(connection=redis_conn)

class ScribusJob(Resource):
    """ REST: ScribusJob resource """
    def writeJobsInfoJson(self, jobsInfoID, template, title, text, image):
        """ Writes json jobs info file """
        jobsInfo = {}
        jobsInfo['template']  = template
        jobsInfo['title']  = title
        jobsInfo['text']   = text
        jobsInfo['image']  = image

        with open(os.path.join('jobs', str(jobsInfoID) + '.json' ), 'w') as outfile:
            outfile.write(json.dumps(jobsInfo))

    def post(self):
        """ handle post method: submitting new jobs """
        # generate job info id (not python-rq id!)
        jobsInfoID = uuid.uuid1()

        # save files
        file = request.files['image']
        fileName = ""
        if file:
            fileName = file.filename
            file.save(os.path.join('jobs', fileName))

        # store job information in a json file
        self.writeJobsInfoJson(
            jobsInfoID,
            request.form['template'],
            request.form['title'],
            request.form['text'],
            fileName
        )

        # add job to our queue
        job = q.enqueue_call(
            func=buildPDF,
            args=(jobsInfoID,),
            result_ttl=86400
        )

        # return our job id
        return jsonify(
            jobQueueID = job.get_id(),
            jobsInfoID = jobsInfoID
        )
