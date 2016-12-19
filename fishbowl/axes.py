"""
axes - Configuration of matplotlib axes
"""
from functools import wraps
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


def _despined(init):
    """ Decorator to remove spines

    Makes the constructor of pyplot.Axes
    return an axes without left right or top spines.
    """
    @wraps(init)
    def despined_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        for spine in ["left", "right", "top"]:
            self.spines[spine].set_visible(False)
        self.xaxis.tick_bottom()
        self.yaxis.tick_right()
        for tick in self.xaxis.get_major_ticks():
            tick.gridline.set_visible(False)
    return despined_init


_initialize_decorators = {'despined': _despined}
