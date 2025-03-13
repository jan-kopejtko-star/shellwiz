# app.py
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import os

app = Flask(__name__)

# Set the database URL directly
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shellwiz_postgre_sxgi_user:p3r79Ft1zQiKUrMYmdTMNj5eld9caUMT@dpg-cv9gqctds78s739g0jqg-a.frankfurt-postgres.render.com/shellwiz_postgre_sxgi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        # Create default user preferences
        user_pref = UserPreference(user_id=new_user.user_id)
        db.session.add(user_pref)
        db.session.commit()
        
        # Flash a success message
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)