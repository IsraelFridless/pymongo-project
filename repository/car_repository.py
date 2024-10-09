from typing import Dict

from bson import ObjectId
from returns.maybe import Maybe, Some, Nothing

from database.connect import cars as original_cars_collection

def create_car(car: Dict[str, str], cars_collection=original_cars_collection ) -> ObjectId:
   res = cars_collection.insert_one(car)
   return res.inserted_id

def find_all_cars(cars_collection=original_cars_collection):
    return list(cars_collection.find())

def find_car_by_id(car_id: str, cars_collection=original_cars_collection) -> Maybe[dict]:
    return Maybe.from_optional(cars_collection.find_one({'_id': ObjectId(car_id)}))

def delete_car_by_id(car_id: str, cars_collection=original_cars_collection):
    cars_collection.delete_one({'_id': ObjectId(car_id)})

def update_car_by_id(car_id: str, car: Dict[str, str], cars_collection=original_cars_collection):
    cars_collection.update_one({'_id': ObjectId(car_id)}, {'$set': car})