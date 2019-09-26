import unittest
from app.models import Pitch, User, Comment
from app import db



class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Movie class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''

        self.user_jj = User(username = 'jj', password = 'jj', email = 'jj@.com')
        self.new_comment = Comment(comment_content = 'movie', pitch_id = 30, user_id=self.user_jj)
        self.new_pitch = Pitch(id=30,pitch_title="movie", content="Watch moremovies",category='Product-Pitch',user_id = self.user_jj,comments = self.new_comment)
    
    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):

        self.new_pitch.save_pitch()
        got_pitches = Pitch.get_pitch(30)
        self.assertTrue(len(got_pitches) == 1)

    # def test_check_instance_variables(self):
    #     self.assertEquals(self.new_pitch.id,30)
    #     self.assertEquals(self.new_pitch.pitch_title,'movie')
    #     self.assertEquals(self.new_pitch.content,'Watch moremovies')
    #     self.assertEquals(self.new_pitch.category,"Product Pitch")
    #     self.assertEquals(self.new_pitch.user_id,self.user_Sophy)
    #     self.assertEquals(self.new_pitch.comments,self.new_comment)    