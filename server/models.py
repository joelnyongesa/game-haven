from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullablle=False, unique=True)
    _password_hash = db.Column(db.String())

    game_entries = db.relationship('GameEntry', backref="user" )
    game_reviews = db.relationship('GameEntry', backref="review" )

    def __repr__(self):
        return f'<User: {self.username}>'



class GameEntry(db.Model):
    __tablename__="game_entries"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    platform = db.Column(db.String(), nullablle=False)
    description = db.Colum(db.String(100))
    user_id = db.Column(db.Integer(), db. ForeignKey('users.id'))

    genres = db.relationship('Genre', secondary='game_genre', back_populates ='games')

    def __repr__(self):
        return f'Game: {self.title}, Platform: {self.platform}'


class GameReview(db.Model):
    __tablename__='game_reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer())
    comment = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    game_entry_id = db.Column(db.Integer(), db.ForeignKey('game_entries.id'))

    def __repr__(self):
        return




class Genre(db.Model):
    __tablename__="genres"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String, nullable=False)

    games = db.relationship('GameEntry', secondary='game_genre', back_populates='genres')

    def __repr__(self):
        return f'Genre: {self.name}'



class GameGenre(db.Model):
    __tablename__ = "game_genre"
    game_entry_id = db.Column(db.Integer(), db.ForeignKey('game_entries.id'), primary_key=True)
    genre_id = db.Column(db.Integer(), db.ForeignKey('genres.id'), primary_key=True)