import pandas as pd
import numpy as np
import requests
import time
import multiprocessing

from geopy.geocoders import Nominatim

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)
pd.set_option("max_colwidth", 100)


class HandleDatasets:
    def __init__(self, trips_file, addresses_file, weather_file, data, lines=None):
        self.trips = pd.read_csv(trips_file, low_memory=False).head(lines)
        self.addresses = pd.read_csv(addresses_file, low_memory=False).head(lines)
        self.weather = pd.read_csv(weather_file, low_memory=False).head(lines)
        self.data = data

    # Get streets names, boroughs by pickup and dropoff coordinates
    def get_pickup_location(self, coord):
        # Using geopy and Nominatim
        geolocator = Nominatim(user_agent="NYC_taxi", timeout=5)
        return geolocator.reverse(coord)

    def get_dropoff_location(self, coord):
        # Using requests and OpenStreetMap
        return requests.get(
            f"https://nominatim.openstreetmap.org/reverse?{coord}&format=json"
        ).json()

    def pickup_dropoff_addresses(self):
        start_time = time.time()
        # Get pickup and dropoff coordinates
        pickup_coordinates = [
            f"{_[0]} {_[1]}" for _ in np.column_stack((
                    self.trips["pickup_latitude"].values,
                    self.trips["pickup_longitude"].values,))
        ]

        dropoff_coordinates = [
            f"lat={_[0]}&lon={_[1]}" for _ in np.column_stack((
                    self.trips["dropoff_latitude"].values,
                    self.trips["dropoff_longitude"].values,))
        ]

        # Use multiprocessing to speed up geocoding
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        pickup_data = pool.map(self.get_pickup_location, pickup_coordinates)
        dropoff_data = pool.map(self.get_dropoff_location, dropoff_coordinates)

        self.trips["pickup_address"] = [i.address for i in pickup_data]
        self.trips["pickup_street"] = [i.raw["address"].get("road", None) for i in pickup_data]
        self.trips["pickup_borough"] = [i.raw["address"].get("suburb", None) for i in pickup_data]

        self.trips["dropoff_address"] = [i.get("display_name", {}) for i in dropoff_data]
        self.trips["dropoff_street"] = [i.get("address", {}).get("road", {}) for i in dropoff_data]
        self.trips["dropoff_borough"] = [i.get("address", {}).get("suburb", {}) for i in dropoff_data]

        # Create new dataset with processed data
        self.trips.to_csv(self.data, index=False)

        print(
            f"The {HandleDatasets.pickup_dropoff_addresses.__name__}() function successfully completed "
            f"processing {len(self.trips)} lines in {round((time.time() - start_time), 2)} seconds."
        )

    def __repr__(self):
        return self.data


if __name__ == "__main__":
    handle_datasets = HandleDatasets(
        trips_file="CSV/datasets/nyc_taxi_trips.csv",
        addresses_file="CSV/datasets/nyc_streets.csv",
        weather_file="CSV/datasets/nyc_weather_central_park.csv",
        data="CSV/nyc_taxi.csv",
        lines=200,
    )

    handle_datasets.pickup_dropoff_addresses()
    print(handle_datasets.__repr__())
