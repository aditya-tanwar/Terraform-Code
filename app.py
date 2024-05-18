from flask import Flask, redirect, render_template, request, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@app.route('/')
def index():
    message = request.args.get('message')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the submitted credentials match the admin credentials
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Store login status in session
        session['logged_in'] = True
        return redirect(url_for('api_call'))
    else:
        # Redirect to login page with error message
        return redirect(url_for('index', message='Incorrect Credentials. Please try again.'))


@app.route('/api_call', methods=['GET', 'POST'])
def api_call():
    # Check if user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        token = request.form['token']
        
        if endpoint == 'account_details':
            url = "https://app.terraform.io/api/v2/account/details"
        elif endpoint == 'list_workspaces':
            organization = request.form['organization']
            url = f"https://app.terraform.io/api/v2/organizations/{organization}/workspaces"
        elif endpoint == 'workspace_runs':
            organization = request.form['organization']
            workspace_id = request.form['workspace_id']
            url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/runs"
        # Add more elif conditions for other API calls
        
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

if __name__ == '__main__':
    app.run(debug=True)
