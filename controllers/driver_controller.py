from flask import Blueprint, jsonify, request

from repository.drivers_repository import find_all_drivers, find_driver_by_id, update_driver_by_id, delete_driver_by_id
from utils.json_handler import parse_json

drivers_blueprint = Blueprint("drivers", __name__)

@drivers_blueprint.route("/", methods=["GET"])
def index():
    try:
        all_drivers = find_all_drivers()
        return jsonify(parse_json(all_drivers)), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@drivers_blueprint.route("/<driver_id>", methods=["GET"])
def get_driver_by_id(driver_id):
    try:
        driver = find_driver_by_id(driver_id)
        driver_data = driver.value_or('Driver not found')
        return jsonify(parse_json(driver_data)), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@drivers_blueprint.route("/<driver_id>", methods=["PUT"])
def update_driver(driver_id):
    driver_to_update = find_driver_by_id(driver_id).value_or(False)
    if not any([driver_to_update ,driver_id]):
        return jsonify({'error': 'Driver id not found'}), 400
    try:
        request_data = request.json
        driver_data: dict = {**request_data}
        update_driver_by_id(driver_id, driver_data)
        return jsonify(parse_json(find_driver_by_id(driver_id).unwrap())), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500


@drivers_blueprint.route("/<driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    driver_to_delete = find_driver_by_id(driver_id).value_or(False)
    if not any([driver_to_delete, driver_id]):
        return jsonify({'error': 'Driver id not found'}), 400
    try:
        delete_driver_by_id(driver_id)
        return jsonify({'message': 'Driver deleted'}), 200
    except Exception as e:
        return jsonify({'error': repr(e)}), 500

