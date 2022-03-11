import configparser
import csv
import geopy
import re
import sys

# Import configs
config = configparser.ConfigParser()
config.read(r"donnees/config")
config = config["coordonnees_a_partir_d_adresses"]

contains_an_empty_config_value = False
for key in config:
    if config[key] == "":
        contains_an_empty_config_value = True
        print(f"`{key}` ne contient aucune value.")
if contains_an_empty_config_value:
    print("Il faut mettre une valeur dans chaque variable ci-dessus.")
    print("*** Voir le fichier `config` dans le dossier `donnees`. ***")
    sys.exit(1)

# Variable initialization
geolocator = geopy.geocoders.GoogleV3(
    api_key=config["cle_api_Google"],
    domain="maps.google.ca",
)

postal_addresses = []

cities_to_search_in = []
for single_city in config["villes_dans_lesquelles_chercher"].splitlines():
    if single_city == "":
        continue
    if ("city", single_city) not in cities_to_search_in:
        cities_to_search_in.append(("city", single_city))
if len(cities_to_search_in) == 1:
    # Transform list of tuple into dictionary
    cities_to_search_in = {"city": cities_to_search_in[0][1]}

regex_pattern = re.compile("\((.*),(.*)\), *\((.*),(.*)\)")
latitude1 = float(
    regex_pattern.sub(r"\1", config["limites_geographiques_ou_chercher"])
)
longitude1 = float(
    regex_pattern.sub(r"\2", config["limites_geographiques_ou_chercher"])
)
latitude2 = float(
    regex_pattern.sub(r"\3", config["limites_geographiques_ou_chercher"])
)
longitude2 = float(
    regex_pattern.sub(r"\4", config["limites_geographiques_ou_chercher"])
)
bounding_box_to_search_in = [(latitude1, longitude1), (latitude2, longitude2)]

# Read addresses from file "addresses.csv" in "data" folder
with open(config["chemin_du_fichier_csv_d_adresses"]) as data_file:
    csv_reader = csv.reader(data_file)
    for row in csv_reader:
        postal_addresses.append(row)

# Fetch and write latitude and longitude to "adresses,latitude,longitude.csv" file in "data" folder
with open(config["chemin_du_fichier_csv_de_coordonnees"], "w+") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["address"] + ["latitude"] + ["longitude"])
    for postal_address in postal_addresses:
        postal_address = postal_address[0]
        location = geolocator.geocode(
            query=postal_address,
            components=cities_to_search_in,
            bounds=bounding_box_to_search_in,
        )

        # If the latitude and longitude are not inside the bounding box
        if not (
            min(
                bounding_box_to_search_in[0][0],
                bounding_box_to_search_in[1][0],
            )
            < float(location.latitude)
            < max(
                bounding_box_to_search_in[0][0],
                bounding_box_to_search_in[1][0],
            )
        ) or not (
            min(
                bounding_box_to_search_in[0][1],
                bounding_box_to_search_in[1][1],
            )
            < float(location.longitude)
            < max(
                bounding_box_to_search_in[0][1],
                bounding_box_to_search_in[1][1],
            )
        ):
            error_text = (
                f"{postal_address} a ete trouve aux coordonnees ({location.latitude:.7f}, "
                f"{location.longitude:.7f}) qui sont a l'exterieur des limites geographiques "
                f"specifiees. Verifiez l'adresse ou cherchez les coordonnees manuellement."
            )
            with open(
                config["chemin_du_fichier_d_erreurs"], "w+"
            ) as error_file:
                print(error_text)
                print(error_text, file=error_file)
            latitude = 0.0
            longitude = 0.0
        else:
            latitude = location.latitude
            longitude = location.longitude
        csv_writer.writerow([postal_address] + [latitude] + [longitude])
