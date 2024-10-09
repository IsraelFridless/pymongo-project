from pymongo import MongoClient


client = MongoClient('mongodb://172.17.242.253:27017')
taxi_db = client['taxi-drivers']
online_retail_db = client['online_retail']

drivers = taxi_db['drivers']
cars = taxi_db['cars']

customers = online_retail_db['customers']
products = online_retail_db['products']
invoices = online_retail_db['invoices']
