import configparser
import csv
import geopy

# TODO Use the config
# TODO Check for empty values
config = configparser.ConfigParser()


geolocator = geopy.geocoders.GoogleV3(
    api_key="Enter api key here",  # TODO Use the config for api_key
    domain="maps.google.ca",
)

postal_addresses = []

# Read addresses from file "addresses.csv" in "data" folder
with open(r"data/adresses.csv") as data_file:  # TODO Use the config
    csv_reader = csv.reader(data_file)
    for row in csv_reader:
        postal_addresses.append(row)

# Fetch and write latitude and longitude to "adresses,latitude,longitude.csv" file in "data" folder
with open(
    r"data/adresses,latitude,longitude.csv", "w+"
) as csvfile:  # TODO Use the config
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["address"] + ["latitude"] + ["longitude"])
    for postal_address in postal_addresses:
        postal_address = postal_address[0]
        location = geolocator.geocode(
            query=postal_address,
            components={"city": "montreal"},  # TODO Use the config
            bounds=[(45.59, -73.72), (45.53, -73.60)],  # TODO Use the config
        )
        # TODO Make the following value configurable
        # TODO Make the following check more robust
        if int(location.latitude) != 45:
            # TODO Export the errors in the file specified in the config
            print(
                f"{postal_address} not found [{location.latitude}, {location.longitude}]"
            )
            latitude = 0.0
            longitude = 0.0
        else:
            latitude = location.latitude
            longitude = location.longitude
        csv_writer.writerow([postal_address] + [latitude] + [longitude])
