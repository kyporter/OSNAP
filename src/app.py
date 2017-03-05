from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
from config import dbname, dbhost, dbport
from time import gmtime, strftime

app = Flask(__name__)
app.secret_key = "wecanpretendthisisarandomkeyright?" #so that session works

conn = psycopg2.connect(database=dbname, host=dbhost, port=dbport)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
##creating connection and cursor here hopefully makes it easier to locate and adjust as needed

def getFacList():
    '''Returns a list of lists where each sublist is a common name and facility code'''
    cur.execute("SELECT common_name, fac_code FROM facilities;")
    fac_list = cur.fetchall()   
    return fac_list

@app.route('/')
def index():
    return redirect("/login")

@app.route("/create_user", methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            uname = request.form['username']
            pword = request.form['password']
            role = request.form['role']
            cur.execute("SELECT password FROM users WHERE username = (%s);", (uname,))
            exist = cur.fetchall()
            if exist == []:
                cur.execute("INSERT INTO users (username, password, role_fk) VALUES ((%s), (%s), (SELECT role_pk FROM roles WHERE title = (%s)));", (uname, pword, role))
                conn.commit()
                return render_template('c_user_success.html', username = uname)
            else:
                return render_template('c_user_fail.html', username = uname)
        else:
            return redirect("/create_user")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            uname = request.form['username']
            pword = request.form['password']
            cur.execute("SELECT active FROM users WHERE username=(%s) and password=(%s);", (uname, pword))
            result = cur.fetchone()
            if result != None and result[0] == True:
                session['name'] = uname
                cur.execute("SELECT title FROM roles JOIN users ON role_fk = role_pk WHERE username=(%s);", (uname,))
                session['role'] = cur.fetchone()[0]
                return redirect("/dashboard")
            else:
                return render_template('login_fail.html')
        else:
            return redirect("/login")

@app.route("/dashboard", methods=['GET'])
def dashboard():
    if request.method == 'GET':
        if 'name' in session:
            uname = session['name']
            role = session['role']
            if role == 'Facilities Officer':
                cur.execute('''SELECT a.asset_tag, tr.request_pk FROM assets a 
JOIN transfer_requests tr ON a.asset_pk=tr.asset_fk WHERE tr.app_time IS NULL;''')
                results = cur.fetchall()                
            elif role == 'Logistics Officer':
                cur.execute('''SELECT a.asset_tag, tr.request_pk FROM assets a 
JOIN transfer_requests tr ON a.asset_pk=tr.asset_fk WHERE tr.app_time IS NOT NULL AND tr.unload_dt 
IS NULL;''')
                results = cur.fetchall()                
            else:
                results = []
            return render_template('dashboard.html', username = uname, role = role, requests = results)
        else:
            return redirect("/login")

@app.route("/add_facility", methods=['GET', 'POST'])
def add_facility():
    fac_list=getFacList()
    if request.method == 'GET':
        return render_template('add_facility.html', faclist = fac_list)
    if request.method == 'POST':
        if 'common' in request.form and 'fcode' in request.form:
            com_name = request.form['common']
            fcode = request.form['fcode']
            cur.execute("SELECT facility_pk FROM facilities WHERE fac_code = (%s) or common_name = (%s);", (fcode, com_name))
            if cur.fetchall() == []:
                cur.execute("INSERT INTO facilities (fac_code, common_name) VALUES ((%s), (%s));", (fcode, com_name))
                conn.commit()
                return redirect("/add_facility")
            else:
                return render_template("add_fac_fail.html", c_name=com_name)
        else:
            return redirect('/add_facility')

@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    if request.method == 'GET':
        cur.execute("SELECT asset_tag, description FROM assets;")
        asset_list = cur.fetchall() #is a list of lists: each item[0] is a tag, each item[1] is a descripiton
        fac_list = getFacList() 
        return render_template('add_asset.html', assets = asset_list, faclist = fac_list)
    if request.method == 'POST':
        a_tag = request.form['tag']
        desc = request.form['desc']
        fcode = request.form['fac_code']
        a_date = request.form['intake']
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = (%s);", (a_tag,))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES ((%s), (%s));", (a_tag, desc))
            cur.execute('''INSERT INTO asset_history (asset_fk, 
facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE 
asset_tag = (%s)), (SELECT facility_pk FROM facilities WHERE fac_code 
= (%s)), (%s));''', (a_tag, fcode, a_date))
            conn.commit()
            return redirect('/add_asset')
        else:
            return render_template("add_ast_fail.html", asset=a_tag)

