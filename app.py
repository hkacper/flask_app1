from flask import Flask, request, jsonify, redirect, session, url_for, Response
from functools import wraps
#import datetime

app = Flask(__name__)
#app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def check_auth(username, password):
    return username == 'TRAIN' and password == 'TuN3L'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def required_auth(funkcja):
    @wraps(funkcja)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return funkcja(*args, **kwargs)
    return decorated

def requires_user_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/', methods = ['GET'])
def hello2():
    return 'Hello, World!'

@app.route('/hello', methods = ['GET'])
def hello():
    return "Hello World!"

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

@app.route('/show_data', methods = ['POST'])
def show_data():    
    return jsonify(request.get_json())

@app.route('/pretty_print_name', methods = ["POST"])
def pretty_print_name():
    return f'Na imię mu {request.get_json()["name"]}, a nazwisko jego {request.get_json()["surename"]}'

#@app.route('/counter')
#def counter():
#    session['visits'] = session.get('visits', 0) + 1
#    return "Visists Count: {}".format(session.get('visits'))

@app.route('/login', methods=['GET', 'POST'])
@required_auth
def login():
    session['username'] = request.authorization.username
    return redirect('https://apka-kurs.herokuapp.com/hello')

@app.route('/logout', methods = ['GET', 'POST'])
@requires_user_session
def logout():
    if request.method == 'GET':
        return redirect(url_for('login'))
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
