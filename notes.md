### postgres in docker

```yaml
# docker-compose.yml
version: "3"
services:
  database:
    image: "postgres" # use latest official postgres version
    env_file:
      - database.env # configure postgres
    volumes:
      - database-data:/var/lib/postgresql/data/ # persist data even if container shuts down
volumes:
  database-data: # named volumes can be managed easier using docker-compose
```

```bash
# database.env
POSTGRES_USER=unicorn_user
POSTGRES_PASSWORD=magical_password
POSTGRES_DB=rainbow_database
```

To tell Docker-Compose to destroy the volume and its data, you need to issue `docker-compose down --volumes`

If we used the following configuration:

```yaml
# docker-compose.yml
services:
  database:
    ...
    volumes:
      - ./host-folder/:/var/lib/postgresql/data/
```

The data will be stored on the host computer. To delete this data and start a fresh new database, you will have to manually remove the data files from the host computer with something like `rm -rf ./host-folder/`.

### Start the Database

Run `docker-compose` up to bring up the database.

we will drop into the database container and use the psql client software that is already installed in the database container.

### Connect to DB

```bash
$ docker-compose run database bash # drop into the container shell
database# psql --host=database --username=unicorn_user --dbname=rainbow_database
Password for user unicorn_user:
psql (12.0 (Debian 12.0-2.pgdg100+1))
Type "help" for help.
rainbow_database=#
```

### Create a Table

```bash
rainbow_database=# \d # verify table does already not exist
Did not find any relations.
rainbow_database=# CREATE TABLE color_table(name TEXT);
CREATE TABLE
rainbow_database=# \d # verify table is created
              List of relations
 Schema |    Name     | Type  |    Owner
--------+-------------+-------+--------------
 public | color_table | table | unicorn_user
(1 row)
```

### Add and Read Data

```bash
rainbow_database=# SELECT * FROM color_table; -- verify record does not already exist
 name
------
(0 rows)
rainbow_database=# INSERT INTO color_table VALUES ('pink'); -- be sure to use single quotes
INSERT 0 1
rainbow_database=# SELECT * FROM color_table; -- verify record is created
 name
------
 pink
(1 row)
```

# L1

postgreSQL:

- postgres starts/stops the server.
- pg_ctl wraps postgres
- psql is the command-line client, that connects to the server and allows you to execute individual

## Database Management System (DBMS).

key characteristics of databases:

1. persistence
2. shared source of truth
3. ability to efficiently store many types of data
4. concurrency control

relational db:

1. All data is stored in tables
2. Every column has a data type
3. It provides constraints and triggers to enforce data integrity

The execution plan gives important insight into the performance of the query.

hash join: expensive, creates a hash in-memory that hashes based the driver_id column.

seq scan(Sequential Scan): most basic operation,

Relational Database Clients: A database client is any program that sends requests to a database. In some cases, the database client is a web server!

Ports allow multiple types of traffic being received at the same time on a given device, to be tracked and routed to where they need to go.

port 5432 -> database traffic, port 80 -> http(web traffic)

1. TCP/IP is connection-based, meaning all communications between parties are arranged over a connection. A connection is established before any data transmission begins.
2. Over TCP/IP, we'll always need to establish a connection between clients and servers in order to enable communications. Moreover:
   - Deliveries over the connection are error-checked: if packets arrive damaged or lost, then they are resent (known as retransmission).
     Connecting starts a session. Ending the connection ends the session.
3. In a database session, many transactions can occur during a given **session**. Each **transaction** does work to commit changes to the database (updating, inserting, or deleting records).

transaction:

1. captures a single change or multiple changes.
2. A transaction either succeeds altogether, or fails altogether as a single unit. A transaction bundles multiple pieces of work into a single unit.
3. Transactions capture operations that change a database's data: this means updates, inserts, and deletions of data. (UPDATE, INSERT, DELETE). Transactions are not concerned with querying (SELECT, GROUP BY) or changes to the data schema (ALTER TABLE).
4. Changes to the database must be committed to the database by executing a commit to the transaction, after changes are queued into the transaction by adding to it.
5. One can clear the queue of operations added to a transaction by doing a rollback.

## Database Application Programming Interfaces (DBAPIs)

