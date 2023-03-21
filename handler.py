import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from datetime import datetime


def pickup_dropoff_addresses(filename, batch_size):
    # This function get all pickup and dropoff addresses by longitude/latitude and add it to dataframe
    data = pd.read_csv(filename).sort_values(by="pickup_datetime")

    pickup_lat = data["pickup_latitude"].values
    pickup_lon = data["pickup_longitude"].values
    dropoff_lat = data["dropoff_latitude"].values
    dropoff_lon = data["dropoff_longitude"].values

    # Stack the latitude/longitude arrays horizontally and transpose to create tuples
    pickup_coordinates = np.vstack((pickup_lat, pickup_lon)).T
    dropoff_coordinates = np.vstack((dropoff_lat, dropoff_lon)).T

    geolocator = Nominatim(user_agent="NYC_taxi")

    pickup_address = []
    pickup_street = []
    pickup_borough = []

    dropoff_address = []
    dropoff_street = []
    dropoff_borough = []

    # Set cache dict
    cache = {}

    # Get exact pickup address, street and borough by location
    counter_ = 0
    for batch_idx in range(0, len(pickup_coordinates), batch_size):
        pickup_coords_batch = pickup_coordinates[batch_idx: batch_idx + batch_size]
        dropoff_coords_batch = dropoff_coordinates[batch_idx: batch_idx + batch_size]

        for coords, addr_list, street_list, borough_list in [
            (pickup_coords_batch, pickup_address, pickup_street, pickup_borough),
            (dropoff_coords_batch, dropoff_address, dropoff_street, dropoff_borough),
        ]:

            for coord in coords:
                counter_ += 1
                print(f"{datetime.now().time().strftime('%H:%M:%S')}, {counter_} line processed...")
                # Check cache for address before calling geolocator
                if tuple(coord) in cache:
                    location = cache[tuple(coord)]
                else:
                    location = geolocator.reverse(coord)
                    cache[tuple(coord)] = location

                addr_list.append(location.address)
                street_list.append(location.raw["address"].get("road", None))
                borough_list.append(location.raw["address"].get("suburb", None))

    data["pickup_address"] = pickup_address
    data["pickup_street"] = pickup_street
    data["pickup_borough"] = pickup_borough

    data["dropoff_address"] = dropoff_address
    data["dropoff_street"] = dropoff_street
    data["dropoff_borough"] = dropoff_borough

    # Create new csv file with proceeded data and added addresses
    print(f"\n{datetime.now().time().strftime('%H:%M:%S')}, {counter_} lines processed")

    data.to_csv("CSV/nyc_taxi_trips_addresses.csv")
    print("Successfully created file with addresses 'CSV/nyc_taxi_trips_addresses.csv'")


pickup_dropoff_addresses("CSV/nyc_taxi_trips.csv", batch_size=100)
