# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # required for session handling

# Simulated user store (for demo purposes only)
users = {'test@example.com': 'password123'}

# Simulated challenge store (in-memory)
challenges = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('place_bet'))
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users:
            error = 'Account already exists.'
        else:
            users[email] = password
            session['user'] = email
            return redirect(url_for('place_bet'))
    return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/place-bet', methods=['GET', 'POST'])
def place_bet():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        challenge = request.form.get('challenge')
        goal = request.form.get('goal')
        timeline = request.form.get('timeline')
        friends = request.form.get('friends')
        amount = request.form.get('amount')

        challenge_data = {
            'creator': session['user'],
            'challenge': challenge,
            'goal': goal,
            'timeline': timeline,
            'friends': friends.split(','),
            'amount': amount
        }
        challenges.append(challenge_data)
        return render_template('place_bet.html', success=True, challenge=challenge, created=True)

    return render_template('place_bet.html', success=False, created=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
