import seaborn as sns
import numpy as np
from ipywidgets import interact, FloatSlider


def get_colors(length):
    colors = sns.color_palette(n_colors=length)

    rgbs = []
    for color in colors:
      rgb = "rgb(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
      rgbs.append(rgb)
    return rgbs
