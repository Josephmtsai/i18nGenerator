# -*- coding: utf-8 -*-
from flask import Flask, make_response, request, send_file
from flask_cors import CORS
import os
import settings
from flask_restful import Resource, Api, reqparse
from crawler import googleExcelCrawler
import zipfile
from flask import send_file
import time
from io import BytesIO
import json
app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/api/*": {"origins": r"*"}})


class HelloWorld(Resource):
    def get(self):
        return "Hello from flask-rest"

class getFile(Resource):
    def get(self):
        keys = ['en-gb','zh-cn','id-id','vi-vn','km-kh','pt-br','ko-kr','ja-jp','th-th']
        datasource = googleExcelCrawler.geti18nFromExcel(os.environ.get('GoogleAuthKey'),os.environ.get('GoogleSheetId'),keys)
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for key in keys:
                data = zipfile.ZipInfo(key +'.json')
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, json.dumps(datasource[key],ensure_ascii= False).encode('utf-8') )
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='i18n.zip', as_attachment=True)

api.add_resource(HelloWorld, '/')
api.add_resource(getFile, '/getfile')
if __name__ == "__main__":
    app.run()        