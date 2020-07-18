import click
from flask_cli import with_appcontext

from webpack import db

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()