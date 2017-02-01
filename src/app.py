from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reportmain', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        result = request.form
        return render_template('report_main.html', result = result)

@app.route('/facility_report')
def facility():
    return render_template('facility_report.html')

@app.route('/transit_report')
def transit():
    return render_template('transit_report.html')

@app.route('/logout')
def goodbye():
    return render_template('logout.html')



