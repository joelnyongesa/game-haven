from flask import Flask, make_response,jsonify,request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, User, GameEntry, GameGenre, Genre, GameReview


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gamehave.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

CORS(app)

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)

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
        
        if password != confirm_password:
            return {"error": "Passwords do not match"}

        new_user = User(username=username, email=email)
        new_user.password_hash = password  # Set the password using password_hash propert

        
        db.session.add(new_user)
        db.session.commit()
        return{"message": "User created successfully", "status":201}

api.add_resource(Signup, "/signup")

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
                # games_list.append({
                #     "id": game_entry.id,
                #     "title": game_entry.title,
                #     "platform": game_entry.platform,
                #     "description": game_entry.description,
                # })
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
            description=request.get_json()['platform'],
            user_id=request.get_json()['user_id']
        )

        description = request.get_json()['description']
        if len(description) > 100:
            response_body = {
                "error": "Description length exceeds the limit of 100 characters",
                "status": 400
            }
            return make_response(jsonify(response_body), 400)

        if new_game:  
            db.session.add(new_game)
            db.session.commit()

            new_game_dict = new_game.to_dict()
            response = make_response(
                jsonify(new_game_dict),
                200,
                "Game created successfully"
            )
            return response
        response_body = {
            "error": "Error occurred while creating a game, check and try again",
            "status": 400
        }
        return response_body

    
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
                # {
                #     "title":game.title,
                #     "platform":game.platform,
                #     "description":game.description,
                #     "user_id": game.user_id
                    
                #     }


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


            
   
api.add_resource(GetGameById, '/games/<int:id>')

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
                201  # Specify the HTTP status code here
            )
            # Add the appropriate headers, such as 'Content-Type'
            response.headers['Content-Type'] = 'application/json'
            return response

        response_body = {
            "error": "Error occurred while creating a game review, check and try again",
            "status": 400
        }
        response = make_response(jsonify(response_body), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


api.add_resource(GetGameReviews, '/game-reviews')



class GetGameReviewById(Resource):
    def get(self, id):
        review = GameReview.query.get(id)  # Query the review by its ID

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
            

if __name__ == "__main__":
 app.run(port=5555, debug=True)


