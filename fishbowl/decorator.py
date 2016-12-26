import itertools
import pydoc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.offsetbox as offsetbox

from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from functools import wraps


def _decorate_all(decorators):
    """ Decorate a function with all decorators

    """
    def decorator(f):
        for d in reversed(decorators):
            f = d(f)
        return f
    return decorator


def _plot_helper(func):
    """ Internally mark a function to be used as a plot helper

    Each function marked this way should accept ax, **kwargs
    """
    _plot_helper._functions.append(func)
    return func


_plot_helper._functions = []


@_plot_helper
def setup_axes(ax, **kwargs):
    """ Setup an axis with passed arguments.

    A shortcut for calls of a bunch of axes member functions.
    Additional kwargs are ignored to facilitate argument passing.

    Parameters
    ----------
    title : str
        Text to be placed on top center of axes.
    xmin : float
        Set minimum of x-axis.
    xmax : float
        Set maximum of x-axis.
    ymin : float
        Set minimum of y-axis.
    ymax : float
        Set maximum of y-axis.
    xlabel : str
        Label for x-axis.
    ylabel : str
        Label for y-axis.
    xticks : str
        String holding space-separated tick locations
    xticklabels : str
        String hold space-separated tick labels
    xtickrot : float
        Rotation for tick labels
    yticks : str
        String holding space-separated tick locations
    yticklabels : str
        String hold space-separated tick labels
    ytickrot : float
        Rotation for tick labels
    xpercent : bool
        Format the x ticks as percentages
    ypercent : bool
        Format the y ticks as percentages
    xdollar : bool
        Format the x ticks as dollars
    ydollar : bool
        Format the y ticks as dollars

    """

    # Handle some shortcut syntaxes
    if kwargs.get('xticks') is not None and 'xticklabels' not in kwargs:
        kwargs['xticklabels'] = kwargs['xticks']
    if kwargs.get('yticks') is not None and 'yticklabels' not in kwargs:
        kwargs['yticklabels'] = kwargs['yticks']

    # Handle space separated strings that should be lists
    fields = ['xticks', 'yticks', 'xticklabels', 'yticklabels']
    converts = [float, float, str, str]
    for field, convert in zip(fields, converts):
        if field in kwargs:
            try:
                kwargs[field] = [convert(x) for x in kwargs[field].split()]
            except (AttributeError):
                pass

    if kwargs.get('title') is not None:
        ax.set_title(kwargs['title'])

    if kwargs.get('ymin') is not None:
        ax.set_ylim(bottom=float(kwargs['ymin']))
    if kwargs.get('ymax') is not None:
        ax.set_ylim(top=float(kwargs['ymax']))
    if kwargs.get('ylabel') is not None:
        ax.set_ylabel(kwargs['ylabel'])
    if kwargs.get('yticks') is not None:
        ax.set_yticks(kwargs['yticks'])
    if kwargs.get('yticklabels') is not None:
        if kwargs.get('ytickrot') is not None:
            ax.set_yticklabels(kwargs['yticklabels'],
                               rotation=kwargs['ytickrot'])
        else:
            ax.set_yticklabels(kwargs['yticklabels'])

    if kwargs.get('xmin') is not None:
        ax.set_xlim(left=float(kwargs['xmin']))
    if kwargs.get('xmax') is not None:
        ax.set_xlim(right=float(kwargs['xmax']))

    if kwargs.get('xlabel') is not None:
        ax.set_xlabel(kwargs['xlabel'])
    if kwargs.get('xticks') is not None:
        ax.set_xticks(kwargs['xticks'])
    if kwargs.get('xticklabels') is not None:
        if kwargs.get('xtickrot') is not None:
            ax.set_xticklabels(kwargs['xticklabels'],
                               rotation=kwargs['xtickrot'])
        else:
            ax.set_xticklabels(kwargs['xticklabels'])

    if kwargs.get('logx'):
        ax.set_xscale('log')
    if kwargs.get('logy'):
        ax.set_yscale('log')

    if ax.get_xscale() != 'log':
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    if ax.get_yscale() != 'log':
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    # Move spinse to back of zorder
    for spine in ax.spines.values():
        spine.set_zorder(100)

    if kwargs.get('xpercent'):
        ax.xaxis.set_major_formatter(ticker.FuncFormatter('{0:.0%}'.format))
    if kwargs.get('ypercent'):
        ax.yaxis.set_major_formatter(ticker.FuncFormatter('{0:.0%}'.format))
    if kwargs.get('xdollar'):
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(r'\${:.0f}'.format))
    if kwargs.get('ydollar'):
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(r'\${:.0f}'.format))
    return


