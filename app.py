from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

@app.route('/show_data', methods = ['GET'])
def show_data():
    return request.get_json(force=True).replace("\'", "\"")


if __name__ == '__main__':
    app.run(debug=True)
