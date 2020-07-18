from flask import Blueprint
from flask_cli import with_appcontext

from webpack import db

cmd = Blueprint(__name__,db)
@cmd.cli.command('create_db')
def create_tables():
    db.create_all()
    print('***** Datebase created ****')