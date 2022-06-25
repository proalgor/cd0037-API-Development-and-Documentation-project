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


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_category(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404, {'message': 'Question with id {} does not exist.'.format(question_id)})
        try:
            question.delete()

            return jsonify({
                'success': True,
                'message': 'Deleted question with id {} successfully'.format(question_id)
            })

        except:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if not body:
            abort(400, {'message': 'request does not contain a JSON body'})

        question = body['question']
        answer = body['answer']
        category = body['category']
        difficulty = body['difficulty']

        if not question:
            abort(400, {'message': 'Question can not be blank'})

        if not answer:
            abort(400, {'message': 'Answer can not be blank'})

        if not category:
            abort(400, {'message': 'Category can not be blank'})

        if not difficulty:
            abort(400, {'message': 'Difficulty can not be blank'})
        
        try:
            new_question = Question(
                question = question, 
                answer = answer, 
                category= category,
                difficulty = difficulty
                )
            new_question.insert()

            return jsonify({
                'success': True,
                'question_id': new_question.id,
            })

        except:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        cat_id_string = str(cat_id)

        category = Category.query.get(cat_id)

        questions = Question.query.filter(Question.category == cat_id_string).order_by(Question.id).all()
        if not questions:
            abort(400, {'message': 'Cateogry with ID {} has no question'.format(cat_id_string) })

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category' : category.type
        })

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
        return jsonify({
            "success": False, 
            "status": 404,
            "message": error_message(error, "resource not found")
        }), 404
    
    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False, 
            "status": 400,
            "message": error_message(error, "Please verify your request parameters")
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False, 
            "status": 500,
            "message": "An error occured try again"
        }), 500
    return app

