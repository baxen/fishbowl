import matplotlib
import fishbowl


original = []
updated = [r'\usepackage{mathspec}',
           r'\setallmainfonts(Digits,Latin,Greek){Arbitrary}']


def test_context_set():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami', font='Arbitrary'):
        assert matplotlib.rcParams['pgf.preamble'] == updated


def test_context_reset():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami', font='Arbitrary'):
        pass
    assert matplotlib.rcParams['pgf.preamble'] == original


def test_set():
    fishbowl.reset_style()
    fishbowl.set_style(font='Arbitrary')
    assert matplotlib.rcParams['pgf.preamble'] == updated


def test_reset():
    fishbowl.set_style(font='Arbitrary')
    fishbowl.reset_style()
    assert matplotlib.rcParams['pgf.preamble'] == original
