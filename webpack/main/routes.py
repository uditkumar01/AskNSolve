from flask import render_template, request, Blueprint, url_for, redirect
from webpack.models import Post, Comment, Post_like, Chat, User
from datetime import datetime
from flask_login import current_user

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    if not (current_user.is_authenticated):
        return redirect(url_for('users.login'))
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    all_his_comments = Comment.query.order_by(Comment.timestamp.desc()).filter(Comment.commentor == current_user.username,Comment.timestamp >= todays_datetime).all()
    all_got_comments = Comment.query.order_by(Comment.timestamp.desc()).filter_by(post_writer = current_user.username).all()
    all_likes = Post_like.query.order_by(Post_like.timestamp.desc()).filter_by(user_post = current_user.id).all()
    all_chats = Chat.query.order_by(Chat.time_of_chat.desc()).filter_by(user__id = current_user.id).all()
    page_no = request.args.get('page',1,type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page_no,per_page = 4)
    all_like_users = []
    all_chat_users = []
    all_his_comment_users = []
    for like in all_likes:
        user = User.query.get_or_404(like.user__id)
        all_like_users.append([user.username,user.id,like.post__id])
    for chat in all_chats:
        user = User.query.get_or_404(chat.user_start_id)
        all_chat_users.append([user.username,user.id])
    for comment in all_his_comments:
        post = Post.query.get_or_404(comment.post__id)
        all_his_comment_users.append([post.author,comment.post__id])
    if current_user.is_authenticated:
        
        profile_image = url_for('static',filename = 'images/' + current_user.profile_pic)
        
        if current_user.theme == 'NULL':
            return render_template('Home_page_light.html' , title = "Home Page",all_got_comments=all_got_comments, all_his_comments = all_his_comment_users, all_likes = all_like_users, all_chats = all_chat_users ,posts = posts, profile_pic = profile_image , username_menu = current_user.username,present_time = datetime.utcnow())
        else:
            return render_template('Home_page_dark.html' , title = "Home Page" ,all_got_comments=all_got_comments, all_his_comments = all_his_comment_users, all_likes = all_like_users, all_chats = all_chat_users,posts = posts, profile_pic = profile_image , username_menu = current_user.username,present_time = datetime.utcnow())
    else:
        profile_image = url_for('static',filename = 'images/' + 'default_profile_pic.jpg')
        return render_template('Home_page_dark.html' , title = "Home Page",posts = posts,all_got_comments=all_got_comments, all_his_comments = all_his_comment_users, all_likes = all_like_users, all_chats = all_chat_users, profile_pic = profile_image , username_menu = 'Unknown User',present_time = datetime.utcnow() )
