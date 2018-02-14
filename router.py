from flask import Flask, jsonify, request, url_for, render_template
from flask_cors import CORS
import json
from python.main import *

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/index.html')
def main():
	return render_template('index.html')


@app.route('/info')
@app.route('/info.html')
def info():
	return render_template('info.html')


@app.route('/rand', methods=['POST'])
def rand():
	path2 = getRandomPath(int(request.values['size']))
	return json.dumps(path2)


@app.route('/solve', methods=['POST'])
def solve():
	initial_field = [int(i) for i in request.values['field'].split(',')]
	rez = from_site(int(request.values['size']), initial_field, request.values['algo'], request.values['heuristics'])
	return json.dumps(rez)


@app.route('/parse_file', methods=['POST'])
def parse_file():
	file = request.values['file']
	initial_field = []
	i = 0
	n = 0
	if not file or file == "":
		return json.dumps({'error': 'Bad file'})
	for line in file.split('\n'):
		j = 0
		if line == "":
			continue
		elif line[0] == '#':
			pass
		elif n == 0:
			print(line.split())
			try:
				n = int(line.split()[0])
			except:
				return json.dumps({'error': 'Bad file'})
			print(n)
			if n != 3 and n != 4:
				return json.dumps({'error': 'Bad file'})
			field_size = pow(n, 2)
			initial_field = [0 for _ in range(field_size)]
		else:
			line = [s for s in line.split() if s != '']
			print(line)
			for j in range(n):
				try:
					initial_field[i * n + j] = int(line[j])
				except:
					return json.dumps({'error': 'Bad file'})
			i += 1
	if not initial_field or len(initial_field) != pow(n, 2):
		return json.dumps({'error': 'Bad file'})
	return json.dumps({'size': n, 'field': initial_field})


if __name__ == "__main__":
	app.run()
