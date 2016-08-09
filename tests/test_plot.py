import matplotlib
matplotlib.use('pgf')
import fishbowl
import matplotlib.pyplot as plt
import numpy as np

fishbowl.set_style(font='Julius Sans One')


def example():
    fig, ax = plt.subplots()
    x = np.linspace(0, 30, 100)
    r1 = np.random.rand(100) * 1 + .5 * x + 10
    r2 = np.random.rand(100) * 1 + 1 * x
    r3 = np.random.rand(100) * 1 + .5 * x
    ax.plot(x, r1)
    ax.plot(x, r2)
    ax.plot(x, r3)
    ax.set_xlabel("TIME OR SOMETHING")
    ax.set_title("DESCRIPTIVE TITLE", y=1.1, loc='left')
    fig.savefig('test.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    example()
