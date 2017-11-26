import os
from flask import Flask, jsonify, request, url_for, render_template
from flask_cors import CORS
import json

from python.generator import *

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/index.html')
def main():
	return render_template('index.html')

@app.route('/rand', methods=['POST'])
def rand():
	path2 = make_puzzle(int(request.json['size']), True, 10000)
	print(path2)
	ret = [str(i)+"," for i in path2]
	return json.dumps(ret)


if __name__ == '__main__':
	app.run(debug=True)
