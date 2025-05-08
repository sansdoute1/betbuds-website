from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

import os

@app.route('/place-bet', methods=['GET', 'POST'])
def place_bet():
    if request.method == 'POST':
        challenge = request.form.get('challenge')
        goal = request.form.get('goal')
        timeline = request.form.get('timeline')
        friends = request.form.get('friends')
        amount = request.form.get('amount')
        return render_template('place_bet.html', success=True, challenge=challenge)
    return render_template('place_bet.html', success=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
