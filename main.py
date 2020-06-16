# -*- coding: utf-8 -*-
from flask import Flask, make_response, request, send_file
from flask_cors import CORS
from flask import render_template
import os
import settings
from flask_restful import Resource, Api, reqparse
from crawler import googleExcelCrawler
import zipfile
from flask import send_file
import time
from io import BytesIO
import json
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/api/*": {"origins": r"*"}})


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


class getFile(Resource):
    def get(self):
        app.logger.info('Processing default request')
        keys = ['en-gb','zh-cn','id-id','vi-vn','km-kh','pt-br','ko-kr','ja-jp','th-th']
        datasource = googleExcelCrawler.geti18nFromExcel(os.environ.get('GoogleAuthKey'),os.environ.get('GoogleSheetId'),keys,app)
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for key in keys:
                data = zipfile.ZipInfo(key +'.json')
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, json.dumps(datasource[key],ensure_ascii= False).encode('utf-8') )
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='i18n.zip', as_attachment=True)

api.add_resource(getFile, '/getfile')
if __name__ == "__main__":
    #app.debug = True    
    app.config['TEMPLATES_AUTO_RELOAD'] = True      
    app.jinja_env.auto_reload = True
    app.run()        