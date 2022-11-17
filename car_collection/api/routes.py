from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import db, Car, car_schema, cars_schema

api = Blueprint('ap', __name__, url_prefix = '/api')


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    mileage = request.json['mileage']
    price = request.json['price']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token}")

    car = Car(make, model, year, color, mileage, price, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid token required!'})


@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.mileage = request.json['mileage']
    car.price = request.json['price']
    car.user_token = current_user_token.token    

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

