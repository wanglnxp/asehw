from flask import Flask, request
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
date_of_game = []

app = Flask(__name__)

DATABASEURI = "postgresql://Linnan@localhost:5432/mydb"

engine = create_engine(DATABASEURI)

engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
      g.conn.close()
    except Exception as e:
      pass


@app.route('/')
def index():
    print request.args
    return render_template("index.html", **locals())


@app.route('/error')
def error():
    print request.args
    return render_template("error.html", **locals())


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    message = request.form['message']

    try:
        g.conn.execute("""INSERT INTO record
        VALUES (%s, %s );""", name, message)
    except:
        return redirect('/error')

    return render_template("index.html", **locals())


@app.route('/record')
def record():
    print request.args

    try:
        newcurs = g.conn.execute("""SELECT * FROM record""")
    except:
        print "database error"
        return "<h1>It is database error<h1>"

    info = []
    for result in newcurs:
        temp = []
        temp.append(result['user_name'].encode("utf-8"))
        temp.append(result['message'].encode("utf-8"))
        info.append(temp)
    newcurs.close()

    if not record:
        return redirect('/')

    return render_template("record.html", **locals())


@app.route('/bacon', methods=['GET', 'POST'])
def bacon():
    if request.method == 'POST':
        return "You're using POST"
    else:
        return "You're using using GET"


@app.route('/tuna')
def tuna():
    return '<h1>Tuna is good</h1>'


@app.route('/profile/<username>')
def profile(username):
    return '<h2>Welcome %s</h2>' % username


@app.route('/post/<int:post_id>')
def post(post_id):
    post_id *= 5
    return '<h2>This is your post ID * 5 = %s</h2>" ' % post_id


if __name__ == "__main__":  # check whether the file is called directly, otherwise do not run
    app.run(debug=true)
