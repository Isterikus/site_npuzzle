import os

# if __name__ == "__main__":
# 	return sys;

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	data = {'data': os.getcwd()}
	return jsonify(data)


@app.route('/tst', methods=['POST'])
def goodbye_world():
	print(request.json)
	data = {'data': os.getcwd()}
	return jsonify(data)


if __name__ == '__main__':
	app.run(debug=True)
