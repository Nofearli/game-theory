# 03 · Barriers and strategies

`[book]` Ch. 3 (§3.0–3.5). The **barrier** is the feasibility criterion for deployment: after
the defenders are placed, which attacker *initial positions* still break through?

## 1. Barrier vs reachable set (the key distinction)

| | independent variable | question |
|---|---|---|
| Reachable set / Apollonius | a spatial point `x` | who reaches `x` first, *now*? |
| **Barrier** `B` | the attacker's **initial position** | for this deployment, which initial positions break through? |

`B` splits the state space into defender-winning `W_P` and attacker-winning `W_E`. On `B` itself
(Isaacs) neither side can guarantee a win. Barrier = the analytic basis of the mvn assignment
feasibility matrix (`02` / Ch. 1.5).

**Model:** `ẋ_P = v_P u_P`, `ẋ_E = v_E u_E`, `α = v_P/v_E > 1` (code uses `ratio = α⁻¹`); target
segment `mn` of length `l`; attacker breaks through by entering the target.

## 2. 1v1 analytic barrier (three branches, closed form)

Attacker at `z` heads straight for escape point `p = (τ, 0)`; cost

$$
J(p) = \|p - D\| - \alpha\|p - z\| \qquad (J = 0 \text{ critical}).
$$

Barrier points satisfy `J = 0` (critical) **and** `dJ/dτ = 0` (attacker-optimal). Solving gives
the escape-point map `τ(x) = (α²x − x_D)/(α² − 1)` and the middle hyperbola; when `τ` hits the
endpoints the branch degenerates to an arc. Three closed-form branches, joints
`δ₁ = x_D/α²`, `δ₂ = δ₁ + (1 − α⁻²)l`:

$$
B_1:\ \|z-m\| = \frac{\|D-m\|}{\alpha},\ x \le \delta_1
\qquad
B_2:\ y = \sqrt{\frac{y_D^2}{\alpha^2} + \frac{(x-x_D)^2}{\alpha^2-1}},\ \delta_1 \le x \le \delta_2
\qquad
B_3:\ \|z-n\| = \frac{\|D-n\|}{\alpha},\ x \ge \delta_2
$$

Arc = escape point pinned to an endpoint; middle = interior escape point. The branches join
smoothly at `δ₁, δ₂` (numerical residual ≈ 0).

> **Full derivation:** `../derivations/barrier-1v1-closed-form.md` (criticality functional →
> escape-point map → three branches → `C¹` joint continuity), verified by `tests/test_barrier.py`.

## 3. 2v1 barrier (no new curves)

The perpendicular-bisector / target-line intersection
`x_z = (‖D₂‖² − ‖D₁‖²)/(2Δx)` splits the escape-point interval in two; each defender applies its
1v1 barrier on its own sub-interval; a **joining arc** centred at `x_z` stitches them. Because
`‖x_z − D₁‖ = ‖x_z − D₂‖`, the joining radii match automatically ⇒ five branches
`F²₁…F²₅` (Yan 2020 base curves), all closed form. Precondition `x_z ∈ [x₁, x₂]` (the typical
"one on each side" deployment); otherwise it degenerates to 1v1.

## 4. Capture radius ⇒ Cartesian oval (no closed form, parameterised)

With capture radius `r`: the endpoint-arc radii become `(‖D−m‖ − r)/α`, and the middle branch
becomes a **Cartesian oval** (quartic) with **no closed form**. Parameterise by the optimal
escape point `τ = (τ, 0)` (Xu 2024, Thm 4.1):

$$
m = \frac{\|\tau - D\| - r}{\alpha}, \qquad
n = \frac{\tau - D_x}{\alpha\,\|\tau - D\|}, \qquad
z(\tau) = \big(\tau - mn,\ m\sqrt{1-n^2}\big).
$$

- `m` = distance the attacker covers while the defender closes to within `r` of `τ`;
  `n` = direction cosine.
- **`r → 0` degenerates exactly** to the 3.1 closed-form hyperbola (verified to `~1e-16`).
- Feasible `τ` set: need `m ≥ 0`; if `|y_D| < r`, `τ` must satisfy
  `|τ − D_x| ≥ √(r² − y_D²)` — no barrier in a window near the defender's projection.
- **Similar points / barrier ratio:** for a fixed `τ`, barrier points for different `r` are
  collinear through `τ` with slope independent of `r` ⇒ one base barrier generates all `r`.

