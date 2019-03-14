from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

@app.route('/show_data', methods = ['POST'])
def show_data():
    #x = request.get_json()
    #return jsonify(x)
    ret = request.get_json()

    resp = Response(response=ret, status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    app.run(debug=True)
