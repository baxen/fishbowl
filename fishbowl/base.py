"""
base - Utilities for saving/loading configurations.
"""

import os
import json

from functools import wraps


def _config_path(path):
    """ Absolute path to file in configuration directory for module.

    """
    return os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__),
                                         'config',
                                         path))


def loads_from_json(path):
    """ Decorator to make function first return values saved at json path.

    Assumes the first argument is the dictionary key if intended to load from
    file. The function is assumed to handle all cases where the key is not
    found in json.
    """
    def loads_from_json_dec(func):
        # Assign a json path to the function for reading
        func._json = _config_path(path)

        @wraps(func)
        def json_load_func(*args, **kwargs):
            if os.path.exists(func._json) and len(args) == 1:
                with open(func._json, 'r') as infile:
                    saved_values = json.load(infile)
                if args[0] in saved_values:
                    return saved_values[args[0]]
            val = func(*args, **kwargs)
            if val:
                return val
            raise ValueError('Could not interpret argument "'
                             + str(args[0])
                             + '" and no saved value found.')
        return json_load_func
    return loads_from_json_dec


def saves_to_json(path):
    """ Decorator to create functions which save their outputs to json file.

    Assumes first argument is the dictionary key to save to the file, and
    returns the saved value.
    """
    def saves_to_json_dec(func):
        # Assign a json path to the function for writing
        func._json = _config_path(path)

        @wraps(func)
        def json_save_func(*args, **kwargs):
            value = func(*args, **kwargs)

            if os.path.exists(func._json):
                with open(func._json, 'r') as infile:
                    saved_values = json.load(infile)
            else:
                saved_values = {}
            saved_values[args[0]] = value

            with open(func._json, 'w') as outfile:
                json.dump(saved_values, outfile)
            return value
        return json_save_func
    return saves_to_json_dec
