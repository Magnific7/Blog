from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile, BlogForm, CommentForm,UpdateBlog
from ..models import User, Role, Blog,Like,Dislike,Comment
from flask_login import login_required, current_user
from .. import db,photos
from sqlalchemy import func
from sqlalchemy.orm import session
from ..requests import get_quotes


# Views
@main.route('/',methods = ['GET', 'POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''

    quotes = get_quotes()
    # print(quotes)
    
    blogs = Blog.query.all()

    title = 'Blog'
    return render_template('index.html', title = title, blogs = blogs, quotes = quotes)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    get_blogs = Blog.query.filter_by(user_id = current_user.id).all()


    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, blogs_content = get_blogs)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/blog/new',methods = ['GET','POST'])
@login_required
def blog():
    '''
    View blog function that returns the blog page and data
    '''
    blog_form = BlogForm()
    my_likes = Like.query.filter_by(blog_id=Blog.id)

    if blog_form.validate_on_submit():
        content = blog_form.content.data
        blog_title = blog_form.blog_title.data

        new_blog = Blog(blog_title=blog_title, content=content,user = current_user)
        new_blog.save_blog()

        return redirect(url_for('main.index'))


    title = 'New Blog'
    return render_template('blog.html', title = title, blog_form = blog_form, likes = my_likes)

@main.route('/blog/<int:blog_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(blog_id):
    '''
    View comments page function that returns the comment page and its data
    '''
    # comment_form = CommentForm()

    comment_form = CommentForm()
    my_blog = Blog.query.get(blog_id)
    if my_blog is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_content = comment_form.comment_content.data

        new_comment = Comment(comment_content=comment_content, blog_id = blog_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', blog_id=blog_id))

    all_comments = Comment.query.filter_by(blog_id=blog_id).all()
    title = 'Comments'

    return render_template('comment.html', title = title, blog=my_blog ,comment_form = comment_form, comment = all_comments )


@main.route('/blog/<int:blog_id>/like',methods = ['GET','POST'])
@login_required
def like(blog_id):
    '''
    View like function that returns likes
    '''
    my_blog = Blog.query.get(blog_id)
    user = current_user

    blog_likes = Like.query.filter_by(blog_id=blog_id)


    if Like.query.filter(Like.user_id==user.id,Like.blog_id==blog_id).first():
        return  redirect(url_for('.index'))

    new_like = Like(blog_id=blog_id, user = current_user)
    new_like.save_likes()
    return redirect(url_for('.index'))

@main.route('/blog/<int:blog_id>/dislike',methods = ['GET','POST'])
@login_required
def dislike(blog_id):
    '''
    View dislike function that returns dislikes
    '''
    my_blog = Blog.query.get(blog_id)
    user = current_user

    blog_dislikes = Dislike.query.filter_by(blog_id=blog_id)

    if Dislike.query.filter(Dislike.user_id==user.id,Dislike.blog_id==blog_id).first():
        return redirect(url_for('.index'))

    new_dislike = Dislike(blog_id=blog_id, user = current_user)
    new_dislike.save_dislikes()
    return redirect(url_for('.index'))

@main.route('/blog//<int:blog_id>/updateblog',methods = ['GET','POST'])
@login_required
def update_blog(blog_id):
    my_blog = Blog.query.get(blog_id)
    print(my_blog.id)
    if my_blog is None:
        abort(404)

    form = UpdateBlog()

    if form.validate_on_submit():
        my_blog.content = form.blog.data

        db.session.add(my_blog)
        db.session.commit()
        print(my_blog.content)
        return redirect(url_for('.profile', uname=current_user.username))

    return render_template('profile/updateblog.html',form =form)

@main.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
def delete_blog(blog_id):
    my_blog = Blog.query.get(blog_id)
    db.session.delete(my_blog)
    db.session.commit()
    return redirect(url_for('.index'))

    