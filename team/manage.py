#!/usr/bin/env python
import os
from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from . import create_app, db
from .user import Role, User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def setup():
    """Runs the set-up needed for local development."""
    setup_general()

def setup_general():
    """Runs the set-up needed for both local development.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=(current_app.config['ADMIN_EMAIL'])).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=(current_app.config['ADMIN_PASSWORD']),
                confirmed=True,
                email=(current_app.config['ADMIN_EMAIL']))
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))

if __name__ == '__main__':
    manager.run()
