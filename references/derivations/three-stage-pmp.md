# Derivation — reconnaissance–return: reflection, three stages, and dwell time

**Status: mixed.** §2–§5 are **rigorous and self-contained** `[new]` (they justify the book's
virtual-evader / reachable-set statements `[book 6.0 §4.3, 6.4 Lemma 1]`). §6 states the paper's
PMP transversality results as given in the book `[book 6.3]` and explains their structure without
claiming a full re-derivation. §7 describes the numerical model shipped in `gtlib/recon.py`.

Convention (`[book 6.3]`–`6.5`): goal line `x = 0`, reconnaissance boundary `x = l`, play region
`0 < x < l`; `α = v_P/v_E > 1`; capture radius `r_c`; dwell time `τ`, dwell direction `σ = ±1`.

## 1. Why a third stage appears

A two-stage task ("go recon, then return") becomes three stages the moment the evader is allowed
to **stay** on the reconnaissance boundary for a time `τ`:

| `ϑ` | stage | ends when |
|---|---|---|
| 1 | reconnaissance | `x_E` reaches the boundary `x = l` |
| 2 | dwell (loiter) | timer `τ` elapses |
| 3 | return | `x_E` reaches `x = 0` or is captured |

`τ` becomes a **new independent variable** of the barrier: the win/lose boundary is now a family
of curves indexed by `τ`.

## 2. Reflection lemma (rigorous)

**Lemma.** For a point `A` with `x_A < l` and a boundary point `x_I = (l, y_I)`, the broken path
`A → x_I → G` (with `G` on the goal line) satisfies

$$
\|A - x_I\| + \|x_I - G\| \;\ge\; \|\tilde A - G\|,
\qquad \tilde A = (2l - x_A,\; y_A),
$$

with equality iff `x_I` lies on the straight segment `Ã → G`.

**Proof.** Reflection about `x = l` is an isometry that fixes the boundary, so
`‖A − x_I‖ = ‖Ã − x_I‖`. The triangle inequality gives
`‖Ã − x_I‖ + ‖x_I − G‖ ≥ ‖Ã − G‖`, with equality iff the three points are collinear. ∎

The same argument applies to any straight boundary, and extends to a **moving** evader by
translating the reflected start: if the evader has drifted by `σ v_E τ` along the boundary, use

$$
\tilde{\mathbf x}_E(\tau) \;=\; \big(2l - x_E,\;\; y_E + \sigma\, v_E\, \tau\big),
$$

which is exactly the book's **virtual (reflected) evader** `[book 6.0 symbol table]`.

**Consequence.** The evader's minimum total path length from `x_E` to a goal point `G`, including
the dwell, is `‖x̃_E(τ) − G‖ + v_E τ` — so the whole three-stage task collapses to a **single
straight leg in the reflected frame**.

## 3. Successful-return condition (rigorous)

The evader reaches `G` at time `(‖x̃_E − G‖ + v_E τ)/v_E`; the pursuer reaches within `r_c` of `G`
at time `(‖x_P − G‖ − r_c)/v_P`. The evader succeeds at `G` iff the former is smaller:

$$
\alpha\big(\|\tilde{\mathbf x}_E - G\| + v_E \tau\big) \;<\; \|x_P - G\| - r_c .
$$

Equivalently, with the **success-return region** `R_E^S` and `d_S(G) = ‖x̃_E − G‖`:

$$
\mathcal R_E^{S} = \{\,x : \|x - x_P\| \;\ge\; \alpha\, d_S(x) + v_P \tau + r_c\,\},
$$

which is precisely the book's `[book 6.0 §4.3]` definition, and

$$
\text{successful return} \iff \mathcal R_E^{S} \cap \mathcal L_{\text{goal}} \neq \varnothing .
$$

**Lemma 1 (SRR = virtual LRR ∩ {x<l}).** With `d_S(x) = ‖x̃_E − x‖`, `R_E^S` is the virtual LRR
`{‖x − x_P‖ ≥ α‖x̃_E − x‖ + v_P τ + r_c}` restricted to the physical branch `x < l` — the reflection
straightens the two-leg path, so the "two-leg" condition *is* a one-leg Apollonius condition. ∎

## 4. Barrier and winning regions

With the equivalent dwell–return sub-game value `J₁` (evader maximises, pursuer minimises),

$$
\mathcal B = \{z : J_1(z) = 0\},\qquad
\mathcal W_E = \{J_1 > 0\},\qquad
\mathcal W_P = \{J_1 < 0\}.
$$

