from datetime import datetime
from webpack import db,login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



# SQLALCHEMY_TRACK_MODIFICATIONS = True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable = False, default = "Unknown")
    last_name = db.Column(db.String(100), nullable = False, default = "Unknown")
    country = db.Column(db.String(50), nullable = False, default = "Unknown")
    skills = db.Column(db.String(100), nullable = False, default = "Unknown")
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    profile_pic = db.Column(db.String(100), nullable = False, default = "default_profile_pic.jpg")
    theme = db.Column(db.String(15), default  = "NULL")
    active =  db.Column(db.String(15), default  = "NULL")
    posts = db.relationship('Post', backref = 'author', lazy = True)


    def get_reset_token(self,expires_in = 900):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.country}','{self.username}','{self.email}','{self.profile_pic}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}','{self.content}','{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentor = db.Column(db.String(30), nullable = False)
    comment = db.Column(db.String(100000), nullable = False)
    post_writer = db.Column(db.String(30), nullable = False)
    post__id = db.Column(db.Integer, nullable = False)
    profile_pic = db.Column(db.String(100), nullable = False, default = "default_profile_pic.jpg")
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.comment}','{self.commentor}',{self.post__id},'{self.timestamp}')"
    
class Post_like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post__id = db.Column(db.Integer, nullable = False)
    user_post = db.Column(db.Integer, nullable = False)
    user__id = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)


    def __repr__(self):
        return f"Post_like('{self.post__id}','{self.user__id}')"

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_start_id = db.Column(db.Integer, nullable = False)
    user__id = db.Column(db.Integer, nullable = False)
    time_of_chat = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    seen = db.Column(db.Integer, default = 0)
    messages = db.Column(db.String(10000),nullable = False, default = "No message")

    def __repr__(self):
        return f"Chat('{self.user_start_id}','{self.user__id}','{self.messages}')"

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False)
    current_user_id = db.Column(db.Integer, nullable = False)
    time_of_follow = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Follow('{self.user_id}','{self.current_user_id}')"
        