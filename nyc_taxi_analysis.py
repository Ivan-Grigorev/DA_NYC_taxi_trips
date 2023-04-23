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
            .sort_values(by="pickup_datetime")
            .head(lines)
        )
        self.date_from = date_from
        self.date_to = date_to

    def rides_of_the_day(self):
        """
        1. Analyze taxi rides based on time of day.
        """
        # This function analyze taxi rides based on time of day: morning, afternoon, evening, late night/early morning
        try:
            # Convert pickup_datetime column to datetime dtypes
            self.data["pickup_datetime"] = pd.to_datetime(
                self.data["pickup_datetime"], format="%Y-%m-%d %H:%M:%S"
            )

            # Calculate the number of rides for each time period
            morning_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("06:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("12:00:00").time())
                ]

            afternoon_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("12:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("18:00:00").time())
                ]

            evening_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("18:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("23:59:59").time())
                ]

            night_rides = self.data.loc[
                (self.data["pickup_datetime"].dt.time >= pd.to_datetime("00:00:00").time())
                & (self.data["pickup_datetime"].dt.time <= pd.to_datetime("06:00:00").time())
                ]

            return (
                f"For the period {datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%B %d, %Y')}"
                f" through {datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%B %d, %Y')} there were:\n"
                f"\t{len(morning_rides)} rides from 6:00 a.m. (06:00:00) to 12:00 p.m. (12:00:00);\n"
                f"\t{len(afternoon_rides)} rides from 12:00 p.m. (12:00:00) to 6:00 p.m. (18:00:00);\n"
                f"\t{len(evening_rides)} rides from 6:00 p.m. (18:00:00) to 12 a.m. (00:00:00);\n"
                f"\t{len(night_rides)} rides from 12:00 a.m. (00:00:00) to 6:00 a.m. (06:00:00).\n"
                f"TOTAL: {sum([len(morning_rides), len(afternoon_rides), len(evening_rides), len(night_rides)])}"
            )

        except KeyError as err:
            # Display error message in error key
            return f"WARNING! The function {NYCTaxiAnalysis.rides_of_the_day.__name__}() error - {err}"

    def most_common_locations(self):
        """
        2. Identify popular pickup and drop-off locations.
        """
        # This function counts the number of locations.
        bronx_pickups, bronx_dropoffs = (
            self.data[["pickup_borough", "dropoff_borough"]].eq("Bronx").sum()
        )
        brooklyn_pickups, brooklyn_dropoffs = (
            self.data[["pickup_borough", "dropoff_borough"]].eq("Brooklyn").sum()
        )
        manhattan_pickups, manhattan_dropoffs = (
            self.data[["pickup_borough", "dropoff_borough"]].eq("Manhattan").sum()
        )
        queens_pickups, queens_dropoffs = (
            self.data[["pickup_borough", "dropoff_borough"]].eq("Queens").sum()
        )
        staten_island_pickups, staten_island_dropoffs = (
            self.data[["pickup_borough", "dropoff_borough"]].eq("Staten Island").sum()
        )

        return (
            f"For the period {datetime.strptime(self.date_from, '%Y-%m-%d').strftime('%B %d, %Y')}"
            f" through {datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%B %d, %Y')} there were:\n"
            f"\tIn Bronx, there were {bronx_pickups} passenger pickups and {bronx_dropoffs} drop-offs;\n"
            f"\tIn Brooklyn, there were {brooklyn_pickups} passenger pickups and {brooklyn_dropoffs} drop-offs;\n"
            f"\tIn Manhattan, there were {manhattan_pickups} passenger pickups and {manhattan_dropoffs} drop-offs;\n"
            f"\tIn Queens, there were {queens_pickups} passenger pickups and {queens_dropoffs} drop-offs;\n"
            f"\tIn Staten Island, there were {staten_island_pickups} passenger pickups and {staten_island_dropoffs} drop-offs."
        )

    def weather_by_day(self):
        """
        3. Analyze the impact of weather on taxi rides.
        """
        weather_data = pd.read_csv("CSV/datasets/nyc_weather_central_park.csv")
        return weather_data

    def analysis_visualization(self):
        print(self.rides_of_the_day(), '\n')
        print(self.most_common_locations())

    def __repr__(self):
        return self.data


if __name__ == "__main__":
    nyc_taxi_analysis = NYCTaxiAnalysis(
        dataset="CSV/nyc_taxi.csv",
        date_from="2016-01-01",
        date_to="2016-12-31",
        # lines=5,
    )

    # print(nyc_taxi_analysis.rides_of_the_day())
    # print(nyc_taxi_analysis.most_common_locations())
    # print(nyc_taxi_analysis.weather_by_day())

    nyc_taxi_analysis.analysis_visualization()
    # print(nyc_taxi_analysis.__repr__())
