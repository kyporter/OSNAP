from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
#Because this is what the websites told me to do(almost):
app.secret_key = 'wecanpretendthisisarandomkeyright?'


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

@app.route('/facility_report')
def facility():
    return render_template('facility_report.html')

@app.route('/transit_report')
def transit():
    return render_template('transit_report.html')

@app.route('/logout')
def goodbye():
    byeuser = session['name']
    session.clear()
    return render_template('logout.html', username = byeuser)



