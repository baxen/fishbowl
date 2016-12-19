"""
core - Style setup and control tools.

Provides simple tools for setting style that should be used the majority
of the time when creating graphics.

style       - Set style temporarily within a ``with`` statement
set_style   - Globally set style according to provided options
reset_style - Globally reset style to matplotlib defaults
get_style   - Return the current style options dictionary
"""

import matplotlib
from fishbowl import color
from fishbowl import font as ft
from fishbowl import axes as ax

from contextlib import contextmanager
from cycler import cycler


_defaultparams = matplotlib.rcParams.copy()
_defaultinit = matplotlib.axes.Axes.__init__


# ------------------------------------------------------------
# Style Configuration
# ------------------------------------------------------------

def _set_style(options):
    """ Internal implementation of style setting.

    """
    _set_style.current_options = options

    # This is a monkey patch to handle some axes styles that
    # cannot be configured in the rc parameters
    # It should be safe in the majority of cases because
    # the decorators only register additional function calls
    # and do not replace the original function
    initialize = options.pop('axes.initialize', None)
    if initialize in ax._initialize_decorators:
        matplotlib.axes.Axes.__init__ = ax._initialize_decorators[initialize](_defaultinit)
    else:
        matplotlib.axes.Axes.__init__ = _defaultinit

    palette = options.pop('color.palette', None)
    if palette:
        options['axes.prop_cycle'] = cycler('color', palette)

    # Remaining options are rcParams
    matplotlib.rcParams.update(options)


_set_style.current_options = _defaultparams.copy()


def reset_style():
    """ Return the style to matplotlib defaults.

    """
    soptions = _defaultparams.copy()
    set_style(style=soptions)


def get_style():
    """ Return a complete style dictionary matching the current style.

    This dictionary is mostly the rc parameters from matplotlib, with
    a few additional options handled by set_style.

    """
    return _set_style.current_options.copy()


def set_style(axes='minimal', palette='goldfish',
              cmap='YlGnBu', font='Inconsolata', style=None):
    """ Set the global style.

    Parameters
    ----------
    axes
        The style option for axes that controls x/y-axis, ticks, grid, etc...
        Accepts names of saved axes styles
    palette
        color palette for consecutive objects
        Accepts names of saved palettes or palettable.palette instances
    cmap
        Name of the cmap to use for 2D plots.
        Accepts names of matplotlib cmaps or palettable.palette instances
    fonts
         Name of the font style to use, typically just a font name
         Accepts names of saved font configurations or names of system fonts.
    style
         A dictionary that contains all style options
         If provided other keywords are ignored

    """

    if style:
        _set_style(style)
        return

    style = get_style()

    # Colors
    style.update(color.palette(palette))
    style.update(color.cmap(cmap))

    # Axes
    style.update(ax.axes(axes))

    # Fonts
    style.update(ft.font(font))

    _set_style(style)


@contextmanager
def style(**kwargs):
    """ Context manager for using style settings temporarily.

    See Also
    --------
    set_style: called with kwargs within the context

    """
    initial_style = get_style()
    set_style(**kwargs)
    yield
    set_style(style=initial_style)