@app.route("/dispose_asset", methods=['GET', 'POST'])
def dispose_asset():
    if session['role'] == 'Logistics Officer':
        if request.method == 'GET':
            return render_template('disposal_form.html')
        if request.method == 'POST':
            if 'tag' in request.form and 'date_disp' in request.form:
                a_tag = request.form['tag']
                d_date = request.form['date_disp']
                cur.execute("SELECT asset_pk FROM assets JOIN asset_history ON asset_pk = asset_fk WHERE asset_tag = (%s) AND arrive_dt < (%s);", (a_tag, d_date))
                a_pk = cur.fetchone()
    #check if asset exists
                if a_pk != None:
                    a_pk = a_pk[0]
    #find current facility(if depart_dt is Null, asset is still 'there'
                    cur.execute("SELECT facility_fk FROM asset_history WHERE asset_fk = (%s) AND depart_dt IS NULL;", (a_pk,)) 
                    location = cur.fetchone()[0]
    #check if asset has already been disposed of
                    if location != None: #if location is None, asset is already disposed of
                        cur.execute("UPDATE asset_history SET depart_dt = (%s) WHERE asset_fk = (%s) AND facility_fk = (%s) AND depart_dt IS NULL;", (d_date, a_pk, location))
                        cur.execute("INSERT INTO asset_history (asset_fk, arrive_dt) VALUES ((%s), (%s));", (a_pk, d_date))
                        conn.commit()
                        return redirect('/dispose_asset')
    #if asset is already disposed:
                    else:
                        return render_template("already_disposed.html", asset=a_tag)
    #if asset doesn't exist:
                else:
                    return render_template("no_asset.html", asset=a_tag)
            else:
                return redirect("/dispose_asset")
    #if current user is not a logistics officer:
    else:
        return render_template("LO_only.html", page="Asset Disposal")    

@app.route("/asset_report", methods=['GET', 'POST'])
def asset_report():
    fac_list = getFacList()
    if request.method == 'GET':
        return render_template('g_report_request.html', faclist = fac_list)
    if request.method == 'POST':
        if 'fac_code' in request.form and 'r_date' in request.form:
            fac_code = request.form['fac_code']
            r_date = request.form['r_date']
    #If a specific facility is chosen, only select assets at that facility
            if fac_code != '':
                cur.execute('''SELECT a.asset_tag, a.description, f.common_name, 
ah.arrive_dt, ah.depart_dt FROM assets a JOIN asset_history ah ON a.asset_pk = 
ah.asset_fk JOIN facilities f ON f.facility_pk = ah.facility_fk WHERE f.fac_code = (%s) AND (((%s) 
BETWEEN ah.arrive_dt AND ah.depart_dt) OR (((%s) >= ah.arrive_dt) AND 
ah.depart_dt IS NULL));''', (fac_code, r_date, r_date))
    #Otherwise, select all assets not disposed of on specified date
            else:
                cur.execute('''SELECT a.asset_tag, a.description, f.common_name, 
ah.arrive_dt, ah.depart_dt FROM assets a JOIN asset_history ah ON a.asset_pk = 
ah.asset_fk JOIN facilities f ON f.facility_pk = ah.facility_fk WHERE (((%s) 
BETWEEN ah.arrive_dt AND ah.depart_dt) OR (((%s) >= ah.arrive_dt) AND 
ah.depart_dt IS NULL));''', (r_date, r_date))
            results = cur.fetchall()
    #Each item in results: item[0]:tag, item[1]:desc, item[2]:fac common, item[3]:arrival, item[4]:departure        
            return render_template('p_report_request.html', faclist = fac_list, results = results)
        else:
            return redirect("/asset_report")

