from typing import Dict

import pytest
from bson import ObjectId
from pymongo.collection import Collection
from returns.maybe import Some, Nothing

from repository.car_repository import create_car, find_car_by_id, find_all_cars, delete_car_by_id, update_car_by_id


@pytest.fixture(scope="function")
def cars_collection(init_test_data):
   return init_test_data['cars']


def test_find_all_cars(cars_collection: Collection):
   res = find_all_cars()
   assert len(res) == 30

def test_create_car(cars_collection: Collection):
   car_id = create_car({'license_id': 'FGH78967', 'brand': 'Ford', 'color': 'red'}, cars_collection)
   assert isinstance(car_id, ObjectId)
   assert ObjectId.is_valid(str(car_id))

def test_delete_car(cars_collection: Collection):
   car_id = '67062f26a83c55d61f6af57c'
   delete_car_by_id(car_id, cars_collection)
   assert find_car_by_id(car_id, cars_collection) is Nothing

def test_update_car(cars_collection: Collection):
   car_id = '67066b1de93fb0366d6fc5eb'
   car = find_car_by_id(car_id, cars_collection).value_or(None)
   updated_driver = {
      'color': 'Blue',
   }
   update_car_by_id(car_id, updated_driver, cars_collection)
   after_update_car = find_car_by_id(car_id, cars_collection).value_or(None)
   assert after_update_car['color'] == 'Blue'
   assert after_update_car != car
   assert 'color' in after_update_car

def test_find_car_by_id(cars_collection: Collection):
   car_id = '67066b1de93fb0366d6fc5eb'
   requested_car = find_car_by_id(car_id, cars_collection)
   assert requested_car.map(lambda d: '_id' in d).value_or(False)