from flask import Blueprint, jsonify, request

from repository.car_repository import find_all_cars, find_car_by_id, update_car_by_id, delete_car_by_id
from utils.json_handler import parse_json

cars_blueprint = Blueprint("cars", __name__)


@cars_blueprint.route("/", methods=["GET"])
def index():
    try:
        all_cars = find_all_cars()
        return jsonify(parse_json(all_cars)), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@cars_blueprint.route("/<car_id>", methods=["GET"])
def get_car_by_id(car_id):
    try:
        car = find_car_by_id(car_id)
        car_data = car.value_or('Car not found')
        return jsonify(parse_json(car_data)), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@cars_blueprint.route("/<car_id>", methods=["PUT"])
def update_car(car_id):
    car_to_update = find_car_by_id(car_id).value_or(False)
    if not any([car_to_update, car_id]):
        return jsonify({'error': 'Car id not found'}), 400
    try:
        request_data = request.json
        car_data: dict = {**request_data}
        update_car_by_id(car_id, car_data)
        return jsonify(parse_json(find_car_by_id(car_id).unwrap())), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@cars_blueprint.route("/<car_id>", methods=["DELETE"])
def delete_car(car_id):
    driver_to_delete = find_car_by_id(car_id).value_or(False)
    if not any([driver_to_delete, car_id]):
        return jsonify({'error': 'Car id not found'}), 400
    try:
        delete_car_by_id(car_id)
        return jsonify({'message': 'Driver deleted'}), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500

