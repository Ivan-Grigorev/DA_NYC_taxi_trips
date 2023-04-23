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
            "For the period January 01, 2022 through January 02, 2022 there were:\n"
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


if __name__ == "__main__":
    unittest.main()
