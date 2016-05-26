<p align="center">
<img src="/docs/fishbowl.svg" height="96">
</p>

<p align="center">
<b><a href="#overview">Overview</a></b>
|
<b><a href="#features">Features</a></b>
|
<b><a href="#installation">Colors</a></b>
</p>

Style options and customization for matplotlib

## Overview

Matplotlib is very versatile but the default configuration produces visualizations which are pretty difficult to follow. `fishbowl` provides an easy-to-use set of functions to configure matplotlib with a nice style that shows qualitative information without clutter.

<p align="center"> 
<img src="/docs/example_goldfish_minimal.png" height="320">
<img src="/docs/example_gourami_minimal.png" height="320">
</p>

## Features
- Minimal axes, grid, and line styles to help figures flow inline with text
- A few custom color schemes and support for `palettable`
- Optional font configurations using xelatex
- Support for saving and loading customized styles within the module

## Colors

`fishbowl` provides three qualitative color-schemes to distinguish separate lines. They are intentionally short - it is almost always hard to distinguish more than four lines.

#### Goldfish
<img src="/docs/goldfish.png" height="96">

#### Guppy
<img src="/docs/guppy.png" height="96">

#### Gourami
<img src="/docs/gourami.png" height="96">


Each of the colors is matched in lightness in CIE Lab space so that they have the same emphasis when drawn together on a plot. None of the lines stand out relative to the others:

<img src="/docs/lines_goldfish.png" height="384">


`fishbowl.color` provides simple methods to make plots like this so you can test your own colors

```python
import fishbowl.color

fishbowl.color.draw_box_palette(['skyblue','goldenrod','plum'])
fishbowl.color.draw_sin_palette(['#CDB380','#036564','#033649'])
```

And if you find one you like, you can save it to use later.

```python
fishbowl.color.save_palette('tetra',['#91050f','#15bac0','#abbb16','#191800'])
```

```python
import fishbowl

fishbowl.set_style(palette='tetra')
```

