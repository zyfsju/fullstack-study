# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm as Form
from forms import *
from datetime import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# class Venue(db.Model):
#     __tablename__ = "Venue"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


# class Artist(db.Model):
#     __tablename__ = "Artist"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    # artists = db.relationship(
    #     "Artist",
    #     secondary="Show",
    #     backref=db.backref("venues", lazy=True),
    #     cascade_backrefs=False,
    # )

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Artist {self.id} {self.name}>"


class Show(db.Model):
    __tablename__ = "Show"

    venue_id = db.Column(
        "venue_id", db.Integer, db.ForeignKey("Venue.id"), primary_key=True
    )
    artist_id = db.Column(
        "artist_id", db.Integer, db.ForeignKey("Artist.id"), primary_key=True
    )
    start_time = db.Column(db.DateTime, primary_key=True)
    venue = db.relationship("Venue", foreign_keys="Show.venue_id", backref="shows")
    artist = db.relationship("Artist", foreign_keys="Show.artist_id", backref="shows")

    def __repr__(self):
        return f"<Show {self.venue_id} {self.artist_id} {self.start_time}>"


def sa_obj_to_dict(sa_obj):

    return {c.name: getattr(sa_obj, c.name) for c in sa_obj.__class__.__table__.columns}


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    if not isinstance(value, str):
        value = value.strftime("%m/%d/%Y, %H:%M:%S")
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # data_0 = [
    #     {
    #         "city": "San Francisco",
    #         "state": "CA",
    #         "venues": [
    #             {"id": 1, "name": "The Musical Hop", "num_upcoming_shows": 0,},
    #             {
    #                 "id": 3,
    #                 "name": "Park Square Live Music & Coffee",
    #                 "num_upcoming_shows": 1,
    #             },
    #         ],
    #     },
    #     {
    #         "city": "New York",
    #         "state": "NY",
    #         "venues": [
    #             {"id": 2, "name": "The Dueling Pianos Bar", "num_upcoming_shows": 0,}
    #         ],
    #     },
    # ]
    data = []
    venues = Venue.query.all()
    for city, state in list(set((v.city, v.state) for v in venues)):
        row = {
            "city": city,
            "state": state,
            "venues": [
                {
                    "id": v.id,
                    "name": v.name,
                    # "num_upcoming_shows": len(
                    #     set(
                    #         show.artist_id
                    #         for show in v.shows
                    #         if show.start_time > datetime.now()
                    #     )
                    # ),
                }
                for v in venues
                if v.city == city and v.state == state
            ],
        }
        data.append(row)
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    # response = {
    #     "count": 1,
    #     "data": [{"id": 2, "name": "The Dueling Pianos Bar", "num_upcoming_shows": 0,}],
    # }
    search_term = request.form.get("search_term", "")
    venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    data = [{"id": v.id, "name": v.name} for v in venues]
    response = {"count": len(data), "data": data}
    return render_template(
        "pages/search_venues.html", results=response, search_term=search_term,
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "past_shows": [
    #         {
    #             "artist_id": 4,
    #             "artist_name": "Guns N Petals",
    #             "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #             "start_time": "2019-05-21T21:30:00.000Z",
    #         }
    #     ],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "genres": ["Classical", "R&B", "Hip-Hop"],
    #     "address": "335 Delancey Street",
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "914-003-1132",
    #     "website": "https://www.theduelingpianos.com",
    #     "facebook_link": "https://www.facebook.com/theduelingpianos",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #     "address": "34 Whiskey Moore Ave",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "415-000-1234",
    #     "website": "https://www.parksquarelivemusicandcoffee.com",
    #     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "past_shows": [
    #         {
    #             "artist_id": 5,
    #             "artist_name": "Matt Quevedo",
    #             "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #             "start_time": "2019-06-15T23:00:00.000Z",
    #         }
    #     ],
    #     "upcoming_shows": [
    #         {
    #             "artist_id": 6,
    #             "artist_name": "The Wild Sax Band",
    #             "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #             "start_time": "2035-04-01T20:00:00.000Z",
    #         },
    #         {
    #             "artist_id": 6,
    #             "artist_name": "The Wild Sax Band",
    #             "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #             "start_time": "2035-04-08T20:00:00.000Z",
    #         },
    #         {
    #             "artist_id": 6,
    #             "artist_name": "The Wild Sax Band",
    #             "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #             "start_time": "2035-04-15T20:00:00.000Z",
    #         },
    #     ],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 1,
    # }

    venue = Venue.query.filter_by(id=venue_id).first()
    if not venue:
        return not_found_error("error")
    shows = [
        {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time,
        }
        for show in venue.shows
    ]
    past_shows = list(filter(lambda x: x.get("start_time") < datetime.now(), shows))
    upcoming_shows = list(
        filter(lambda x: x.get("start_time") >= datetime.now(), shows)
    )
    # print(past_shows)
    data = {
        # **{x.name: getattr(venue, x.name) for x in Venue.__table__.columns},
        **sa_obj_to_dict(venue),
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(set(x.get("artist_id") for x in past_shows)),
        "upcoming_shows_count": len(set(x.get("artist_id") for x in upcoming_shows)),
    }

    # data = list(filter(lambda d: d["id"] == venue_id, [data1, data2, data3]))[0]
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    data = request.form or {}
    kwargs = {k: v for k, v in data.items() if k in Venue.__table__.columns}
    kwargs.update(
        {"genres": data.getlist("genres"), "seeking_talent": True if "y" else False}
    )
    existed = (
        Venue.query.filter_by(name=kwargs.get("name"))
        .filter_by(city=kwargs.get("city"))
        .filter_by(state=kwargs.get("state"))
        .first()
    )
    if existed:
        flash("Venue " + data.get("name") + " is already listed.")
    else:
        try:
            new_venue = Venue(**kwargs)
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash("Venue " + data.get("name") + " was successfully listed!")
        except Exception as e:
            db.session.rollback()
            raise e
            flash(
                "An error occurred. Venue " + data.get("name") + " could not be listed."
            )
        finally:
            db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash("Venue " + venue.name + " was successfully deleted.")
    except:
        db.session.rollback()
        flash("An error occurred. Venue " + venue.name + " could not be deleted.")
    finally:
        db.session.close()

    return render_template("pages/home.html")


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    # data = [
    #     {"id": 4, "name": "Guns N Petals",},
    #     {"id": 5, "name": "Matt Quevedo",},
    #     {"id": 6, "name": "The Wild Sax Band",},
    # ]

    artists = Artist.query.all()
    data = [{"id": a.id, "name": a.name} for a in artists]
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # response = {
    #     "count": 1,
    #     "data": [{"id": 4, "name": "Guns N Petals", "num_upcoming_shows": 0,}],
    # }
    search_term = request.form.get("search_term", "")
    artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    data = [{"id": a.id, "name": a.name} for a in artists]
    response = {"count": len(data), "data": data}
    return render_template(
        "pages/search_artists.html", results=response, search_term=search_term,
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [
    #         {
    #             "venue_id": 1,
    #             "venue_name": "The Musical Hop",
    #             "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #             "start_time": "2019-05-21T21:30:00.000Z",
    #         }
    #     ],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    #     "genres": ["Jazz"],
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "300-400-5000",
    #     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "past_shows": [
    #         {
    #             "venue_id": 3,
    #             "venue_name": "Park Square Live Music & Coffee",
    #             "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #             "start_time": "2019-06-15T23:00:00.000Z",
    #         }
    #     ],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    #     "genres": ["Jazz", "Classical"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "432-325-5432",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [
    #         {
    #             "venue_id": 3,
    #             "venue_name": "Park Square Live Music & Coffee",
    #             "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #             "start_time": "2035-04-01T20:00:00.000Z",
    #         },
    #         {
    #             "venue_id": 3,
    #             "venue_name": "Park Square Live Music & Coffee",
    #             "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #             "start_time": "2035-04-08T20:00:00.000Z",
    #         },
    #         {
    #             "venue_id": 3,
    #             "venue_name": "Park Square Live Music & Coffee",
    #             "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #             "start_time": "2035-04-15T20:00:00.000Z",
    #         },
    #     ],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d["id"] == artist_id, [data1, data2, data3]))[0]
    artist = Artist.query.get(artist_id)
    if not artist:
        return not_found_error("error")
    shows = [
        {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time,
        }
        for show in artist.shows
    ]
    past_shows = list(filter(lambda x: x.get("start_time") < datetime.now(), shows))
    upcoming_shows = list(
        filter(lambda x: x.get("start_time") >= datetime.now(), shows)
    )
    # print(past_shows)
    data = {
        # **{x.name: getattr(venue, x.name) for x in Venue.__table__.columns},
        **sa_obj_to_dict(artist),
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(set(x.get("venue_id") for x in past_shows)),
        "upcoming_shows_count": len(set(x.get("venue_id") for x in upcoming_shows)),
    }
    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    # }
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)
    if not artist:
        return not_found_error("error")
    artist = sa_obj_to_dict(artist)
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    artist = Artist.query.get(artist_id)
    if not artist:
        return not_found_error("error")
    artist_name = artist.name
    data = request.form or {}
    try:
        kwargs = {k: v for k, v in data.items() if k in Artist.__table__.columns}
        kwargs.update({"genres": data.getlist("genres")})
        db.session.query(Artist).filter(Artist.id == artist_id).update(
            kwargs, synchronize_session=False
        )
        db.session.commit()
        # on successful db insert, flash success
        flash("Artist " + data.get("name") + " was successfully updated!")
    except Exception as e:
        db.session.rollback()
        raise e
        flash("An error occurred. Artist " + artist_name + " could not be updated.")
    finally:
        db.session.close()
    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    # venue = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    # }
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    if not venue:
        return not_found_error("error")
    venue = sa_obj_to_dict(venue)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    if not venue:
        return not_found_error("error")
    venue_name = venue.name
    data = request.form or {}
    try:
        kwargs = {k: v for k, v in data.items() if k in Venue.__table__.columns}
        kwargs.update({"genres": data.getlist("genres")})
        db.session.query(Venue).filter(Venue.id == venue_id).update(
            kwargs, synchronize_session=False
        )
        db.session.commit()
        # on successful db insert, flash success
        flash("Venue " + data.get("name") + " was successfully updated!")
    except Exception as e:
        db.session.rollback()
        raise e
        flash("An error occurred. Venue " + venue_name + " could not be updated.")
    finally:
        db.session.close()
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    data = request.form or {}
    kwargs = {k: v for k, v in data.items() if k in Artist.__table__.columns}
    kwargs.update(
        {
            "genres": data.getlist("genres"),
            "seeking_venue": True if data.get("seeking_venue") == "y" else False,
        }
    )
    existed = (
        Artist.query.filter_by(name=kwargs.get("name"))
        .filter_by(city=kwargs.get("city"))
        .filter_by(state=kwargs.get("state"))
        # .filter_by(phone=kwargs.get("phone"))
        # .filter_by(phone=kwargs.get("website"))
        .first()
    )
    if existed:
        flash("Venue " + data.get("name") + " is already listed.")
    try:
        new_artist = Artist(**kwargs)
        db.session.add(new_artist)
        db.session.commit()
        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully listed!")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred. Artist " + data.get("name") + " could not be listed.")
    finally:
        db.session.close()
    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # data = [
    #     {
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "artist_id": 4,
    #         "artist_name": "Guns N Petals",
    #         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #         "start_time": "2019-05-21T21:30:00.000Z",
    #     },
    #     {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "artist_id": 5,
    #         "artist_name": "Matt Quevedo",
    #         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z",
    #     },
    #     {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z",
    #     },
    #     {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z",
    #     },
    #     {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z",
    #     },
    # ]
    shows = Show.query.all()
    data = [
        {
            **sa_obj_to_dict(sh),
            "venue_name": sh.venue.name,
            "artist_name": sh.artist.name,
            "artist_image_link": sh.artist.image_link,
        }
        for sh in shows
    ]
    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    data = request.form or {}
    try:
        kwargs = {k: v for k, v in data.items() if k in Show.__table__.columns}
        new_show = Show(**kwargs)
        db.session.add(new_show)
        db.session.commit()
        # on successful db insert, flash success
        flash("Show was successfully listed!")
    except:
        db.session.rollback()
        flash("An error occurred. Show could not be listed.")
    finally:
        db.session.close()
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
