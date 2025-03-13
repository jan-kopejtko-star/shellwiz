"""Initial database schema

Revision ID: b7753b5546f4
Revises: 
Create Date: 2025-03-13 17:01:35.311138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7753b5546f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('badge_image_url', sa.String(length=255), nullable=True),
    sa.Column('achievement_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('achievement_id')
    )
    op.create_table('challenges',
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('difficulty', sa.String(length=20), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('success_criteria', sa.Text(), nullable=False),
    sa.Column('estimated_minutes', sa.Integer(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('challenge_id')
    )
    op.create_table('commands',
    sa.Column('command_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('syntax', sa.Text(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('shell_type', sa.String(length=20), nullable=False),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('command_id')
    )
    op.create_table('quiz_questions',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.Text(), nullable=False),
    sa.Column('difficulty', sa.String(length=20), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('terminal_context', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table('tutorial_sections',
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('section_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.Column('premium_expiry', sa.DateTime(), nullable=True),
    sa.Column('profile_image_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('challenge_completions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=True),
    sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenges.challenge_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'challenge_id')
    )
    op.create_table('command_examples',
    sa.Column('example_id', sa.Integer(), nullable=False),
    sa.Column('command_id', sa.Integer(), nullable=True),
    sa.Column('example', sa.Text(), nullable=False),
    sa.Column('explanation', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['command_id'], ['commands.command_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('example_id')
    )
    op.create_table('command_mastery',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('command_id', sa.Integer(), nullable=False),
    sa.Column('mastery_level', sa.Integer(), nullable=True),
    sa.Column('last_practiced', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['command_id'], ['commands.command_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'command_id')
    )
    op.create_table('quiz_attempts',
    sa.Column('attempt_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('total_questions', sa.Integer(), nullable=True),
    sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('attempt_id')
    )
    op.create_table('quiz_options',
    sa.Column('option_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('option_text', sa.Text(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('explanation', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.question_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('option_id')
    )
    op.create_table('tutorial_pages',
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.Column('estimated_minutes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['tutorial_sections.section_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('page_id')
    )
    op.create_table('user_achievements',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.Column('earned_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievements.achievement_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'achievement_id')
    )
    op.create_table('user_preferences',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('preferred_shell', sa.String(length=20), nullable=True),
    sa.Column('dark_mode', sa.Boolean(), nullable=True),
    sa.Column('email_notifications', sa.Boolean(), nullable=True),
    sa.Column('show_hints', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('quiz_answers',
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('attempt_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('selected_option_id', sa.Integer(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attempt_id'], ['quiz_attempts.attempt_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.question_id'], ),
    sa.ForeignKeyConstraint(['selected_option_id'], ['quiz_options.option_id'], ),
    sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table('tutorial_progress',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['tutorial_pages.page_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'page_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutorial_progress')
    op.drop_table('quiz_answers')
    op.drop_table('user_preferences')
    op.drop_table('user_achievements')
    op.drop_table('tutorial_pages')
    op.drop_table('quiz_options')
    op.drop_table('quiz_attempts')
    op.drop_table('command_mastery')
    op.drop_table('command_examples')
    op.drop_table('challenge_completions')
    op.drop_table('users')
    op.drop_table('tutorial_sections')
    op.drop_table('quiz_questions')
    op.drop_table('commands')
    op.drop_table('challenges')
    op.drop_table('achievements')
    # ### end Alembic commands ###
