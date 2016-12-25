'''
Task : Web Service for controlling the pi board
Author : FoxIOT Study Group members
Version : 1.0 
Date : 24th December 2016
'''

# Importing modules
from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask.ext.cors import CORS, cross_origin
import os

# Declaring the app object
app = Flask(__name__)
cors = CORS(app)
# GET /
@app.route('/')
def api_root():
    return 'Welcome'

# Get /articles
@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

#Get particular article detail
@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

# Get request with arguments
# @app.route('/hello')
# def api_hello():
#     if 'name' in request.args:
#         return 'HI ' + request.args['name']
#     else:
#         return 'HI John Doe'

# Handling different types of request 
@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

# POST Request header 
@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type ;)"

@app.route('/hello', methods = ['GET'])
def api_hello():
    data = {
        'hello'  : 'world',
        'number' : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp

def glow_4():	
	os.system("sshpass -p raspberry ssh -o StrictHostKeyChecking=no pi@172.16.12.128 python /home/pi/Desktop/glow_4.py")
	processed_data = {}
	processed_data['status']="Success"
	return processed_data

@app.route('/rpiglow', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_rpiglow():
	if request.headers['Content-Type'] == 'application/json':
		req = request.json
		command_details = req['command']
		if str(command_details) == "on":
			process_data = glow_4()
        	return json.dumps(process_data)
        else:
        	return "Command not found"


# Starting the flask server
if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0')
