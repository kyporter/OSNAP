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
    return redirect("/login")

@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        role = request.form['role']
        cur.execute("SELECT password FROM users WHERE username = (%s);", (uname,))
        exist = cur.fetchall()
        if exist == []:
            cur.execute("INSERT INTO users (username, password, role_Fk) VALUES ((%s), (%s), (SELECT role_pk FROM roles WHERE title = (%s)));", (uname, pword, role))
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
        if result != None and result[0] == True:
            session['name'] = uname
            return redirect("/dashboard")
        else:
            return render_template('login_fail.html')

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if request.method == 'GET':
        uname = session['name']
        cur.execute("SELECT title FROM roles JOIN users ON role_pk = role_fk WHERE username=(%s);", (uname,))
        role = cur.fetchone()[0]
        return render_template('dashboard.html', username = uname, role = role)

@app.route("/add_facility", methods=['GET', 'POST'])
def add_facility():
    if request.method == 'GET':
        return render_template('add_facility.html')
    if request.method == 'POST':
        com_name = request.form['common']
        fcode = request.form['fcode']
        cur.execute("SELECT facility_pk FROM facilities WHERE fac_code = (%s) or common_name = (%s);", (fcode, com_name))
        if cur.fetchall() == []:
            cur.execute("INSERT INTO facilities (fac_code, common_name) VALUES ((%s), (%s));", (fcode, com_name))
            conn.commit()
            return redirect("/add_facility")
        else:
            return render_template("add_fac_fail.html", c_name=com_name)

@app.route("/logout", methods=['GET'])
def logout():
    if request.method == 'GET':
        uname = session['name']
        session.clear() #ends session
        return render_template("logout.html", username=uname)
