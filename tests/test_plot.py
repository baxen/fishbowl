import os
import fishbowl
import numpy as np

fishbowl.set_style()


@fishbowl.plot
def example(fig, ax, **kwargs):
    x = np.linspace(0, 30, 100)
    r1 = np.random.rand(100) * 1 + .5 * x + 10
    r2 = np.random.rand(100) * 1 + 1 * x
    r3 = np.random.rand(100) * 1 + .5 * x
    ax.plot(x, r1)
    ax.plot(x, r2)
    ax.plot(x, r3)
    return 'test.png'


def test_example_plot():
    try:
        import click
    except ImportError:
        click = None
    if click:
        ctx = click.Context(example)
        ctx.invoke(example)
    else:
        example()
    assert os.path.exists('test.png')
    os.remove('test.png')


if __name__ == "__main__":
    example()
