from flask import Flask, render_template, request, flash, g, abort, jsonify, session, url_for
import datetime, sqlite3, os


DATABASE='/tmp/flboard.db'
DEBUG=True
SECRET_KEY = 'ir9guewg8ey8f04(*&^&@#@$$hgfy%WEFE*((*^$#%$uoei&^y8e9rujhEJFUEFbdfigudru9gLURG7Y84Y'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flboard.db')))
app.config['UPLOAD_FOLDER']="static\images"


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def cursor_db():
    c = connect_db()
    cursor = c.cursor()
    return cursor


def create_db():
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "/anime/", "url": "/anime"},
        {"name": "/autos/", "url": "/autos"},
        {"name": "/cook/", "url": "/cook"},
        {"name": "/films/", "url": "/films"},
        {"name": "/manga/", "url": "/manga"},
        {"name": "/science/", "url": "/science"},
        {"name": "/serials/", "url": "/serials"},
        {"name": "/shiz/", "url": "/shiz"},
        {"name": "/sport/", "url": "/sport"},
        {"name": "/testdb/", "url": "/testdb"}]


menu1 = [{"name": "/anime/", "url": "/anime"},
        {"name": "/autos/", "url": "/autos"},
        {"name": "/cook/", "url": "/cook"},
        {"name": "/films/", "url": "/films"},
        {"name": "/manga/", "url": "/manga"}]


menu2 = [{"name": "/science/", "url": "/science"},
        {"name": "/serials/", "url": "/serials"},
        {"name": "/shiz/", "url": "/shiz"},
        {"name": "/sport/", "url": "/sport"},
        {"name": "/testdb/", "url": "/testdb"}]


@app.route("/")
def index():
    return render_template('index.html', title="Welcome to rach.ch!", menu1=menu1, menu2=menu2)


@app.route("/testdb", methods=['POST', 'GET'])
def testdb():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'testdb', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'testdb', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'testdb' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('testdb-threads.html', title="/Testing DB/", threads=threads, menu=menu, topic="testdb")


@app.route("/anime", methods=['POST', 'GET'])
def anime():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'anime', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'anime', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'anime' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('anime-threads.html', title="/Anime/", threads=threads, menu=menu, topic="anime")


@app.route("/anime/<post>", methods=['POST', 'GET'])
def anime_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", post).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", post).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", post).fetchall()
    db.close()
    return render_template('anime-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/autos", methods=['POST', 'GET'])
def autos():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'autos', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'autos', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'autos' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('autos-threads.html', title="/Autos/", threads=threads, menu=menu, topic="autos")


@app.route("/autos/<post>", methods=['POST', 'GET'])
def autos_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('autos-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/cook", methods=['POST', 'GET'])
def cook():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'cook', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'cook', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'cook' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('cook-threads.html', title="/Cook/", threads=threads, menu=menu, topic="cook")


@app.route("/cook/<post>", methods=['POST', 'GET'])
def cook_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('cook-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/films", methods=['POST', 'GET'])
def films():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'films', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'films', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'films' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('films-threads.html', title="/Films/", threads=threads, menu=menu, topic="films")


@app.route("/films/<post>", methods=['POST', 'GET'])
def fimls_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('films-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/manga", methods=['POST', 'GET'])
def manga():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'manga', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'manga', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'manga' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('manga-threads.html', title="/Manga/", threads=threads, menu=menu, topic="manga")


@app.route("/manga/<post>", methods=['POST', 'GET'])
def manga_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('manga-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/science", methods=['POST', 'GET'])
def science():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'science', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'science', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'science' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('science-threads.html', title="/Science/", threads=threads, menu=menu, topic="science")


@app.route("/science/<post>", methods=['POST', 'GET'])
def science_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('science-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/serials", methods=['POST', 'GET'])
def serials():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'serials', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'serials', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'serials' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('serials-threads.html', title="/Serials/", threads=threads, menu=menu, topic="serials")


@app.route("/serials/<post>", methods=['POST', 'GET'])
def serials_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('serials-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/sport", methods=['POST', 'GET'])
def sport():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'sport', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'sport', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'sport' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('sport-threads.html', title="/Sport/", threads=threads, menu=menu, topic="sport")


@app.route("/sport/<post>", methods=['POST', 'GET'])
def sport_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('sport-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/shiz", methods=['POST', 'GET'])
def shiz():
    db = get_db()
    if request.method == 'POST':
        upload_image = request.files['thread-image']
        if len(request.form['thread-name']) >= 4:
            flash("Thread created successfully!", category='success')
            name = request.form['thread-name']
            date = datetime.datetime.now()
            text = request.form['thread-text']
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO threads(name_thread, date_thread, img_thread, category_thread, text_thread) VALUES (?, ?, ?, ?, ?)",
                (name, str(date), upload_image.filename, 'shiz', text))
            else:
                db.execute("INSERT INTO threads(name_thread, date_thread, category_thread, text_thread) VALUES (?, ?, ?, ?)",
                (name, str(date), 'shiz', text))
            db.commit()
        else:
            flash("Too short thread name!", category='error')
    threads = db.execute("SELECT * FROM threads WHERE category_thread = 'shiz' ORDER BY id_thread DESC").fetchall()
    db.close()
    return render_template('shiz-threads.html', title="/Shiz/", threads=threads, menu=menu, topic="shiz")


@app.route("/shiz/<post>", methods=['POST', 'GET'])
def shiz_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", (post,)).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", (post,)).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", (post,)).fetchall()
    db.close()
    return render_template('shiz-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/testdb/<post>", methods=['POST', 'GET'])
def num_post(post):
    db = get_db()
    cursor = cursor_db()
    cursor.execute("SELECT COUNT(id_thread) FROM threads WHERE category_thread = 'testdb'")
    count = cursor.fetchone()[0]
    if str(post).isdigit() == False or int(post) > count or int(post) <= 0:
        raise ValueError("Incorrect argument")
        abort(404)
    if request.method == 'POST':
        upload_image = request.files['post-image']
        if len(request.form['post-text']) > 0:
            flash("Post created successfully!", category='success')
            text = request.form['post-text']
            date = datetime.datetime.now()
            if upload_image.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
                upload_image.save(filepath)
                db.execute("INSERT INTO posts(id_thread_post, date_post, img_post, text_post) VALUES (?, ?, ?, ?)", 
                (post, str(date), upload_image.filename, text))
            else:
                db.execute("INSERT INTO posts(id_thread_post, date_post, text_post) VALUES (?, ?, ?)", 
                (post, str(date), text))
            db.commit()
        else:
            flash("Too short post!", category='error')
    title = db.execute("SELECT name_thread FROM threads WHERE id_thread = ?", post).fetchall()
    description = db.execute("SELECT * FROM threads WHERE id_thread = ?", post).fetchall()
    posts = db.execute("SELECT * FROM posts WHERE id_thread_post = ? ORDER BY id_post DESC", post).fetchall()
    db.close()
    return render_template('testdb-posts.html', names=title, descriptions=description, posts=posts, menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title="About rach.ch")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found :("), 404


create_db()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True, port = 5000)