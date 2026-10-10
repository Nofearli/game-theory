# 02 · Parameter-uncertainty games

`[book]` Ch. 2 (§2.0–2.4). Ch. 1's framework with **observation error** on the players' states.

## 1. Problem class

Same scenario as Ch. 1; the only change: **positions come from sensors with error**. Uncertainty
plays two roles:

| Role | Meaning | Tool | Used in |
|---|---|---|---|
| Geometric bound | how large an estimation error the situation allows | `kesai_ij` model | judgement fix, robust assignment (2.1/2.2) |
| Statistical accuracy | how small an error the data can achieve | Kalman filter | perception (2.3) |

The model gives an **upper bound**, the filter gives a **lower bound**; reality is in between,
and the gap is the "reliability margin bought by filtering".

## 2. Distance-dependent uncertainty model `kesai_ij`

$$
\xi(d, r, a) = \frac{1}{k}\,\min\!\Big(d - r,\ \ \frac{\min(a-1,1)}{a}\,d + \frac{r}{a}\Big),
\qquad k = 3 \ (\text{conservatism}).
$$

- Branch `d − r`: **far away ⇒ coarse estimate allowed**; contact (`d ≤ r`) ⇒ zero error.
- Branch `(min(a−1,1)/a)d + r/a`: **small speed advantage ⇒ accurate estimate required**
  (`a→1` makes it small).
- Properties: `ξ` increases with distance, → 0 at contact. Consequences: filtering pays off in
  the **far field**, and multi-pursuer defence is *insurance* under uncertainty.

`k` (`mul` in code) is tunable; **smaller `k` ⇒ larger `ξ` ⇒ coarser observation.**

## 3. Correction: capture radius shrinkage

Fold `ξ` into the judgement:

$$
r_{eff} = r - a\,\xi, \qquad
\|x-p_p\| \ge a\|x-p_e\| + r_{eff}.
$$

Geometric effect: larger `ξ` ⇒ smaller `r_{eff}` ⇒ the conservative boundary expands toward the
attacker (the defender is pessimistic about its own capability). `r_{eff}` may be **negative**;
the judgement function still works, but plotting routines may not.

## 4. Robust pairwise judgement (Monte Carlo)

The Ch. 1 judgement is unchanged; plug in estimated positions, then quantify reliability by
perturbing inside the uncertainty disk `N` times and counting "interception succeeds":

$$
P^{succ} = \frac{1}{N}\sum_{s=1}^{N} \mathbf 1\{\text{judge}(x^{(s)}) = \text{success}\}.
$$

Book measurement at test point `(−1,0)` (truth: 1v1 fails, 2v1 succeeds):
`P_{1v1}^{succ} = 30%`, `P_{2v1}^{succ} = 74%`. Two lessons: (i) uncertainty turns a
deterministic outcome into a probabilistic one — **multi-pursuer is insurance**; (ii) errors are
two-sided (false positive for 1v1, false negative for 2v1) — the right criterion is *agreement
with the true geometry*, not the success rate.

## 5. Robust task assignment

Ch. 1's assignment upgraded: feasibility is judged **on perturbed positions inside the
uncertainty disk**, not at nominal positions — only combos that still stop the attacker after
perturbation are feasible (*pairwise outcomes under uncertainty*):

$$
xcj^{rob}_{ij} = \begin{cases}1 & \text{perturbed } x_1^* < x_d\\ 0 & \text{else}\end{cases},
\qquad
\max \sum_{i,j} reward_{ij} x_{ij}.
$$

`reward = 1/(x_1^* − x_{e,x})` (tighter suppression ⇒ higher reward). Constraints as in Ch. 1
(row/column ≤ 1, shared-defender exclusion), infeasible cells capped at 0 (**rational
abandonment**). The "nominally feasible but fails after perturbation" cell (the `u` cell) is the
most dangerous trap.

## 6. Perception: Kalman filter

Filtering is the *data-side* way to shrink `ξ`. Two implementations:

**Position-state KF (known input):**
`X⁻ = AX + BU`, `P⁻ = APAᵀ + Q`, `K = P⁻Hᵀ(HP⁻Hᵀ + R)⁻¹`,
`X = X⁻ + K(Z − HX⁻)`, `P = (I − KH)P⁻`.

**Constant-velocity KF (game integration):** state `[x, y, v_x, v_y]`, predict–update as above
with `B = 0`.

Measured payoff (observation noise injected by `kesai_ij`):

| Scenario | raw error | after filter | model `ξ` |
|---|---|---|---|
| original demo (noise 5/i) | 0.923 m | 0.684 m | — |
| game trajectory (distance-dependent) | 0.896 m | **0.368 m** | ≈0.66 m |

Reading: raw error hugs the `ξ` model; the filter removes more than half. Model = upper bound
(0.66), filter = lower bound (0.37). Since `ξ → 0` at contact, **the gain is concentrated in the
far field**.

## 7. End-to-end check: closed-loop capture rate

Run the full closed loop (no prior judgement) with 100 Monte-Carlo runs per condition:

| `mul` (noise level) | no filter | with filter |
|---|---|---|
| 1.0 (at the model bound, far-field ±2.6 m) | **0%** | 100% |
| 2.0 (2× conservative) | 100% | 100% |
| 3.0 (model default) | 100% | 100% |

Conclusions: (i) when noise exceeds the conservative margin (`mul=1`) the unfiltered defender
chases a phantom and fails, the filtered one succeeds; (ii) under conservative noise (`mul=2/3`)
both succeed — the gain is far-field only; (iii) the 1v1 **open-loop** optimum is two straight
lines (open-loop mode reproduces it), so curved closed-loop paths are the normal behaviour of a
receding-horizon feedback law, not sub-optimality.

## 8. Assumptions & boundaries

- The `kesai_ij` model is a **heuristic conservative bound**, not derived from sensor physics.
- Monte-Carlo reliability depends on the noise model; changing the model changes the numbers.
- KF assumes (approximately) linear Gaussian dynamics; the game's nonlinear judgement is not
  filtered — only the state is.

## 9. Code

- `examples/partial-observation/` — perception + robust judgement.
- `scripts/gtlib/uncertainty.py` — `kesai_ij`, `r_eff`, Monte-Carlo judgement.
- `scripts/gtlib/filters.py` — linear KF and constant-velocity KF.

## 10. Research extensions `[ext]`

- Chance-constrained reach–avoid (`P(success) ≥ 1−δ`) with explicit distribution assumptions.
- Robust barrier under bounded disturbance (set-membership / interval analysis).
- Distributionally-robust assignment (ambiguity sets instead of a single noise model).
- Joint estimation + strategy (dual control) rather than "estimate then plan".
