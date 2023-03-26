import pandas as pd


pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)


class HandleDatasets:
    def __init__(self, trips_file, addresses_file, weather_file, data, lines=None):
        self.trips = pd.read_csv(trips_file, low_memory=False).head(lines)
        self.addresses = pd.read_csv(addresses_file, low_memory=False).head(lines)
        self.weather = pd.read_csv(weather_file, low_memory=False).head(lines)
        self.data = data

    def pickup_dropoff_addresses(self):
        for index, row in self.addresses.iterrows():
            string_ = row['the_geom'].replace('MULTILINESTRING ((', '').replace('))', '')
            self.addresses.loc[index, 'the_geom'] = string_
        self.addresses.to_csv('CSV/datasets/nyc_streets.csv', index=False)


if __name__ == '__main__':
    handle_datasets = HandleDatasets(
        trips_file='CSV/datasets/nyc_taxi_trips.csv',
        addresses_file='CSV/datasets/Centerline.csv',
        weather_file='CSV/datasets/nyc_weather_central_park.csv',
        data='CSV/nyc_taxi.csv',
        # lines=5
    )

    handle_datasets.pickup_dropoff_addresses()
