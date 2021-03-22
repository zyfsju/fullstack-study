from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost:5432/example"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    person = Person.query.first()
    return f"Hello {person.name}"


# By inheriting from db.Model, we map from our classes to tables via SQLAlchemy ORM
class Person(db.Model):
    # By default, SQLAlchemy will pick the name of the table for you,
    # setting it equal to the lower-case version of your class's name
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    # db.Column takes <datatype>, <primary_key?>, <constraint?>, <default?>
    name = db.Column(db.String(), nullable=False)

    # Python __repr__() function returns the object representation.
    # It could be any valid python expression such as tuple, dictionary, string etc.
    # This method is called when repr() function is invoked on the object,
    # in that case, __repr__() function must return a String otherwise error will be thrown.
    def __repr__(self):
        return f"<Person ID: {self.id}, name: {self.name}>"


db.create_all()

# FLASK_APP=flask_hello_app.py flask run
# optional FLASK_DEBUG=true
if __name__ == "__main__":
    app.run(debug=True)

# Interactive
# $ python3
# >>> from flask_hello_app import Person, db
# >>> Person.query.all()
# >>> Person.query.first()
# >>> query = Person.query.filter(Person.name == 'Amy')
# >>> query.first()
# >>> query.all()
