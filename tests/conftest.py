import pytest
from pymongo import MongoClient


from database.connect import drivers, taxi_db
from repository.csv_repository import init_taxi_drivers


@pytest.fixture(scope="function")
def mongodb_client():
   client = MongoClient('mongodb://172.17.242.253:27017/')
   yield client
   client.close()

@pytest.fixture(scope="function")
def drivers_collection(init_test_data):
   return init_test_data['drivers']

@pytest.fixture(scope="function")
def cars_collection(init_test_data):
   return init_test_data['cars']

@pytest.fixture(scope="function")
def taxi_db_test(mongodb_client):
   db_name = 'test_taxi_db'
   db = mongodb_client[db_name]
   yield db
   mongodb_client.drop_database(db_name)


@pytest.fixture(scope="function")
def init_test_data(taxi_db_test):
   # Initialize the main database if it's empty
   if taxi_db['drivers'].count_documents({}) == 0:
       init_taxi_drivers()


   # Copy data from main database to test database
   for collection_name in taxi_db.list_collection_names():
       taxi_db_test[collection_name].drop()
       taxi_db_test[collection_name].insert_many(taxi_db[collection_name].find())


   yield taxi_db_test


   # Clean up test data after each test
   for collection_name in taxi_db_test.list_collection_names():
       taxi_db_test[collection_name].drop()
