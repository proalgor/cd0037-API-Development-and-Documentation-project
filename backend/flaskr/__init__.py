from crypt import methods
from email import message
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import func

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
        return_categories = {}
        for cat in categories:
            return_categories.update({cat.id: cat.type})
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
        
        search_term = body.get("searchTerm", None)

        if search_term:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            if not questions:
                abort(404, {'message': 'no questions contains the search string "{}"'.format(search_term)})
            
            questions_found = [question.format() for question in questions]
            
            return jsonify({
                'success': True,
                'questions': questions_found,
                'total_questions': len(questions_found),
                'current_category' : get_categories()
            })

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


    @app.route('/categories/<int:cat_id>/questions')
    def get_category_questions(cat_id):
        cat_id_string = str(cat_id)

        questions = Question.query.filter(Question.category == cat_id_string).order_by(Question.id).all()
        formated_questions = [ q.format() for q in questions]
        if not questions:
            abort(400, {'message': 'Cateogry with ID {} has no question'.format(cat_id_string) })

        return jsonify({
            'success': True,
            'questions': formated_questions,
            'total_questions': len(formated_questions),
            'current_category' : cat_id_string
        })


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        req_body = request.get_json()

        if not req_body:
            # If no JSON Body was given, raise error.
            abort(400, {'message': 'Invalid JSON in the Request'})
            
        previous_questions = req_body.get('previous_questions', None)

        current_category = req_body.get('quiz_category', None)

        if not previous_questions:
            previous_questions = []
        
        if current_category:
            if not Category.query.get(int(current_category['id'])):
                question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first() 
            else:
                question = Question.query.filter(Question.category == str(current_category['id'])).filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        else:
            question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        
        return jsonify({
            'success': True,
            'question': question.format()
        })


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
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "status": 405,
            "message": error_message(error, "HTTP method is not allowed on this route")
        }), 405
    
    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False, 
            "status": 400,
            "message": error_message(error, "Please verify your request parameters")
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        print(error)
        return jsonify({
            "success": False, 
            "status": 500,
            "message": "An error occured try again"
        }), 500
    return app

