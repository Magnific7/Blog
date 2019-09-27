import unittest
from app.models import Blog, User, Comment
from app import db



class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Movie class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''

        self.user_jj = User(username = 'jj', password = 'jj', email = 'jj@.com')
        self.new_comment = Comment(comment_content = 'movie', blog_id = 30, user_id=self.user_jj)
        self.new_blog = Blog(id=30,blog_title="movie", content="Watch moremovies",category='Product-blog',user_id = self.user_jj,comments = self.new_comment)
    
    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())>0)

    def test_get_blog_by_id(self):

        self.new_blog.save_blog()
        got_blogs = Blog.get_blog(30)
        self.assertTrue(len(got_blogs) == 1)

