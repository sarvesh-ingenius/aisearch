import os
import sys
import traceback
from flask import Flask, request, jsonify, json, Response, abort, Blueprint, render_template
from flask_cors import CORS, cross_origin
import json
from werkzeug.exceptions import HTTPException
import numpy as np
import time

# from flasgger import Swagger, swag_from
from flask import current_app as app

# from app.factory import is_mongo_connected 
from app.models.text2sql import write_query
from app.models.text2sql import get_tables_from_question 

query_gen_bp = Blueprint('query_gen_bp', __name__)
# Swagger(app)

# Error handling Functions
@query_gen_bp.errorhandler(400)
def bad_request(err):
    app.logger.exception(err)
    responseMessage = {"status": "error", "result": "{}", "error": "Bad Request Error", "statusCode":"400","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=400, mimetype='application/json'), 400


@query_gen_bp.errorhandler(403)
def forbidden_error(err):
    app.logger.exception(err)
    responseMessage = {"status": "error", "result": "{}", "error": "Access Forbidden! Sorry.", "statusCode": "403","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=403, mimetype='application/json')


@query_gen_bp.errorhandler(404)
def not_found(err):
    app.logger.exception(err)
    responseMessage = {"status": "error", "result":" {}", "error": "Resource Not Found! Check Again.",
                       "statusCode": "404","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=404, mimetype='application/json')


@query_gen_bp.errorhandler(405)
def method_not_allowed(err):
    app.logger.exception(err)
    responseMessage = {"status": "error", "result": "{}", "error": "Method Not Allowed! Check Again.",
                       "statusCode": "405","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=405, mimetype='application/json')


@query_gen_bp.errorhandler(500)
def internal_server_error(err):
    app.logger.exception(err)
    responseMessage = {"status": "error", "result": "{}", "error": "Internal Server Error!", "statusCode": "500","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=500, mimetype='application/json')


#  Route Functions

@query_gen_bp.route('/', methods=['GET', 'POST'])
@cross_origin()
def homepage():
    # responseMessage = {"status": "success", "result": "{}", "error": "I am healthy","statusCode":"200","request_id":""}
    # responseMessage = json.dumps(responseMessage)
    # return Response(response=responseMessage, status=200, mimetype='application/json')
    return render_template('index.html')

@query_gen_bp.route('/welcome', methods=['GET', 'POST'])
@cross_origin()
def welcome():
    # responseMessage = {"status": "success", "result": "{}", "error": "I am healthy","statusCode":"200","request_id":""}
    # responseMessage = json.dumps(responseMessage)
    # return Response(response=responseMessage, status=200, mimetype='application/json')
    return render_template('index.html')
    

@query_gen_bp.route('/liveness', methods=['GET', 'POST'])
@cross_origin()
def healthx():
    responseMessage = {"status": "success", "result": "{}", "error": "I am live","statusCode":"200","request_id":""}
    responseMessage = json.dumps(responseMessage)
    return Response(response=responseMessage, status=200, mimetype='application/json')

@query_gen_bp.route('/readiness', methods=['GET', 'POST'])
@cross_origin()
def healthz():
    if True:#is_mongo_connected:
        responseMessage = {"status": "success", "result": "{}", "error": "I am ready","statusCode":"200","request_id":""}
        responseMessage = json.dumps(responseMessage)
        return Response(response=responseMessage, status=200, mimetype='application/json')

@query_gen_bp.route('/process_question', methods=['POST'])
@cross_origin()
def process_question():
    mode = 'freehandmode' if 'freehandmode' in request.form else 'safemode'
    team = request.form['team']
    question = request.form['query']
    words_in_question = [x for x in question.split(" ") if (x.replace(" ", "")!="") and (len(x) >= 2)]
    if len(question) < 15 or len(words_in_question)<5:
        app.logger.info('Bad Question')
        return render_template('results.html', label='Error', question=question, query='You will have to be more specific than that', box_color = 'red')
    query = write_query(question, team)
    if query is None:
        return render_template('results.html', label='Error', question=question, query='Query could not be generated', box_color = 'red')
    return render_template('results.html', label='Your AI generated query', question=question, query=query, box_color = '#1893f7')