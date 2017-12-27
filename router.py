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
	path2 = getRandomPath(int(request.values['size']))
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

@app.route('/parse_file', methods=['POST'])
def parse_file():
	file = request.values['file']
	initial_field = []
	i = 0
	n = 0
	for line in file.split('\n'):
		j = 0
		if line == "":
			continue
		# line = line.strip()
		print("[", line, "]")
		if line[0] != '#' and not line[0].isdigit():
			return json.dumps({'error': 'Bad file'})
		elif line[0] == '#':
			pass
		elif n == 0:
			n = int(line)
			if n < 1:
				return json.dumps({'error': 'Bad file'})
			field_size = pow(n, 2)
			initial_field = [0 for s in range(field_size)]
		else:
			line = [s for s in line.split(' ') if s != '']
			for j in range(n):
				try:
					initial_field[i * n + j] = int(line[j])
				except:
					return json.dumps({'error': 'Bad file'})
			i += 1
	return json.dumps({'size': n, 'field': initial_field})

if __name__ == '__main__':
	app.run(debug=True)