> **Full derivation:** `../derivations/cartesian-oval-parameterisation.md` (two conditions →
> `z(τ)`, feasibility window, similar-points theorem, exact `r→0` degeneration).

## 5. Unexpected strategy (attacker manoeuvres) `[book 3.4]`

The attacker may **turn mid-flight**. Xu 2024 Lemma 3.2: the defender runs **strategy (8)**,
solving the interception angle from the attacker's *current* heading `ζ`:

$$
\varepsilon = \arcsin\!\Big(\frac{r_2}{\alpha r_2 + r}\sin\zeta\Big), \qquad
r_2(\zeta) = \frac{\alpha r + \delta\cos\zeta - \sqrt{(\alpha r + \delta\cos\zeta)^2 - (1-\alpha^2)(\delta^2 - r^2)}}{1-\alpha^2}
$$

(sine rule in triangle PCE + simultaneous-arrival `r₁ = αr₂ + r`; the **negative root** is the
inner oval, the positive root is the physically invalid outer one). Guarantees: on straight
segments the capture point lies exactly on the current oval (`|f| ≤ 4e-16`); when the attacker
turns, the ovals nest into a tangent chain `C → C¹ → C²`, the capture point stays on the current
oval, and a fold-back manoeuvre pulls it back **inside the initial oval** — an unexpected
manoeuvre cannot escape the attacker's own first-step reachable set. Sustained escape is cut off
by a lifeline.

## 6. "One Apollonius circle is enough" `[book 3.5]`

A strategy **independent of the attacker's control** (Dorothy 2022, Thm 1; `ν = v_E/v_P < 1`,
`v_P` normalised): inflate the initial AC by `δ` into a fixed disk `C`
(`x_C = x_A(t₀)`, `R_C = R_A(t₀) + δ`) and run

$$
v_P = \hat z_P,\qquad z_P = (R_C - R_A(t))\,\hat r + \nu\,y,\qquad y = x_A(t) - x_C .
$$

`z_P` uses only the line-of-sight direction and AC geometry — **no attacker control input**;
the `νy` term cancels the AC-centre drift. Lyapunov `V = d_max·d_min` satisfies
`V̇ ≥ 2νV/(‖z_P‖+‖z_E‖) ≥ 0`, giving

$$
t_{capture} \le 2(1+\nu^{-1}) R_C \ln(R_C/\delta).
$$

Consequences: (i) the AC never leaves `C`; (ii) **Cor. 1** capture occurs within the
`δ₁ = R_C − √(R_C² − δ²)` neighbourhood of the initial AC; (iii) **Cor. 2** sensing is never
lost (the rigorous version of Ch. 4's "keep sensing" assumption); (iv) **Cor. 3–8** the game
value = min of `φ` over the initial AC; generalised target-guarding is a win iff the initial AC
excludes the target; multi-defender is fully decentralised (draw each AC, intersect); speed
uncertainty uses `ν̃ ≥ ν_true`.

**3.4 vs 3.5:** 3.4 spends the attacker's *strategy* (heading) to sit on the optimal oval; 3.5
gives that up for **full immunity** to the attacker's strategy (smooth feedback, no chatter).
Choose by what the sensor can provide.

## 7. Assumptions & boundaries

- Point capture in 3.1/3.2; `r > 0` in 3.3/3.4. 3.5 is **point capture only**.
- `α > 1`. 2v1 assumes a non-overlapping deployment.
- The barrier answers a *deployment* question, not a real-time control question.

## 8. Pitfalls

`α` direction (`v_P/v_E` vs `v_E/v_P`) flips all three branches; "which side is the attacker's
winning region" is easy to flip; `τ` window when `|y_D| < r`; degenerate `Δx = 0` in `x_z`.

## 9. Code

- `examples/barrier/barrier_1v1.py` — three-branch barrier + oval parameterisation.
- `scripts/gtlib/barrier.py` — `barrier_1v1`, `cartesian_oval_points`, `barrier_2v1`.

## 10. Research extensions `[ext]`

- 3v1+ non-overlapping barriers (base-curve stitching generalises).
- Barriers with acceleration limits / nonholonomic dynamics.
- Robust barriers under bounded disturbance (reachability via HJ PDE).
- Barrier for the three-stage reconnaissance game (Ch. 6.4).
