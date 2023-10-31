from faker import Faker
import random
from random import choice as rc
from app import app
from models import db, User, GameEntry, GameGenre, GameReview, Genre

fake = Faker()

with app.app_context():
    # Begin with deleting existing data
    User.query.delete()
    GameEntry.query.delete()
    GameGenre.query.delete()
    GameReview.query.delete()
    Genre.query.delete()


    users = []

    for _ in range(20):
        user = User(
            username=fake.user_name(),
            email = fake.email()
        )
        users.append(user)

    db.session.add_all(users)

    # Genres
    game_genres = [
        "Action RPG",
        "Social Deduction",
        "Life Simulation",
        "Battle Royale",
        "Sandbox",
        "First-Person Shooter",
        "Augmented Reality",
        "Action-Adventure",
        "Open World",
        "Multiplayer Online Battle Arena (MOBA)"
    ]

    genres = []

    for _ in range(10):
        genre = Genre(
            name=rc(game_genres)
        )
        genres.append(genre)

    db.session.add_all(genres)


    # List of 10 game titles
    game_titles = [
        "The Witcher 3: Wild Hunt", 
        "Among Us",
        "Animal Crossing: New Horizons",
        "Fortnite",
        "Minecraft",
        "Call of Duty: Warzone",
        "Pokémon Go",
        "Grand Theft Auto V",
        "Cyberpunk 2077",
        "League of Legends"
    ]

    # List of corresponding platforms
    game_platforms = [
        "Mobile", "Desktop","PlayStation","Nintendo Switch",
        ]
    
    game_entries = []
    
    for _ in range(20):
        game_entry = GameEntry(
            title=rc(game_titles),
            platform=rc(game_platforms),
            description=fake.sentence(15),
            user=rc(users),
            # genre=rc(genres)
        )

        game_entries.append(game_entry)

    db.session.add_all(game_entries)

    game_reviews = []

    for _ in range(20):
        random_user = rc(users)
        random_game_entry = rc(game_entries)
        
        game_review = GameReview(
            rating = random.randint(0,10),
            comment=fake.sentence(),
            user=rc(users),
            game_entry=rc(game_entries)
        )

        game_reviews.append(game_review)

    db.session.add_all(game_reviews)

    game_genres = []

    for _ in range(20):
        game_genre = GameGenre(
            game_entry=rc(game_entries),
            genre=rc(genres)
        )
        game_genres.append(game_genre)

    db.session.add_all(game_genres)
    db.session.commit()