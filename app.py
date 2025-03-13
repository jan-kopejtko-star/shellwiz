# app.py
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Home page route (Quiz Game)"""
    return render_template('index.html')

@app.route('/premium')
def premium():
    """Premium page route"""
    return render_template('premium.html')

@app.route('/tutorial')
def tutorial():
    """Tutorial page route"""
    return render_template('tutorial.html')

@app.route('/quiz')
def quiz():
    """Quiz page route - currently same as index"""
    return render_template('index.html')

@app.route('/challenges')
def challenges():
    """Challenges page route"""
    return render_template('challenges.html')

@app.route('/leaderboard')
def leaderboard():
    """Leaderboard page route"""
    return render_template('leaderboard.html')

@app.route('/commands')
def commands():
    """Commands reference page route"""
    return render_template('commands.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/static/<path:path>')
def send_static(path):
    """Route for serving static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)