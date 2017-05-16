"""
draw - Functions for specific ways to illustrate data
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from functools import wraps
from fishbowl.decorator import setup_axes
from fishbowl.color import next_color


def handle_args(func):
    """ Handle standard arguments for plot style functions
    """
    @wraps(func)
    def default_func(x, y, data=None, **kwargs):
        if data is not None and x in data:
            x = data[x]
        if data is not None and y in data:
            y = data[y]
        ax = kwargs.pop('ax', None)
        if not ax:
            ax = plt.gca()
        return func(x, y, ax, **kwargs)
    return default_func


@handle_args
def line(x, y, ax, **kwargs):
    """ Draw a line connecting discrete points x,y

    Passes kwargs to ax.plot for the line.
    """
    yerr = kwargs.pop('yerr', None)
    lines = ax.plot(x, y, zorder=1, **kwargs)
    if yerr is not None:
        ax.errorbar(x, y,
                    yerr=yerr,
                    marker=None,
                    color=lines[0].get_color(),
                    zorder=1,
                    capsize=0)
    ax.scatter(x, y, marker='o', s=80, color='white', zorder=2)
    ax.scatter(x, y, marker='o', s=10, color=lines[0].get_color(), zorder=3)
    return lines


@handle_args
def bar(labels, heights, ax, **kwargs):
    """ Draw bars with heights and corresponding labels

    Passes kwargs to ax.bar
    """
    width = kwargs.pop('width', 0.36)
    offset = kwargs.pop('offset', 0.0)
    if 'color' in kwargs:
        color = kwargs.pop('color')
    else:
        color = next_color()  # make sure not to advance iterator if not used

    dummy = np.arange(0, len(labels)) + offset
    bars = ax.bar(dummy,
                  heights,
                  width=width,
                  color=color,
                  linewidth=0,
                  **kwargs)
    setup_axes(ax, xticks=dummy + width/2.0, xticklabels=labels)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(4))
    ax.grid(axis='y', color='white', ls='-', lw=1.2)
    ax.set_axisbelow(False)
    ax.tick_params(axis='both', which='both', length=0)
    return bars


@handle_args
def barh(labels, widths, ax, **kwargs):
    """ Draw bars with widths and corresponding labels

    Passes kwargs to ax.barh
    """
    height = kwargs.pop('height', 0.36)
    offset = kwargs.pop('offset', 0.0)
    if 'color' in kwargs:
        color = kwargs.pop('color')
    else:
        color = next_color()  # make sure not to advance iterator if not used

    dummy = np.arange(0, len(labels)) + offset
    bars = ax.barh(dummy,
                   widths,
                   height=height,
                   color=color,
                   linewidth=0,
                   **kwargs)
    setup_axes(ax, yticks=dummy + height/2.0, yticklabels=labels)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(4))
    ax.grid(axis='x', color='white', ls='-', lw=1.2)
    ax.set_axisbelow(False)
    ax.tick_params(axis='both', which='both', length=0)
    return bars
