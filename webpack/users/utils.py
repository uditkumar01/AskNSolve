import smtplib
from PIL import Image
from flask import url_for, current_app, flash
import secrets
import os

def add_profile_pic(pic):
    name = secrets.token_hex(16)
    NAME,EXT = os.path.splitext(pic.filename)
    picture_name = name + EXT
    profile_pic_path = os.path.join(current_app.root_path,'static/images', picture_name)
    size = (155,155)
    img1 = Image.open(pic)
    img1.thumbnail(size)
    img1.save(profile_pic_path)
    print(img1.size)
    return picture_name

def send_request_email(user):
    token = user.get_reset_token()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('abhixuditxpiyushcompany@gmail.com','gcwkuocyvoppnfnz')

    subject = 'Reset Your Password'

    msg = f"Subject: {subject}\n\n\n\n Hi { user.username },\n\nYou requested to reset the password for your AskNSolve account with the e-mail address ({ user.email }).\nPlease click this link to reset your password.\n\n{url_for('users.request_token', token = token, _external = True)}\n\nPlease ignore it if you haven't made any request.\n\nThanks,\nAskNSolve Team\n"

    server.sendmail(
        'abhixuditxpiyushcompany@gmail.com',
        user.email,
        msg
    )
    flash('An email has been sent to you to reset your password','success')
    flash('Link will be active for 15 minutes ','primary')