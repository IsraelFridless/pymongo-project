from typing import Dict

from bson import ObjectId
from returns.maybe import Maybe, Some, Nothing

from database.connect import drivers as original_drivers_collection

def create_driver(driver: Dict[str, str], drivers_collection=original_drivers_collection) -> ObjectId:
    res = drivers_collection.insert_one(driver)
    return res.inserted_id

def find_all_drivers(drivers_collection=original_drivers_collection):
    return list(drivers_collection.find())

def find_driver_by_id(driver_id: str, drivers_collection=original_drivers_collection) -> Maybe[dict]:
    return Maybe.from_optional(drivers_collection.find_one({'_id': ObjectId(driver_id)}))


def delete_driver_by_id(driver_id: str, drivers_collection=original_drivers_collection):
    drivers_collection.delete_one({'_id': ObjectId(driver_id)})

def update_driver_by_id(driver_id: str, driver: Dict[str, str], drivers_collection=original_drivers_collection):
    drivers_collection.update_one({'_id': ObjectId(driver_id)}, {'$set': driver})
