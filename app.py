from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('login.html', message=message)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('api_call'))
    else:
        return redirect(url_for('index', message='Incorrect Credentials. Please try again.'))

@app.route('/api_call', methods=['GET', 'POST'])
def api_call():
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        api_type = request.form['api_type']
        endpoint = request.form['endpoint']
        token = request.form['token']

        if endpoint == 'account_details':
            url = f"https://app.terraform.io/api/v2/account/details"
        elif endpoint == 'list_workspaces':
            organization = request.form['organization']
            url = f"https://app.terraform.io/api/v2/organizations/{organization}/workspaces"
        elif endpoint == 'workspace_runs':
            workspace_id = request.form['workspace_id']
            url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/runs"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return render_template('api_response.html', data=data)
        else:
            error_message = f"Failed to fetch data. Status code: {response.status_code}"
            return render_template('error.html', error_message=error_message)
    else:
        return render_template('api_call.html')

@app.route('/get_endpoints/<api_type>')
def get_endpoints(api_type):
    api_endpoints = {
        'account': ['account_details'],
        'workspace': ['list_workspaces', 'workspace_runs']
    }
    return jsonify(api_endpoints.get(api_type, []))

if __name__ == '__main__':
    app.run(debug=True)