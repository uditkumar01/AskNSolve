from flask import render_template, flash,redirect,url_for,request, abort, Blueprint
from webpack.users.forms import Login_form,Registration_Form, Update_Form, Request_reset_form, Change_password, Chatting
from webpack import db,bcrypt
from webpack.models import User, Post, Chat
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from webpack.users.utils import add_profile_pic, send_request_email

users = Blueprint('users',__name__)

@users.route("/login",methods = ['GET','POST'])
def login():
    form = Login_form()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.checkbox.data)
            flash("{} logined successfully!".format(user.username),'success')
            user.active = "active"
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif user and not bcrypt.check_password_hash(user.password,form.password.data):
            flash("{}, please check your password!".format(user.username),'danger')
        elif user == None:
            flash("Your E-mail is not registered!",'danger')
    return render_template('login_page.html' , title = "Login Page", form = form)


@users.route("/theme_select", methods = ['GET','POST'])
def theme_select():
    if current_user.theme == 'NULL':
        current_user.theme = 'DARK'
        db.session.commit()
    elif current_user.theme == 'DARK':
        current_user.theme = 'NULL'
        db.session.commit()
    return redirect(url_for('users.account',user_id = current_user.id))

@users.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Registration_Form()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("{}'s account created successfully!".format(form.username.data),'success')
        return redirect(url_for('users.login'))
    return render_template('register1.html' , title = "Register", form = form)


@login_required
@users.route("/account/<int:user_id>", methods = ['POST','GET'])
def account(user_id):
    form = Update_Form()
    MY_SKILLS_LIST = []
    _user = User.query.get_or_404(user_id)
    if current_user.id != _user.id:
        MY_SKILLS_LIST = (_user.skills).split(',')
        profile_image = url_for('static',filename = 'images/' + _user.profile_pic)
        if current_user.theme == 'NULL':
            return render_template('account.html',title = _user.username + '\'s Account Info', profile_picture = profile_image, form = "NULL", MY_SKILLS_LIST = MY_SKILLS_LIST, _user = _user)
        else:
            return render_template('account_dark.html',title = _user.username + '\'s Account Info', profile_picture = profile_image, form = "NULL", MY_SKILLS_LIST = MY_SKILLS_LIST, _user = _user)
    else:
        if current_user.skills != 'Unknown':
                MY_SKILLS_LIST = (current_user.skills).split(',')
        if form.validate_on_submit():
            flash(f'Updated','info')
            if form.profile_pic.data:
                pic_name = add_profile_pic(form.profile_pic.data)
                current_user.profile_pic = pic_name
            if form.username.data:
                current_user.username = form.username.data
            if form.email.data:
                current_user.email = form.email.data
            if form.country.data:
                current_user.country = form.country.data
            if form.skills.data:
                current_user.skills = form.skills.data
                MY_SKILLS_LIST = (form.skills.data).split(',')
            current_user.first_name = form.first_name.data.title()
            current_user.last_name = form.last_name.data.title()
            current_user.country = form.country.data.title()

            db.session.commit()
            flash('Your account info is Updated !!!','success')
            return redirect(url_for('users.account', user_id = current_user.id))
        elif request.method == 'GET':
            if current_user.first_name != 'Unknown':
                form.first_name.data = current_user.first_name
            if current_user.last_name != 'Unknown':
                form.last_name.data = current_user.last_name
            if current_user.skills != 'Unknown':
                form.skills.data = current_user.skills
            form.username.data = current_user.username
            form.email.data = current_user.email
        profile_image = url_for('static',filename = 'images/' + current_user.profile_pic)

        if current_user.theme == 'NULL':
            return render_template('account.html',title = 'Your Account Info', profile_picture = profile_image, form = form, MY_SKILLS_LIST = MY_SKILLS_LIST, _user = current_user)
        else:
            return render_template('account_dark.html',title = 'Your Account Info', profile_picture = profile_image, form = form, MY_SKILLS_LIST = MY_SKILLS_LIST, _user = current_user)

