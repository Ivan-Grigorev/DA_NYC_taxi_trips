import unittest
import pandas as pd
import os

from nyc_taxi_analysis import NYCTaxiAnalysis


class TestNYCTaxiAnalysis(unittest.TestCase):
    def setUp(self):
        # Create sample test dataframe
        self.data = pd.DataFrame(
            {
                "pickup_datetime": [
                    "2022-01-01 06:00:00",
                    "2022-01-01 07:00:00",
                    "2022-01-01 13:00:00",
                    "2022-01-01 19:00:00",
                    "2022-01-02 01:00:00",
                ],
                "pickup_latitude": [
                    40.73743057250977,
                    40.71784210205078,
                    40.80733108520508,
                    40.76977157592773,
                    40.79424285888672,
                ],
                "pickup_longitude": [
                    -73.98407745361328,
                    -74.00550842285155,
                    -73.96442413330078,
                    -73.9669189453125,
                    -73.9701156616211,
                ],
                "dropoff_latitude": [
                    40.74998092651367,
                    40.73522567749024,
                    40.77615737915039,
                    40.78138732910156,
                    40.804161071777344,
                ],
                "dropoff_longitude": [
                    -73.99140930175781,
                    -74.00328063964845,
                    -73.95807647705078,
                    -73.9584732055664,
                    -73.96289825439453,
                ],
                "pickup_address": [
                    "Spectrum, 261, 3rd Avenue, Manhattan Community Board "
                    "6, Manhattan, New York County, City of New York, New "
                    "York, 10010, United States",
                    "251, Church Street, Manhattan Community Board 1, "
                    "Manhattan, New York County, City of New York, New "
                    "York, 10013, United States",
                    "West 115th Street, Morningside Heights, Manhattan, "
                    "New York County, City of New York, New York, 10025, "
                    "United States",
                    "824, Madison Avenue, Manhattan Community Board 8, "
                    "Manhattan, New York County, City of New York, New "
                    "York, 10065, United States",
                    "Amsterdam Avenue & West 96th Street, Amsterdam "
                    "Avenue, Manhattan Community Board 7, Manhattan, New "
                    "York County, City of New York, New York, 10025, "
                    "United States",
                ],
                "pickup_street": [
                    "3rd Avenue",
                    "Church Street",
                    "West 115th Street",
                    "Madison Avenue",
                    "Amsterdam Avenue",
                ],
                "pickup_borough": [
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                ],
                "dropoff_address": [
                    "Pennsylvania Station, Pennsylvania Plaza, Chelsea "
                    "District, Manhattan, New York County, City of New "
                    "York, New York, 10119, United States",
                    "258, West 4th Street, Manhattan Community Board 2, "
                    "Manhattan, New York County, City of New York, New "
                    "York, 10014, United States",
                    "1186, Lexington Avenue, Manhattan Community Board "
                    "8, Manhattan, New York County, City of New York, "
                    "New York, 10028, United States",
                    "Alexander Florals, Madison Avenue, Manhattan "
                    "Community Board 8, Manhattan, New York County, City "
                    "of New York, New York, 10037, United States",
                    "Cathedral of Saint John the Divine, 1047, Amsterdam "
                    "Avenue, Manhattan Community Board 9, Manhattan, New "
                    "York County, City of New York, New York, 10025, "
                    "United States",
                ],
                "dropoff_street": [
                    "Pennsylvania Plaza",
                    "West 4th Street",
                    "Lexington Avenue",
                    "Madison Avenue",
                    "Amsterdam Avenue",
                ],
                "dropoff_borough": [
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                    "Manhattan",
                ],
                "maximum temperature": [38, 43, 29, 32, 40],
                "precipitation": ["0.00", "0.00", "1.03", "0.00", "0.24"],
            }
        )

        # Create CSV file with test data
        self.file_ = "test_dataset.csv"
        self.data.to_csv(self.file_, index=False)

        # Create instance of NYCTaxiAnalysis class
        self.analysis = NYCTaxiAnalysis(
            dataset=self.file_, lines=None, date_from="2022-01-01", date_to="2022-01-02"
        )

    def tearDown(self) -> None:
        # Remove test dataset after testing
        os.remove(self.file_)

    def test_rides_of_the_day(self):
        # Call the function and get result for test
        result = self.analysis.rides_of_the_day()

        # Assert the function output is type string
        self.assertIsInstance(result, str)

        # Ensure the total number of rides is correct
        self.assertEqual(
            result,
            "For the period January 01, 2022 through January 02, 2022 there were:\n"
            "\t2 rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00);\n"
            "\t1 rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00);\n"
            "\t1 rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00);\n"
            "\t1 rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00).\n"
            "TOTAL: 5\n",
        )

        # Ensure the output includes the expected number of rides for each time period
        self.assertIn(
            "2 rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00)",
            result,
        )
        self.assertIn(
            "1 rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00)",
            result,
        )
        self.assertIn(
            "1 rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00)",
            result,
        )
        self.assertIn(
            "1 rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00)",
            result,
        )

    def test_most_common_locations(self):
        # Call the function and get result for test
        result = self.analysis.most_common_locations()

        # Assert the function output is type string
        self.assertIsInstance(result, str)

        # Assert the function output is correct
        self.assertEqual(
            result,
            "For the period January 01, 2016 through January 02, 2016 there were:\n"
            "\tIn Bronx, there were 0 passenger pickups and 0 drop-offs;\n"
            "\tIn Brooklyn, there were 0 passenger pickups and 0 drop-offs;\n"
            "\tIn Manhattan, there were 5 passenger pickups and 5 drop-offs;\n"
            "\tIn Queens, there were 0 passenger pickups and 0 drop-offs;\n"
            "\tIn Staten Island, there were 0 passenger pickups and 0 drop-offs.\n",
        )

    def test_weather_effect(self):
        # Call the function and get result for test
        result = self.analysis.weather_effect()

        # Assert the function output is type string
        self.assertIsInstance(result, str)

        # Assert the function output is correct
        self.assertEqual(
            result,
            "For the period January 01, 2022 through January 02, 2022 there were:\n"
            "\t3 rides that took place during weather conditions with temperatures below 40° Fahrenheit (4.5° Celsius);\n"
            "\t0 rides that occurred during weather conditions with temperatures exceeding 85° Fahrenheit (29.5° Celsius);\n"
            "\t2 rides that took place during weather conditions with precipitations;\n"
            "\t1 was the number of rides in average weather conditions with no precipitation.\n"
            "TOTAL: 5\n",
        )


if __name__ == "__main__":
    unittest.main()
