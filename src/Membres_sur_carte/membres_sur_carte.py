# FIXME Change name to "membres_sur_carte.py"
import configparser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

# Import configs
config = configparser.ConfigParser()
config.read(r"data/config")
config = config["membres_sur_cartes"]

# TODO Use the config
# TODO Check for empty values
if config["longitude_min_affichee_par_defaut"] == "":
    pass

# Bounding box to define default view
# TODO Use the config
bounding_box = (
    (-73.6505),
    (-73.6069),
    (45.5225),
    (45.5547),
)

# Read scatter data
df = pd.read_csv(
    r"data/adresses,latitude,longitude.csv"
)  # TODO Use the config

# Plot
(
    fig,
    ax,
) = plt.subplots()  # TODO This can probably be cleaner. Look for examples

ax.set_title("QS membres")  # TODO Use the config
ax.scatter(
    df.longitude,
    df.latitude,
    zorder=1,
    alpha=1,
    c="b",  # TODO Use the config
    s=20,  # TODO Use the config
    edgecolors="k",  # TODO Use the config
    linewidths=1,  # TODO Use the config
)
ax.set_xlim(bounding_box[0], bounding_box[1])
ax.set_ylim(bounding_box[2], bounding_box[3])

# Put background street images
for x_min in np.arange(-73.65, -73.61, 0.02):  # TODO Use the config
    x_max = x_min + 0.02
    for y_min in np.arange(45.52, 45.56, 0.01):  # TODO Use the config
        y_max = y_min + 0.01
        map_image = Image.open(
            rf"data/carte_{x_min:.2f},{x_max:.2f},{y_min:.2f},{y_max:.2f}.png"
        )
        ax.imshow(
            map_image,
            aspect="equal",
            extent=((x_min), (x_max), (y_min), (y_max)),
            zorder=0,
        )

plt.show()
