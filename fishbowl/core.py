"""
core - Style setup and control tools.

Provides simple tools for setting style that should be used the majority
of the time when creating graphics.

style       - Set style temporarily within a ``with`` statement
set_style   - Globally set style according to provided options
reset_style - Globally reset style to matplotlib defaults
get_style   - Return the current style options dictionary
"""

import functools

import matplotlib

from .color import palette_config, cmap_config

_defaultparams = matplotlib.rcParams.copy()
_defaultinit = matplotlib.axes.Axes.__init__


def _despined(init):
    """
    Decorator to make the constructor of pyplot.Axes
    return an axes with despined up spines, grid, and ticks.
    """
    @functools.wraps(init)
    def despined_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        for spine in ["left", "right", "top"]:
            self.spines[spine].set_visible(False)
        self.xaxis.tick_bottom()
        self.yaxis.tick_right()
        for tick in self.xaxis.get_major_ticks():
            tick.gridline.set_visible(False)
    return despined_init


class _Style(dict):
    """
    Internal class to handle temporary styling.
    """
    def __enter__(self):
        self._original = get_style()
        set_style(**self)
        
    def __exit__(self, t, v, traceback):
        set_style(style=self._original)


def reset_style():
    """
    Return the style to matplotlib defaults.
    """
    soptions = _defaultparams.copy()
    set_style(style=soptions)


def get_style():
    """
    Return a complete style dictionary matching the current style.

    This dictionary is mostly the rc parameters from matplotlib, with
    a few additional options handled by set_style.
    """
    return _set_style.current_options.copy()

    
def _set_style(options):
    """
    Internal implementation of style setting.
    """
    _set_style.current_options = options

    # This is a trick to handle some axes styles that
    # cannot be configured in the rc parameters
    # The init function for axes is modified to make necessary edits
    # on construction
    if options.pop('axes.despined', None):
        matplotlib.axes.Axes.__init__ = _despined(_defaultinit)
    else:
        matplotlib.axes.Axes.__init__ = _defaultinit
    
    # Remaining options are rcParams
    matplotlib.rcParams.update(options)

_set_style.current_options = _defaultparams.copy()


def set_style(axes='minimal', palette='goldfish', fonts='inconsolata', cmap='YlGnBu', style=None):
    """
    Set the global style.

    Kwargs:
    axes   -- The style option for axes that controls x/y-axis, ticks, grid, etc...
    palette -- color palette for 
               Accepts 
    fonts  -- Name of the font style to use, typically just a font name
    style  -- A dictionary that contains all style options 
              If provided other keywords are ignored
    """

    if style:
        _set_style(style)
        return

    style = get_style()

    # Colors
    style.update(palette_config(palette))
    style.update(cmap_config(cmap))    
    
    # Axes
    style.update(_axes_style[axes])
    
    # Fonts
    style.update(_fonts_style[fonts])

    _set_style(style)


def style(**kwargs):
    """
    Return a style object to use temporarily in a ``with`` statement.

    See documentation for set_style for kwargs.
    """
    return _Style(kwargs)


# TODO
# Move these into separate modules and/or json files

_axes_style = {}
_axes_style['minimal'] = {
    'axes.edgecolor'    : 'black', # For a pronounced x-axis relative to grid lines
    'axes.grid'         : True,
    'axes.facecolor'    : 'white',
    'axes.axisbelow'    : True,  # Precendence for data
    'axes.despined'     : True,
    'grid.color'        : '#e0e0e0',
    'grid.linestyle'    : '-',
    'grid.linewidth'    : 1.0,
    'lines.linewidth'   : 2.5 ,
    'xtick.direction'   : 'out',
    'xtick.major.size'  : 6, # Only xticks
    'xtick.major.width' : 1,
    'xtick.minor.size'  : 0,
    'ytick.major.size'  : 0,
    'ytick.minor.size'  : 0,
    'legend.numpoints'  : 1,
    'legend.frameon'    : False,
}

_fonts_style = {}
_fonts_style['inconsolata'] = {
    'backend'       : 'pgf',
    'font.family'   : 'serif', # Controlled through mathspec below
    'font.size'     : '20',    # Controlled through mathspec below
    'text.usetex'   : True,
    'pgf.texsystem' : 'xelatex',
    'pgf.rcfonts'   : False,   # don't setup fonts from rc parameters 
    'pgf.preamble'  : [r"\usepackage{mathspec}", r"\setallmainfonts(Digits,Latin,Greek){Inconsolata}"]
}
