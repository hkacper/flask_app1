from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

if __name__ == '__main__':
    app.run(debug=True)
