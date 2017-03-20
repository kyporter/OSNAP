from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
from config import dbname, dbhost, dbport
from time import gmtime, strftime
from datetime import datetime

app = Flask(__name__)
app.secret_key = "wecanpretendthisisarandomkeyright?" #so that session works

conn = psycopg2.connect(database=dbname, host=dbhost, port=dbport)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
##creating connection and cursor here hopefully makes it easier to locate and adjust as needed

def getFacList():
    '''Returns a list of lists where each sublist is a common name and facility code'''
    cur.execute("SELECT common_name, fac_code FROM facilities WHERE common_name != 'in transit';")
    fac_list = cur.fetchall()   
    return fac_list

@app.route('/')
def index():
    return redirect("/login")

#web service for adding/revoking users
@app.route("/update_user", methods=['POST'])
def update_user():
    if request.method == 'POST' and 'update_type' in request.form and 'username' in request.form:
        action = request.form['update_type']
        uname = request.form['username']

        if action == 'activate' and 'password' in request.form:
            pword = request.form['password']
            cur.execute("SELECT COUNT(*) FROM users WHERE username = (%s);", (uname,))
            exists = cur.fetchone()[0]

            if exists:
                cur.execute("UPDATE users SET password = (%s), active = TRUE WHERE username = (%s);", (pword, uname))
            else:
                role = request.form['role']
                cur.execute("INSERT INTO users (username, password, role_fk) VALUES ((%s), (%s), (SELECT role_pk FROM roles WHERE title = (%s)));", (uname, pword, role))
            conn.commit()
            return jsonify(response="user activated")

        elif action == 'revoke':
            cur.execute("SELECT COUNT(*) FROM users WHERE username = (%s);", (uname,))
            exists = cur.fetchone()[0]

            if exists:
                cur.execute("UPDATE users SET active = FALSE WHERE username = (%s);", (uname,))
                conn.commit()
                return jsonify(response="user access revoked")

            else:
                return jsonify(response ="Revoke Failed: user doesn't exist")
        else:
            return jsonify(response= 'Activate Failed: missing password')
    else:
        return jsonify(response= 'Action Failed: missing information')

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
	#session['name'] is only set if user is active
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
    return redirect("/login")

@app.route("/add_facility", methods=['GET', 'POST'])
def add_facility():
    fac_list=getFacList()
    if request.method == 'GET' and 'name' in session:
        return render_template('add_facility.html', faclist = fac_list)
    if request.method == 'POST' and 'name' in session:
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
    else:
        return redirect('/login')

@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    if request.method == 'GET' and 'name' in session:
        cur.execute("SELECT asset_tag, description FROM assets;")
        asset_list = cur.fetchall() #is a list of lists: each item[0] is a tag, each item[1] is a descripiton
        fac_list = getFacList() 
        return render_template('add_asset.html', assets = asset_list, faclist = fac_list)
    if request.method == 'POST' and 'name' in session:
        a_tag = request.form['tag']
        desc = request.form['desc']
        fcode = request.form['fac_code']
        a_date = request.form['intake']
        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = (%s);", (a_tag,))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO assets (asset_tag, description, acq_date) VALUES ((%s), (%s), (%s));", (a_tag, desc, a_date))
            cur.execute('''INSERT INTO asset_history (asset_fk, 
facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE 
asset_tag = (%s)), (SELECT facility_pk FROM facilities WHERE fac_code 
= (%s)), (%s));''', (a_tag, fcode, a_date))
            conn.commit()
            return redirect('/add_asset')
        else:
            return render_template("add_ast_fail.html", asset=a_tag)
    else:
        return redirect('/login')

@app.route("/dispose_asset", methods=['GET', 'POST'])
def dispose_asset():
    if 'name' in session and session['role'] == 'Logistics Officer':
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
    #if current user is not a logistics officer and not logged in:
    elif 'name' not in session:
        return redirect('/login')
    #if current user is logged in as facilities officer
    else:
        return render_template("LO_only.html", page="Asset Disposal")    

