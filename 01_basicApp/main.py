"""
This is Toy System for homework 2
The website can store user message and retrive all of them
"""

# import os
# import traceback
import sys
from sqlalchemy import create_engine
from flask import Flask, request, render_template, g, redirect


# TMPL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# APP = Flask(__name__, template_folder=TMPL_DIR)

APP = Flask(__name__)

DATABASEURI = "postgresql://Linnan@localhost:5432/mydb"
ENGINE = create_engine(DATABASEURI)


@APP.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = ENGINE.connect()
    except Exception:
        print "uh oh, problem connecting to database"
        # traceback.print_exc()
        g.conn = None


@APP.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception:
        print exception


@APP.route('/')
def index():
    """
    access the main page
    :return:
    """
    return render_template("index.html", **locals())


@APP.route('/error')
def error():
    """
    access the error page
    :return:
    """
    return render_template("error.html", **locals())


@APP.route('/add', methods=['POST'])
def add():
    """
    add user enter message and user name to database
    :return: main page
    """
    name = request.form['name']
    message = request.form['message']

    try:
        newcurs = g.conn.execute("""INSERT INTO record
        VALUES (%s, %s );""", name, message)
        newcurs.close()
    except Exception:
        print "can not write record to database"
        return redirect('/error')

    return render_template("index.html", **locals())


@APP.route('/record')
def record():
    """
    access record page where can see all the data in database
    :return: record page
    """

    try:
        newcurs = g.conn.execute("""SELECT * FROM record""")
    except Exception:
        print "can not read record from database"
        return redirect('/error')

    info = []
    for result in newcurs:
        temp = [result['user_name'].encode("utf-8"), result['message'].encode("utf-8")]
        info.append(temp)
    newcurs.close()

    if not record:
        return redirect('/')

    return render_template("record.html", **locals())


@APP.route('/delete', methods=['POST'])
def delete():
    """
    This is method only for test purpose to delete test case
    :return: delete info
    """
    name = request.form['name']
    message = request.form['message']

    try:
        newcurs = g.conn.execute("""DELETE FROM record
        WHERE record.user_name = %s AND record.message = %s;""", name, message)
        newcurs.close()
    except Exception:
        print "can not write record to database"
        return redirect('/error')

    return "successfully deleted the message"

if __name__ == "__main__":
    # check whether the file is called directly, otherwise do not run
    reload(sys)
    sys.setdefaultencoding('utf8')
    APP.run(debug=True)
