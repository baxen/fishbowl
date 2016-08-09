import matplotlib
import fishbowl

def test_context_set():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami'):
        assert matplotlib.rcParams['grid.color'] == '#e0e0e0'

def test_context_reset():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami'):
        pass
    assert matplotlib.rcParams['grid.color'] == 'k'


def test_set():
    fishbowl.reset_style()
    fishbowl.set_style(font='Arbitrary')
    assert matplotlib.rcParams['pgf.preamble'] == [r'\usepackage{mathspec}', r'\setallmainfonts(Digits,Latin,Greek){{{}}}'.format('Arbitrary')]

def test_reset():
    fishbowl.set_style(font='Arbitrary')
    fishbowl.reset_style()
    assert matplotlib.rcParams['pgf.preamble'] == []
