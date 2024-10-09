import pytest
from bson import ObjectId
from pymongo.collection import Collection
from repository.drivers_repository import create_driver, find_driver_by_id, delete_driver_by_id, update_driver_by_id, find_all_drivers
from repository.car_repository import create_car


def test_create_driver(drivers_collection: Collection, cars_collection: Collection):
   car_id = create_car({'license_id': 'FGH78967','brand': 'Ford', 'color': 'red'}, cars_collection)
   driver = {
    'passport': 'T0149879874',
    'first_name': 'Israel',
    'last_name': 'Fridless',
    'car_id': car_id,
    'address': { 'city': 'Bnei-brak', 'street': 'Hida', 'state': 'Israel' }
    }
   new_driver_id = create_driver(driver, drivers_collection)
   assert isinstance(new_driver_id, ObjectId)
   assert ObjectId.is_valid(str(new_driver_id))


from bson import ObjectId
from returns.maybe import Some, Nothing


def test_find_driver_by_id(drivers_collection: Collection):
    driver_id = '6706651eecec526b194e378a'
    requested_driver = find_driver_by_id(driver_id, drivers_collection)
    assert requested_driver.map(lambda d: '_id' in d).value_or(False)
    assert requested_driver.map(lambda d: 'passport' in d).value_or(False)
    assert requested_driver.map(lambda d: isinstance(d, dict)).value_or(False)


def test_delete_driver(drivers_collection: Collection):
    driver_id = '67062f26a83c55d61f6af57d'
    delete_driver_by_id(driver_id, drivers_collection)
    assert not find_driver_by_id(driver_id, drivers_collection)

def test_update_driver(drivers_collection: Collection):
    driver_id = '67062f26a83c55d61f6af57d'
    driver = find_driver_by_id(driver_id, drivers_collection)
    updated_driver = {
        'last_name': 'Fridless',
      }
    update_driver_by_id(driver_id, updated_driver, drivers_collection)
    after_update_driver = find_driver_by_id(driver_id, drivers_collection)
    assert after_update_driver['last_name'] == 'Fridless'
    assert after_update_driver != driver
    assert 'passport' in after_update_driver

def test_find_all_drivers(drivers_collection: Collection):
    res = find_all_drivers(drivers_collection)
    assert len(res) == 30
    assert isinstance(res[0], dict)

