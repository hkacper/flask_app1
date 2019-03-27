from flask import Flask, request, jsonify, redirect, session, url_for, flash, Response

app = Flask(__name__)
app.counter = 0
app.secret_key = 'VFJBSU46VHVOM0w='


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


@app.route('/counter')
def counter():
    app.counter += 1
    return str(app.counter)
def check_auth(username, password):
    """This function is called to check if a username password combination is
    valid."""
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
    def wraps(func):
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return please_authenticate()
            return func(*args, **kwargs)
        return wrapper
    return wraps


@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))



if __name__ == '__main__':
    app.run(debug=True)
