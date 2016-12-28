import os
import pytest
import fishbowl
import fishbowl.draw
import numpy as np

fishbowl.set_style()


@fishbowl.plot
def simple(fig, ax, **kwargs):
    x = np.linspace(0, 30, 20)
    r1 = np.random.rand(20) * 1 + .5 * x + 10
    r2 = np.random.rand(20) * 1 + 1 * x
    r3 = np.random.rand(20) * 1 + .5 * x
    ax.plot(x, r1)
    ax.plot(x, r2)
    ax.plot(x, r3)
    return 'simple.png'


@fishbowl.plot
def line(fig, ax, **kwargs):
    x = np.linspace(2, 28, 10)
    r1 = np.random.rand(10) * 3.0 + .5 * x + 10
    r2 = np.random.rand(10) * 3.0 + .6 * x + 5
    fishbowl.draw.line(x, r1)
    fishbowl.draw.line(x, r2, yerr=np.sqrt(r2))
    return 'line.png'


@fishbowl.plot
def bar(fig, ax, **kwargs):
    labels = ['AB'+str(x) for x in range(6)]
    r1 = np.random.rand(6) * 20 + 5 * np.arange(6) + 5
    fishbowl.draw.bar(labels, r1)
    return 'bar.png'


@pytest.mark.parametrize("plot,expected",
                         [(simple, 'simple.png'),
                          (line, 'line.png'),
                          (bar, 'bar.png')])
def test_plot(plot, expected):
    try:
        import click
    except ImportError:
        click = None
    if click:
        ctx = click.Context(plot)
        ctx.invoke(plot)
    else:
        plot()
    assert os.path.exists(expected)
    os.remove(expected)


def save_plots(*plots):
    try:
        import click
    except ImportError:
        click = None
    for plot in plots:
        if click:
            ctx = click.Context(plot)
            ctx.invoke(plot)
        else:
            plot()


if __name__ == "__main__":
    save_plots(simple, line, bar)
