from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
from config import dbname, dbhost, dbport

app = Flask(__name__)
app.secret_key = "wecanpretendthisisarandomkeyright?" #so that session works

conn = psycopg2.connect(database=dbname, host=dbhost, port=dbport)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
##creating connection and cursor here hopefully makes it easier to locate and adjust as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        cur.execute("SELECT password FROM users WHERE username = (%s);", (uname,))
        exist = cur.fetchall()
        if exist == []:
            cur.execute("INSERT INTO users (username, password) VALUES ((%s), (%s));", (uname, pword))
            conn.commit()
            return render_template('c_user_success.html', username = uname)
        else:
            return render_template('c_user_fail.html', username = uname)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        cur.execute("SELECT active FROM users WHERE username=(%s) and password=(%s);", (uname, pword))
        result = cur.fetchone()
        if result != [] and result[0] == True:
        ##FIXME: if no session, remove
            session['name'] = uname
            return redirect("/dashboard")
            ##redirect to dashboard
        else:
            return render_template('login_fail.html')
