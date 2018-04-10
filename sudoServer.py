from flask import Flask, request, make_response

from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

import subprocess


app = Flask(__name__)
api = Api(app)


class PyExecutor(Resource):
    def get(self, file):
        command = "python3 /home/homeassistant/.homeassistant/scripts/" + file
        stdoutdata = subprocess.getoutput(command)
        res = stdoutdata
        return make_response(res)
        
class BashExecutor(Resource):
    def get(self, file):
        command = "/home/homeassistant/.homeassistant/scripts/" + file
        stdoutdata = subprocess.getoutput(command)
        res = stdoutdata
        return make_response(res)
        
        

api.add_resource(PyExecutor, '/execute/python/<file>')
api.add_resource(BashExecutor, '/execute/bash/<file>')



if __name__ == '__main__':
     app.run(port=5002)