@app.route("/asset_report", methods=['GET', 'POST'])
def asset_report():
    fac_list = getFacList()
    if request.method == 'GET' and 'name' in session:
        return render_template('g_report_request.html', faclist = fac_list)
    if request.method == 'POST' and 'name' in session:
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
    else:
        return redirect('/login')

@app.route("/transfer_req", methods=['GET', 'POST'])
def transfer_req():
    if 'name' in session and session['role'] != 'Logistics Officer':
        return render_template('LO_only.html', page = 'Transfer Requests')
    elif 'name' not in session:
        return redirect('/login')
    if request.method == 'GET':
        cur.execute('''SELECT asset_tag, common_name FROM assets JOIN 
asset_history ON asset_pk = asset_fk JOIN facilities ON facility_fk = facility_pk
WHERE facility_fk IS NOT NULL and depart_dt IS NULL AND common_name != 'in 
transit';''')
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
        if src_code == dest:
            return render_template("invalid_request.html")
        cur.execute('''INSERT INTO transfer_requests (asset_fk, source, 
destination, requester, req_time) VALUES ((SELECT asset_pk FROM assets WHERE 
asset_tag=(%s)), (SELECT facility_pk FROM facilities WHERE fac_code=(%s)), (SELECT 
facility_pk FROM facilities WHERE fac_code=(%s)), (SELECT user_pk FROM users WHERE 
username=(%s)), (%s));''', (a_tag, src_code, dest, session['name'], today))
        conn.commit()
        return render_template("request_made.html", a_tag=a_tag, fac_src=src_code, fac_dest = dest)

@app.route("/approve_req", methods = ['GET', 'POST'])
def approve_req():
    if 'name' in session and session['role'] != 'Facilities Officer':
        return render_template("FO_only.html", page='Request Approval')
    elif 'name' not in session:
        return redirect('/login')

    if request.method == 'GET' and 'req_num' in request.args:
        req_num = request.args.get('req_num')
        cur.execute("SELECT app_time FROM transfer_requests WHERE request_pk = (%s);", (req_num,))
        approved = cur.fetchone()
    #If request exists but has no app_time, this will return [None]. 
    #If request doesn't exist, this will return None.
        if approved != None and approved == [None]:
            cur.execute('''SELECT a.asset_tag, a.description, src.common_name, 
dest.common_name, tr.request_pk FROM assets a JOIN transfer_requests tr ON 
tr.asset_fk=a.asset_pk JOIN facilities src ON tr.source = src.facility_pk JOIN facilities dest ON 
tr.destination = dest.facility_pk WHERE tr.request_pk = (%s);''', (req_num,))
            results = cur.fetchone()
    #results[0]: asset tag, results[1]: asset description, results[2]: source name, 
    #results[3]: destination name, results[4]: request number
            return render_template("approve_request.html", result = results)

        else:
            return render_template("invalid_request.html") 

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

