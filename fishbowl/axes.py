"""
axes - Configuration of matplotlib axes
"""
from fishbowl.base import loads_from_json, saves_to_json


@loads_from_json('fishbowl.axes.json')
def axes(name):
    """ Configuration for named axes

    name must be a saved (or default) configuration
    """
    # Only handled through the save/load system
    pass


@saves_to_json('fishbowl.axes.json')
def save_axes(name, config):
    """ Save a new axes style as name.

    Parameters
    ----------
    name
        save name for the axes configuration
    config
        can be a dictionary of params or a named axes style
    """
    if isinstance(config, dict):
        return config
    return axes(config)