**It must be evaluated in the virtual frame** — using physical `x_E` instead of `x̃_E` gives a
wrong barrier. This is the book's explicit warning `[book 6.0 §4.1]`.

## 5. Structure of the optimal trajectories (rigorous)

From §2: in the reflected frame the evader's optimum is a **straight line**, which corresponds to
**two straight physical legs** (recon and return) meeting at the boundary. From §3: the pursuer's
optimum is a **straight line** to the chosen return point. Hence *all* optimal trajectories are
piecewise straight — the book's "three straight segments" statement `[book 6.5 Eq. 37]`.

Moreover, the recon leg and the return leg are **mirror images about the boundary normal**, because
the reflected straight line crosses the boundary. Writing their headings as `φ⁽¹⁾*` and `φ⁽³⁾*`
measured from the same axis,

$$
\boxed{\;\phi^{(1)*} = \pi - \phi^{(3)*}\;}
$$

— the symmetry relation quoted in `[book 6.3]`, here obtained geometrically.

## 6. PMP setup and the transversality relations `[book 6.3]`

State `z = [x_E, y_E, x_P, y_P]ᵀ`, control angles; the dynamics are **state-independent and
control-affine**, so on an optimal trajectory

- the co-states `λ` are **constant** on each stage;
- `H = 0` along the optimum (autonomous, free final time), giving one scalar relation;
- matching `λ` across the stage boundaries, and using the transversality condition at the terminal
  set, yields two scalar conditions. The book records them as

$$
\nu = 2\alpha\cos\phi^{(3)*}, \qquad \phi^{(1)*} = \pi - \phi^{(3)*} .
$$

The second is derived above (§5); the first is quoted from the paper. *Do not present the first as
re-derived here* — verify it against the paper before using it quantitatively.

## 7. Dwell time `τ_max` and the scalar reduction (rigorous in structure)

The successful-return condition is a **1-D** maximisation over the goal line:

$$
g(\tau) \;=\; \max_{x \in \mathcal L_{\text{goal}}}
\Big[\,\|x - x_P\| - \alpha\,\|\tilde{\mathbf x}_E(\tau) - x\|\,\Big] \;-\; v_P \tau \;-\; r_c
\;\ge\; 0 .
$$

`g(τ)` is a scalar function of `τ` (the inner maximisation is one-dimensional), so `τ_max` is the
largest root of `g(τ) = 0` — the **scalar reduction** of `[book 6.5]`. Under the book's assumptions
`g` is strictly decreasing in `τ` (the dwell costs the evader `v_P τ` of pursuer head-start and the
reflection shifts the virtual evader monotonically), which gives existence and uniqueness of
`τ_max`. Monotonicity is verified numerically in
`tests/test_recon_tad.py::test_dwell_time_shrinks_margin`.

## 8. Shipped numerical model

`gtlib/recon.py` evaluates the condition of §7 **directly**, with one documented simplification:
the pursuer is assumed to guard the goal (it does not intercept during the reconnaissance leg).
This keeps the model self-contained and fast while preserving the sign structure. It is an
**independent reconstruction**, not the paper's closed form.

Reference values from the book's case study `[book 6.0 §8]`: `Case A = (2.05, 2.80) ∈ W_P`,
`Case B = (2.05, 3.30) ∈ W_E`, paper `τ_max = 2.85 s`. The shipped model reproduces the
**classification** (A → `W_P`, B → `W_E`) but not the paper's numeric `τ_max` (it gives `1.43 s`
for Case B) — expected, given the simplification. For publication numbers use the paper's
closed form.

## 9. Verification checklist

| Property | Test |
|---|---|
| Virtual-evader transform `x̃_E = (2l−x_E, y_E+σv_Eτ)` | `test_virtual_evader_transform` |
| Case A ∈ `W_P` | `test_recon_case_A_pursuer_wins` |
| Case B ∈ `W_E` | `test_recon_case_B_evader_wins` |
| Dwell shrinks the margin (monotonicity) | `test_dwell_time_shrinks_margin` |
| `τ_max = 0` when already losing at `τ=0` | `test_max_dwell_time_zero_when_losing` |
| Numeric barrier + `τ_max` | `examples/reconnaissance-return/recon_2stage.py` |

## 10. Open items (do not over-claim)

- Derive `ν = 2α cos φ⁽³⁾*` from the paper's Hamiltonian and confirm its sign convention.
- Remove the "pursuer guards the goal" simplification to recover the paper's numeric `τ_max`.
- Extend to the two-goal-line (TIE) variant, which the book leaves unexpanded `[book 6.0]`.