@app.route("/update_transit", methods=['GET', 'POST'])
def update_transit():
    if 'name' in session and session['role'] != 'Logistics Officer':
        return render_template('LO_only.html', page = 'Transit Updates')
    elif 'name' not in session:
        return redirect('/login')

    if request.method == 'GET' and 'req_num' in request.args:
        req_num = request.args.get('req_num')
        cur.execute("SELECT unload_dt, load_dt FROM transfer_requests WHERE request_pk=(%s);", (req_num,))
        needs_dates = cur.fetchone()

    #if unload_dt(needs_dates[0]) is None, then it still needs to be set
    #if needs_dates == None, then there was no request with that number
        if needs_dates != None and needs_dates[0] == None:
            type = 'Unload'

            if needs_dates[1] == None:
                type = 'Load' 

            return render_template("update_request.html", type=type, req_num=req_num)

        else:
            return render_template("invalid_request.html")

    if request.method == 'POST' and 'update_type' in request.form and 'u_time' in request.form:
        u_type = request.form['update_type']
        u_time = request.form['u_time']
        req_num = request.form['request_num']
        cur.execute("SELECT asset_fk FROM transfer_requests WHERE request_pk=(%s);", (req_num,))
        asset = cur.fetchone()[0]

        if u_type == 'Load':
            cur.execute('''SELECT request_pk FROM transfer_requests WHERE 
app_time<=(%s) AND request_pk = (%s);''', (u_time, req_num))
            request_good = cur.fetchone()

            if request_good != None: 
    #Update request information
                cur.execute('''UPDATE transfer_requests SET load_dt=(%s), 
sets_load=(SELECT user_pk FROM users WHERE username=(%s)) WHERE 
request_pk=(%s);''', (u_time, session['name'], req_num))
    #update asset location(remove from current facility)
                cur.execute('''UPDATE asset_history SET depart_dt=(%s) WHERE 
asset_fk=(%s) AND facility_fk=(SELECT source FROM transfer_requests WHERE 
request_pk=(%s)) AND depart_dt IS NULL;''', (u_time, asset, req_num))
    #update asset location(set 'in transit')
                cur.execute('''INSERT INTO asset_history (asset_fk, 
facility_fk, arrive_dt) VALUES ((%s), (SELECT facility_pk FROM facilities WHERE 
common_name='in transit'), (%s));''', (asset, u_time))
                conn.commit()

        else:
            cur.execute('''SELECT load_dt FROM transfer_requests WHERE 
request_pk=(%s) AND load_dt <= (%s);''', (req_num, u_time))
            load_time = cur.fetchone()
            if load_time != None:
    #Update transfer information
                cur.execute('''UPDATE transfer_requests SET unload_dt=(%s), sets_unload=(SELECT 
user_pk FROM users WHERE username=(%s)) WHERE request_pk=(%s);''', (u_time, session['name'], req_num))
    #Update asset location(remove from 'in transit')
                cur.execute('''UPDATE asset_history SET depart_dt=(%s) WHERE 
asset_fk=(%s) AND facility_fk=(SELECT facility_pk FROM facilities WHERE 
common_name='in transit') AND depart_dt IS NULL;''', (u_time, asset))
    #Update asset location(set at destination)
                cur.execute('''INSERT INTO asset_history (asset_fk, 
facility_fk, arrive_dt) VALUES ((%s), (SELECT destination FROM 
transfer_requests WHERE request_pk=(%s)), (%s));''', (asset, req_num, u_time))
                conn.commit()

    return redirect("/dashboard")

@app.route("/transfer_report", methods=['GET', 'POST'])
def transfer_report():
    if request.method == 'GET' and 'name' in session:
        return render_template("g_trans_rep.html")

    if request.method == 'POST' and 'req_date' in request.form and 'name' in session:
        req_date = request.form['req_date']
        cur.execute('''SELECT tr.request_pk, a.asset_tag, src.common_name, 
dest.common_name, tr.load_dt, tr.unload_dt, sl.username, su.username FROM 
transfer_requests tr JOIN assets a ON tr.asset_fk=a.asset_pk JOIN facilities src 
ON src.facility_pk=tr.source JOIN facilities dest ON dest.facility_pk = 
tr.destination LEFT OUTER JOIN users sl ON tr.sets_load=sl.user_pk LEFT OUTER JOIN
users su ON 
tr.sets_unload=su.user_pk WHERE ((%s) BETWEEN tr.load_dt AND tr.unload_dt) OR 
(((%s)>tr.load_dt) AND tr.unload_dt IS NULL);''', (req_date, req_date))  
        results = cur.fetchall()
    #for item in results: item[0]: request number, item[1]: asset tag, 
    #item[2]: departed from, item[3]: will arrive at, item[4]: loaded on, 
    #item[5]: unloaded on, item[6]: load date set by, item[7]: unload date set by
        return render_template("p_trans_rep.html", rep_date=req_date, info=results)
    else:
        return redirect('/login')

@app.route("/logout", methods=['GET'])
def logout():
    if request.method == 'GET' and 'name' in session:
        uname = session['name']
        session.clear() #ends session
        return render_template("logout.html", username=uname)
    return redirect("/login")
