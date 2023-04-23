import unittest
import pandas as pd

from handler import HandleDatasets


class TestHandleDatasets(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset
        trips = pd.DataFrame({"pickup_datetime": ["2022-01-01 06:00:00",
                                                  "2022-01-01 07:00:00",
                                                  "2022-01-01 13:00:00",
                                                  "2022-01-01 19:00:00",
                                                  "2022-01-02 01:00:00",
                                                  ],
                                  "pickup_latitude": [40.737431,
                                                      40.731610,
                                                      40.717842,
                                                      40.734610,
                                                      40.737431,
                                                      ],
                                  "pickup_longitude": [-73.984077,
                                                       -73.936242,
                                                       -74.005508,
                                                       -73.939242,
                                                       -73.984077,
                                                       ],
                                  "dropoff_latitude": [40.749981,
                                                       40.741610,
                                                       40.735226,
                                                       40.744610,
                                                       40.749981,
                                                       ],
                                  "dropoff_longitude": [-73.991409,
                                                        -73.936242,
                                                        -74.003281,
                                                        -73.939242,
                                                        -73.991409,
                                                        ],
                              })

        addresses = pd.DataFrame({
            "lat": [40.712776, 40.720504],
            "lon": [-74.005974, -73.996510],
            "address": ["1 Liberty Plaza, New York, NY 10006, United States",
                        "2-98 Beaver St, New York, NY 10004, United States"]
        })

        weather = pd.DataFrame({
            "date": ["2021-01-01", "2021-01-02"],
            "temperature": [5.6, 2.3],
            "humidity": [40, 60],
        })

        self.handle_datasets = HandleDatasets(
            trips_file=trips,
            addresses_file=addresses,
            weather_file=weather,
            lines=3,
            data="CSV/nyc_taxi.csv",
        )

    def test_pickup_dropoff_addresses(self):
        self.handle_datasets.pickup_dropoff_addresses()

        # check that the new columns were added to the trips dataframe
        self.assertTrue("pickup_address" in self.handle_datasets.trips.columns)
        self.assertTrue("pickup_street" in self.handle_datasets.trips.columns)
        self.assertTrue("pickup_borough" in self.handle_datasets.trips.columns)
        self.assertTrue("dropoff_address" in self.handle_datasets.trips.columns)
        self.assertTrue("dropoff_street" in self.handle_datasets.trips.columns)
        self.assertTrue("dropoff_borough" in self.handle_datasets.trips.columns)

        # check that the new columns contain the expected values
        self.assertEqual(
            self.handle_datasets.trips["pickup_address"].tolist(),
            ["1 Liberty Plaza, New York, NY 10006, United States"] * 3
        )
        self.assertEqual(
            self.handle_datasets.trips["pickup_street"].tolist(),
            ["Liberty Street"] * 3
        )
        self.assertEqual(
            self.handle_datasets.trips["pickup_borough"].tolist(),
            ["Manhattan"] * 3
        )
        self.assertEqual(
            self.handle_datasets.trips["dropoff_address"].tolist(),
            ["2-98 Beaver St, New York, NY 10004, United States"] * 3
        )
        self.assertEqual(
            self.handle_datasets.trips["dropoff_street"].tolist(),
            ["Beaver Street"] * 3
        )
        self.assertEqual(
            self.handle_datasets.trips["dropoff_borough"].tolist(),
            ["Manhattan"] * 3
        )


if __name__ == '__main__':
    unittest.main()

    # def test_pickup_dropoff_addresses(self):
    #     # Ensure the pickup and dropoff addresses are correctly retrieved
    #     addresses = self.analysis.pickup_dropoff_addresses()
    #
    #     self.assertIsNotNone(self.analysis.pickup_coordinates)
    #     self.assertIsNotNone(self.analysis.dropoff_coordinates)
    #
    #     self.assertEqual(
    #         addresses.loc[0, "pickup_address"],
    #         "Spectrum, 261, 3rd Avenue, Manhattan Community Board 6, "
    #         "Manhattan, New York County, City of New York, New York, 10010, United States",
    #     )
    #     self.assertEqual(
    #         addresses.loc[0, "dropoff_address"],
    #         "Pennsylvania Station, Lincoln Tunnel Expressway, Chelsea District, "
    #         "Manhattan, New York County, City of New York, New York, 10119, United States",
    #     )
    #     self.assertEqual(
    #         addresses.loc[2, "pickup_address"],
    #         "251, Church Street, Manhattan Community Board 1, "
    #         "Manhattan, New York County, City of New York, New York, 10013, United States",
    #     )
    #     self.assertEqual(
    #         addresses.loc[2, "dropoff_address"],
    #         "258, West 4th Street, Manhattan Community Board 2, "
    #         "Manhattan, New York County, City of New York, New York, 10014, United States",
    #     )
