from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class Quote:
    '''
    Quote class to define quote objects.
    '''
    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    likes = db.relationship('Like',backref = 'user',lazy = "dynamic")
    dislikes = db.relationship('Dislike',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Blog(db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)
    blog_title = db.Column(db.String)
    category = db.Column(db.String())
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'blog',lazy = "dynamic")
    likes = db.relationship('Like',backref = 'blog',lazy = "dynamic")
    dislikes = db.relationship('Dislike',backref = 'blog',lazy = "dynamic")


    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls,id):
        blogs = Blog.query.filter_by(blog_id=id).all()
        return blogs

    def __repr__(self):
        return f'Blog {self.blog_title}'
class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    comment_content = db.Column(db.String())
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()
        return comments

    @classmethod
    def get_all_comments(cls,id):
        comments = Comment.query.order_by('-id').all()
        return comments

class Like (db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key=True)
    like = db.Column(db.Integer,default=1)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_likes(self):
        db.session.add(self)
        db.session.commit()

    def add_likes(cls,id):
        like_blog = Like(user = current_user, blog_id=id)
        like_blog.save_likes()

    @classmethod
    def get_likes(cls,id):
        like = Like.query.filter_by(blog_id=id).all()
        return like


    @classmethod
    def get_all_likes(cls,blog_id):
        likes = Like.query.order_by('-id').all()
        return likes


    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}'


class Dislike (db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.Integer,primary_key=True)
    dislike = db.Column(db.Integer,default=1)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_dislikes(self):
        db.session.add(self)
        db.session.commit()

    def add_dislikes(cls,id):
        dislike_blog = Dislike(user = current_user, blog_id=id)
        dislike_blog.save_dislikes()

    @classmethod
    def get_dislikes(cls,id):
        dislike = Dislike.query.filter_by(blog_id=id).all()
        return dislike


    @classmethod
    def get_all_dislikes(cls,blog_id):
        dislikes = Dislike.query.order_by('-id').all()
        return dislikes


    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}'