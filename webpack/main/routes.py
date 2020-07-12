from flask import render_template, request, Blueprint, url_for, redirect
from webpack.models import Post
from datetime import datetime
from flask_login import current_user

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    if not (current_user.is_authenticated):
        return redirect(url_for('users.login'))
    page_no = request.args.get('page',1,type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page_no,per_page = 4)
    if current_user.is_authenticated:
        if current_user.profile_pic:
            profile_image = url_for('static',filename = 'images/' + current_user.profile_pic)
        else:
            profile_image = url_for('static',filename = 'images/' + 'default_profile_pic.jpg')

        return render_template('Home_page_light.html' , title = "Home Page" ,posts = posts, profile_pic = profile_image , username_menu = current_user.username,present_time = datetime.utcnow())
    else:
        profile_image = url_for('static',filename = 'images/' + 'default_profile_pic.jpg')
        return render_template('Home_page_light.html' , title = "Home Page",posts = posts, profile_pic = profile_image , username_menu = 'Unknown User',present_time = datetime.utcnow() )
