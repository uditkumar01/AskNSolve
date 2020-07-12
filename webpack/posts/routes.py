from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from webpack import db
from webpack.models import Post,Comment,User,Post_like
from webpack.posts.forms import Post_form, Comment_form
from datetime import datetime

posts = Blueprint('posts',__name__)

@login_required
@posts.route("/ask/new", methods = ['GET','POST'])
def create_post():
    form = Post_form()
    if form.validate_on_submit():
        post = Post(title = form.post_title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Question is Uploded! ', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title = "Ask", form = form, form_title_webpage = "Ask Here" , button_name = "Ask")

@login_required
@posts.route("/like/<int:post_id>", methods = ['POST','GET'])
def like(post_id):
    post = Post.query.get_or_404(post_id)
    user_exist = Post_like.query.filter_by(post__id = post_id,user__id = current_user.id).first()
    if post and (not user_exist):
        like = Post_like(post__id = post_id, user__id = current_user.id)
        db.session.add(like)
        db.session.commit()
    elif post and user_exist:
        db.session.delete(user_exist)
        db.session.commit()

    return redirect(url_for('posts.post', post_id = post_id))

@login_required
@posts.route("/ask/<int:post_id>", methods = ['POST','GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    user_exist = Post_like.query.filter_by(post__id = post_id,user__id = current_user.id).first()
    no_of_likes = len(Post_like.query.filter_by(post__id = post_id).all())
    post_like_name = "like"
    if post and (not user_exist):
        post_like_name = "like"
    elif post and user_exist:
        post_like_name = "unlike"
    
    form = Comment_form()
    _comments = Comment.query.order_by(Comment.timestamp.desc()).filter_by(post__id = post_id).all()
    if current_user.is_authenticated:
        form.commentor.data = current_user.username
    if form.validate_on_submit and request.method == 'POST':
        # flash('Not ommented successfully!!!', 'success')
        if current_user.username == form.commentor.data:
            comment = Comment(commentor = form.commentor.data,comment = form.comment.data, post__id = post_id, profile_pic = current_user.profile_pic)
            db.session.add(comment)
            db.session.commit()
            flash('Commented successfully!!!', 'success')
            return redirect(url_for('main.home'))
        elif current_user.username != form.commentor.data:
            flash(f'Please don\'t use anyone else\'s username','danger')
            return  redirect(url_for('main.home'))
        else:
            flash(f'Your Comment is not uploaded successfully!','danger')
    if current_user.is_authenticated:
        if current_user.profile_pic:
            profile_image = url_for('static',filename = 'images/' + current_user.profile_pic)
        else:
            profile_image = url_for('static',filename = 'images/' + 'default_profile_pic.jpg')

        return render_template('sep_post_light.html' , title = post.title ,post = post, profile_pic = profile_image ,_comments = _comments ,no_of_likes = no_of_likes ,username_menu = current_user.username,form = form,post_like_name = post_like_name ,present_time = datetime.utcnow())
    else:
        profile_image = url_for('static',filename = 'images/' + 'default_profile_pic.jpg')
        return render_template('sep_post_light.html' , title = post.title ,post = post, profile_pic = profile_image ,_comments = _comments ,no_of_likes = no_of_likes , username_menu = 'Unknown User' , form = form,post_like_name = post_like_name , present_time = datetime.utcnow())

# @login_required
# @posts.route("/post_id=<int:post_id>/viewcomments", methods = ['POST','GET'])
# def view_comments(post_id):
#     form = Comment_form()
#     post_id = request.args.get('post_id',1,type = int)
#     page_no = request.args.get('page',1,type = int)
#     _comments = Comment.query.order_by(Comment.timestamp.desc()).filter_by(post__id = post_id).paginate(page = page_no, per_page = 5)
#     user = current_user
#     if current_user.is_authenticated:
#         form.commentor.data = current_user.username
#     if form.validate_on_submit and request.method == 'POST':
#         # flash('Not ommented successfully!!!', 'success')
#         if current_user.username == form.commentor.data:
#             comment = Comment(commentor = form.commentor.data,comment = form.comment.data, post__id = post_id)
#             db.session.add(comment)
#             db.session.commit()
#             flash('Commented successfully!!!', 'success')
#             return redirect(url_for('main.home'))
#         elif current_user.username != form.commentor.data:
#             flash(f'Please don\'t use anyone else\'s username','danger')
#             return  redirect(url_for('main.home'))
#         else:
#             flash(f'Your Comment is not uploaded successfully!','danger')
#     if current_user.is_authenticated:
#         return render_template('comment_page.html', title = "Comments",form = form ,user = user, _comments = _comments, present_time = datetime.utcnow(),username_menu = user.username)
#     else:
#         return redirect(url_for('users.login'))
    
@login_required
@posts.route("/ask/<int:post_id>/update" , methods = ['POST','GET'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Post_form()
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your question is updated!','success')
        return redirect(url_for('posts.post', post_id = post.id))
    form.post_title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title = "Update Question", form = form , form_title_webpage = "Edit Question" , button_name = 'Update')

@login_required
@posts.route("/ask/<int:post_id>/delete" , methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_comments = Comment.query.filter_by(post__id = post_id).all()
    if post.author != current_user:
        abort(403)
    for comment in post_comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    flash('Your question is deleted successfully!','success')
    return redirect(url_for('main.home'))
