from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required,Email
from ..models import User

class PitchForm(FlaskForm):

    pitch_title = StringField('Title', validators=[Required()])
    content = TextAreaField('Your Pitch', validators=[Required()])
    category = SelectField('Type', choices=[('Interview-Pitch','Motivational'),('Interview-Pitch','Educative'),('Interview-Pitch','Fun time'),('Interview-Pitch','Other')], validators=[Required()])
    submit = SubmitField('Pitch It!')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class UpdateBlog(FlaskForm):
    blog = TextAreaField('Update your blog here',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Leave your comments', validators=[Required()])
    submit = SubmitField('Comment')    