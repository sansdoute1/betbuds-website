from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/place-bet', methods=['GET', 'POST'])
def place_bet():
    if request.method == 'POST':
        # Get form inputs
        challenge = request.form.get('challenge')
        goal = request.form.get('goal')
        timeline = request.form.get('timeline')
        friends = request.form.get('friends')
        amount = request.form.get('amount')

        # For now, just show a success message
        return render_template('place_bet.html', success=True, challenge=challenge)

    return render_template('place_bet.html', success=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
