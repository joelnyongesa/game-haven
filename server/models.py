from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin



db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__="users"

    serialize_rules = ("-game_entries", "-game_reviews",)

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    # _password_hash = db.Column(db.String())

    game_entries = db.relationship('GameEntry', backref="user" )
    game_reviews = db.relationship('GameReview', backref="user" )

    def __repr__(self):
        return f'<User: {self.username}>'



class GameEntry(db.Model, SerializerMixin):
    __tablename__="game_entries"

    serialize_rules = ("-genres", "-game_reviews", "-user.game_entries",)

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    platform = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(100))

    user_id = db.Column(db.Integer(), db. ForeignKey('users.id'))
    # genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

    genres = db.relationship('GameGenre', backref='game_entry')
    game_reviews = db.relationship('GameReview', backref='game_entry')

    def __repr__(self):
        return f'Game: {self.title}, Platform: {self.platform}'


class GameReview(db.Model, SerializerMixin):
    __tablename__='game_reviews'

    serialize_rules = ("-user", "-game_entry",)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer())
    comment = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    game_entry_id = db.Column(db.Integer(), db.ForeignKey('game_entries.id'))

    def __repr__(self):
        return f'<Review: \n Score: {self.rating}, Comment: {self.comment}>'




class Genre(db.Model, SerializerMixin):
    __tablename__="genres"

    serialize_rules = ("-game_entries",)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, nullable=False)

    game_entries = db.relationship('GameGenre', backref='genre')

    def __repr__(self):
        return f'<Genre: {self.name}>'



class GameGenre(db.Model, SerializerMixin):
    __tablename__ = "game_genres"

    serialize_rules = ("-game_entry", "-genre",)

    id=db.Column(db.Integer, primary_key=True)
    game_entry_id = db.Column(db.Integer(), db.ForeignKey('game_entries.id'))
    genre_id = db.Column(db.Integer(), db.ForeignKey('genres.id'))