from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/method')
def method():
    response=make_response() 
    return response

if __name__ == '__main__':
    app.run(debug=True)
