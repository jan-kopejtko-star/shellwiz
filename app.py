# app.py
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models (after db is defined)
from models import *

@app.route('/')
def index():
    """Home/landing page route"""
    return render_template('home.html')

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
    """Quiz page route"""
    return render_template('quiz.html')

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