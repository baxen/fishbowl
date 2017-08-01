import matplotlib
import fishbowl


original = True
updated = False


def test_context_set():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami', font='Arbitrary'):
        assert matplotlib.rcParams['axes.spines.left'] == updated


def test_context_reset():
    fishbowl.reset_style()
    with fishbowl.style(axes='minimal', palette='gourami', font='Arbitrary'):
        pass
    assert matplotlib.rcParams['axes.spines.left'] == original


def test_set():
    fishbowl.reset_style()
    fishbowl.set_style(font='Arbitrary')
    assert matplotlib.rcParams['axes.spines.left'] == updated


def test_reset():
    fishbowl.set_style(font='Arbitrary')
    fishbowl.reset_style()
    assert matplotlib.rcParams['axes.spines.left'] == original
