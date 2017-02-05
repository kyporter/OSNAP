from flask import Flask, render_template, request, session, redirect, url_for 
import psycopg2 
import psycopg2.extras

app = Flask(__name__)
#Because this is what the websites told me to do(almost):
app.secret_key = 'wecanpretendthisisarandomkeyright?'

conn = psycopg2.connect(database="LOST", host="127.0.0.1", port="5432")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  ##Should create a cursor that produces a 	
								##dictionary of results

@app.route('/')
def index(): 
    return render_template('index.html') #FIXME: add link to login page to index.html?

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reportmain', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        username = request.form["uname"]
        session['name'] = username
        return render_template('report_main.html')

@app.route('/facility_report', methods=['POST', 'GET'])
def facility():
    if request.method == 'POST':
        datecheck = request.form["date"]
        facname = request.form["facility_name"]
        cur.execute('''SELECT a.asset_tag, a.description, aa.arrive_dt, aa.depart_dt 
FROM asset_at aa JOIN facilities f ON aa.facility_fk = f.facility_pk JOIN assets a ON 
a.asset_pk = aa.asset_fk WHERE f.common_name = (%s) AND (((%s) BETWEEN aa.arrive_dt AND aa.depart_dt) 
OR (((%s) >= aa.arrive_dt) AND (aa.depart_dt IS NULL)));''', (facname, datecheck, datecheck))
        return render_template('facility_report.html')
    else:
        return render_template('report_main.html')

@app.route('/transit_report', methods=['POST', 'GET'])
def transit():
    if request.method == 'POST':
        datecheck = request.form["date"]
        cur.execute('''SELECT a.asset_tag, a.description, f1.common_name, t.load_dt, f2.common_name, 
t.unload_dt FROM facilities f1 JOIN convoys c ON f1.facility_pk = c.source_fk JOIN facilities f2 ON 
f2.facility_pk = c.dest_fk JOIN asset_on t ON t.convoy_fk = c.convoy_pk JOIN assets a ON a.asset_pk 
= t.asset_fk WHERE (%s) BETWEEN t.load_dt AND t.unload_dt;''', (datecheck,))
        infos = cur.fetchall()
        facsleaving = [i[2] for i in infos]
        return render_template('transit_report.html', datecheck=datecheck, leftfac = facsleaving)
    else:
        return render_template('report_main.html')


@app.route('/logout', methods=['POST', 'GET'])
def goodbye():
    byeuser = session['name']
    session.clear()
    return render_template('logout.html', username = byeuser)



