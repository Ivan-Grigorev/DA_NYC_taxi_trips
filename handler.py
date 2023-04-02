import pandas as pd
import numpy as np
import requests
import time

from geopy import Nominatim


pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)
pd.set_option("display.width", 1000)
pd.set_option('max_colwidth', 100)


class HandleDatasets:
    def __init__(self, trips_file, addresses_file, weather_file, data, lines=None):
        self.trips = pd.read_csv(trips_file, low_memory=False).head(lines)
        self.addresses = pd.read_csv(addresses_file, low_memory=False).head(lines)
        self.weather = pd.read_csv(weather_file, low_memory=False).head(lines)
        self.data = data

    def pickup_dropoff_addresses(self):
        start_time = time.time()
        # Get pickup and dropoff coordinates
        pickup_coordinates = [f"{_[0]} {_[1]}" for _ in np.column_stack(
            (self.trips['pickup_latitude'].values, self.trips['pickup_longitude'].values))
                              ]

        dropoff_coordinates = [f"lat={_[0]}&lon={_[1]}" for _ in np.column_stack(
            (self.trips['dropoff_latitude'].values, self.trips['dropoff_longitude'].values))
                               ]

        # Get streets names, boroughs by pickup and dropoff coordinates
        # Using geopy and Nominatim
        GEOLOCATOR = Nominatim(user_agent='NYC_taxi')

        self.trips['pickup_address'] = [
            GEOLOCATOR.reverse(coord).address
            for coord in pickup_coordinates
        ]
        self.trips['pickup_street'] = [
            GEOLOCATOR.reverse(coord).raw['address'].get('road', None)
            for coord in pickup_coordinates
        ]
        self.trips['pickup_borough'] = [
            GEOLOCATOR.reverse(coord).raw['address'].get('suburb', None)
            for coord in pickup_coordinates
        ]

        # Using requests and OpenStreetMap
        self.trips['dropoff_address'] = [
            requests.get(
                f"https://nominatim.openstreetmap.org/reverse?{coord}&format=json"
            ).json().get('display_name', {})
            for coord in dropoff_coordinates
        ]
        self.trips['dropoff_street'] = [
            requests.get(
                f"https://nominatim.openstreetmap.org/reverse?{coord}&format=json"
            ).json().get('address', {}).get('road', None)
            for coord in dropoff_coordinates
        ]
        self.trips['dropoff_borough'] = [
            requests.get(
                f"https://nominatim.openstreetmap.org/reverse?{coord}&format=json"
            ).json().get('address', {}).get('suburb', None)
            for coord in dropoff_coordinates
        ]

        print(f"The {HandleDatasets.pickup_dropoff_addresses.__name__}() function successfully completed "
              f"processing {len(self.trips)} lines in {round((time.time() - start_time), 2)} seconds.")

    def __repr__(self):
        return self.trips


if __name__ == '__main__':
    handle_datasets = HandleDatasets(
        trips_file='CSV/datasets/nyc_taxi_trips.csv',
        addresses_file='CSV/datasets/nyc_streets.csv',
        weather_file='CSV/datasets/nyc_weather_central_park.csv',
        data='CSV/nyc_taxi.csv',
        lines=5,
    )

    handle_datasets.pickup_dropoff_addresses()
    print(handle_datasets.__repr__())
