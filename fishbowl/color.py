"""
color - Definitions and controls for color palettes

Provides a series of custom qualitative palettes and an interface for saving 
(and developing) additional palettes. All functions which accept a palette
support the `palettable` package. 

This module is used by core to set colors with the simple tools, but can also
be accessed directly to retrieve and customize palettes.
"""

import os
import json
import itertools
import matplotlib

import numpy as np
import matplotlib.pyplot as plt

from cycler import cycler

_json = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__),'config','fishbowl.color.json'))

# Loading and saving colors

def palette_config(palette):
    """
    Return the rcparams needed to set the default cycle to palette
    
    palette can be any name known by fishbowl or previously saved, or a 
    palettable.palette instance.
    """
    return {'axes.prop_cycle':cycler('color',hex_palette(palette))}


def cmap_config(palette):
    """
    Return the rcparams needed to set the default cmap to palette
    
    palette can be any cmap known by matplotlib or a palettable.palette
    instance.
    """
    name, cmap = cmap_palette(palette)
    matplotlib.cm.register_cmap(name, cmap)
    return {'image.cmap':name}
    


def cmap_palette(palette):
    """
    Return the cmap name and cmap instance for palette.

    palette can be any matplotlib cmap name or a palettable.palette instance.
    """
    if hasattr(palette,'hex_colors'):
        return palette.name, palette.mpl_colormap
    else:
        return palette, matplotlib.cm.get_cmap(palette)


def hex_palette(palette):
    """
    Return a list of hex colors that forms the palette.
    
    Name can be any name known by fishbowl or previously saved, or a 
    palettable.palette instance.
    """
    if hasattr(palette,'hex_colors'):
        return palette.hex_colors

    with open(_json,'r') as infile:
        return json.load(infile)[palette]


def save_palette(name, palette):
    """
    Save a new color palette to configuration json.

    palette can be a list of hex colors or a palettable.palette instance
    """
    if hasattr(palette,'hex_colors'):
        palette = palette.hex_colors
        
    with open(_json,'r') as infile:
        palettes = json.load(infile)

    palettes[name] = palette
    with open(_json,'w') as outfile:
        json.dump(palettes, outfile)


# Utility functions for visualizing colors

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
    side = block + 2*sep
    image = np.zeros((side*rows, side*cols))

    # Assign a unique, consecutive value to each color block
    for col in xrange(cols): 
        for row in xrange(rows):
            image[sep+side*row : sep+block+side*row, sep+side*col:sep+block+side*col] = rows*col + row + 1

    # Figure without border or axis, sized to just contain the blocks
    fig = plt.figure(frameon=False, figsize=(cols,rows))
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Show it as an image, using one color per box value in a cmap
    ax.imshow(image, cmap=matplotlib.colors.ListedColormap([background]+list(itertools.chain(*colors))), interpolation="nearest")
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
    for i in range(1, n+1):
        ax.plot(x, np.sin(x + i * .5) * (n + 1 - i))
    ax.set_axis_off()
    if save_name:
        fig.savefig(save_name, dpi=300)


