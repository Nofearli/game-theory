# Derivation — Cartesian-oval parameterisation of the barrier (`r > 0`)

**Status: rigorous, self-contained** `[new]`. The book states the parameterisation as
`[book 3.3]` (attributed to Xu 2024, Thm 4.1); this note derives it. Numerically verified by
`tests/test_barrier.py::test_oval_degenerates_to_closed_form` and
`examples/barrier/barrier_1v1.py`.

## 1. Why no closed form

With capture radius `r > 0` the criticality functional becomes

$$
J_r(\tau) = \|p - D\| - r - \alpha\,\|p - z\| , \qquad p = (\tau, 0),
$$

and the barrier is again `max_{τ∈[0,l]} J_r(τ) = 0`. Eliminating `τ` between `J_r = 0` and
`dJ_r/dτ = 0` now produces a **quartic** in `(x, y)` — a **Cartesian oval** — so there is no
elementary closed form. The way out is to keep `τ` as a **parameter**.

## 2. Two conditions

$$
\text{(criticality)}\quad \|p-D\| = \alpha\,\|p-z\| + r ,
\qquad
\text{(optimality)}\quad
\frac{\tau - x_D}{\|p-D\|} = \alpha\,\frac{\tau - x}{\|p-z\|} .
$$

Define the two geometric quantities

$$
m \;=\; \|p-z\| \;=\; \frac{\|p-D\| - r}{\alpha},
\qquad
n \;=\; \frac{\tau - x_D}{\alpha\,\|p-D\|}.
$$

`m` is the distance the attacker can cover while the defender closes to within `r` of `τ`;
`n` is the direction cosine of the escape direction.

## 3. The parameterisation

Substituting `m` into the optimality condition:

$$
\frac{\tau - x_D}{\|p-D\|} = \alpha\,\frac{\tau - x}{m}
\;\Longrightarrow\;
\alpha n = \alpha\,\frac{\tau - x}{m}
\;\Longrightarrow\;
\tau - x = m n .
$$

Criticality, `‖p − z‖ = m`, expands to `(τ − x)² + y² = m²`, hence `y = ± m√(1 − n²)`. Taking the
play-region branch (`y > 0`):

$$
\boxed{\;
m = \frac{\|\tau - D\| - r}{\alpha},\qquad
n = \frac{\tau - D_x}{\alpha\,\|\tau - D\|},\qquad
z(\tau) = \big(\tau - m n,\;\; m\sqrt{1 - n^2}\big)
\;}
$$

which is the book's `[book 3.3]` parameterisation.

## 4. Feasibility of `τ`

`m ≥ 0` ⟺ `‖p − D‖ ≥ r` ⟺ `(τ − x_D)² + y_D² ≥ r²`. When `|y_D| < r` this excludes a window

$$
|\tau - D_x| < \sqrt{r^2 - y_D^2}
$$

around the defender's projection — there the escape point already lies inside the capture disk and
**no barrier point exists** (the book's "jump window"). Restricting `τ ∈ [0,l]` further clips the
curve to the target segment.

## 5. Similar points / barrier ratio (rigorous)

For a **fixed** `τ`, `‖τ − D‖` is independent of `r`, so `n` is independent of `r` while `m` is
affine in `r`. Therefore

$$
z_r(\tau) - p \;=\; m\,(-n,\; \sqrt{1-n^2}), \qquad m = \frac{\|\tau-D\|-r}{\alpha},
$$

i.e. **for fixed `τ` the barrier points for different `r` are collinear along a fixed ray through
`τ`, with a slope independent of `r`.** One reference barrier therefore generates every `r` by
radial scaling about the escape points — the book's "similar points / barrier ratio" phenomenon
`[book 3.3]`.

## 6. Exact degeneration as `r → 0`

Set `r = 0`: `m = ‖p−D‖/α` and `n = (τ − x_D)/(α‖p−D‖)`, so

$$
x = \tau - mn = \tau - \frac{\tau - x_D}{\alpha^2}
\;\Longleftrightarrow\;
\tau = \frac{\alpha^2 x - x_D}{\alpha^2 - 1},
$$

which is exactly the escape-point map of the closed-form barrier (see
`barrier-1v1-closed-form.md` §3). Substituting back reproduces

$$
y = m\sqrt{1-n^2} = \sqrt{\frac{y_D^2}{\alpha^2} + \frac{(x-x_D)^2}{\alpha^2-1}} .
$$

Numerically the agreement is at machine precision (`|dy| ≤ 1.1e-16` in
`examples/barrier/barrier_1v1.py`).

## 7. Verification checklist

| Property | Test / check |
|---|---|
| `r→0` degeneracy | `test_oval_degenerates_to_closed_form` (`< 1e-9`) |
| Barrier point moves toward `τ` as `r` grows | `test_oval_radius_shrinks_with_r` |
| Branch geometry reproduced | `examples/barrier/barrier_1v1.py` |

## 8. Notes for use

- The oval parameterisation is by **escape point**, not by `x`; do not index it by abscissa.
- `n` may be negative (escape point left of the defender); `√(1−n²)` stays real as long as the
  feasibility window is respected.
- For `2v1` the same parameterisation is used per defender on its own escape sub-interval.
