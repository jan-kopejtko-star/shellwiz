# app.py
from flask import Flask, render_template, send_from_directory, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
import os
from datetime import datetime

app = Flask(__name__)

# Initialize CSRF protection
csrf = CSRFProtect(app)

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

# Add these route handlers to your app.py file

@app.route('/tutorial')
def tutorial_index():
    """Tutorial landing page showing all available tutorials"""
    # In a real implementation, you would fetch the tutorial sections from the database
    # For now, we'll use dummy data
    
    # Mock data for tutorial categories
    categories = [
        {
            'slug': 'basics',
            'title': 'Command Line Basics',
            'description': 'Start your journey with these fundamental tutorials.',
            'icon': 'fas fa-graduation-cap',
            'tutorials': [
                {
                    'slug': 'intro-to-shell',
                    'title': 'Introduction to the Shell',
                    'description': 'Understand what the command line is and why it\'s useful for developers.',
                    'difficulty': 'beginner',
                    'duration': 20
                },
                {
                    'slug': 'navigation',
                    'title': 'Navigation & File System',
                    'description': 'Learn to navigate directories and understand file system structure.',
                    'difficulty': 'beginner',
                    'duration': 30
                },
                {
                    'slug': 'file-operations',
                    'title': 'File Operations',
                    'description': 'Create, copy, move, and delete files and directories efficiently.',
                    'difficulty': 'beginner',
                    'duration': 25
                }
            ]
        },
        {
            'slug': 'text-processing',
            'title': 'Text Processing',
            'description': 'Master tools for manipulating and analyzing text files.',
            'icon': 'fas fa-file-alt',
            'tutorials': [
                {
                    'slug': 'viewing-files',
                    'title': 'Viewing File Content',
                    'description': 'Learn various ways to view and inspect file contents from the command line.',
                    'difficulty': 'beginner',
                    'duration': 20
                },
                {
                    'slug': 'text-editors',
                    'title': 'Text Editors: Vim & Nano',
                    'description': 'Edit files directly from the terminal using popular text editors.',
                    'difficulty': 'intermediate',
                    'duration': 45
                },
                {
                    'slug': 'grep-sed',
                    'title': 'Search & Replace with Grep & Sed',
                    'description': 'Find patterns in text and perform complex search and replace operations.',
                    'difficulty': 'intermediate',
                    'duration': 40
                }
            ]
        },
        {
            'slug': 'scripting',
            'title': 'Shell Scripting',
            'description': 'Automate tasks and build powerful shell scripts.',
            'icon': 'fas fa-code',
            'is_premium': True,
            'tutorials': [
                {
                    'slug': 'scripting-fundamentals',
                    'title': 'Scripting Fundamentals',
                    'description': 'Learn the basics of shell scripting, variables, and simple commands.',
                    'difficulty': 'intermediate',
                    'duration': 35,
                    'is_premium': True
                },
                {
                    'slug': 'control-flow',
                    'title': 'Control Flow & Logic',
                    'description': 'Master conditionals, loops, and logical operations in shell scripts.',
                    'difficulty': 'advanced',
                    'duration': 50,
                    'is_premium': True
                },
                {
                    'slug': 'advanced-scripting',
                    'title': 'Advanced Scripting Techniques',
                    'description': 'Learn functions, error handling, and best practices for shell scripts.',
                    'difficulty': 'advanced',
                    'duration': 60,
                    'is_premium': True
                }
            ]
        },
        {
            'slug': 'system-administration',
            'title': 'System Administration',
            'description': 'Manage systems and servers using command line tools.',
            'icon': 'fas fa-server',
            'tutorials': [
                {
                    'slug': 'process-management',
                    'title': 'Process Management',
                    'description': 'Learn to monitor, control, and manage running processes.',
                    'difficulty': 'intermediate',
                    'duration': 30
                },
                {
                    'slug': 'user-management',
                    'title': 'User Management',
                    'description': 'Create and manage users, groups, and permissions.',
                    'difficulty': 'intermediate',
                    'duration': 35
                },
                {
                    'slug': 'network-admin',
                    'title': 'Network Administration',
                    'description': 'Master network tools, diagnostics, and configuration via command line.',
                    'difficulty': 'advanced',
                    'duration': 55,
                    'is_premium': True
                }
            ]
        }
    ]
    
    # Featured tutorials
    featured_tutorials = [
        {
            'slug': 'beginners-guide',
            'title': 'Beginner\'s Guide to the Shell',
            'description': 'Start your command line journey with the basics. Learn navigation, file operations, and essential commands.',
            'difficulty': 'beginner',
            'duration': 45,
            'icon': 'fas fa-terminal'
        },
        {
            'slug': 'text-processing',
            'title': 'Text Processing with Grep & Sed',
            'description': 'Master powerful text processing commands to filter, search, and transform text files efficiently.',
            'difficulty': 'intermediate',
            'duration': 60,
            'icon': 'fas fa-file-alt'
        },
        {
            'slug': 'shell-scripting',
            'title': 'Shell Scripting Mastery',
            'description': 'Automate complex tasks with shell scripts. Learn variables, conditions, loops, and best practices.',
            'difficulty': 'advanced',
            'duration': 120,
            'icon': 'fas fa-code',
            'is_premium': True
        }
    ]
    
    # In a real implementation, this would be actual user progress data from the database
    user_progress = {}
    if current_user.is_authenticated:
        # Just mocking some progress for demo purposes
        user_progress = {
            'basics': {
                'section': {'slug': 'basics', 'title': 'Command Line Basics'},
                'last_page': {'slug': 'navigation', 'title': 'Navigation & File System'},
                'percentage': 65
            }
        }
    
    return render_template(
        'tutorial_index.html',
        categories=categories,
        featured_tutorials=featured_tutorials,
        user_progress=user_progress
    )

