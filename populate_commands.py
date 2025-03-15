# populate_commands.py
from app import app, db
from models import Command, CommandExample, CommandOption

def populate_database():
    # First, clear existing data
    CommandExample.query.delete()
    CommandOption.query.delete()
    Command.query.delete()
    
    # Add ls command
    ls_command = Command(
        name='ls',
        syntax='ls [OPTION]... [FILE]...',
        description='List information about the FILEs (the current directory by default). Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.',
        category='File Operations',
        shell_type='bash'
    )
    db.session.add(ls_command)
    db.session.flush()  # Get ID before adding related objects
    
    # Add ls command options
    ls_options = [
        CommandOption(
            command_id=ls_command.command_id,
            flag='-a, --all',
            description='do not ignore entries starting with .'
        ),
        CommandOption(
            command_id=ls_command.command_id,
            flag='-l',
            description='use a long listing format'
        ),
        CommandOption(
            command_id=ls_command.command_id,
            flag='-h, --human-readable',
            description='with -l, print sizes in human readable format (e.g., 1K 234M 2G)'
        ),
        CommandOption(
            command_id=ls_command.command_id,
            flag='-r, --reverse',
            description='reverse order while sorting'
        ),
        CommandOption(
            command_id=ls_command.command_id,
            flag='-t',
            description='sort by modification time, newest first'
        )
    ]
    db.session.add_all(ls_options)
    
    # Add ls command examples
    ls_examples = [
        CommandExample(
            command_id=ls_command.command_id,
            title='List all files including hidden ones',
            command='ls -a',
            output='.              .profile       Desktop        Downloads      Pictures\n..             .bash_history  Documents      Music          Videos\n.bash_logout   .bashrc        .hidden_file   example.txt',
            explanation='Shows all files, including those that start with a dot (.) which are normally hidden.'
        ),
        CommandExample(
            command_id=ls_command.command_id,
            title='List files with detailed information',
            setup_command='touch example.txt',
            command='ls -l example.txt',
            output='-rw-r--r-- 1 user group 0 Mar 15 10:23 example.txt',
            explanation='Shows detailed information about example.txt including permissions, owner, size, and modification date.'
        ),
        CommandExample(
            command_id=ls_command.command_id,
            title='List files sorted by modification time',
            command='ls -lt',
            output='total 16\ndrwxr-xr-x 2 user group 4096 Mar 15 10:23 Documents\ndrwxr-xr-x 2 user group 4096 Mar 15 10:22 Downloads\ndrwxr-xr-x 2 user group 4096 Mar 15 10:20 Pictures\ndrwxr-xr-x 2 user group 4096 Mar 15 10:18 Music',
            explanation='Lists all files in long format, sorted by modification time with newest first.'
        )
    ]
    db.session.add_all(ls_examples)
    
    # Add more commands here (cp, mkdir, etc.)
    
    # Commit changes
    db.session.commit()
    print("Database populated successfully!")

if __name__ == "__main__":
    with app.app_context():
        populate_database()