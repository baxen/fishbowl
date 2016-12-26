"""
fishbowl - Style options and customization for matplotlib

fishbowl provides a minimalist style for matplotlib plots, including nice
presets for axes, colors, and fonts.

Call set_style() to enable globally or use style() in a with statement.

If you want to make full use of the font features, you need the 'pgf' backend.
The easiest way to do this is usually:

>>> import matplotlib
>>> matplotlib.use('pgf')
>>> import fishbowl
>>> import matplotlib.pyplot as plt

Modules:

core -- Style setup and control tools

"""

from fishbowl.core import (style, set_style,  # noqa: F401
                           get_style, reset_style)
from fishbowl.decorator import plot  # noqa: F401
