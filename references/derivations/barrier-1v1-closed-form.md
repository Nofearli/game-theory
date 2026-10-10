# Derivation — 1v1 analytic barrier (arc–hyperbola–arc)

**Status: rigorous, self-contained** `[new]` (the book states the result `[book 3.0 §2 / 3.1]`;
this note derives it from first principles). Numerically verified by
`tests/test_barrier.py::test_barrier_joint_continuity` and
`examples/barrier/barrier_1v1.py`.

## 1. Setup

- Defender `D = (x_D, y_D)`; attacker at `z = (x, y)`, `y > 0` (play region).
- Target segment on `y = 0` from `m = (0,0)` to `n = (l,0)`.
- Speeds: attacker `v_E`, defender `v_P`, ratio `α = v_P/v_E > 1`.
- Point capture (`r = 0`) for this note (the `r > 0` case is in
  `cartesian-oval-parameterisation.md`).
- The attacker commits to a straight run to a single escape point `p = (τ, 0)`, `τ ∈ [0, l]`.

## 2. Criticality functional

Arrival times: `t_E = ‖p − z‖ / v_E`, `t_P = ‖p − D‖ / v_P`. The attacker succeeds at `p` iff
`t_E < t_P`, i.e.

$$
J(\tau) \;=\; \|p - D\| - \alpha\,\|p - z\| \;>\; 0 .
$$

The attacker plays the best escape point, so it wins iff `max_{τ∈[0,l]} J(τ) > 0`. The **barrier**
is the locus of attacker initial positions `z` where

$$
\max_{\tau \in [0,l]} J(\tau) = 0 . \tag{B}
$$

Two conditions follow:

1. **Criticality:** `J(τ*) = 0` at the optimal `τ*`;
2. **Attacker optimality:** `dJ/dτ |_{τ*} = 0` (interior optimum).

## 3. Escape-point map (from the two conditions)

With `p = (τ,0)`,

$$
\frac{dJ}{d\tau} = \frac{\tau - x_D}{\|p-D\|} - \alpha\,\frac{\tau - x}{\|p-z\|} = 0,
\qquad
J = 0 \;\Rightarrow\; \|p-D\| = \alpha\|p-z\| .
$$

Substituting the second into the first:

$$
\frac{\tau - x_D}{\alpha\|p-z\|} = \alpha\,\frac{\tau - x}{\|p-z\|}
\;\Longrightarrow\;
\tau - x_D = \alpha^2(\tau - x)
\;\Longrightarrow\;
\boxed{\;\tau(x) = \frac{\alpha^2 x - x_D}{\alpha^2 - 1}\;}
$$

## 4. Middle branch (interior escape point)

Using `J = 0` with `p = (τ(x), 0)`:

$$
(\tau - x_D)^2 + y_D^2 = \alpha^2\big[(\tau - x)^2 + y^2\big] .
$$

Now

$$
\tau - x = \frac{x - x_D}{\alpha^2-1}, \qquad
\tau - x_D = \frac{\alpha^2 (x - x_D)}{\alpha^2-1},
$$

so

$$
y^2 = \frac{\alpha^2(x-x_D)^2}{(\alpha^2-1)^2} + \frac{y_D^2}{\alpha^2}
     - \frac{(x-x_D)^2}{(\alpha^2-1)^2}
     = \frac{(x-x_D)^2}{\alpha^2-1} + \frac{y_D^2}{\alpha^2},
$$

$$
\boxed{\;y = \sqrt{\frac{y_D^{2}}{\alpha^{2}} + \frac{(x-x_D)^{2}}{\alpha^{2}-1}}\;}
\qquad (B_2)
$$

which is exactly the book's `B₂`.

## 5. End branches (escape point pinned to an endpoint)

If the unconstrained optimum `τ(x)` leaves `[0, l]`, the attacker is forced to an endpoint.

- `τ* = 0` (point `m`): `J = 0` becomes `‖m − D‖ = α‖m − z‖`, i.e. a circle centred at `m`:

$$
\boxed{\;\|z - m\| = \frac{\|D-m\|}{\alpha}\;} \qquad (B_1)
$$

- `τ* = l` (point `n`): `‖z − n‖ = ‖D − n‖ / α`. `(B_3)`

## 6. Branch boundaries and joint continuity

`τ(x) ∈ [0,l]` ⟺ `x ∈ [δ₁, δ₂]` with

$$
\tau(x) = 0 \Rightarrow \delta_1 = \frac{x_D}{\alpha^2}, \qquad
\tau(x) = l \Rightarrow \delta_2 = \delta_1 + \Big(1 - \frac{1}{\alpha^2}\Big) l .
$$

**Continuity at `δ₁`** (both must give the same `y`):

$$
y_{B_2}^2(\delta_1) = \frac{(\delta_1-x_D)^2}{\alpha^2-1} + \frac{y_D^2}{\alpha^2}
= \frac{x_D^2(\alpha^2-1)}{\alpha^4} + \frac{y_D^2}{\alpha^2}
= \frac{x_D^2(\alpha^2-1) + y_D^2\alpha^2}{\alpha^4},
$$

$$
y_{B_1}^2(\delta_1) = \frac{\|D\|^2}{\alpha^2} - \delta_1^2
= \frac{x_D^2+y_D^2}{\alpha^2} - \frac{x_D^2}{\alpha^4}
= \frac{x_D^2(\alpha^2-1) + y_D^2\alpha^2}{\alpha^4}.
$$

They are **identically equal** ⇒ `C¹`-smooth junction at `δ₁`; the same algebra holds at `δ₂`.

## 7. Which side is the attacker's winning region?

Evaluate `J` at a single test point. E.g. for `D = (2, 1.5)`, `α = 2`, the barrier at `x = 1.6`
gives `y ≈ 0.785`. A point **above** the barrier, `z = (1.6, 2.0)`, yields `J > 0` ⇒ the attacker
wins above the barrier; the defender wins below. (Always re-check with a test point — the sign is
easy to flip.)

## 8. Verification

- Joint continuity: `tests/test_barrier.py::test_barrier_joint_continuity` (analytically and
  numerically, `< 1e-9`).
- Criticality on the whole curve: `test_barrier_points_are_critical` (residual `< 1e-5` over the
  sampled branches).
- Numeric reproduction of the three branches: `examples/barrier/barrier_1v1.py`.

## 9. Extensions

- `r > 0`: `J_r(τ) = ‖p−D‖ − r − α‖p−z‖` — see `cartesian-oval-parameterisation.md`.
- `2v1`: split the escape interval at the perpendicular-bisector point
  `x_z = (‖D₂‖² − ‖D₁‖²)/(2Δx)` and apply each 1v1 barrier on its own sub-interval, joined by an
  arc of radius `(‖x_z − D‖ − r)/α` (equal for both defenders by construction).
- Non-straight attacker paths require a different functional (the barrier becomes a viscosity
  solution of a Hamilton–Jacobi PDE rather than an algebraic curve).
