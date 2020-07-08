from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField,BooleanField
from wtforms.validators import DataRequired, ValidationError, Length
from webpack.models import User


class Post_form(FlaskForm):

    post_title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    # like = BooleanField('Like')
    submit = SubmitField('Ask')

class Comment_form(FlaskForm):
    commentor = StringField('Commentor',validators=[DataRequired(),Length(min = 3 , max = 20,message="Length should be between 3 to 20")])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    # like = BooleanField('Like')
    post__id = IntegerField('Post_id', validators=[DataRequired()])
    submit = SubmitField('Post')

    def user_existance(self, commentor):
        user = User.query.filter_by(username = commentor.data).first()
        if not user:
            raise ValidationError('No such username exists')