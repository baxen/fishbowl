"""
color - Definitions and controls for color palettes

Provides a series of custom qualitative palettes and an interface for saving
(and developing) additional palettes. All functions which accept a palette
support the `palettable` package.

This module is used by core to set colors with the simple tools, but can also
be accessed directly to retrieve and customize palettes.
"""

import itertools
import matplotlib

import numpy as np
import matplotlib.pyplot as plt

from cycler import cycler
from fishbowl.base import loads_from_json, saves_to_json


def cmap(arg):
    """
    Return configuration for cmap specified by arg

    Arg can be any cmap known by matplotlib or a palettable.palette instance.
    """
    if hasattr(arg, 'mpl_colormap'):
        matplotlib.cm.register_cmap(arg.name, arg.mpl_colormap)
        return {'image.cmap': arg.name}
    elif isinstance(arg, str):
        return {'image.cmap': arg}
    else:
        raise ValueError('Could not interpret the argument provided for cmap: ' + str(arg))


@loads_from_json('fishbowl.palettes.json')
def palette(arg):
    """
    Return configuration for palette specified by arg

    Arg can be any name known by fishbowl or previously saved, or a
    palettable.palette instance.
    """
    if hasattr(arg, 'hex_colors'):
        return {'color.palette': arg.hex_colors}


@saves_to_json('fishbowl.palettes.json')
def save_palette(name, config):
    """
    Save a new color palette as name.

    config can be a list of hex colors, a palettable.palette instance, or a
    previously known palette.
    """
    return palette(config)

# ------------------------------------------------------------
# Utility functions for visualizing colors
# ------------------------------------------------------------


def draw_box_palette(colors, save_name=None, block=10, sep=1, background='white'):
    """
    Draw a series of boxes of color in a grid to show a palette.

    args:
    colors -- a list or list of lists of colors for the boxes
              A list of lists is drawn as a 2D grid
              Each entry must be a color understood by matplotlib.

    kwargs:
    save_name  -- If provided, saves plot to save_name
    block      -- Size of the side of each box (pixels)
    sep        -- Separation between each box (pixels)
    background -- Color of the background between palettes
    """
    if not hasattr(colors[0], "__iter__"):
        colors = [colors]

    # Calculate pixel sizes
    rows = len(colors)
    cols = len(colors[0])
    side = block + 2 * sep
    image = np.zeros((side * rows, side * cols))

    # Assign a unique, consecutive value to each color block
    for col in range(cols):
        for row in range(rows):
            image[sep + side * row: sep + block + side * row, sep +
                  side * col:sep + block + side * col] = rows * col + row + 1

    # Figure without border or axis, sized to just contain the blocks
    fig = plt.figure(frameon=False, figsize=(cols, rows))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Show it as an image, using one color per box value in a cmap
    ax.imshow(image, cmap=matplotlib.colors.ListedColormap(
        [background] + list(itertools.chain(*colors))), interpolation="nearest")
    if save_name:
        fig.savefig(save_name, dpi=120)


def draw_sin_palette(colors, save_name=None):
    """
    Draw a series of sin waves in each color to show a palette.

    args:
    colors -- a list of colors
              Each entry must be a color understood by matplotlib.

    kwargs:
    save_name  -- If provided, saves plot to save_name
    """
    fig, (ax) = plt.subplots()
    ax.set_prop_cycle(cycler('color', colors))
    n = len(colors)
    x = np.linspace(-5, 5, 100)
    for i in range(1, n + 1):
        ax.plot(x, np.sin(x + i * .5) * (n + 1 - i))
    ax.set_axis_off()
    if save_name:
        fig.savefig(save_name, dpi=300)
