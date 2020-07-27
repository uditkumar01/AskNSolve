import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    size = (80,80)
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
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = "AskNsolve Team <Config.MAIL_USERNAME>"
    message["To"] = user.email

    # Create the plain-text and HTML version of your message
    text = """\
        Please ignore if you have not requested Password Reset.
    """
    html = u"""\
    <html>
    <body>
        <p>Hi """+str(user.username)+""",</p>
        <p>You requested to reset the password for your AskNSolve account with the e-mail address <mark style = "background: red; color: white;">"""+str(user.email)+"""</mark>.<br>Please click this link to reset your password.</p>
        <a href = '"""+str(url_for('users.request_token', token = token, _external = True))+"""'><h3>PASSWORD RESET</h3></a>
        <br>
        <p>Here, is the link in case Password Reset above is not working</p><br>
        <u>"""+str(url_for('users.request_token', token = token, _external = True))+"""</u><br><br>
        <p>Thanks,<br><br>AskNSolve Team</p>

    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(Config.MAIL_USERNAME, 'rypktgiqkystabig')
        server.sendmail(
            Config.MAIL_USERNAME, user.email, message.as_string()
        )

# def send_request_email(user):
#     token = user.get_reset_token()
#     server = smtplib.SMTP('smtp.gmail.com',587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()

#     server.login(Config.MAIL_USERNAME,'rypktgiqkystabig')

#     subject = 'Reset Your Password'

#     msg = f"Subject: {subject}\n\n\n\n Hi { user.username },\n\n You requested to reset the password for your AskNSolve account with the e-mail address ({ user.email }).\nPlease click this link to reset your password.\n\n {url_for('users.request_token', token = token, _external = True)}\n\nPlease ignore it if you haven't made any request.\n\nThanks,\nAskNSolve Team\n"

#     server.sendmail(
#         'abhixuditxpiyushcompany@gmail.com',
#         user.email,
#         msg
#     )
#     flash('An email has been sent to you to reset your password','success')
#     flash('Link will be active for 15 minutes ','primary')