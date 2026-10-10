# IEEE-style figure standards

Publication-quality defaults. Implemented in `scripts/gtlib/plotting.py` (`ieee_style()`).

## 1. Palette (colour-blind safe, low saturation)

| Role | Colour | Hex |
|---|---|---|
| Defender / pursuer | blue | `#2166AC` |
| Attacker / evader | red | `#B2182B` |
| Helper / boundary / auxiliary | green | `#1B7837` |
| Target / goal | orange | `#F1A340` |
| Extra | purple | `#762A83` |
| Neutral / text | grey | `#666666` |

Chinese-market finance convention (red = up) does **not** apply here; the colour roles above are
the game-theory convention used by the source book.

## 2. Typography & layout

- Serif fonts (Times New Roman); maths in STIX.
- Remove top/right spines; no boxed legend; legend font ≈ 6 pt.
- Sizes: single column 89 mm, double column 183 mm; font 7–8 pt.
- Export **both** SVG (vector, text editable) and 300 dpi PNG.
- Figure text in English (venue requirement); the surrounding prose may be Chinese.

## 3. Geometry rules

- **Equal axis aspect** for arena/trajectory plots (`ax.set_aspect('equal')`), else trajectories
  look distorted. For 3-D, set a real box aspect.
- Draw the defence line / target segment explicitly and label it.
- Fill winning regions with low-alpha colour; keep the barrier a distinct solid line.
- Mark capture points, escape points, and start points with distinct markers.

## 4. Readability checks

- Legible in greyscale (do not encode meaning by colour alone — add line style / marker).
- No overlapping labels; no clipped titles.
- Axis labels include units.
- Caption states what the reader should conclude.

## 5. Usage

```python
from gtlib.plotting import ieee_style, save_figs, C_DEFENDER, C_ATTACKER, C_ACCENT
ieee_style()
fig, ax = plt.subplots(figsize=(3.5, 3.0))   # ~89 mm single column
...
save_figs(fig, "figs/my_experiment_1")        # writes .svg + .png
```
