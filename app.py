import os
from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set secret key after creating the app instance

users = {}
users['alice'] = generate_password_hash('pass123')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return "Missing username or password", 400

    if username in users:
        return "User already exists", 409

    users[username] = generate_password_hash(password)
    return "User registered successfully", 201

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return "Missing username or password", 400

    if username in users and check_password_hash(users[username], password):
        session['user_id'] = username
        return "Login successful"
    else:
        return "Invalid username or password", 401
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return "Logged out"

@app.route('/')
def home():
    return 'Hello'

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Welcome back, {session['user_id']}!"
    else:
        return redirect('/login')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html', username=session['user_id'])
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

