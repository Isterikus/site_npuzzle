import os

# if __name__ == "__main__":
# 	return sys;

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
	url_for('web', filename='style.css')
	url_for('web/js', filename='style.css')
	return jsonify(data)

@app.route('/tst', methods=['POST'])
def goodbye_world():
	print(request.json)
	data = {'data': os.getcwd()}
	return jsonify(data)


if __name__ == '__main__':
	app.run(debug=True)
