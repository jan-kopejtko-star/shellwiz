# models.py
from app import db
from datetime import datetime

# User Management Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_premium = db.Column(db.Boolean, default=False)
    premium_expiry = db.Column(db.DateTime)
    profile_image_url = db.Column(db.String(255))

    # Relationships
    preferences = db.relationship('UserPreference', backref='user', uselist=False)
    quiz_attempts = db.relationship('QuizAttempt', backref='user')
    tutorial_progress = db.relationship('TutorialProgress', backref='user')
    challenge_completions = db.relationship('ChallengeCompletion', backref='user')
    command_masteries = db.relationship('CommandMastery', backref='user')
    achievements = db.relationship('UserAchievement', backref='user')

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    preferred_shell = db.Column(db.String(20))
    dark_mode = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    show_hints = db.Column(db.Boolean, default=True)

# Content Management Models
class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    terminal_context = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    options = db.relationship('QuizOption', backref='question', cascade='all, delete-orphan')

class QuizOption(db.Model):
    __tablename__ = 'quiz_options'
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.question_id', ondelete='CASCADE'))
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.Text)

class TutorialSection(db.Model):
    __tablename__ = 'tutorial_sections'
    section_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Relationships
    pages = db.relationship('TutorialPage', backref='section', cascade='all, delete-orphan')

class TutorialPage(db.Model):
    __tablename__ = 'tutorial_pages'
    page_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('tutorial_sections.section_id', ondelete='CASCADE'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    estimated_minutes = db.Column(db.Integer)

class Command(db.Model):
    __tablename__ = 'commands'
    command_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    syntax = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    shell_type = db.Column(db.String(20), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Relationships
    examples = db.relationship('CommandExample', backref='command', cascade='all, delete-orphan')
    masteries = db.relationship('CommandMastery', backref='command')

class CommandExample(db.Model):
    __tablename__ = 'command_examples'
    example_id = db.Column(db.Integer, primary_key=True)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.command_id', ondelete='CASCADE'))
    example = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    challenge_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    success_criteria = db.Column(db.Text, nullable=False)
    estimated_minutes = db.Column(db.Integer)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Relationships
    completions = db.relationship('ChallengeCompletion', backref='challenge')

# Progress Tracking Models
class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    time_spent_seconds = db.Column(db.Integer)
    
    # Relationships
    answers = db.relationship('QuizAnswer', backref='attempt', cascade='all, delete-orphan')

class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.attempt_id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.question_id'))
    selected_option_id = db.Column(db.Integer, db.ForeignKey('quiz_options.option_id'))
    is_correct = db.Column(db.Boolean)
    time_spent_seconds = db.Column(db.Integer)

class TutorialProgress(db.Model):
    __tablename__ = 'tutorial_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('tutorial_pages.page_id', ondelete='CASCADE'), primary_key=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChallengeCompletion(db.Model):
    __tablename__ = 'challenge_completions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.challenge_id', ondelete='CASCADE'), primary_key=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.Column(db.Integer, default=1)
    time_spent_seconds = db.Column(db.Integer)

class CommandMastery(db.Model):
    __tablename__ = 'command_mastery'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.command_id', ondelete='CASCADE'), primary_key=True)
    mastery_level = db.Column(db.Integer)
    last_practiced = db.Column(db.DateTime)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    achievement_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge_image_url = db.Column(db.String(255))
    achievement_type = db.Column(db.String(50), nullable=False)
    
    # Relationships
    earned_by = db.relationship('UserAchievement', backref='achievement')

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.achievement_id', ondelete='CASCADE'), primary_key=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)