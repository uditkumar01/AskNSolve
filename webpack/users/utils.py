import smtplib
from PIL import Image
from flask import url_for, current_app, flash
import secrets
from webpack import mail
from webpack.config import Config
from flask_mail import Message
import os

def add_profile_pic(pic):
    name = secrets.token_hex(16)
    NAME,EXT = os.path.splitext(pic.filename)
    picture_name = name + '.webp'
    profile_pic_path = os.path.join(current_app.root_path,'static/images', picture_name)
    size = (50,50)
    img1 = Image.open(pic)
    img1.thumbnail(size)
    img1.save(profile_pic_path)
    return picture_name

# def send_request_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender='abhixuditxpiyushcompany@gmail.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}

# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)

def send_request_email(user):
    token = user.get_reset_token()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(Config.MAIL_USERNAME,'rypktgiqkystabig')

    subject = 'Reset Your Password'

    msg = f"Subject: {subject}\n\n\n\n Hi { user.username },\n\nYou requested to reset the password for your AskNSolve account with the e-mail address ({ user.email }).\nPlease click this link to reset your password.\n\n{url_for('users.request_token', token = token, _external = True)}\n\nPlease ignore it if you haven't made any request.\n\nThanks,\nAskNSolve Team\n"

    server.sendmail(
        'abhixuditxpiyushcompany@gmail.com',
        user.email,
        msg
    )
    flash('An email has been sent to you to reset your password','success')
    flash('Link will be active for 15 minutes ','primary')