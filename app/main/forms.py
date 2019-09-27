from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required,Email
from ..models import User

class BlogForm(FlaskForm):

    blog_title = StringField('Title', validators=[Required()])
    content = TextAreaField('Your Blog', validators=[Required()])
    # category = SelectField('Type', choices=[('Interview-Blog','Motivational'),('Interview-Blog','Educative'),('Interview-Blog','Fun time'),('Interview-Blog','Other')], validators=[Required()])
    submit = SubmitField('submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class UpdateBlog(FlaskForm):
    blog = TextAreaField('Update your blog here',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Leave your comments', validators=[Required()])
    submit = SubmitField('Comment')

    