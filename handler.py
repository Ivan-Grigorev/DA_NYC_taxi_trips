import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from functools import lru_cache


# Create geolocator object outside the function, so it can be reused
GEOLOCATOR = Nominatim(user_agent="NYC_taxi")


# Use LRU cache to cache the most recently addresses
@lru_cache(maxsize=1000)
def get_location(coord):
    # Convert NumPy array to tuple
    coord = tuple(coord)

    # Check cache for address before calling geolocator
    if coord in get_location.cache:
        location = get_location.cache[coord]
    else:
        location = GEOLOCATOR.reverse(coord)
        get_location.cache[coord] = location
    return location


get_location.cache = {}


def pickup_dropoff_addresses(filename, batch_size):
    # This function get all pickup and dropoff addresses by longitude/latitude and add it to dataframe
    data = pd.read_csv(filename).sort_values(by="pickup_datetime").head(5)

    # Stack the latitude/longitude arrays horizontally and transpose to create tuples
    pickup_coordinates = np.vstack(
        (data["pickup_latitude"].values, data["pickup_longitude"].values)
    ).T
    dropoff_coordinates = np.vstack(
        (data["dropoff_latitude"].values, data["dropoff_longitude"].values)
    ).T

    pickup_address = []
    pickup_street = []
    pickup_borough = []

    dropoff_address = []
    dropoff_street = []
    dropoff_borough = []

    counter_ = 0

    # Use list comprehension for faster and more concise code
    for batch_idx in range(0, len(pickup_coordinates), batch_size):
        pickup_coords_batch = pickup_coordinates[batch_idx: batch_idx + batch_size]
        dropoff_coords_batch = dropoff_coordinates[batch_idx: batch_idx + batch_size]

        for coords, addr_list, street_list, borough_list in [
            (pickup_coords_batch, pickup_address, pickup_street, pickup_borough),
            (dropoff_coords_batch, dropoff_address, dropoff_street, dropoff_borough),
        ]:
            for coord in coords:
                counter_ += 1

                # Get location from cache or geolocator
                location = get_location(tuple(coord))

                # Append data to respective lists
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
    data.to_csv("CSV/nyc_taxi.csv")
    print("Successfully created file with addresses 'CSV/nyc_taxi.csv'")


pickup_dropoff_addresses("CSV/datasets/nyc_taxi_trips.csv", batch_size=500)
