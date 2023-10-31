from flask import Flask, make_response,jsonify,request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound
from models import db, User, GameEntry, GameGenre, Genre


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
            

if __name__ == "__main__":
 app.run(port=5555, debug=True)


