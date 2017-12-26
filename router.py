import os
from flask import Flask, jsonify, request, url_for, render_template
from flask_cors import CORS
import json

# from python.generator import *
from python.main import *
# from python.solver import *

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/index.html')
def main():
	return render_template('index.html')

@app.route('/rand', methods=['POST'])
def rand():
	print(request.values)
	path2 = make_puzzle(int(request.values['size']), True, 10000)
	print(path2)
	# ret = [str(i)+"," for i in path2]
	return json.dumps(path2)

@app.route('/solve', methods=['POST'])
def solve():
	print(request.values)
	initial_field = [int(i) for i in request.values['field'].split(',')]
	print(initial_field)
	rez = from_site(int(request.values['size']), initial_field)
	# print("TIME = ", rez[''])
	return json.dumps(rez)

if __name__ == '__main__':
	app.run(debug=True)
