from flask import Flask

from controllers.car_controller import cars_blueprint
from controllers.driver_controller import drivers_blueprint
from repository.csv_repository import init_taxi_drivers, init_online_retail

app = Flask(__name__)

if __name__ == '__main__':
    # init_taxi_drivers()
    init_online_retail()
    app.register_blueprint(drivers_blueprint, url_prefix="/api/drivers")
    app.register_blueprint(cars_blueprint, url_prefix="/api/cars")
    app.run(debug=True)