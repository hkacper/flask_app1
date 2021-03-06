from flask import Flask, request, jsonify, redirect, session, url_for, Response, g, render_template
from functools import wraps
import json
from uuid import uuid4, UUID
import sqlite3
#import datetime

app = Flask(__name__)
#app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.trains = {}

def check_auth(username, password):
    return username == 'TRAIN' and password == 'TuN3L'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def auth_required(funkcja):
    @wraps(funkcja)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return funkcja(*args, **kwargs)
    return decorated

def session_required(funkcja):
    @wraps(funkcja)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return funkcja(*args, **kwargs)
    return wrapper

@app.route('/', methods = ['GET'])
def hello2():
    return 'Hello, World!'

@app.route('/method', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return request.method

@app.route('/show_data', methods = ['POST', 'GET'])
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
@auth_required
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))

@app.route('/logout', methods = ['GET', 'POST'])
@session_required
def logout():
    session.pop('username', None)
    return redirect(url_for('hello2'))

@app.route('/hello', methods = ['GET'])
@session_required
def hello():
    return render_template('greeting.html', user = session['username'])

def get_train_from_json():
    train_data = request.get_json()
    if not train_data:
        pass
    return train_data

def set_train(train_id=None, data=None, update=False):
    if train_id is None:
        train_id = str(uuid4())
    if data is None:
        data = get_train_from_json()
        if data is None:
            pass
    if update:
        app.trains[train_id].update(data)
    else:
        app.trains[train_id] = data

    return train_id

@app.route('/trains', methods=['GET', 'POST'])
@session_required
def trains():
    if request.method == 'GET':
        return jsonify(app.trains)
    elif request.method == 'POST':
        train_id = set_train()
        return redirect(url_for('train', train_id=train_id, format='json'))

@app.route('/trains/<train_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@session_required
def train(train_id):
    if train_id not in app.trains:
        return 'No such train', 404

    elif request.method == 'DELETE':
        del app.trains[train_id]
        return Response('', 204)

    elif request.method == 'PUT':
        set_train(train_id)
    elif request.method == 'PATCH':
        set_train(train_id, update=True)

    elif request.method == 'GET' and request.args.get('format') != 'json':
        pass

    return jsonify(app.trains[train_id])

DATABASE = 'chinook.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.route('/tracks', methods = ['GET', 'POST'])
def tracks_list():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        if request.args.get('per_page') and request.args.get('page') and request.args.get('artist'):
            per_page = int(request.args.get('per_page'))
            page = int(request.args.get('page'))
            artist = request.args.get('artist')
            offset = (page-1)*per_page
            data = cursor.execute("""SELECT tracks.name FROM tracks
                            JOIN albums ON tracks.albumid = albums.albumid
                            JOIN artists ON albums.artistid = artists.artistid 
                            WHERE artists.name = ? ORDER BY tracks.name LIMIT ? OFFSET ? COLLATE NOCASE""", (artist, per_page, offset )).fetchall()
        elif request.args.get('per_page') and request.args.get('artist'):
            per_page = int(request.args.get('per_page'))
            artist = request.args.get('artist')
            data = cursor.execute("""SELECT tracks.name FROM tracks
                                JOIN albums ON tracks.albumid = albums.albumid
                                JOIN artists ON albums.artistid = artists.artistid 
                                WHERE artists.name = ? ORDER BY tracks.name LIMIT ? COLLATE NOCASE""", (artist, per_page)).fetchall()                                    
        elif request.args.get('per_page') and request.args.get('page'):
            per_page = int(request.args.get('per_page'))
            page = int(request.args.get('page'))
            offset = (page-1)*per_page
            data = cursor.execute("""SELECT name FROM tracks
                                ORDER BY name LIMIT ? OFFSET ? COLLATE NOCASE""", (per_page, offset)).fetchall()
        elif request.args.get('artist'):
            artist = request.args.get('artist')
            data = cursor.execute("""SELECT tracks.name FROM tracks
                                JOIN albums ON tracks.albumid = albums.albumid
                                JOIN artists ON albums.artistid = artists.artistid 
                                WHERE artists.name = ? ORDER BY tracks.name COLLATE NOCASE""", (artist,)).fetchall()
        else:
            data = cursor.execute('SELECT Name FROM tracks ORDER BY Name COLLATE NOCASE').fetchall()
        cursor.close()
        tracks = [track[0] for track in data]
        return jsonify(tracks)


    elif request.method == 'POST':
        try:
            json_data = request.get_json()
            album_id = json_data['album_id']
            media_type_id = json_data['media_type_id']
            genre_id = json_data['genre_id']
            name = json_data['name']
            composer = json_data['composer']
            milliseconds = json_data['milliseconds']
            bytes1 = json_data['bytes']
            price = json_data['price']
            cursor.execute("""INSERT INTO tracks (Name, AlbumId, MediaTypeId, GenreId, 
                            Composer, Milliseconds, Bytes, UnitPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                            (name, album_id, media_type_id, genre_id, composer, milliseconds, bytes1, price))
            db.commit()
            data = cursor.execute("SELECT * FROM tracks WHERE trackid = ?", (str(cursor.lastrowid),)).fetchone()
            cursor.close()
            return jsonify(dict(data))
        except Exception:
            return 'No error handling cuz I\'m lazy', 400


@app.route('/genres', methods = ['GET'])
def genres():
    db = get_db()
    cursor = db.cursor()
    data = cursor.execute("""SELECT genres.name, COUNT(tracks.trackid) FROM genres
                            JOIN tracks ON genres.genreid = tracks.genreid
                            GROUP BY genres.name""").fetchall()
    cursor.close()
    return jsonify(dict(data))


if __name__ == '__main__':
    app.run(debug=True)
