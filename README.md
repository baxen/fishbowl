<p align="center">
<img src="/docs/fishbowl.png" height="96">
</p>

<p align="center">
<b><a href="#overview">Overview</a></b>
|
<b><a href="#features">Features</a></b>
|
<b><a href="#cli">CLI</a></b>
|
<b><a href="#axes">Axes</a></b>
|
<b><a href="#fonts">Fonts</a></b>
|
<b><a href="#colors">Colors</a></b>
</p>

Style options and customization for matplotlib

## Overview

Matplotlib is very versatile but the default settings produce mediocre graphics. `fishbowl` provides an easy-to-use set of functions to configure matplotlib with an uncluttered style and nice fonts.

<p align="center">
<img src="/docs/example_goldfish_minimal_inconsolata.png" height="320">
<img src="/docs/example_gourami_minimal_latolight.png" height="320">
</p>

## Features
- A decorator to enable easy plot customization from the command line
- Minimal axes and lines to help figures flow with text
- A few custom color schemes and support for `palettable`
- Optional font configurations using xelatex
- Support for saving and loading customized styles within the module

## CLI
`fishbowl` defines a decorator that sets up a function with a standard CLI. The function should accept a `fig, ax` argument, draw the actual plot content on the axis, and return the output filename. The command line interface will then handle common options. For example, create a `test.py`:

```python
import fishbowl
import numpy as np

fishbowl.set_style()


@fishbowl.plot
def example(fig, ax, **kwargs):
    x = np.linspace(0, 30, 100)
    r = np.random.rand(100) * 1 + .5 * x + 10
    ax.plot(x, r)
    return 'test.png'

if __name__ == "__main__":
    example()
```

Then `test.py` can handle a variety of setup arguments, such as labels, ticks, and ranges. For example
```
python test.py --xmin 0.0 --ymax 1.0 --xlabel 'Time'
```

To see more options for this setup, try `python test.py --help`.

## Axes

In `fishbowl`, axes refers to the layout of all of the features of the plot besides the data: the x- and y- axis, grid lines, line widths, ticks and labels.

The default axes style, `minimal` removes plot junk but leaves enough labels to be quite precise. You can modify this to suit your needs by editing the usual `matplotlibrc` options:

```python
import fishbowl
config = fishbowl.axes.axes('minimal')
config['grid.linestyle'] = '--'

fishbowl.axes.save_axes('minimal_dashed')
```

```python
import fishbowl

fishbowl.set_style(axes='minimal_dashed')
```

`fishbowl.axes` introduces a new parameter to configure matplotlib: `axes.initialize`. This parameter registers additional calls to all axes initialized by matplotlib to handle actions like removing the spines for the y-axis. To return to default behavior, you can set it to `None`.

## Fonts

Matplotlib has powerful options for fonts through the combination of the `pgf` backend and `xelatex`. If you have a working xelatex installation, you can use arbitrary system fonts for your graphics. `fishbowl` makes this easy, set your backend to `'pgf'` in your `matplotlibrc` and then just pass the name of a system font to `set_style`. The name should match the name used by `fc-list`, check for the currently installed options like this:

```bash
fc-list :outline -f "%{family}\n" | sort | uniq
```

and then set it (globally or locally)

```python
set_style(font='Lato Light')
```

You can use `fishbowl.font` to check how these fonts are configured, and then modify and save for future use if desired.

```python
import fishbowl
config = fishbowl.font.font('Lato Light')
config['font.size'] = 30

fishbowl.font.save_font('Lato30')
```

```python
import fishbowl

fishbowl.set_style(font='Lato30')
```


## Colors

`fishbowl` provides three qualitative color-schemes to distinguish separate lines. They are intentionally short - it is almost always hard to distinguish more than four lines. Each of the colors is matched in lightness in CIE Lab space so that they have the same emphasis when drawn together on a plot. None of the lines stand out relative to the others.

<table style="border: 0px">
<tr>
  <td>
  <b>Goldfish</b><br>
  <img src="/docs/goldfish.png" height="96"><br>

  <b>Guppy</b><br>
  <img src="/docs/guppy.png" height="96"><br>

  <b>Gourami</b><br>
  <img src="/docs/gourami.png" height="96"><br>
  </td>
  <td>
  <img src="/docs/lines.gif" height="384">
  </td>
</tr>
</table>

`fishbowl.color` provides simple methods to make plots like this so you can test your own colors

```python
import fishbowl

fishbowl.color.draw_box_palette(['skyblue','goldenrod','plum'])
fishbowl.color.draw_sin_palette(['#CDB380','#036564','#033649'])
```

And if you find a combination you like, you can save it to use later.

```python
fishbowl.color.save_palette('tetra',['#91050f','#15bac0','#abbb16','#191800'])
```

```python
import fishbowl

fishbowl.set_style(palette='tetra')
```

