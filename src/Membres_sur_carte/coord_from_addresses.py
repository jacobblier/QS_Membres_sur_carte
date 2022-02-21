import geopy

import csv

geolocator = geopy.geocoders.Nominatim(user_agent="Membres_sur_carte")

postal_addresses = []

# Read addresses from file "addresses.csv" in "data" folder
with open(r"data/adresses.csv") as data_file:
    csv_reader = csv.reader(data_file)
    for row in csv_reader:
        postal_addresses.append(row)

# Fetch and write latitude and longitude to "addresses,latitude,longitude.csv" file in "data" folder
with open(r"data/addresses,latitude,longitude.csv", "w+") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["address"] + ["latitude"] + ["longitude"])
    for postal_address in postal_addresses:
        postal_address = postal_address[0]
        location = geolocator.geocode(
            query={postal_address[0]},
            country_codes="ca",
        )
        csv_writer.writerow(
            [postal_address] + [location.latitude] + [location.longitude]
        )
