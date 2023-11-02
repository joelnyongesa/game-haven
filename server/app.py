from flask import Flask, make_response,jsonify,request,session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, User, GameEntry, GameGenre, Genre, GameReview


app = Flask(__name__)

app.config['SECRET_KEY'] ="sdfghjl"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gamehave.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

CORS(app)

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)

@app.before_request
def check_if_logged_in():
    allowed_endpoints=['users','games','signup', 'login','logout','session']
    if not session.get('person_id') and request.endpoint not in allowed_endpoints:
            return {"error":"first login"}


class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        response = make_response(
            jsonify(users),
            200
        )

        return response
    
    def post(self):
        username = request.get_json()['username']
        email = request.get_json()['email']

        new_user = User(
            username=username,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        response = make_response(
            jsonify(new_user.to_dict()),
            201
        )

        return response

api.add_resource(Users, '/users', endpoint='users')

class Signup(Resource):
    def post(self):
        username = request.get_json()["username"]
        email = request.get_json()["email"]
        password =request.get_json()["password"]
        confirm_password = request.get_json()["confirm_password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already exists in the database"}
        
        if password != confirm_password:
            return {"error": "Passwords do not match"}

        new_user = User(username=username, email=email)
        new_user.password_hash = password  

        
        db.session.add(new_user)
        db.session.commit()
        return{"message": "User created successfully", "status":201}

api.add_resource(Signup, "/signup")


class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json().get('password')

        user = User.query.filter(User.username == username).first()  

        if user:
            
            if user.authenticate(password):
                session['person_id'] = user.id
                user_dict = user.to_dict()
                response_body = {"message": "logged in successfully","status": 201}
                return response_body
            else:
                return {"error": "password incorrect"}
        else:
            return {"error": "username not found"} 



api.add_resource(Login,'/login',endpoint='login')


class CheckSession(Resource):
    def get(self):
        if session['person_id']:
            return {"message": "user in session"}
        else:
            return {"error": "user not in session:please signin/login"}

api.add_resource(CheckSession,'/session',endpoint='session' )

    

class Logout(Resource):
    def delete(self):
        if session.get('person_id'):
            session['person_id']=None
            return {"message": "User logged out successfully"}
        else:
            return {"error":"User must be logged in to logout"}

api.add_resource(Logout, '/logout', endpoint='logout')
     



class UserByID(Resource):
    def get(seld, id):
        user = User.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(user),
            200
        )

        return response

api.add_resource(UserByID, '/users/<int:id>', endpoint='user_id')


class GetGames(Resource):
    def get(self):
        
        games_list = []
        games = GameEntry.query.all()
        
        if games:
            for game in games:
                game_dict = game.to_dict()
                
                games_list.append(game_dict)

                response = make_response(
                jsonify(games_list),
                200
                )
            return response
        response_body = {
           "Message":"No games at the Moment",
           "status":404
        }

        return response_body
    

    def post(self):
        new_game = GameEntry(
            title=request.get_json()['title'],
            platform=request.get_json()['platform'],
            image_url = request.get_json().get('image_url'),
            description=request.get_json()['description'],
            user_id=request.get_json()['user_id']
        )

        description = request.get_json()['description']

        if len(description) <= 100:
            if new_game:
                db.session.add(new_game)
                db.session.commit()

                new_game_dict = new_game.to_dict()
                response = make_response(
                    jsonify(new_game_dict),
                    200,
                )
                response.headers['Content-Type'] = 'application/json'  
                return response

        response_body = {
            "error": "Description length exceeds the limit of 100 characters",
            "status": 400
        }
        response = make_response(jsonify(response_body), 400)
        response.headers['Content-Type'] = 'application/json'  
        return response
    


    
api.add_resource(GetGames, '/games')


class GetGameById(Resource):
    def get(self,id):
        game = GameEntry.query.filter_by(id=id).first()

        if game:
            game_dict = game.to_dict()

            response = make_response(
                jsonify(game_dict),
                200,

                
            )
            return response
        
        response_body = {
            "Message":"Game not found"
        }
        return response_body
    

    def patch(self, id):
            game = GameEntry.query.filter_by(id=id).first()

            if game:
                for attr in request.get_json():
                    setattr(game, attr, request.get_json()[attr])

                db.session.add(game)
                db.session.commit()

                game_dict = game.to_dict()
                

                response = make_response(
                    jsonify({"message": "Game updated successfully", "data": game_dict}),
                    201
                )
                return response

            response_body = {
                "error": "Failed to update game"
            }

            return response_body
    
    def delete(self, id):
        game = GameEntry.query.filter_by(id=id).first()
        db.session.delete(game)
        db.session.commit()

        response_body = {
            "message": "User deleted successfully"
        }

        response = make_response(jsonify(response_body), 200)

        return response


            
   
api.add_resource(GetGameById, '/games/<int:id>', endpoint="game_id")

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({"message": "Resource not found in the server"}), 
        404
        )
    
    return response

class GetGameReviews(Resource):
    def get(self):
        reviews_list = []
        reviews = GameReview.query.all()
        
        if reviews:
            for review in reviews:
                review_dict = review.to_dict()
                reviews_list.append(review_dict)

            response = make_response(
                jsonify(reviews_list),
                200
            )
            return response

        response_body = {
            "Message": "No game reviews at the moment",
            "status": 404
        }
        return response_body

    def post(self):
        new_review = GameReview(
            rating=request.get_json()['rating'],
            comment=request.get_json()['comment'],
            user_id=request.get_json()['user_id'],
            game_entry_id=request.get_json()['game_entry_id']
        )

        if new_review:
            db.session.add(new_review)
            db.session.commit()

            new_review_dict = new_review.to_dict()
            response = make_response(
                jsonify(new_review_dict),
                201
            )
          
            response.headers['Content-Type'] = 'application/json'
            return response

        response_body = {
            "error": "Error occurred while creating a game review, check and try again",
            "status": 400
        }
        response = make_response(jsonify(response_body), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


api.add_resource(GetGameReviews, '/game-reviews', endpoint='game-reviews')



class GetGameReviewById(Resource):
    def get(self, id):
        review = GameReview.query.get(id)  

        if review:
            review_dict = review.to_dict()
            response = make_response(jsonify(review_dict), 200)
            return response

        response_body = {
            "Message": "Game review not found",
            "status": 404
        }
        return response_body

api.add_resource(GetGameReviewById, '/game-reviews/<int:id>')


class GenreResource(Resource):
    def get(self):
        genres_list = []
        genres = Genre.query.all()
            
        if genres:
            for genre in genres:
                genre_dict = genre.to_dict()
                genres_list.append(genre_dict)

            response = make_response(
                jsonify(genres_list),
                200
            )
            return response

        response_body = {
            "Message": "No game genres at the moment",
            "status": 404
        }
        return response_body
    

    def post(self):
        new_genre = Genre(
            name=request.get_json()['name'],
            
        )

        if new_genre:
            db.session.add(new_genre)
            db.session.commit()

            new_genre_dict = new_genre.to_dict()
            response = make_response(
                jsonify(new_genre_dict),
                201  
            )
            
            response.headers['Content-Type'] = 'application/json'
            return response

        response_body = {
            "error": "Error occurred while creating a genre, check and try again",
            "status": 400
        }
        response = make_response(jsonify(response_body), 400)
        response.headers['Content-Type'] = 'application/json'
        return response






api.add_resource(GenreResource, '/genres', endpoint='genres')
            

if __name__ == "__main__":
 app.run(port=5555, debug=True)