from flask import Flask, request, jsonify
import json
app = Flask(__name__)
app.counter = 0

@app.route('/', methods = ['GET'])
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

@app.route('/show_data', methods = ['POST'])
def show_data():    
    return jsonify(request.get_json())

@app.route('/pretty_print_name', methods = ["POST"])
def pretty_print_name():
    return f'Na imię mu {request.get_json()["name"]}, a nazwisko jego {request.get_json()["surename"]}'

@app.route('/counter')
def counter():
    app.counter += 1
    return str(app.counter)

if __name__ == '__main__':
    app.run(debug=True)
