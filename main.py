from flask import Flask, render_template, request, redirect, session, url_for
import json  # For handling JSON files

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Load JSON file into a dictionary
def load_user_data():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
        print("User data loaded successfully!")
        return users
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

# Load user data when the app starts
users = load_user_data()

@app.route('/')
def home():
    # Check if the user is already logged in
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')  # Displays the login form

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists and the password matches
    if username in users and users[username]['password'] == password:
        session['username'] = username  # Store username in session
        return redirect(url_for('dashboard'))
    else:
        return "Invalid username or password! Please try again."

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        # Fetch user-specific data
        dashboard_link = users[username]['dashboard_link']
        return render_template('dashboard.html', dashboard_link=dashboard_link)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user from the session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
