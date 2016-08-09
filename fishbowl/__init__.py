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

TODO
Migrate examples stored in core to individual modules for color, axes, fonts
Create support for customizations and storing them! jsons?
"""

from fishbowl.core import style, set_style, get_style, reset_style