@app.route("/transfer_req", methods=['GET', 'POST'])
def transfer_req():
    if session['role'] != 'Logistics Officer':
        return render_template('LO_only.html', page = 'Transfer Requests')
    
    if request.method == 'GET':
        cur.execute('''SELECT asset_tag, common_name FROM assets JOIN 
asset_history ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk 
WHERE facility_fk IS NOT NULL and depart_dt IS NULL;''')
        assets = cur.fetchall()
        fac_list = getFacList()
        return render_template('transfer_req.html', faclist = fac_list, asset_list=assets)

    if request.method == 'POST':
        dest = request.form['des_code']
        today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        a_tag = request.form['tag']

    ##Get facility code for asset's current location
        cur.execute('''SELECT fac_code FROM assets JOIN asset_history ON 
asset_pk=asset_fk JOIN facilities ON facility_pk=facility_fk WHERE depart_dt IS         
NULL and asset_tag=(%s);''', (a_tag,))
        src_code = cur.fetchone()[0]
        cur.execute('''INSERT INTO transfer_requests (asset_fk, source, 
destination, requester, req_time) VALUES ((SELECT asset_pk FROM assets WHERE 
asset_tag=(%s)), (SELECT facility_pk FROM facilities WHERE fac_code=(%s)), (SELECT 
facility_pk FROM facilities WHERE fac_code=(%s)), (SELECT user_pk FROM users WHERE 
username=(%s)), (%s));''', (a_tag, src_code, dest, session['name'], today))
        conn.commit()
        return render_template("request_made.html", a_tag=a_tag, fac_src=src_code, fac_dest = dest)

@app.route("/approve_req", methods = ['GET', 'POST'])
def approve_req():
    if session['role'] != 'Facilities Officer':
        return render_template("FO_only.html", page='Request Approval')

    if request.method == 'GET' and 'req_num' in request.args:
        req_num = request.args.get('req_num')
        cur.execute("SELECT app_time FROM transfer_requests WHERE request_pk = (%s);", (req_num,))
        approved = cur.fetchone()

        if approved != None:
            cur.execute('''SELECT a.asset_tag, a.description, src.common_name, 
dest.common_name, tr.request_pk FROM assets a JOIN transfer_requests tr ON 
tr.asset_fk=a.asset_pk JOIN facilities src ON tr.source = src.facility_pk JOIN facilities dest ON 
tr.destination = dest.facility_pk WHERE tr.request_pk = (%s);''', (req_num,))
            results = cur.fetchone()
    #results[0]: asset tag, results[1]: asset description, results[2]: source name, 
    #results[3]: destination name, results[4]: request number
            return render_template("approve_request.html", result = results)

        else:
            return render_template("request_na.html", app_date = approved[0]) 

    if request.method == 'POST' and 'approval' in request.form and 'req_num' in request.form:
        approved = request.form['approval']
        req_num = request.form['req_num']

        if approved == 'True':
            today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #request has been approved: add approver and app_time
            cur.execute('''UPDATE transfer_requests SET app_time=(%s), 
approver=(SELECT user_pk FROM users WHERE username=(%s)) WHERE 
request_pk=(%s);''', (today, session['name'], req_num))

        else:
    #request has been denied: remove from system
            cur.execute("DELETE FROM transfer_requests WHERE request_pk=(%s);", (req_num,))                                

        conn.commit()

    return redirect('/dashboard')

@app.route("/logout", methods=['GET'])
def logout():
    if request.method == 'GET':
        uname = session['name']
        session.clear() #ends session
        return render_template("logout.html", username=uname)
