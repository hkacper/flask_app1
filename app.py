from flask import Flask, request, jsonify, redirect, session, url_for, flash

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)

def login_required(funkcja):
    def dekorator(funkcja):
        def wrapper(*args, **kwargs):
            if request.authorization and request.authorization.username == 'TRAIN' and request.authorization.password == 'TuN3L':
                return funkcja
            return "invalid login"
        return wrapper
    return dekorator 


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
    session['visits'] = session.get('visits', 0) + 1
    return "Visists Count: {}".format(session.get('visits'))

@app.route('/login', methods=['POST'])
@login_required
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True)
