import unittest
import pandas as pd

from handler import pickup_dropoff_addresses


class TestPickupDropoffAddresses(unittest.TestCase):
    def test_pickup_dropoff_addresses(self):
        # Ensure the pickup and dropoff addresses are correctly retrieved
        addresses = pickup_dropoff_addresses('CSV/test_data.csv')

        # self.assertIsNotNone(self.analysis.pickup_coordinates)
        # self.assertIsNotNone(self.analysis.dropoff_coordinates)

        # self.assertEqual(
        #     addresses.loc[0, "pickup_address"],
        #     "Spectrum, 261, 3rd Avenue, Manhattan Community Board 6, "
        #     "Manhattan, New York County, City of New York, New York, 10010, United States",
        # )
        # self.assertEqual(
        #     addresses.loc[0, "dropoff_address"],
        #     "Pennsylvania Station, Lincoln Tunnel Expressway, Chelsea District, "
        #     "Manhattan, New York County, City of New York, New York, 10119, United States",
        # )
        # self.assertEqual(
        #     addresses.loc[2, "pickup_address"],
        #     "251, Church Street, Manhattan Community Board 1, "
        #     "Manhattan, New York County, City of New York, New York, 10013, United States",
        # )
        # self.assertEqual(
        #     addresses.loc[2, "dropoff_address"],
        #     "258, West 4th Street, Manhattan Community Board 2, "
        #     "Manhattan, New York County, City of New York, New York, 10014, United States",
        # )


if __name__ == "__main__":
    unittest.main()
