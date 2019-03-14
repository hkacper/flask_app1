from flask import Flask, request, jsonify
import json
app = Flask(__name__)
app.counter = 0

@app.route('/')
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
    response = jsonify(request.get_json())
    return f'Na imię mu {response.name}, a nazwisko jego {response.surname}'

@app.route('/counter')
def counter():
    app.counter += 1
    return str(app.counter)

if __name__ == '__main__':
    app.run(debug=True)
