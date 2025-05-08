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


# templates/login.html

<!DOCTYPE html>
<html>
<head>
  <title>Login - BetBuds</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center h-screen">
  <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    {% if error %}<p class="text-red-500 mb-4">{{ error }}</p>{% endif %}
    <form method="POST">
      <input type="email" name="email" placeholder="Email" class="w-full mb-3 px-4 py-2 border rounded" required>
      <input type="password" name="password" placeholder="Password" class="w-full mb-4 px-4 py-2 border rounded" required>
      <button type="submit" class="bg-primary text-white px-4 py-2 rounded w-full">Log In</button>
    </form>
    <p class="mt-4 text-sm">Don't have an account? <a href="/signup" class="text-blue-500">Sign up</a></p>
  </div>
</body>
</html>


# templates/signup.html

<!DOCTYPE html>
<html>
<head>
  <title>Sign Up - BetBuds</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center h-screen">
  <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
    <h2 class="text-2xl font-bold mb-4">Sign Up</h2>
    {% if error %}<p class="text-red-500 mb-4">{{ error }}</p>{% endif %}
    <form method="POST">
      <input type="email" name="email" placeholder="Email" class="w-full mb-3 px-4 py-2 border rounded" required>
      <input type="password" name="password" placeholder="Password" class="w-full mb-4 px-4 py-2 border rounded" required>
      <button type="submit" class="bg-primary text-white px-4 py-2 rounded w-full">Sign Up</button>
    </form>
    <p class="mt-4 text-sm">Already have an account? <a href="/login" class="text-blue-500">Log in</a></p>
  </div>
</body>
</html>


# Add to bottom of templates/place_bet.html before </body>

{% if created %}
<div class="mt-6 bg-blue-100 text-blue-700 p-4 rounded">
  🎉 Challenge created and shared with: {{ challenge_data.friends | join(', ') }}
</div>
{% else %}
<div class="mt-6 text-center">
  <button type="submit" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">Create Challenge</button>
</div>
{% endif %}
