"""
font - Configurations for system fonts through latex
"""

from fishbowl.base import loads_from_json, saves_to_json


@loads_from_json('fishbowl.font.json')
def font(name, size=20):
    """ Return configuration for named font

    If a saved font config is not found, assumes the named font is a system
    font and attempts to use it through pgf and xelatex.
    """
    config = {'font.family': 'serif',
              'font.serif': name,
              'font.size': size}
    return config


@saves_to_json('fishbowl.font.json')
def save_font(name, config):
    """ Save a new font specified by config as name.

    Parameters
    ----------
    name : str
        save name for the font
    config
        a dictionary of params or a named font
    """
    if isinstance(config, dict):
        return config
    return font(config)
