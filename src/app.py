from flask import Flask, render_template, request, session, redirect, url_for, jsonify 
import psycopg2 
import psycopg2.extras
from config import dbname, dbhost, dbport  ##FROM dellsword/lost app.py
import json



app = Flask(__name__)
#Because this is what the websites told me to do(almost):
app.secret_key = 'wecanpretendthisisarandomkeyright?'

conn = psycopg2.connect(database=dbname, host=dbhost, port=dbport)  ##using variables from config file
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  ##Should create a cursor that produces a 	
								##dictionary of results

@app.route('/')
def index(): 
    return render_template('login.html') 

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/reportmain', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        username = request.form["uname"]
        session['name'] = username  #start the session and link to username, will end when logout page is hit
        facquery = cur.execute("SELECT common_name FROM facilities;")
        faclist = []
        for result in cur:
            faclist.append(result[0]) #because psycopg2 SQL queries return lists of tuples, and I don't want to send a tuple to my html
        return render_template('report_main.html', faclist = faclist)

@app.route('/facility_report', methods=['POST', 'GET'])
def facility():
    if request.method == 'POST':
        day = request.form["day"]
        month = request.form["month"]
        year = request.form["year"]
        datecheck = month + '/' + day + '/' + year
        facname = request.form["facility_name"]
	#because the returned facname, if it had a space in it, is now truncated, I need the next 4 lines to retrieve the rest of the name
        cur.execute("SELECT common_name FROM facilities WHERE common_name LIKE (%s);", (facname+'%',))
        factuple = cur.fetchall()
        if len(factuple) != 0:
            facname = factuple[0][0]
        else:
            facname = 'Did Not Work'  ##I'm leaving this in, if this shows up it means facility name wasn't read 
##correctly from the form, which is important to know because it would affect the results displayed
        cur.execute('''SELECT a.asset_tag, a.description, aa.arrive_dt, aa.depart_dt 
FROM asset_at aa JOIN facilities f ON aa.facility_fk = f.facility_pk JOIN assets a ON 
a.asset_pk = aa.asset_fk WHERE f.common_name = (%s) AND (((%s) BETWEEN aa.arrive_dt AND aa.depart_dt) 
OR (((%s) >= aa.arrive_dt) AND (aa.depart_dt IS NULL)));''', (facname, datecheck, datecheck))
        infos = cur.fetchall() #elements are parsed in my html
        return render_template('facility_report.html', results = infos, facility=facname, date=datecheck)
    else:
        return render_template('logout.html') #if something goes wrong, it's supposed to redirect to logout page

@app.route('/transit_report', methods=['POST', 'GET'])
def transit():
    if request.method == 'POST':
        day = request.form["day"]
        month = request.form["month"]
        year = request.form["year"]
        datecheck = month + '/' + day + '/' + year
        cur.execute('''SELECT a.asset_tag, a.description, f1.common_name, t.load_dt, f2.common_name, 
t.unload_dt FROM facilities f1 JOIN convoys c ON f1.facility_pk = c.source_fk JOIN facilities f2 ON 
f2.facility_pk = c.dest_fk JOIN asset_on t ON t.convoy_fk = c.convoy_pk JOIN assets a ON a.asset_pk 
= t.asset_fk WHERE (%s) BETWEEN t.load_dt AND t.unload_dt;''', (datecheck,))
        infos = cur.fetchall() #elements are parsed in my html
        return render_template('transit_report.html', datecheck=datecheck, results = infos)
    else:
        return render_template('logout.html') #if something goes wrong, it's supposed to redirect to logout page

@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/activate_user', methods=['POST'])
def activate_user():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])
        dat = dict()
        dat['timestamp'] = req['timestamp']
	##needs check for pre-existence,validation note
        cur.execute("INSERT INTO users (username, active) VALUES ((%s), TRUE);", (req['username'],))
        conn.commit()
	#fix return to correct json file
        return jsonify(timestamp = req['timestamp'], result = "OK")
    else:
        return render_template('rest.html')


@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    if request.method == 'POST' and 'arguments' in request.form:
	#there may be an issue with this?
        req = json.loads(request.form['arguments'])
        dat = dict()
        dat['timestamp'] = req['timestamp']
        dat['result'] = 'OK'
        cur.execute("UPDATE users SET active = FALSE WHERE username=(%s);", (req['username'],))
        conn.commit()
	#make sure is returning as correct json file
        return jsonify(timestamp = req['timestamp'], result = "OK")
    else:
        return render_template('rest.html')

@app.route('/rest/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])
        #because all or none, will need to check if any product already in table before adding any
        for arg in req['new_products']:
            vend = arg['vendor']
            desc = arg['description']
            alt = arg['alt_description']
            comps = arg['compartments']
            cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES ((%s), (%s), (%s));", 
                (vend, desc, alt))
            ##add insert into security_tags
            conn.commit()
        return render_template('rest.html')
    else:
        return render_template('rest.html')

@app.route('/logout', methods=['POST', 'GET'])
def goodbye():
    byeuser = session['name']
    session.clear()  #ends session
    return render_template('logout.html', username = byeuser)



