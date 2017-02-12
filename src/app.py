from flask import Flask, render_template, request, session, redirect, url_for, jsonify 
import psycopg2 
import psycopg2.extras
from config import dbname, dbhost, dbport, lost_pub  ##FROM dellsword/lost app.py
import json
from time import gmtime, strftime


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
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        req = json.loads(request.form['arguments'])
        cur.execute("SELECT user_pk, active FROM users WHERE username = (%s);", (req['username'],))
        user_id = cur.fetchall()
##runs if username is not already in database
        if user_id == []:  
            cur.execute("INSERT INTO users (username, active) VALUES ((%s), TRUE);", (req['username'],))
            conn.commit()
            return jsonify(timestamp = req['timestamp'], result = "NEW")
##runs if username in database but inactive
        elif user_id[0][1] == False: 
            cur.execute("UPDATE users SET active = TRUE WHERE username = (%s);", (req['username'],))
            conn.commit()
            return jsonify(timestamp = req['timestamp'], result = "OK")
        else:
            return jsonify(timestamp = req['timestamp'], result = "FAIL")
    else:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "FAIL")


@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        req = json.loads(request.form['arguments'])
        cur.execute("UPDATE users SET active = FALSE WHERE username=(%s);", (req['username'],))
        conn.commit()
        return jsonify(timestamp = req['timestamp'], result = "OK")
    else:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "FAIL")

@app.route('/rest/add_asset', methods=['POST'])
def add_asset():
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        req = json.loads(request.form['arguments'])
        vend = req['vendor']
        desc = req['description']
        comps = req['compartments']
        fac = req['facility']
        cur.execute("INSERT INTO assets (description) VALUES (%s);", (desc,))
        conn.commit()
        cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE description = (%s)), (SELECT facility_pk FROM facilities WHERE fcode = (%s)), (%s));", (desc, fac, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        conn.commit()
        if comps != '':
            comp_bits = comps.split(':')
            level = comp_bits[1]
            compartment = comp_bits[0]
            cur.execute('''INSERT INTO security_tags (level_fk, compartment_fk, asset_fk) VALUES ((SELECT level_pk FROM 
levels WHERE abbrv = (%s)), (SELECT compartment_pk FROM compartments WHERE abbrv = (%s)), (SELECT asset_pk FROM assets JOIN 
asset_at ON assets.asset_pk = asset_at.asset_fk JOIN facilities ON asset_at.facility_fk = facilities.facility_pk WHERE 
assets.description = (%s) and facilities.fcode = (%s)));''', (level, compartment, desc, fac))
            conn.commit()
        return jsonify(timestamp = req['timestamp'], result = "OK")
    else:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "FAIL")


@app.route('/rest/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        req = json.loads(request.form['arguments'])
        #because all or none, will need to check if any product already in table before adding any
        prods_list = []
        keep_adding = True
        for arg in req['new_products']:
            if keep_adding:
                vend = arg['vendor']
                desc = arg['description']
                alt = arg['alt_description']
                comps = arg['compartments']
                keep_adding = product_notin(vend, desc, alt)
                if keep_adding:
##if product wasn't already in database, an execute line is added to the commit stack
                    add_sql(prods_list, vend, desc, alt, comps)
##if no products are duplicates, insert statements will be executed
        if keep_adding:
            conn.commit()
            return jsonify(timestamp = req['timestamp'], result = "OK")
##otherwise FAIL is returned without affecting the database
        return jsonify(timestamp = req['timestamp'], result = "FAIL")
    else:            
        return jsonify(timestamp = req['timestamp'], result = "FAIL")

@app.route('/rest/list_products', methods=['POST'])
def list_products():
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        req = json.loads(request.form['arguments'])
        vend = str(req['vendor'])
        vend = '%' + vend + '%'
        desc = str(req['description'])
        desc = '%' + desc + '%'
        comps = req['compartments']
        print(comps)
        if comps != []:
            comp_bits = comps[0].split(':')
            level = comp_bits[1]
            compartment = comp_bits[0]
            cur.execute('''SELECT p.vendor, p.description FROM products p JOIN security_tags 
s ON p.product_pk=s.product_fk WHERE s.compartment_fk=(SELECT compartment_pk FROM compartments 
WHERE abbrv = (%s)) AND s.level_fk = (SELECT level_pk FROM levels WHERE abbrv = (%s)) and 
p.vendor LIKE (%s) and p.description LIKE (%s);''', (compartment, level, vend, desc)) 
            listings = cur.fetchall()
        else:
            cur.execute("SELECT vendor, description FROM products WHERE vendor LIKE (%s) and description LIKE (%s);", (vend, desc))
            listings = cur.fetchall()
        json_listify = []
        for info in listings:
            result = {"vendor" : info[0], "description" : info[1], "compartments" : req['compartments']}
            json_listify.append(result)
        return jsonify(timestamp = req['timestamp'], listing = json.dumps(json_listify))
    else:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "FAIL")

@app.route('/rest/lost_key', methods=['POST'])
def lost_key():
    if request.method == 'POST' and 'arguments' in request.form and 'signature' in request.form:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "OK", key = lost_pub)
    else:
        return jsonify(timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime()), result = "FAIL")

@app.route('/logout', methods=['POST', 'GET'])
def goodbye():
    byeuser = session['name']
    session.clear()  #ends session
    return render_template('logout.html', username = byeuser)



def product_notin(vend, desc, alt):
    cur.execute("SELECT product_pk FROM products WHERE vendor = (%s) AND description = (%s) AND alt_description = (%s);", (vend, desc, alt))
    listing = cur.fetchall()
##If product doesn't already exist, listing will be an empty list and the function will return true
    if listing == []:
        return True
    return False

def add_sql(prods, vend, desc, alt, comps):
    cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES ((%s), (%s), (%s));", 
        (vend, desc, alt))
    if comps != "":
        sec_bits = comps.split(':')
        cur.execute('''INSERT INTO security_tags (level_fk, compartment_fk, product_fk) VALUES ((SELECT level_pk FROM levels 
WHERE abbrv = (%s)), (SELECT compartment_pk FROM compartments WHERE abbrv = (%s)), (SELECT product_pk FROM products WHERE vendor 
= (%s) AND description = (%s) AND alt_description = (%s)));''', (sec_bits[1], sec_bits[0], vend, desc, alt))
#doesn't return, just adds executes to stack, waiting for commit (or not to commit)

def add_sectag_sql(comps, types, items):
    sec_bits = comps.split(':')
    if types == 'product':
        items.append(string.format('''INSERT INTO security_tags (level_fk, compartment_fk, product_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv = {}), (SELECT compartment_pk FROM compartments WHERE abbrv = {}), (SELECT product_pk FROM products WHERE vendor = {} AND description = (%s) AND alt_description = {}));''', (sec_bits[1], sec_bits[0], vend, desc, alt)))
    elif types == 'asset':
        items.append(string.format('''INSERT INTO security_tags (level_fk, compartment_fk, 
asset_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv = {}), (SELECT compartment_pk FROM 
compartments WHERE abbrv = {}), (SELECT asset_pk FROM products WHERE vendor = {} AND 
description = (%s) AND alt_description = {}));''', (sec_bits[1], sec_bits[0], vend, desc, alt)))

