import unittest
import pandas as pd

from handler import HandleDatasets


class TestHandleDatasets(unittest.TestCase):
    def setUp(self):
        self.handle_datasets = HandleDatasets(
            trips_file="CSV/datasets/nyc_taxi_trips.csv",
            weather_file="CSV/datasets/nyc_weather_central_park.csv",
            data_file="CSV/nyc_taxi.csv",
            lines=10,  # set small number of lines for faster tests
        )

    def test_get_pickup_location(self):
        coord = "40.778873 -73.953918"
        result = self.handle_datasets.get_pickup_location(coord)

        # Assert that received address is correct
        self.assertEqual(
            result.address,
            "1530, 3rd Avenue, Manhattan Community Board 8, Manhattan, "
            "New York County, City of New York, New York, 10028, United States",
        )

    def test_get_dropoff_location(self):
        coord = "lat=40.694931&lon=-73.994751"
        result = self.handle_datasets.get_dropoff_location(coord)

        # Assert that received address is correct
        self.assertEqual(
            result.get("display_name", {}),
            "119, Montague Street, Brooklyn, "
            "Kings County, City of New York, New York, 11201, United States",
        )

    def test_get_pickup_dropoff_addresses(self):
        self.handle_datasets.get_pickup_dropoff_addresses()
        self.assertIsNotNone(self.handle_datasets.trips["pickup_address"])
        self.assertIsNotNone(self.handle_datasets.trips["pickup_street"])
        self.assertIsNotNone(self.handle_datasets.trips["pickup_borough"])
        self.assertIsNotNone(self.handle_datasets.trips["dropoff_address"])
        self.assertIsNotNone(self.handle_datasets.trips["dropoff_street"])
        self.assertIsNotNone(self.handle_datasets.trips["dropoff_borough"])

    def test_get_weather_by_date(self):
        self.handle_datasets.get_weather_by_date()

        # Load the nyc_taxi.csv file
        data = pd.read_csv("CSV/nyc_taxi.csv")

        # Assert that all rows are present in the merged data
        self.assertEqual(len(self.handle_datasets.data), len(data))

        original_cols = pd.read_csv("CSV/datasets/nyc_taxi_trips.csv", nrows=1).columns
        weather_cols = pd.read_csv("CSV/datasets/nyc_weather_central_park.csv", nrows=1).columns
        merged_cols = list(data.columns)

        # Assert that the merged data contains all the columns from the original data
        self.assertCountEqual(merged_cols, list(original_cols) + list(weather_cols))

        pickup_dates = pd.read_csv(
            "CSV/datasets/nyc_taxi_trips.csv", usecols=["pickup_datetime"], nrows=10
        )["pickup_datetime"].tolist()
        weather_dates = pd.read_csv(
            "CSV/datasets/nyc_weather_central_park.csv", usecols=["date"], nrows=10
        )["date"].tolist()
        merged_dates = data["pickup_datetime"].tolist()

        # Assert that the merged data is correctly merged by checking that all the dates match
        self.assertCountEqual(pickup_dates, merged_dates)
        self.assertCountEqual(weather_dates, data["date"].tolist())


if __name__ == "__main__":
    unittest.main()
