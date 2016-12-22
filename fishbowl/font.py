"""
font - Configurations for system fonts through latex
"""

from fishbowl.base import loads_from_json, saves_to_json


def _pgf_params(name):
    """ PGF parameters configured for the font name
    """
    preamble = [r"\usepackage{mathspec}",
                r"\setallmainfonts(Digits,Latin,Greek){{{}}}".format(name)]
    return {'font.family': 'serif',  # Controlled through mathspec below
            'font.size': '20',    # Controlled through mathspec below
            'pgf.texsystem': 'xelatex',
            'pgf.rcfonts': False,   # don't setup fonts from rc parameters
            'pgf.preamble': preamble
            }


@loads_from_json('fishbowl.font.json')
def font(name):
    """ Return configuration for named font

    If a saved font config is not found, assumes the named font is a system
    font and attempts to use it through pgf and xelatex.
    """
    return _pgf_params(name)


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
