import unittest
import pandas as pd

from nyc_taxi_analysis import NYCTaxiAnalysis


class TestNYCTaxiAnalysis(unittest.TestCase):
    def setUp(self):
        # Create sample dataframe
        self.data = pd.DataFrame({"pickup_datetime": ["2022-01-01 06:00:00",
                                                      "2022-01-01 07:00:00",
                                                      "2022-01-01 13:00:00",
                                                      "2022-01-01 19:00:00",
                                                      "2022-01-02 01:00:00",],
                                  "pickup_latitude": [40.737431,
                                                      40.731610,
                                                      40.717842,
                                                      40.734610,
                                                      40.737431,],
                                  "pickup_longitude": [-73.984077,
                                                       -73.936242,
                                                       -74.005508,
                                                       -73.939242,
                                                       -73.984077,],
                                  "dropoff_latitude": [40.749981,
                                                       40.741610,
                                                       40.735226,
                                                       40.744610,
                                                       40.749981,],
                                  "dropoff_longitude": [-73.991409,
                                                        -73.936242,
                                                        -74.003281,
                                                        -73.939242,
                                                        -73.991409,],})

        # Create CSV file with test data
        self.file_ = "test_data.csv"
        self.data.to_csv(self.file_, index=False)

        # Create instance of NYCTaxiAnalysis class
        self.analysis = NYCTaxiAnalysis(
            dataset=self.file_, lines=5, date_from="2022-01-01", date_to="2022-01-02"
        )

    def test_rides_of_the_day(self):
        # Ensure the total number of rides is correct
        self.assertEqual(
            self.analysis.rides_of_the_day(),
            "For the period 2022-01-01 through 2022-01-02 there were:\n"
            "\t2 rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00);\n"
            "\t1 rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00);\n"
            "\t1 rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00);\n"
            "\t1 rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00).\n"
            "TOTAL: 5",
        )

        # Ensure the output includes the expected number of rides for each time period
        self.assertIn(
            "2 rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00)",
            self.analysis.rides_of_the_day(),
        )
        self.assertIn(
            "1 rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00)",
            self.analysis.rides_of_the_day(),
        )
        self.assertIn(
            "1 rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00)",
            self.analysis.rides_of_the_day(),
        )
        self.assertIn(
            "1 rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00)",
            self.analysis.rides_of_the_day(),
        )

    def test_pickup_dropoff_addresses(self):
        # Ensure the pickup and dropoff addresses are correctly retrieved
        addresses = self.analysis.pickup_dropoff_addresses()

        self.assertIsNotNone(self.analysis.pickup_coordinates)
        self.assertIsNotNone(self.analysis.dropoff_coordinates)

        self.assertEqual(
            addresses.loc[0, "pickup_address"],
            "Spectrum, 261, 3rd Avenue, Manhattan Community Board 6, "
            "Manhattan, New York County, City of New York, New York, 10010, United States",
        )
        self.assertEqual(
            addresses.loc[0, "dropoff_address"],
            "Pennsylvania Station, Lincoln Tunnel Expressway, Chelsea District, "
            "Manhattan, New York County, City of New York, New York, 10119, United States",
        )
        self.assertEqual(
            addresses.loc[2, "pickup_address"],
            "251, Church Street, Manhattan Community Board 1, "
            "Manhattan, New York County, City of New York, New York, 10013, United States",
        )
        self.assertEqual(
            addresses.loc[2, "dropoff_address"],
            "258, West 4th Street, Manhattan Community Board 2, "
            "Manhattan, New York County, City of New York, New York, 10014, United States",
        )


if __name__ == "__main__":
    unittest.main()
