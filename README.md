# fishbowl
Style options and customization for matplotlib

![Default Style](/docs/example_default.png?raw=true)

# Colors

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

