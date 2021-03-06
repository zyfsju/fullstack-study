# Project - Coffee Shop Full Stack

The application manages the drink menu for a coffee shop. It can:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

### Backend

Flask server + SQLAlchemy + SQLite

#### Start Server

`cd` into the `backend` directory, create a virtual environment and install dependencies:

```bash
cd backend
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To run the development server,

```bash
FLASK_APP=api.py flask run --reload
```

#### Run Tests

Import the collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json` in Postman and send requests.

### Frontend

Angular + Ionic

`cd` into the `frontend` directory and install dependencies by running

```bash
cd frontend
npm install
```

To run the development server, and run:

```bash
ionic serve
```