@app.route('/tutorial/<section_slug>')
def tutorial_section(section_slug):
    """Display a specific tutorial section"""
    # In a real implementation, you would look up the section in the database
    # For now, we'll just redirect to a specific tutorial page
    
    # Mock handling for different sections
    if section_slug == 'intro-to-shell':
        return render_template('tutorial_content.html', content_id='intro-to-shell')
    elif section_slug == 'beginners-guide':
        return render_template('tutorial_content.html', content_id='beginners-guide')
    elif section_slug.startswith('script') and not (current_user.is_authenticated and current_user.is_premium):
        flash('This tutorial requires a premium subscription.', 'premium')
        return redirect(url_for('premium'))
    else:
        # Default content page or 404
        flash('This tutorial is coming soon. Check back later!', 'info')
        return redirect(url_for('tutorial_index'))

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

# @app.route('/commands')
# def commands():
#     """Commands reference page route"""
#     return render_template('commands.html')

@app.route('/commands')
def commands():
    """Commands reference page route"""
    # Get all commands grouped by category
    categories = db.session.query(Command.category).distinct().all()
    categories = [category[0] for category in categories]  # Extract category names
    
    commands_by_category = {}
    for category in categories:
        commands_by_category[category] = Command.query.filter_by(category=category).all()
    
    return render_template('commands.html', 
                          categories=categories, 
                          commands_by_category=commands_by_category)

# @app.route('/commands/<command_name>')
# def command_detail(command_name):
#     """Display detailed information for a specific command"""
#     # For now, we'll handle 'ls' as a special case with hardcoded data
#     # Later this would be replaced with database queries
    
#     if command_name == 'ls':
#         command = {
#             'name': 'ls',
#             'syntax': 'ls [OPTION]... [FILE]...',
#             'description': 'List information about the FILEs (the current directory by default). Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.',
#             'category': 'File Operations',
#             'shell_type': 'bash',
#             'options': [
#                 {
#                     'flag': '-a, --all',
#                     'description': 'do not ignore entries starting with .'
#                 },
#                 {
#                     'flag': '-l',
#                     'description': 'use a long listing format'
#                 },
#                 {
#                     'flag': '-h, --human-readable',
#                     'description': 'with -l, print sizes in human readable format (e.g., 1K 234M 2G)'
#                 },
#                 {
#                     'flag': '-r, --reverse',
#                     'description': 'reverse order while sorting'
#                 },
#                 {
#                     'flag': '-t',
#                     'description': 'sort by modification time, newest first'
#                 }
#             ],
#             'examples': [
#                 {
#                     'title': 'List all files including hidden ones',
#                     'command': 'ls -a',
#                     'explanation': 'Shows all files, including those that start with a dot (.) which are normally hidden.'
#                 },
#                 {
#                     'title': 'List files with detailed information',
#                     'setup_command': 'touch example.txt',
#                     'command': 'ls -l example.txt',
#                     'explanation': 'Shows detailed information about example.txt including permissions, owner, size, and modification date.'
#                 },
#                 {
#                     'title': 'List files sorted by modification time',
#                     'command': 'ls -lt',
#                     'explanation': 'Lists all files in long format, sorted by modification time with newest first.'
#                 }
#             ]
#         }
#         return render_template('command_detail.html', command=command)
#     else:
#         # For any other command, redirect to commands page for now
#         flash(f'Details for "{command_name}" coming soon!', 'info')
#         return redirect(url_for('commands'))

