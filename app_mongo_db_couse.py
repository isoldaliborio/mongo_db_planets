from flask import flask, request, jsonify
from flask_pymongo import PyMongo 
# PyMongo allows user the mongoDB
from bson import objectid
# to convert string in object IDs


# set up the app itself
app = Flask(__name__)
# databse URL to use (you can make a configuration file, you can use environment variables, to do this selfcontained:)
app.config["MONGO_URI"] = "mongodb://localhost:27017/planetsdb"
# 27017 is a standad port to mongoDB -- planetsdb is the name of the DB that I'm going to work with. 
mongo = PyMongo(app)
# mongo varible = PyMongo constructor passing the app - this is taking care about ... 
# a lot of will be boiler plate code, for conecting the working with the database. 

# the routes
# GET route
@app.route("/api/v1/all", methods=["GET"])
# in the industry best practice - put api in front of my json calls - everything that returns json shoud have api in front
# v1 is a version - a way to rewrite the api in the future - so I can have one in production and have a separeted instance v2 or whatever. 
def list_planets():
# def (define my function)
    planet_result = mongo.db.planets.find()
    # 24 - my DB
    planets = []
    # each one of this planets is going to have an list 
    # aour planet results is going to contain the full list start in the database
    # planets is going to have an objectID on it and objectID is not serializeble in Python. So...
    # .. so there is no way to convert it from the objectID that comes as into a string, so we can send it back to our API
    # so bellow I'm going to loop over and convert in a string after
    for planet in planet_result:
        planet["id"] = str(planet["_id"])
        planets.append(planet)

    return jsonify(planets)
    # We convert in a strig so jsonify can complain it 

# read
@app.rout("/api/v1/find/<string:planet_id>", methods=["GET"])
def find_planet_by_id(planet_id:str):
    status_code = 200
    planet.result = mongo.db.planets.find_one({"_id:": objectid.objectID(planet_id)})
    if planet_result is None:
        status_code = 404
    else:
        planet_result["_id"] = planet_id
    
    return jsonify(planet_result), status_code

# create
@app.rout("/api/v1/create/", methods["POST"])
def add_planet():
    status_code = 201
    message = "Planet added"
    result = {}
    try:
        inbound_data = request.get_json()
        inserted = mongo.db.planet.insert_one(inbound_data)
        result["inserted_id"] = str(inserted.inserted_id)
    except:
        status_code = 500
        message = "ERROR"
    return jsonify(result), status_code


# update
@app.rout("/api/v1/update/<string:planet_id>", methods = ["PUT", "POST"])
def update_planet(planet_id: str):
    status_code = 200
    message = "Planet updated"
    inbound_data = request.json()
    result = {}
    try:
        mongo.db.planet.update_one({_id:objectid.objectID(planet_id)}, {"$SET": inbound_data})
    except:
        message = "ERROR"
        status_code = 500
    
    return jsonify(result), status_code

# delete route

@pp.route("api/v1/delete/<string:planet_id>", methods = ["DELETE", "POST"])
def delete_planet(planet_id: str):
    status_code = 200
    result = {}
    message = "I fear something terrible has happened"
    try:
        mongo.db.planets.delete_one({"_id": objectid.objectID(planet_id)})
    except:
        message = "ERROR"
        status_code = 500

    result["message"] = message
    return jsonify(resul), status_code