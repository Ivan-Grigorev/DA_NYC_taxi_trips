import pandas as pd

from datetime import datetime


pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 1000)


class NYCTaxiAnalysis:
    def __init__(self, dataset, date_from: str, date_to: str, lines=None):
        # Filter dataset by date
        self.data = (
            pd.read_csv(dataset)
            .query("@date_from <= pickup_datetime <= @date_to")
            .sort_values(by='pickup_datetime')
            .head(lines)
        )

        self.morning_rides = None
        self.afternoon_rides = None
        self.evening_rides = None
        self.night_rides = None
        self.date_from = date_from
        self.date_to = date_to

    def rides_of_the_day(self):
        """
        1. Analyze taxi rides based on time of day.
        """
        # This function analyze taxi rides based on time of day: morning, afternoon, evening, late night/early morning
        try:
            # Convert pickup_datetime column to datetime dtypes
            self.data["pickup_datetime"] = pd.to_datetime(self.data["pickup_datetime"], format="%Y-%m-%d %H:%M:%S")

            # Calculate the number of rides for each time period
            self.morning_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("06:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("12:00:00").time())
                ]

            self.afternoon_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("12:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("18:00:00").time())
                ]

            self.evening_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("18:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("23:59:59").time())
                ]

            self.night_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("00:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("06:00:00").time())
                ]

            return (
                f"For the period {datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%B %d, %Y')}"
                f" through {datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%B %d, %Y')} there were:\n"
                f"\t{len(self.morning_rides)} rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00);\n"
                f"\t{len(self.afternoon_rides)} rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00);\n"
                f"\t{len(self.evening_rides)} rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00);\n"
                f"\t{len(self.night_rides)} rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00).\n"
                f"TOTAL: {sum([len(self.morning_rides), len(self.afternoon_rides), len(self.evening_rides), len(self.night_rides)])}"
            )

        except KeyError as err:
            # Display error message in error key
            return f"WARNING! The function {NYCTaxiAnalysis.rides_of_the_day.__name__}() error - {err}"

    def most_common_locations(self):
        """
        2. Identify popular pickup and drop-off locations.
        """
        # This function count number of locations.
        pickup_bronx_number = self.data[self.data['pickup_borough'] == 'Bronx'].__len__()
        dropoff_bronx_number = self.data[self.data['dropoff_borough'] == 'Bronx'].__len__()

        pickup_brooklyn_number = self.data[self.data['pickup_borough'] == 'Brooklyn'].__len__()
        dropoff_brooklyn_number = self.data[self.data['dropoff_borough'] == 'Brooklyn'].__len__()

        pickup_manhattan_number = self.data[self.data['pickup_borough'] == 'Manhattan'].__len__()
        dropoff_manhattan_number = self.data[self.data['dropoff_borough'] == 'Manhattan'].__len__()

        pickup_queens_number = self.data[self.data['pickup_borough'] == 'Queens'].__len__()
        dropoff_queens_number = self.data[self.data['dropoff_borough'] == 'Queens'].__len__()

        pickup_staten_island_number = self.data[self.data['pickup_borough'] == 'Staten Island'].__len__()
        dropoff_staten_island_number = self.data[self.data['dropoff_borough'] == 'Staten Island'].__len__()

        return (
            f"For the period {datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%B %d, %Y')}"
            f" through {datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%B %d, %Y')} there were:\n"
            f"\tIn Bronx, there were {pickup_bronx_number} of passenger pickups "
            f"and {dropoff_bronx_number} drop-offs;\n"
            f"\tIn Brooklyn, there were {pickup_brooklyn_number} passenger pickups "
            f"and {dropoff_brooklyn_number} drop-offs;\n"
            f"\tIn Manhattan, there were {pickup_manhattan_number} passenger pickups "
            f"and {dropoff_manhattan_number} drop-offs;\n"
            f"\tIn Queens, there were {pickup_queens_number} passenger pickups "
            f"and {dropoff_queens_number} drop-offs;\n"
            f"\tIn Staten Island, there were {pickup_staten_island_number} passenger pickups "
            f"and {dropoff_staten_island_number} drop-offs."
        )

    def weather_by_day(self):
        """
        3. Analyze the impact of weather on taxi rides.
        """
        weather_data = pd.read_csv("CSV/datasets/nyc_weather_central_park.csv")
        return weather_data

    def analysis_visualization(self):
        # self.pickup_dropoff_addresses()
        new_data = pd.read_csv('CSV/nyc_taxi.csv').head(1)
        return new_data.loc[0, 'pickup_longitude'], new_data.loc[0, 'pickup_latitude']


if __name__ == "__main__":
    nyc_taxi_analysis = NYCTaxiAnalysis(
        dataset="CSV/datasets/nyc_taxi_trips.csv",
        date_from="2016-01-01",
        date_to="2016-12-31",
        # lines=2,
    )

    # print(nyc_taxi_analysis.rides_of_the_day())
    # print(nyc_taxi_analysis.pickup_dropoff_addresses())
    # print(nyc_taxi_analysis.weather_by_day())

    print(nyc_taxi_analysis.analysis_visualization())
