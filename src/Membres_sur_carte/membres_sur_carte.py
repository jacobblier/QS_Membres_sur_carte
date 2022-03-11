import configparser
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from PIL import Image
import re
import sys

# Import configs
config = configparser.ConfigParser()
config.read(r"donnees/config")
config = config["membres_sur_carte"]

contains_an_empty_config_value = False
for key in config:
    if config[key] == "":
        contains_an_empty_config_value = True
        print(f"`{key}` ne contient aucune valeur.")
if contains_an_empty_config_value:
    print("Il faut mettre une valeur dans chaque variable ci-dessus.")
    print("*** Voir le fichier `config` dans le dossier `donnees`. ***")
    sys.exit(1)


# Bounding box to define default view
# ((longitude_min), (longitude_max), (latitude_min), (latitude_max))
regex_pattern = re.compile("\((.*),(.*)\), *\((.*),(.*)\)")
bounding_box = (
    (
        float(
            regex_pattern.sub(
                r"\2", config["limites_geographiques_a_afficher_par_defaut"]
            )
        )
    ),
    (
        float(
            regex_pattern.sub(
                r"\4", config["limites_geographiques_a_afficher_par_defaut"]
            )
        )
    ),
    (
        float(
            regex_pattern.sub(
                r"\1", config["limites_geographiques_a_afficher_par_defaut"]
            )
        )
    ),
    (
        float(
            regex_pattern.sub(
                r"\3", config["limites_geographiques_a_afficher_par_defaut"]
            )
        )
    ),
)

# Read scatter data
df = pd.read_csv(
    config["chemin_du_fichier_csv_de_coordonnees"].replace(os.sep, "/")
)

# Plot
(
    fig,
    ax,
) = plt.subplots()  # TODO This can probably be cleaner. Look for examples

ax.set_title(config["titre_du_graphique"])
ax.scatter(
    df.longitude,
    df.latitude,
    zorder=1,
    alpha=1,
    c=config["couleur_des_points"],
    s=float(config["taille_des_points"]),
    edgecolors=config["couleur_du_contour_des_points"],
    linewidths=float(config["largeur_du_contour_des_points"]),
)
ax.set_xlim(bounding_box[0], bounding_box[1])
ax.set_ylim(bounding_box[2], bounding_box[3])

# Put background street images
for coord in config["limites_geographiques_des_cartes"].splitlines():
    if coord == "":
        continue
    map_image = Image.open(rf"donnees/carte_{coord}.png")
    x_min = float(coord.split(",")[0])
    x_max = float(coord.split(",")[1])
    y_min = float(coord.split(",")[2])
    y_max = float(coord.split(",")[3])
    ax.imshow(
        map_image,
        aspect="equal",
        extent=((x_min), (x_max), (y_min), (y_max)),
        zorder=0,
    )

plt.show()
