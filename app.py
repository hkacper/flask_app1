from flask import Flask, request, jsonify, redirect, session, url_for, flash

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

@app.route('/login', methods=["POST"])
def login():
    if request.form['password'] == 'TuN3L' and request.form['username'] == 'TRAIN':
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()



if __name__ == '__main__':
    app.run(debug=True)
