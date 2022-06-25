import os
import unittest
import json
from warnings import catch_warnings
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import dotenv_values

config = dotenv_values(".env")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "{}/{}".format(config['DB_URL'], self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']) > 0)
        self.assertIn('Science', data['categories'])

    def test_get_all_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)


    def test_error_404_get_all_questions(self):
        res = self.client().get('/questions?page=1245')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertEqual(data['success'], False)
    
    def test_delete_category(self):
        res = self.client().delete('/questions/{}'.format(14))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_category_404(self):
        res = self.client().delete('/questions/{}'.format(1234323234))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Question with id {} does not exist.'.format(1234323234))

    def test_create_question(self):
        new_question = {
            'question' : 'How long does it take to boil an egg?',
            'answer' : '3min',
            'category' : '1',
            'difficulty' : 1
        } 

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question_id'] > 0)

    def test_create_question_bad_request(self):
        new_question = {
            'question' : '',
            'answer' : '3min',
            'category' : '1',
            'difficulty' : 1
        } 

        res = self.client().post('/questions', json = new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Question can not be blank') 

    def test_get_category_questions(self):
        category_id = 2
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], str(category_id))

    def test_get_category_questions(self):
        category_id = 235
        res = self.client().get('/categories/{}/questions'.format(category_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Cateogry with ID {} has no question'.format(category_id))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()