## psycopg2: database adapter that allows us to interact with a Postgres database from Python.

## SQLAlchemy

Layers of SQLAlchemy

1. DBAPI
2. The Dialect
3. The Connection Pool
4. The Engine
5. SQL Expressions
6. SQLAlchemy ORM (optional)

connection pool

1. Handles dropped connections
2. Avoids doing very many small calls to the DB
3. Avoids opening and closing connections for every data change

The Engine

1. 1 of 3 main layers for how you may choose to interact with the database.
2. Is the lowest level layer of interacting with the database, and is much like using the DBAPI directly. Very similar to using psycopg2, managing a connection directly.
3. Moreover, the Engine in SQLAlchemy refers to both itself, the Dialect and the Connection Pool, which all work together to interface with our database.
   A connection pool gets automatically created when we create a SQLAlchemy engine.

### SQLAlchemy ORM

- db.Model.query offers us the Query object
- Query has method chaining. until you chain it with a terminal method that returns a non-query object like count(), all(), first(), delete(), etc.
- MyModel.query directly on the model, or db.session.query(MyModel) using db.session.query instead.

### Object Lifecycle:

- Within a session, we create transactions every time we want to commit work to the database.
- Transient: an object exists, it was defined. but not attached to a session (yet). `user1 = User(name='Amy')`
- Pending: an object was attached to a session. "Undo" becomes available via db.session.rollback(), which will make the object `transient` again. Waits for a flush to happen
- Flushed: about ready to be committed to the database, translating actions into SQL command statements for the engine. It occurs: when you call Query. Or on db.session.commit(). When a statement has been flushed already, SQLAlchemy knows not to do the work again of translating actions to SQL statements.
- Committed: manually called for a change to persist to the database (permanently); session's transaction is cleared for a new set of changes. A commit leads to persisted changes on the database + lets the db.session start with a new transaction.

### Model View Controller (MVC)

common pattern for architecting web applications -> isolate concerns, help debugging

