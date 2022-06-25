from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    # REUSABLE FUNCTIONS
    def get_categories():
        categories = Category.query.all()
        return_categories = []
        for cat in categories:
            return_categories.append(cat.type)
        return return_categories

    @app.route('/categories')
    def get_all_categories():
        return jsonify({
            'success': True,
            'categories': get_categories()
        })


    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
    
        # Calculate start and end slicing
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # Format selection into list of dicts and slice
        questions = [question.format() for question in Question.query.order_by(Question.id).all()]
        current_questions = questions[start:end]
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'categories' : get_categories(),
            'current_category' : get_categories()
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    def error_message(error, default_message):
        try:
            return error.description["message"]
        except TypeError:
            return default_message

    @app.errorhandler(404)
    def ressource_not_found(error):
        print("404")
        return jsonify({
            "success": False, 
            "status": 404,
            "message": error_message(error, "resource not found")
        }), 404

    return app

