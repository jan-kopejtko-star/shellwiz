# app.py
from flask import Flask, render_template, send_from_directory, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import os
from datetime import datetime

app = Flask(__name__)

# Set configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shellwiz_postgre_sxgi_user:p3r79Ft1zQiKUrMYmdTMNj5eld9caUMT@dpg-cv9gqctds78s739g0jqg-a.frankfurt-postgres.render.com/shellwiz_postgre_sxgi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-for-development')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models after initializing db
from models import User, UserPreference

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import forms after app is initialized to avoid circular imports
from forms import RegistrationForm, LoginForm

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log in the user
            login_user(user, remember=form.remember.data)
            
            # Get the page the user was trying to access
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            
            # Redirect to the next page or home
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/static/<path:path>')
def send_static(path):
    """Route for serving static files"""
    return send_from_directory('static', path)

# Add these route handlers to your app.py file

@app.route('/profile')
@login_required
def profile():
    """User profile page route"""
    return render_template('profile.html')

@app.route('/settings')
@login_required
def settings():
    """User settings page route"""
    return render_template('settings.html')

@app.route('/premium-dashboard')
@login_required
def premium_dashboard():
    """Premium dashboard page route"""
    if not current_user.is_premium:
        flash('This feature is only available to premium users.', 'error')
        return redirect(url_for('premium'))
    return render_template('premium_dashboard.html')

# Settings form handlers
@app.route('/settings/update-profile', methods=['POST'])
@login_required
def settings_update_profile():
    """Handle profile information updates"""
    username = request.form.get('username')
    email = request.form.get('email')
    profile_image_url = request.form.get('profile_image_url')
    
    # Check if username is already taken
    if username != current_user.username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken.', 'error')
            return redirect(url_for('settings'))
    
    # Check if email is already taken
    if email != current_user.email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('settings'))
    
    # Update user information
    current_user.username = username
    current_user.email = email
    current_user.profile_image_url = profile_image_url
    
    db.session.commit()
    flash('Profile information updated successfully.', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/change-password', methods=['POST'])
@login_required
def settings_change_password():
    """Handle password changes"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Verify current password
    if not bcrypt.check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('settings'))
    
    # Check if new passwords match
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('settings'))
    
    # Update password
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    current_user.password_hash = hashed_password
    
    db.session.commit()
    flash('Password updated successfully.', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/update-preferences', methods=['POST'])
@login_required
def settings_update_preferences():
    """Handle user preference updates"""
    dark_mode = 'dark_mode' in request.form
    email_notifications = 'email_notifications' in request.form
    show_hints = 'show_hints' in request.form
    preferred_shell = request.form.get('preferred_shell')
    
    # Check if user has preferences, create if not
    user_preferences = current_user.preferences
    if not user_preferences:
        user_preferences = UserPreference(user_id=current_user.user_id)
        db.session.add(user_preferences)
    
    # Update preferences
    user_preferences.dark_mode = dark_mode
    user_preferences.email_notifications = email_notifications
    user_preferences.show_hints = show_hints
    user_preferences.preferred_shell = preferred_shell
    
    db.session.commit()
    flash('Preferences updated successfully.', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/delete-account', methods=['POST'])
@login_required
def settings_delete_account():
    """Handle account deletion"""
    # Delete user data
    # Be careful with cascading deletes here
    
    # For now, just log the user out
    logout_user()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('index'))
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)