@app.route('/commands/<command_name>')
def command_detail(command_name):
    """Display detailed information for a specific command"""
    # Query the database for the command
    command = Command.query.filter_by(name=command_name).first_or_404()
    
    # Get related commands (similar category)
    related_commands = Command.query.filter(
        Command.category == command.category,
        Command.name != command.name
    ).limit(4).all()
    
    return render_template('command_detail.html', 
                          command=command,
                          related_commands=related_commands)
    
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

# Add or modify this route in your app.py file

@app.route('/tutorial/basics/intro-to-shell')
def tutorial_intro_to_shell():
    """Specific route for the Introduction to Shell tutorial"""
    # Check if user is logged in to track progress
    if current_user.is_authenticated:
        # In a real implementation, you would update the user's progress
        # For example:
        # progress = TutorialProgress.query.filter_by(
        #     user_id=current_user.user_id,
        #     page_id=1  # Assuming this is the ID for the intro tutorial
        # ).first()
        # 
        # if not progress:
        #     progress = TutorialProgress(
        #         user_id=current_user.user_id,
        #         page_id=1,
        #         completed_at=datetime.utcnow()
        #     )
        #     db.session.add(progress)
        #     db.session.commit()
        pass
    
    # Render the tutorial template
    return render_template('tutorial_content.html', 
                          section_slug='basics',
                          page_slug='intro-to-shell',
                          title='Introduction to the Shell',
                          difficulty='beginner',
                          duration=20,
                          category='Command Line Basics')

# Alternative approach using the generic handler
@app.route('/tutorial/<section_slug>/<page_slug>')
def tutorial_page(section_slug, page_slug):
    """Generic handler for tutorial pages"""
    # Default values
    title = 'Tutorial'
    difficulty = 'beginner'
    duration = 20
    category = 'Command Line Basics'
    
    # Determine which tutorial to show based on the slugs
    if section_slug == 'basics' and page_slug == 'intro-to-shell':
        title = 'Introduction to the Shell'
        template_file = 'intro_to_shell.html'
    elif section_slug == 'basics' and page_slug == 'navigation':
        title = 'Navigation & File System'
        difficulty = 'beginner'
        duration = 30
        template_file = 'navigation.html'
    elif section_slug == 'text-processing' and page_slug == 'grep-sed':
        title = 'Search & Replace with Grep & Sed'
        difficulty = 'intermediate'
        duration = 40
        category = 'Text Processing'
        template_file = 'grep_sed.html'
    # Add other tutorials here
    else:
        # For tutorials that don't have dedicated templates yet
        flash('This tutorial is coming soon. Check back later!', 'info')
        return redirect(url_for('tutorial_index'))
    
    # Mock check for premium content
    if section_slug in ['scripting'] and not (current_user.is_authenticated and current_user.is_premium):
        flash('This tutorial requires a premium subscription.', 'premium')
        return redirect(url_for('premium'))
    
    # Track progress for logged-in users
    if current_user.is_authenticated:
        # In a real implementation, you would update the user's progress
        pass
    
    # For the proof of concept, always return the intro tutorial template
    # In a real implementation, you would use different templates or dynamic content
    return render_template('tutorial_content.html',
                          section_slug=section_slug,
                          page_slug=page_slug,
                          title=title,
                          difficulty=difficulty,
                          duration=duration,
                          category=category)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)