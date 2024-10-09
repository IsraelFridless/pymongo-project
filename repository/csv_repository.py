import logging

from pymongo import ReturnDocument

from database.connect import *
import csv
import os

logging.basicConfig(level=logging.INFO)

def read_csv(csv_path):
   with open(csv_path, 'r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           yield row


def init_taxi_drivers():
   drivers.drop()
   cars.drop()


   for row in read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'practice_data.csv')):
       car = {
           'license_id': row['CarLicense'],
           'brand': row['CarBrand'],
           'color': row['CarColor']
       }

       car_id = cars.insert_one(car).inserted_id

       address = {
           'city': row['City'],
           'street': row['Street'],
           'state': row['State']
       }

       driver = {
           'passport': row['PassportNumber'],
           'first_name': row['FullName'].split(' ')[0],
           'last_name': row['FullName'].split(' ')[1],
           'car_id': car_id,
           'address': address
       }

       drivers.insert_one(driver)


def init_online_retail():
    customers.drop()
    products.drop()
    invoices.drop()

    count = 0

    for row in read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'online_retail.csv')):
        customer = {
            'customer_id': row['CustomerID'],
            'country': row['Country'],
        }
        customer_result = customers.find_one_and_update(
            {'customer_id': row['CustomerID']},
            {'$set': customer},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        customer_id = customer_result['_id']

        product = {
            'stock_code': row['StockCode'],
            'description': row['Description'],
            'unitPrice': float(row['UnitPrice'])
        }
        product_result = products.find_one_and_update(
            {'stock_code': row['StockCode']},
            {'$set': product},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        product_id = product_result['_id']

        invoice = {
            'invoice_no': row['InvoiceNo'],
            'quantity': int(row['Quantity']),
            'invoice_date': row['InvoiceDate'],
            'customer_id': customer_id,
            'product_id': product_id
        }
        invoices.insert_one(invoice)
        count += 1
        logging.info(f'Total insertions: {count}')