@login_required
@users.route("/user/<string:username>")
def all_user_post(username):
    page_no = request.args.get('page',1,type = int)
    user = User.query.filter_by(username = username).first_or_404()
    _posts = Post.query.order_by(Post.date_posted.desc()).filter_by(user_id = user.id).paginate(page = page_no, per_page = 5)
    if current_user.is_authenticated:
        if current_user.theme == 'NULL':
            return render_template('only_his_post.html' , title = user.username ,posts = _posts, profile_pic = current_user.profile_pic , username_menu = user.username ,present_time = datetime.utcnow(), user = user)
        else:
            return render_template('only_his_post_dark.html' , title = user.username ,posts = _posts, profile_pic = current_user.profile_pic , username_menu = user.username ,present_time = datetime.utcnow(), user = user)
    else:
        redirect(url_for('users.login'))


@users.route("/reset_password", methods = ['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Request_reset_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_request_email(user)
       
        return redirect(url_for('users.login'))
    
    return render_template('reset_request.html', title = "Request Reset", form = form)


@users.route("/reset_password/<token>", methods = ['GET','POST'])
def request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user:
        flash('Invalid Token','warning')
    form = Change_password()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash("{}'s password is updated successfully!".format(user.username),'success')
        return redirect(url_for('users.login'))
    return render_template('password_reset.html', title = "Password Reset", form = form)

@login_required
@users.route("/logout")
def logout():
    
    current_user.active = "notactive"
    current_user.total_time_spent = datetime.utcnow()
    db.session.commit()
    logout_user()
    flash(f'Logout Successfull!','success')
    return redirect(url_for('users.login'))



@users.route("/chat_room/<int:user_id>" , methods = ['GET','POST'])
def chat_room(user_id):
    form = Chatting()
    my_chat = Chat.query.filter_by(user_start_id = user_id, user__id = current_user.id).all()
    his_chat = Chat.query.filter_by(user_start_id = current_user.id, user__id = user_id).all()
    _user = User.query.filter_by(id = user_id).first()
    all_messages = []
    for chat in my_chat:
        all_messages.append([chat.user_start_id, chat.messages, chat.time_of_chat])
    for chat in his_chat:
        all_messages.append([chat.user_start_id, chat.messages, chat.time_of_chat])
    all_messages.sort(reverse=True, key = lambda x:x[2])
    if form.validate_on_submit() and request.method == "POST":
        text_1 = Chat(user_start_id = current_user.id, user__id = user_id, messages = form.message.data)
        db.session.add(text_1)
        print('text_1',text_1)
        flash(f"{all_messages}")
        db.session.commit()
        form.message.data = ""
    if my_chat != None and his_chat != None:
        if current_user.theme == "NULL":
            return render_template('chat_room_light.html',title = 'Chat', form = form, messages = all_messages ,user_id = user_id, _user = _user)
        else:
            return render_template('chat_room.html',title = 'Chat', form = form, messages = all_messages ,user_id = user_id, _user = _user)
    return redirect(url_for('users.account', user_id = user_id))


@users.route("/chats/<int:user_id>" , methods = ['GET'])
def all_chats(user_id):
    my_chat = Chat.query.filter_by(user_start_id = user_id, user__id = current_user.id).all()
    his_chat = Chat.query.filter_by(user_start_id = current_user.id, user__id = user_id).all()
    _user = User.query.filter_by(id = user_id).first()
    all_messages = []
    for chat in my_chat:
        all_messages.append([chat.user_start_id, chat.messages, chat.time_of_chat])
    for chat in his_chat:
        all_messages.append([chat.user_start_id, chat.messages, chat.time_of_chat])
    all_messages.sort(reverse=True, key = lambda x:x[2])
    if my_chat != None and his_chat != None:
        if current_user.theme == "NULL":
            return render_template('chats_light.html',title = 'Chat', messages = all_messages ,user_id = user_id, _user = _user)
        else:
            return render_template('chats.html',title = 'Chat', messages = all_messages ,user_id = user_id, _user = _user)
    return redirect(url_for('users.account', user_id = user_id))

    