import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        }), 200
    except:
        abort(422)

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['Get'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    try:
        drinks = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
        }), 200
    except:
        abort(422)

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    drink_details = request.get_json()

    try:
        drink = Drink(drink_details.get("title"), drink_details.get("recipe"))
        drink.insert()
    except:
        abort(400)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200

'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(id):
    drink_details = request.get_json()

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(400)
    
    try:
        update_drink = Drink(drink_details.get("title"), drink_details.get("recipe"))
        update_drink.update()
    except:
        abort(400)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200

'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    drink_details = request.get_json()

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(400)
    
    try:
        delete_drink = Drink(drink_details.get("title"), drink_details.get("recipe"))
        delete_drink.delete()
    except:
        abort(400)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200

## Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
        jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
    }), 400
    
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "unauthorized"
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "forbidden"
    }), 403

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "server error"
    }), 500

'''
@DONE implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@DONE implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error.get("description")
    }), error.status_code