# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

### Getting Started
 
 - Base URL: when run locally `http://127.0.0.1:5000`
 - Authentication: NONE

### Error Handling

Errors are returned as JSON Objects in the following format

```json
{
    "succes": "FALSE",
    "error": "[code]",
    "message" : "[message]"
}
```

The API returns four errors when requests fail
```
 - 400: bad request
 - 404: resource not found
 - 405: method not allowed
 - 500: internal error
```

### Documentation


<!--- If we have only one group/collection, then no need for the "ungrouped" heading -->
1. [play quizz](#1-play-quizz)
   1. [play quizz](#i-example-request-play-quizz)
1. [category questions](#2-category-questions)
   1. [category questions](#i-example-request-category-questions)
1. [Search questions](#3-search-questions)
   1. [Search questions](#i-example-request-search-questions)
1. [Create question](#4-create-question)
   1. [Create question](#i-example-request-create-question)
1. [question](#5-question)
   1. [question](#i-example-request-question)
1. [questions](#6-questions)
   1. [questions](#i-example-request-questions)
1. [categories](#7-categories)
   1. [Categories](#i-example-request-categories)



## Endpoints


--------



### 1. play quizz


Get the next random question from the server


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{base_url}}/quizzes
```



***Body:***

```js        
{
    "previous_questions": [],
    "quiz_category": {
        "id": "1",
        "type": "science"
    }
}
```



***More example Requests/Responses:***


#### I. Example Request: play quizz



***Body:***

```js        
{
    "previous_questions": [],
    "quiz_category": {
        "id": "1",
        "type": "science"
    }
}
```



#### I. Example Response: play quizz
```js
{
    "question": {
        "answer": "Blood",
        "category": "1",
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```


***Status Code:*** 200

<br>



### 2. category questions


Get all the questions on the particular category


***Endpoint:***

```bash
Method: GET
Type: 
URL: 
```



***More example Requests/Responses:***


#### I. Example Request: category questions



***Query:***

| Key | Value | Description |
| --- | ------|-------------|
| id | 1 |  |



***Body: None***



#### I. Example Response: category questions
```js
{
    "current_category": "1",
    "questions": [
        {
            "answer": "The Liver",
            "category": "1",
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": "1",
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": "1",
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "complete",
            "category": "1",
            "difficulty": 1,
            "id": 25,
            "question": "My new question "
        },
        {
            "answer": "500km",
            "category": "1",
            "difficulty": 2,
            "id": 26,
            "question": "how far is Lagos?"
        }
    ],
    "success": true,
    "total_questions": 5
}
```


***Status Code:*** 200

<br>



### 3. Search questions


Create a new question


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{base_url}}/questions
```



***Body:***

```js        
{
    "searchTerm": "how"
}
```



***More example Requests/Responses:***


#### I. Example Request: Search questions



***Body:***

```js        
{
    "searchTerm": "how"
}
```



#### I. Example Response: Search questions
```js
{
    "current_category": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "One",
            "category": "2",
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "500km",
            "category": "1",
            "difficulty": 2,
            "id": 26,
            "question": "how far is Lagos?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```


***Status Code:*** 200

<br>



### 4. Create question


Create a new question


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: {{base_url}}/questions
```



***Body:***

```js        
{
    "question": "how far is Lagos?",
    "answer": "500km",
    "category": "1",
    "difficulty": "2"
}
```



***More example Requests/Responses:***


#### I. Example Request: Create question



***Body:***

```js        
{
    "question": "how far is Lagos?",
    "answer": "500km",
    "category": "1",
    "difficulty": "2"
}
```



#### I. Example Response: Create question
```js
{
    "question_id": 26,
    "success": true
}
```


***Status Code:*** 200

<br>



### 5. question


Delete a particular question


***Endpoint:***

```bash
Method: DELETE
Type: 
URL: {{base_url}}/questions/:id
```



***URL variables:***

| Key | Value | Description |
| --- | ------|-------------|
| id | 24 |  |



***More example Requests/Responses:***


#### I. Example Request: question



***Query:***

| Key | Value | Description |
| --- | ------|-------------|
| id | 24 |  |



***Body: None***



#### I. Example Response: question
```js
{
    "message": "Deleted question with id 24 successfully",
    "success": true
}
```


***Status Code:*** 200

<br>



### 6. questions


Get all questions


***Endpoint:***

```bash
Method: GET
Type: 
URL: {{base_url}}/questions
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| page | 2 | Pagination  query param for questions  |



***More example Requests/Responses:***


#### I. Example Request: questions



***Query:***

| Key | Value | Description |
| --- | ------|-------------|
| page | 2 | Pagination  query param for questions  |



***Body: None***



#### I. Example Response: questions
```js
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": "2",
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": "2",
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": "1",
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": "1",
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": "1",
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": "4",
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "complete",
            "category": "1",
            "difficulty": 1,
            "id": 24,
            "question": "new "
        },
        {
            "answer": "complete",
            "category": "1",
            "difficulty": 1,
            "id": 25,
            "question": "My new question "
        }
    ],
    "success": true,
    "total_questions": 10
}
```


***Status Code:*** 200

<br>



### 7. categories


Get all categories


***Endpoint:***

```bash
Method: GET
Type: 
URL: {{base_url}}/categories
```



***More example Requests/Responses:***


#### I. Example Request: Categories



***Body: None***



#### I. Example Response: Categories
```js
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```


***Status Code:*** 200

<br>


---
[Back to top](#trivia)

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