- Models manage data and business logic for us. What happens inside models and database, capturing logical relationships and properties across the web app objects
- Views handles display and representation logic. What the user sees (HTML, CSS, JS from the user's perspective)
- Controllers: routes commands to the models and views, containing control logic. Control how commands are sent to models and views, and how models and views wound up interacting with each other.

Example:
index() function is the controller, telling the model to do a select statement on the to-do table in the database and the view to use index.html to show the data.

How we'd add Create To-Do item functionality:

- On the view: implement an HTML form
- On the controller: retrieve the user's input, and manipulate models
- On the models: create a record in our database, and return the newly created to-do item to the controller
- On the controller: take the newly created to-do item, and decide how to update the view with it.

### Getting User Data in Flask

There are 3 methods of getting user data from a view to a controller.

- URL query parameters: using a traditional html form with `action` (route name) and `method` (`get` request) attributes. request.args.get('my_key', '<default_value>'), listed as key-value pairs at the end of a URL, preceding a "?" question mark. E.g. `www.example.com/hello?my_key=my_value`.
- Forms: `post` request with request body "field1=value1&field2=value2". request.form.get('<name>') reads the value from a form input control (text input, number input, password input, etc) by the `name` attribute on the input HTML element.
- application/json: request.data retrieves JSON as a string. Then json.loads.

### Using AJAX to send data to flask

- Data request are either synchronous or async (asynchronous)
- Async data requests are requests that get sent to the server and back to the client without a page refresh.
- Async requests (AJAX requests) use one of two methods:

  - XMLHttpRequest
  - Fetch (modern way)

## Migrations

- Migrations deal with how we manage modifications to our data schema, over time.
- Mistakes to our database schema are very expensive to make. The entire app can go down, so we want to
  - quickly roll back changes, and
  - test changes before we make them
- A migration is a file that keep track of changes to our database schema (structure of our database). Offers version control on our schema. git commit --> applying a migration (a schema upgrade)
- Migrations stack together in order to form the latest version of our database schema.
- We can upgrade our database schema by applying migrations
- We can roll back our database schema to a former version by reverting migrations that we applied

###

- flask_migrate: uses Alembic under the hood
- flask-script: lets us run the migration scripts we defined from the terminal

```bash
flask db init # create initial migrations directory structure
flask db migrate # detects model changes to make, creates a migration file with upgrade and downgrade logic set up
flask db upgrade # apply the migration
flask db downgrade # roll back
```

To stop and start postgres server using pg_ctl

```bash
pg_ctl -D /usr/local/var/postgres stop
pg_ctl -D /usr/local/var/postgres start
```

### Working with Existing Data

Add a new column: update existing records that don't have this column, using op.execute to assign default value, and then alter_column nullable=False

### Recap

Overall Steps to Set Up & Run Migrations

- Bootstrap database migrate commands: link to the Flask app models and database, link to command line scripts for running migrations, set up folders to store migrations (as versions of the database)
- Run initial migration to create tables for SQLAlchemy models, recording the initial schema: ala git init && first git commit. Replaces use of db.create_all()
- Migrate on changes to our data models
  - Make changes to the SQLAlchemy models
  - Allow Flask-Migrate to auto-generate a migration script based on the changes
  - Fine-tune the migration scripts
  - Run the migration, aka “upgrade” the database schema by a “version”

## Build a CRUD App - Part 2

### db.relationship

- Allows SQLAlchemy to identity relationships between models
- Links relationships with backrefs (child1.some_parent)
- Configures relationship dynamics between parents and children, including options like lazy, collection_class, and cascade

```python
class SomeParent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("SomeChild", backref="some_parent")

child1 = SomeChild(name="Andrew")
child1.some_parent # <-- Name of the backref, returns the parent object that child1 object belongs to
```

- db.relationship does not set up foreign key constraints for you. We need to add a column, some_parent_id, on the child model that has a foreign key constraint
- Whereas we set db.relationship on the parent model, we set the foreign key constraint on the child model.
- A foreign key constraint preserves referential integrity from one table to another, by ensuring that the foreign key column always maps a primary key in the foreign table.

db.ForeignKey passing in a string '<tablename>.<primary key name>'

### Many-To-Many Relationships

```python
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
```

# L2

## Intro to APIs

- Transmission Control Protocol (TCP) which is used for data transmission
- Hypertext Transmission Protocol (HTTP) which is used for transmitting text and hyperlinks
- File Transfer Protocol (FTP) which is used to transfer files between server and client

- Your API will handle HTTP requests and HTTP functions over TCP.

### How APIs Work

- Client sends a request to the API server
- The API server parses that request
- Assuming the request is formatted correctly, the server queries the database for the information or performs the action in the request
- The server formats the response and sends it back to the client
- The client renders the response according to its implementation

### RESTful APIs

Here's a short summary of the REST principles:

- Uniform Interface: Every rest architecture must have a standardized way of accessing and processing data resources. This include unique resource identifiers (i.e., unique URLs) and self-descriptive messages in the server response that describe how to process the representation (for instance JSON vs XML) of the data resource.
- Stateless: Every client request is self-contained in that the server doesn't need to store any application data in order to make subsequent requests
- Client-Server: There must be both a client and server in the architecture
- Cacheable & Layered System: Caching and layering increases networking efficiency

  Benefits:

- It doesn't expose the implementation to those who shouldn't have access to it
- The API provides a standard way of accessing the application
- It makes it much easier to understand how to access the application's data

Some frequently used APIs include:

- Google Maps API
- Stripe API: process payments
- Facebook API
- Instagram API
- Spotify API: application with music

## HTTP and Flask Basics

### HTTP Requests

HTTP requests are sent from the client to the server to initiate some operation. In addition to the URL, HTTP requests have other elements to specify the requested resource.

Elements:

- Method: Defines the operation to be performed
- Path: The URL of the resource to be fetched, excluding the scheme and host
- HTTP Version
- Headers: optional information, success as Accept-Language
- Body: optional information, usually for methods such as POST and PATCH, which contain the resource being sent to the server

### HTTP Responses

After the request has been received by the server and processed, the server returns an HTTP response message to the client. The response informs the client of the outcome of the requested operation.

Example:

```
HTTP/2.0 200 OK
Date: Fri, 21 June 2019 16:17:18 GMT
Content-Type: text/html
Accept-Ranges: bytes
Body: {'success': True}
```

Elements:

- Status Code & Status Message
- HTTP Version
- Headers: similar to the request headers, provides information about the response and resource representation. Some common headers include:
  - Date
  - Content-Type: the media type of the body of the request
- Body: optional data containing the requested resource

Status Codes:

As an API developer, it's important to send the correct status code. As a developer using an API, the status codes—particularly the error codes—are important for understanding what caused an error and how to proceed.

Codes fall into five categories:

- 1xx Informational: typically will be part of OPTION request
- 2xx Success
- 3xx Redirection
- 4xx Client Error
- 5xx Server Error

Common Status Code and Status Message:
200: OK
201: Created -> POST
304: Not Modified
400: Bad Request
401: Unauthorized
404: Not Found
405: Method Not Allowed
500: Internal Server Error

More can be found [here](https://httpstatusdogs.com/)

## Endpoints and Payloads

### Organizing API Endpoints

Principles:

- Should be intuitive
- Organize by resource:
  - Use nouns in the path, not verbs.
  - The method used will determine the operation taken
  - GOOD: https://example.com/posts
  - BAD: https://example.com/get_posts
- Keep a consistent scheme
  - Plural nouns for collections
  - Use parameters to specify a specific item
  - GOOD: https://example.com/entrees, https://example.com/entrees/5
  - BAD: https://example.com/entree, https://example.com/entree_five
- Don’t make them too complex or lengthy
  - No longer than collection/item/collection
  - GOOD: https://example.com/entrees/5/reviews
  - BAD: https://example.com/entrees/5/customers/4/reviews

`PATCH` is responsible for partial updates of a resource.

PUT and PATCH both update resource representations but `PUT` replaces the entire representation.

`POST` requests create new resources.

Q: Which endpoint is correctly formatted to complete operations on all movies of genre id 1?

A: Endpoints should be organized by resource and in the structure of `collection/item/collection`. `genres/1/movies` should access all movies related to genre 1.

Q: Which method—endpoint combination should you use to create a new movie of genre 1?

A: `POST genres/1/movies`

Q: Which of the following endpoint-method combinations would raise an error?

A: `POST /messages/1` You cannot POST to an endpoint to a single resource. That resource already exists, and POST creates an entirely new resource

### CORS

- Security and the Same-Origin Policy: allows scripts in Webpage 1 to access data from Webpage 2 only if they share the same domain
- Block requests from rogue JavaScript
- This means that the above error will be raised in the following cases:
  - Different domains
  - Different subdomains (example.com and api.example.com)
  - Different ports (example.com and example.com:1234)
  - Different protocols (http://example.com and https://example.com)

Why?

- Rogue or malicious scripts
- Ability to complete non-simple requests(beyond some basic headers)
  - preflight OPTIONS sent
  - No CORS, no request sent
- Protects you and your user

In order for the requests to be processed properly, CORS utilizes headers to specify what the server will allow:

- Access-Control-Allow-Origin: What client domains can access its resources. For any domain use \*. not hightly secure
- Access-Control-Allow-Credentials: Only if using cookies for authentication, in which case its value must be true
- Access-Control-Allow-Methods: List of HTTP request types allowed
- Access-Control-Allow-Headers: List of http request header values the server will allow, particularly useful if you use any custom headers

### Flask-CORS

```python
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
    return response
```

Initialization

```python
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app)
```

Resource-Specific Usage

```python
# keys are regular expressions and values are dictionary or kwargs
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Route-Specific Usage

```python
# enable CORS on a given route,
@app.route("/hello")
@cross_origin()
def get_greeting():
    return jsonify({'message':'Hello, World!'})
```

### Error Handling

abort(404) shows

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>
  The requested URL was not found on the server. If you entered the URL manually
  please check your spelling and try again.
</p>
```

we want to ensure all of our server responses have **consistent formatting** and that we provide **adequate information** to the client regarding the error. The `@app.errorhandler` decorator allows you to specify the behavior for expected errors. When using this decorator take into consideration:

- passing the status code or Python error as an argument to the decorator
- logical naming of the function handler
- consistent formatting and messaging of the JSON object response

### Flask Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404
```

Test-Driven Development (or TDD) is a software development paradigm used very commonly in production. It is based on a short, rapid development cycle in which tests are written before the executable code and constantly iterated on.

- Write test for specific application behavior.
- Run the tests and watch them fail.
- Write code to execute the required behavior.
- Test the code and rewrite as necessary to pass the test
- Refactor your code.
- Repeat - write your next test.

Often while pair programming, one partner will write the test and the other will write the executable code, after which the partner will switch. This process is helpful for checking assumptions about behavior and making sure all expected behavior is captured.

## API Documentation

### API Documentation

Here's a recap (for your reference) of the components that are typically included in good API documentation:

- Introduction
- Getting Started
  - Base URL
  - API Keys /Authentication (if applicable)
- Errors
  - Response codes
  - Messages
  - Error types
- Resource endpoint library
  - Organized by resource
  - Include each endpoint
  - Sample request
  - Arguments including data types
  - Response object including status codes and data types

### Project Documentation

- Project Title

  - Description of project and motivation
  - Screenshots (if applicable), with captions
  - Code Style if you are following particular style guides

- Getting Started

  - Prerequisites & Installation, including code samples for how to download all pre-requisites
  - Local Development, including how to set up the local development environment and run the project locally
  - Tests and how to run them

- API Reference. If the API documentation is not very long, it can be included in the README
- Deployment (if applicable)
- Authors
- Acknowledgements

# L3

project github: https://github.com/udacity/FSND

- Authentication systems - design, implementation, and use of third party services.
- Common vulnerabilities while working with passwords and how to avoid these pitfalls.
- Authorization systems - design and implementation for backend and frontend.
- Basic security best practices and key principles to keep in mind.

Questions: API Keys, authentication, authorization, OAuth, OpenID Connect, http

## Foundation

### Python Decorators

```python
from functools import wraps

# Our Basic Function Defn
def print_name(name):
    print(name)

print_name("jimmy")

# Let's add a simple decorator to inject a greeting
def add_greeting(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print("Hello!")
        return f(*args, **kwargs)
    return wrapper

@add_greeting
def print_name(name):
    print(name)


print_name("sandy")
# output:
# Hello!
# sandy

# Let's add some complexity in the form of a paramater
def add_greeting(greeting=''):
    def add_greeting_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(greeting)
            return f(*args, **kwargs)
        return wrapper
    return add_greeting_decorator

@add_greeting("what's up!")
def print_name(name):
    print(name)

print_name("kathy")
# output:
# what's up!
# kathy

# We can also pass information back to the wrapped method
def add_greeting(greeting=''):
    def add_greeting_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(greeting)
            return f(greeting, *args, **kwargs)
        return wrapper
    return add_greeting_decorator

@add_greeting("Yo!")
def print_name(greeting, name):
    print(greeting)
    print(name)


print_name("Abe")
# output:
# Yo!
# Yo!
# Abe
```

## Identity and Authentication

### Username and Passwords

Most common in Saas. POST/GET request, find the user in db.

Many issues come from user behavior:

- Users forget their passwords
- Users use simple passwords
- Users use common passwords
- Users repeat passwords
- Users share passwords

In contrast, some issues are within our control as developers:

- Passwords can be compromised
- Developers can incorrectly check: while implementing password checks. For example, comparing the string or the object that the string represents, could be a critical security vulnerability.
- Developers can cut corners

#### HTTP Status Codes

401 Unauthorized: cannot validate the identity. doesn't know who

403 Forbidden: The client does not have permission to access the resource. knows who is making the request.

### SSO (single sign-on)

3rd-party identity provider: google, facebook, etc

### MFA (multi-factor authentication)

- send the code to the device: SMS. Thwarted with malicious apps on android which used to be able to read SMS messages. Once this vulnerability was discovered, Google changed the permission system to access these messages. However, the adversaries found a new exploit, by reading the message in the notification bar.
- have the device generate the code that corresponds to a specific time, using decaying temporal algorithm: Google Auth App

### 3rd-party auth

Ofen in **Monolithic** services with many responsibilities, there are interdependencies that make it difficult to make changes to your code --> **technical debt**

**Auth Microservices**: split up responsibilities into smaller servers deployed across different areas of a stack. Self-contained, minimal interaction between them.

#### token

temporary credentials that allow front-end to remember who it is for subsequent requests

### Auth0

Auth0 Authorize Link
The complete documentation for the authorization code flow can be found in Auth0's Documentation. It may help to fill in the url in the textbox below before copying it into your browser:

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

Integrating Auth0 With Your Frontend

### JSON Web Tokens (JWTs)

stateless

sequence diagram for a 3rd party authentication flow:

- the user submits info from the frontend to auth service
- if the login attempt is successful, the auth service will return a successful result with a token.
- The token will be used in subsequent requests to send credentials to whatever service requests it, to verify the identity on that service.

Traditionally, servers validated authentication using a session table, including a session ID and the user ID pair, stored in db. On every request, the client provides that session ID to the user and the server will make a request to DB to see if the session ID is still valid.

But using a microservice architecture, we might have one or hundreds of services who need to maintain that state across entire systems. Hard to maintain and manage. latency, time involved to check the session. and session might change across different parts of the stack, and it take time for the change to propogate.

Statelessness solves the problem.

- When JWT's are sent to a front end and then to a server, that server only has to fetch a public key one time from the auth service. This authentication key will then be stored within the API server, allowing us to verify this JWT is valid and we can trust who it is.
- scaleable. multiple instances of the same service. JWT could be hitting any one of these servers within the stack. Since it's stateless, each of the services can be confident in the identity provided.

Q: What are some benefits of JWTs?

A: Stateless, Difficult to fake, popular and easily implemented across platforms, flexible

### JWT - Data structure

To ansewr the questions: who is making the request, if it is still valid

header.payload.signature
(base-64)(base-64)(HS256)

base-64 encoding is two-way transformation.

- Payload: user object. don't store sensitive data in payload.

### JWT - Validation

function(header, payload, SECRET) = signature

A secret is essentially a string that we store on our authentication service, and on this server that we'll be validating the JWT.

If the signature strings match, we can trust that the data within the JWT is authentic.

### Generating and Verifying JWTs

```python
import jwt
import base64
import json

payload = {'school':'udacity'}
algo = 'HS256' #HMAC-SHA 256
secret = 'learning'

encoded_jwt = jwt.encode(payload, secret, algorithm=algo)

## Q1
jwt_string = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiY2VudHJhbCBwYXJrIn0.H7sytXDEHK1fOyOYkII5aFfzEZqGIro0Erw_84jZuGc"
secret = "learning"
header, payload, signature = jwt_string.split(".")
decoded_header = json.loads(base64.b64decode(header))
decoded_payload = json.loads(base64.b64decode(payload+"=="))
jwt_string == jwt.encode(decoded_payload, secret, algorithm=decoded_header.get("alg")).decode()
```

### Validating Auth0 Tokens

We need the secret/key to verify the token. Auth0 uses a public private key pair, or asymmetric encription to sign these keys

### Local Storage

Local Storage is an implementation of a key-value store which is accessible through a javascript interface in most modern browsers.

It is a general purpose interface to store strings which will persist in memory from session to session.

It is designed for smaller strings and alternative opensource systems like localForage exist for large amounts of data.

- Domain specific
- Persistent from session to session
- Cross browser compatible

Cookies have the same above characteristics. Also

- Inaccessible to JS when HTTP only flag is turned on

**Security Considerations of Local Storage**

- XSS: inject script into the client code for our website which accesses all of the keys within local store and drops it into a malicious server

**Cross-Site Scripting Attacks**
Input Sanitation

Example:

Describe your favorite book:

```text
<script type="text/javascript">localStore.getItem("token");sendToMaliciousServer();</script>
```

1. Unsanitized and rendered user input strings

If malicious code, such as javascript, is saved in place of a valid string. In other words, this malicious text will be interpreted by the browser as code and executed on the client. Input Sanitation transforms characters like < to &lt; which will not be interpreted as code and print as text (<). This step should always be performed on the server to prevent someone from sending the malicious text directly to your server using curl or Postman.

2. Compromised 3rd Party Hosted Javascript
3. Software dependencies

- npm for JS
- pip for Python
- Brew for Mac
  Some care should be taken to ensure that these packages are compliant with your license and security policies and are monitored for security vulnerabilities.

**Concerns when storing JWTs in local store**

1. Never store sensitive info within JWT. The payload can easily be decoded. Change secret or public key should it compromised
2. JWT should expire frequently, automatically refreshes tokens

### Storing JWTs

```javascript
jwt = response.jwt;
localStorage.setItem("token", jwt);

// get the jwt
jwt = localStorage.getItem("token");
```

### Sending Tokens with Requests

Authorization Headers

"Bearer <token>": it's a bearer token

```python
# unpack the header in flask
if "Authorization" not in request.headers:
    abort(401)

auth_header = request.headers["Authorization"]
header_parts = auth_header.split()
# perform checks
if len(header_parts) != 2:
    abort(401)
elif header_parts[0] != "Bearer":
    abort(401)
```

### Recap

Q: Authentication Tokens (specifically JWTs) are used to:

A:

- Carry claims in the form of a verifiable payload
- Perform authentication on requests after login

## Passwords

### Problems with Plain Text

#### User Table Vulnerability: SQL Injection

- Validate inputs
- Sanitize inputs
- Use ORMs
- Use prepared or parameterized SQL statements
- Choose complex admin passwords for db
- Store backups as securely as production db

### Problems - Data Handling and Logging

**Serialization** is the process of transforming a data model into a more easily shared format. For example, this is commonly performed when sending information as a response from a server to the requesting client in the form of a JSON object.

**Logging Best Practices**

- Information that leaves an audit trail
  - Login Attempts (ids)
  - Login Sources
  - Requested Resources

What should we NOT log?

- Personally Identifiable Information
- Secrets
- Passwords

### Encryption

reversible

1. simple subsitution
2. polyalphabetic cipher

Plaintext Block --> Key/cipher + Algorithm --> Ciphertext Block

Feistel Block cipher

### Recap

- Data in Transit: Send only over HTTPS, TLS/SSL
- Storing Passwords: Salt and Hash Passwords before storing in db
- Password Checking on API: Code review to ensure not logging passwords

## Access and Authorization

### Role-Permission Based Access

Permissions are actions.

### Defining Roles in Auth0

### Using RBAC in Flask

```python
def check_permissions(permission, payload):
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True
```

## Thinking adversarialy

### Auth Validation Testing

Write some integration tests using Postman for the server we've been working on throughout the course.

- Load or clone the flask server, enter the virtual environment, and start the server
- Open Postman, make a few requests, and think about edge cases
- Add your tests in Postman and observe the test results
- Save your requests to a collection and run with the Postman collection runner
-

## Project

Reviews:

- As a future reference tip, I'd strongly suggest having a look at how to structure a Flask app that allows **scalability**. We can structure app into `modules`/`Flask blueprints` instead of writing all code in one file as such, which will make code hard to read and maintain when the application grows.
- Resources:
  - http://flask.pocoo.org/docs/0.12/patterns/packages/
  * https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
- If you want to build API endpoints with Flask, a scalable method is to use the `flask-restful` library:

https://flask-restful.readthedocs.io/en/latest/quickstart.html

- There's a generalized error response schema defined by IETF in RFC 7807 - Problem Details for HTTP APIs. Not everyone follows this standard in error response but it is roughly adopted by many large web frameworks such as DotNet, Spring, etc. It is a great reference for your future project! Here's an example from the document:

```text
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json
Content-Language: en

{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc",
  "balance": 30,
  "accounts": ["/account/12345",
                  "/account/67890"]
}
```

# L4

Virtual machines and containers:

- The application, its dependencies and its runtime environment are deployed as a unit.
- Application and dependencies bundled
- Dev and prod differences minimized
- Can be used to horizontally scale an application

Containers:

- Single app defines lifespan
- containers are faster to start and more lightweight than VMs due to their shared kernel.

|                       | Virtual Machines      | Containers        |
| --------------------- | --------------------- | ----------------- |
| OS                    | one host, many guests | one host          |
| management            | software hypervisor   | container manager |
| resource requirements | heavy                 | light             |
| speed                 | slower                | faster            |
| flexibility           | total                 | limited           |

## Deployment

### Kubernetes

- Cluster: A group of machines running Kubernetes
- Master: The system which controls a Kubernetes cluster. You will typically interact with the master when you communicate with a cluster. The master includes an api, scheduler, and management daemon.
- Nodes: The machines in a cluster. These can be virtual, physical, or a combination of both.
- Pods: A deployment of an application. This consists of a container, it’s storage resources, and a unique IP address. Pods are not persistent, and may be brought up and down by the master during scaling.
- Service: An abstraction for communicating with a set of pods
- Additionally, in order to have a persistent way to store data, volumes can be attached to pods.

### EKS: Kubernetes on AWS

- A managed Kubernetes service
- Control layer runs the master system
- Secure networks are set up automatically
- You only setup Nodes, Pods, and Services
- Multiple availability zones

### AWSCLI

## Project

The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready **Gunicorn** server when deploying the app.

Open a new shell and install jq, which is a package that helps to read or manipulate JSON processors.

```text
jq is a tool for processing JSON inputs, applying the
  given filter to its JSON text inputs and producing the
  filter's results as JSON on standard output.
  The simplest filter is ., which is the identity filter,
  copying jq's input to its output unmodified (except for
  formatting).
```

### Containerizing and Running Locally

1. Create a Dockerfile named Dockerfile in the app repo. Your Dockerfile should:

- Use the python:stretch image as a source image
- Set up an app directory for your code
- Install pip and needed Python packages from requirements.txt
- Define an entrypoint which will run the main app using the Gunicorn WSGI server. The Gunicorn should run with the arguments as follows: ["gunicorn", "-b", ":8080", "main:APP"].

2. Create a file named .env_file and save both JWT_SECRET and LOG_LEVEL into .env_file. These environment variables will run locally in your container. Here, we do not need the export command, just an equals sign:

```text
 JWT_SECRET='myjwtsecret'
 LOG_LEVEL=DEBUG
```

This .env_file is only for the purposes of running the container locally, you do not want to check it into github or other public repositories. You can prevent this by adding it to your .gitignore file, which will cause git to ignore it. To safely store and use secrets in the cloud, use a secure solution such as AWS’s parameter store.

3. Build a local Docker image with the tag jwt-api-test

```bash
docker build -t "jwt-api-test" .
docker image ls
```

If required, you can delete an image using `docker image rm -f <image_name>``

4. Create and run a Container using the image locally:
   You can pass the name of the env file using the flag `--env-file=<YOUR_ENV_FILENAME>`.
   You should expose the port 8080 of the container to the port 80 on your host machine.

```bash
docker run --env-file=.env_file -p 80:8080 jwt-api-test
docker container ls
```

If required, you can stop a container using `docker stop [OPTIONS] CONTAINER [CONTAINER...]` or delete a container using `docker rm [OPTIONS] CONTAINER [CONTAINER...]`

5. To use the endpoints, you can use the same curl commands as before, except using port 80 this time:

- To try the /auth endpoint, use the following command:

```bash
export TOKEN=`curl -d '{"email":"<EMAIL>","password":"<PASSWORD>"}' -H "Content-Type: application/json" -X POST localhost:80/auth  | jq -r '.token'`
```

- To try the /contents endpoint which decrypts the token and returns its content, run:

```bash
curl --request GET 'http://127.0.0.1:80/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
```

You should see the email that you passed in as one of the values.

TRUST="{ \"Version\": \"2012-10-17\", \"Statement\": [ { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::<ACCOUNT_ID>:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"

ace3cc96fb62c902bc8876bf4b2bed906acf3f66

external IP: af560aafd4c834ad6aab012666c99c67-374629712.us-west-2.elb.amazonaws.com
af560aafd4c834ad6aab012666c99c67-374629712.us-west-2.elb.amazonaws.com

# Capstone

## Auth0 React SDK

`Auth0Provider` component provides `Auth0Context` (React Context) to its child components. It needs to have access to the session history of the app, so that it can take the user back to the route where they want to go after a successful log in attempt. Use React Router's `useHistory()` hook to access the session history through a `history` object. Consequently, we need to wrap `Auth0Provider` with `BrowswerRouter`, which uses a `RouterContext.Provider` component to maintain the routing state.