@_plot_helper
def text(ax, text=None, text_location="upper left", **kwargs):
    """ Place text on an axis at text_location

    Additional kwargs are ignored to facilitate argument passing.

    Parameters
    ----------
    text : str
        The text to put on the axis
    text_location : str
        One of matplotlibs string or integer locations or a tuple of x,y

    """
    if text is None:
        return
    locations = {'best': 0,
                 'upper right': 1,
                 'upper left': 2,
                 'lower left': 3,
                 'lower right': 4,
                 'right': 5,
                 'center left': 6,
                 'center right': 7,
                 'lower center': 8,
                 'upper center': 9,
                 'center': 10}
    bbox = {}
    if text_location in locations:
        text_location = locations[text_location]
    elif text_location in locations.values():
        pass
    # handle tuple string
    elif '(' in text_location:
        text_location = tuple(float(x)
                              for x in text_location[1:-1].split(','))
    elif type(text_location) is tuple:
        # Specify x,y coordinates for upper left corner
        bbox['bbox_to_anchor'] = text_location
        bbox['bbox_transform'] = ax.transAxes
        text_location = None

    text = text.replace(";", "\n")
    anchored = AnchoredText(text,
                            prop=dict(size=18),
                            loc=text_location,
                            frameon=False,
                            **bbox)
    ax.add_artist(anchored)


@_plot_helper
def legend(ax, legend=None, legend_text=None, **kwargs):
    """ Place legend on an axis at legend_loc

    Additional kwargs are ignored to facilitate argument passing.

    Parameters
    ----------
    legend : str
        either a mpl name for the location or tuple coordinates
    legend_text : str
        additional text to place above legend
        semicolons are replaced with newlines

    """
    if legend is None:
        return
    bbox = {}
    # Specify x,y coordinates for upper left corner
    if '(' in legend:
        bbox['bbox_to_anchor'] = tuple(float(x)
                                       for x in legend[1:-1].split(','))
        bbox['bbox_transform'] = ax.transAxes
        legend_loc = 2

    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles,
                       labels,
                       frameon=False,
                       loc=legend_loc if legend_loc else 'best',
                       prop={'size': 18},
                       labelspacing=0.25,
                       ncol=1 if len(labels) < 6 else 2,
                       **bbox)

    # Add extra text above legend.
    if legend_text:
        for sub in legend_text.split(";")[::-1]:
            txt = offsetbox.TextArea(sub, {'size': 18})
            box = legend._legend_box
            box.get_children().insert(0, txt)
            box.set_figure(box.figure)
    return legend


def plot(func):
    try:
        import click
    except ImportError:
        click = None

    if click:
        doc_strings = [f.__doc__ for f in _plot_helper._functions]
        decorators = [click.command()]
        chain = itertools.chain(*(s.split("\n") for s in doc_strings))
        lines1, lines2 = itertools.tee(chain)
        next(lines2, None)
        for line1, line2 in itertools.izip(lines1, lines2):
            if ':' in line1:
                opt, t = [s.strip() for s in line1.split(":")]
                decorators.append(click.option('--' + opt,
                                               type=pydoc.locate(t),
                                               help=line2.strip()))
        decorators.append(wraps(func))
    else:
        decorators = [wraps(func)]

    @_decorate_all(decorators)
    def plotted_func(**kwargs):
        fig, ax = plt.subplots()
        name = func(fig, ax, **kwargs)
        for helper in _plot_helper._functions:
            helper(ax, **kwargs)
        fig.savefig(name)
    return plotted_func
