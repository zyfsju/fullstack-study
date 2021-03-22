# Trivia App

## Features

1. View all questions or by category.
2. Play the quiz game.
3. Add questions.
4. Search for questions.

### Frontend

Implemented with React. Install dependencies and develop locally with npm as follows.

```bash
cd frontend
npm install
npm start
```

### Database Setup

PostgreSQL + psql

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Backend

Python 3.7 + Flask + SQLAlchemy

API endpoints are implemented with Flask and data are stored in a PostgreSQL instance.

Create a virtual environment and install dependencies in `/backend` folder:

```bash
cd backend
virtualenv --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
```

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Endpoints

**GET "/categories"**

-   Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
-   Request Arguments: None
-   Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

**GET "/questions?page="**

-   Fetches all categories, paginatd questions, current category and total questions.
-   Request Arguments: page number
-   Returns: An object with keys, "categories", "questions", "current category" and "total questions". Example:

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled "I Know Why the Caged Bird Sings"?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer"s original name is Cassius Clay?"
        }
    ],
    "total_questions": 2
}
```

**DELETE "/questions/<question_id>"**

-   Deletes a question using question_id.
-   Request Arguments: question_id
-   Returns: An object with keys if successful. If `question_id` is 2, then

```
{
    "success": true,
    "id": 9
}
```

**POST "/questions"**

-   Returns questions based on a search term, if `searchTerm` is in the request body.

```
# Request body
{
    "searchTerm": "box"
}

# Response body
{
    "current_category": null,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer"s original name is Cassius Clay?"
        }
    ],
    "total_questions": 1
}
```

-   Adds a new question, otherwise.

```
# Request body
{
    "question": "How far is the mooon away from the earth?",
    "answer": "238,900 mi",
    "category": 3,
    "difficulty": 4
}

# Response body
{
    "success": true
}
```

**GET "/categories/<category_id>/questions"**

-   Fetches a list of questions for a given category_id
-   Request Arguments: category_id
-   Returns: An object with keys, `questions`, `current_category` and `total_questions`.

```
# response body if category_id is 2,
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "total_questions": 1
}
```

**POST "/quizzes"**

-   Fetches questions to play the quiz.
-   Request body contains `quiz_category`, `previous_questions`.
-   Returns: A random questions within the given category,
    if provided, and that is not one of the previous questions.

```
# request body
{
    "previous_questions": [],
    "quiz_category": {
        "type": "History",
        "id": "4"
    }
}

# response body
{
    "question":{
        "id": 5,
        "question": "Whose autobiography is entitled "I Know Why the Caged Bird Sings"?",
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2
    }
}
```
