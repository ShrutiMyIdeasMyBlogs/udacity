import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from models import setup_db
from models import *
from auth import *

port = os.environ.get('FLASK_RUN_PORT')
page_limit = os.environ.get('ITEMS_PER_PAGE')

def paginate_items(request, selection):
    page = (request.args.get('page', 1, type=int))
    start = (page - 1) * int(page_limit) 
    end = int(start) + int(page_limit)
    items = [item.format() for item in selection]
    current_items = items[int(start):int(end)]
    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)   
    db = setup_db(app)
    cors = CORS(app)
    
    @app.route("/actors", methods=['GET'])    
    def display_actors():           
            actors = Actors.query.order_by(Actors.id).all()
            current_actors_paginated = paginate_items(request, actors) 
            if (len(current_actors_paginated) == 0):
                abort(404)
            return jsonify({
                    "success":True,
                    "actors":current_actors_paginated}),200           
        
            
    @app.route("/actors", methods=['POST'])
    @requires_auth('add:actors')
    def add_actor(jwt):        
            data = request.get_json()
            if 'firstname' in data:
                if data['firstname'] is None:
                    abort(400)  
            if 'lastname' in data:
                if data['lastname'] is None:
                    abort(400)
            if 'gender' in data:
                if data['gender'] is None:
                    abort(400)
            if 'age' in data:
                if data['age'] is None:
                    abort(400)
            new_actor = Actors(firstname= data['firstname'],
                            lastname = data['lastname'],
                            gender = data['gender'],
                            age = data['age'])
            new_actor.insert()
            return jsonify({
                    "success":True,
                    "actors":data}),200              
        
            
            
    @app.route("/actors/<int:id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt,id):        
            actor_to_delete = Actors.query.get(id)
            if actor_to_delete is None:
                abort(404)
            actor_to_delete.delete()
            return jsonify({
                    "success":True,
                    "delete":id}),200
        
                    
                    
                    
    @app.route("/actors/<int:id>", methods=['PATCH'])
    @requires_auth('modify:actors')
    def patch_actor(jwt,id):        
            actor_to_patch = Actors.query.get(id)
            if actor_to_patch is None:
                abort(404)
            data = request.get_json()
            if 'firstname' in data:
                if data['firstname'] is None:
                    abort(400)
                actor_to_patch.firstname = data.get('firstname')            
            if 'lastname' in data:
                if data['lastname'] is None:
                    abort(400)
                actor_to_patch.lastname = data.get('lastname')
            if 'gender' in data:
                if data['gender'] is None:
                    abort(400)
                actor_to_patch.gender = data.get('gender')
            if 'age' in data:
                if data['age'] is None:
                    abort(400)
                actor_to_patch.age = data.get('age')            
            actor_to_patch.update() 
            actor = actor_to_patch.format()    
            return jsonify({
                    "success":True,
                    "actor":actor}),200
        
            
            
            
                    
    @app.route("/movies", methods=['GET'])    
    def display_movies():           
            movies = Movies.query.order_by(Movies.id).all()   
            current_movies_paginated = paginate_items(request, movies) 
            if (len(current_movies_paginated) == 0):
                abort(404)
            return jsonify({
                    "success":True,
                    "movies":current_movies_paginated}),200         
       
        
            
    @app.route("/movies", methods=['POST'])
    @requires_auth('add:movies')
    def add_movie(jwt):        
            data = request.get_json()
            if 'title' in data:
                if data['title'] is None:
                    abort(400)
            if 'release_date' in data:
                if data['release_date'] is None:
                    abort(400)              
            new_movie = Movies(title= data['title'],
                            release_date = data['release_date'])                          
            new_movie.insert()
            return jsonify({
                    "success":True,
                    "movies":data}),200              
        
            
            
            
    @app.route("/movies/<int:id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt,id):        
            movie_to_delete = Movies.query.get(id)
            if movie_to_delete is None:
                abort(404)
            movie_to_delete.delete()
            return jsonify({
                    "success":True,
                    "delete":id}),200
        
            
            
                    
    @app.route("/movies/<int:id>", methods=['PATCH'])
    @requires_auth('modify:movies')
    def patch_movie(jwt,id):        
            movie_to_patch = Movies.query.get(id)
            if movie_to_patch is None:
                abort(404)
            data = request.get_json()
            if 'title' in data:
                if data['title'] is None:
                    abort(400)
                movie_to_patch.title = data.get('title')            
            if 'release_date' in data:
                if data['release_date'] is None:
                    abort(400)
                movie_to_patch.release_date = data.get('release_date')
            movie_to_patch.update() 
            movie = movie_to_patch.format()    
            return jsonify({
                    "success":True,
                    "movie":movie}),200
        
            
    
    @app.route("/relations", methods=['GET'])
    def display_relations():
            relations = Relations.query.order_by(Relations.id).all()
            current_relations_paginated = paginate_items(request, relations) 
            if (len(current_relations_paginated) == 0):
                abort(404)
            
            return jsonify({
                    "success":True,
                    "relations":[relation.format() for relation in current_relations_paginated]}),200   
        
            
            
        
    @app.route("/relations", methods=['POST'])
    def add_relation():        
            data = request.get_json()
            if data['movie_id'] is None:
                    abort(400)
            if data['actor_id'] is None:
                    abort(400)
            new_relation = Relations(movie_id= data['movie_id'],
								actor_id = data['actor_id'])   
            new_relation.insert()
            return jsonify({
                "success":True,
                "relations":data}),200
        
            
        
    @app.route("/relations/<int:id>", methods=['DELETE'])
    def delete_relation(id):
            relation_to_delete = Relations.query.get(id)
            if relation_to_delete is None:
                abort(404)   
            relation_to_delete.delete()
            return jsonify({
                "success":True,
                "delete":id}),200                

            
            
                
    @app.route("/relations/<int:id>", methods=['PATCH'])
    def patch_relation(id):
            relation_to_patch = Relations.query.get(id)
            data = request.get_json()            
            if relation_to_patch is None:
                abort(404)            
            if 'movie_id' in data:
                if data['movie_id'] is None:
                    abort(400)
                relation_to_patch.movie_id = data.get('movie_id')            
            if 'actor_id' in data:
                if data['actor_id'] is None:
                    abort(400)
                relation_to_patch.actor_id = data.get('actor_id')
            relation_to_patch.update() 
            relation = relation_to_patch.format()    
            return jsonify({
                "success":True,
                "relation":relation}),200

            
            
    
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success":False,
        "error":422,
        "message":"unprocessable"        
        }), 422
        
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
        }), 400 
    
    @app.errorhandler(AuthError)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": "Authentication fails"
         }), error.status_code
    return app  

app = create_app()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)