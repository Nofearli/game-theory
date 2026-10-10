# 01 · Traditional pursuit–evasion & defense games

`[book]` Ch. 1 (§1.0–1.6). Complete-information, simple-motion games from 1v1 to mvn.

## 1. Problem class

- **Players**: `m` defenders (pursuers, `p`) vs `n` attackers (evaders, `e`).
- **Motion**: simple motion `ẋ = u`, `‖u‖ ≤ v_i` (speed fixed, heading free).
- **Objective (defender)**: prevent any attacker from reaching the defence line `x = x_d`.
- **Objective (attacker)**: reach `x ≥ x_d` alive.
- **Capture**: `‖p_p − p_e‖ ≤ r`.
- **Information**: perfect, symmetric (this is the baseline; Ch. 2/4 relax it).

## 2. Core building block — the Apollonius inequality

Time-to-go `t_p(x) = ‖x−p_p‖/v_p`, `t_e(x) = ‖x−p_e‖/v_e`. The attacker reaches `x` first iff

$$
t_e < t_p \iff \|x-p_p\| \ge a\,\|x-p_e\|, \qquad a = v_p/v_e > 1 .
$$

- Boundary `‖x−p_p‖ = a‖x−p_e‖` is the **Apollonius circle** (`r = 0`) / **Cartesian oval**
  (`r > 0`).
- With capture radius, the usable constraint is `g(x) = −‖x−p_p‖ + a‖x−p_e‖ + r ≤ 0`.
- `g ≤ 0` = attacker **safe set**. `a↑` or defender closer ⇒ safe set shrinks.

**Derivation (why the ratio form).** `t_e < t_p` ⇔ `‖x−p_e‖/v_e < ‖x−p_p‖/v_p` ⇔
`‖x−p_p‖ > (v_p/v_e)‖x−p_e‖`; the `+r` term comes from requiring the defender to be *strictly*
inside the capture disk at the meeting instant.

## 3. Interception judgement = a small NLP

The attacker advances as far right as possible while staying safe:

$$
\max_{x}\ x_1 \quad \text{s.t.}\quad g_i(x) \le 0,\ i = 1,\dots,m .
$$

- Solve with `scipy.optimize.minimize(method="SLSQP")` on `−x₁`.
- `x₁* < x_d` ⇒ **interception succeeds**; `x₁* ≥ x_d` ⇒ **interception fails**.
- `x*` is the **optimal breakthrough point** (both sides head for it in closed loop).

**Necessary/sufficient:** the NLP optimum is exact for simple motion (convex-ish single
constraint), so `x₁* ⋚ x_d` is a *necessary and sufficient* condition for a single attacker
against a fixed defender set.

## 4. Optimal strategies & closed loop

Isaacs' theory for simple motion: both sides go **full speed to the predicted meeting point**:

$$
u_p = v_p \frac{x^* - p_p}{\|x^* - p_p\|}, \qquad u_e = v_e \frac{x^* - p_e}{\|x^* - p_e\|}.
$$

Re-solve `x*` every control step (receding horizon). Attacker strategies compared in the book:
straight line, sinusoidal manoeuvre, optimal — only the optimal one guarantees the safe-set
payoff. **Open-loop optimum is two straight lines to a fixed point**; the curved closed-loop
path is normal and not sub-optimal.

**3-D layered extension `[book 1.3]`**: judge in the horizontal plane, track altitude by a
rate-limited law, capture needs horizontal `≤ r` **and** vertical `≤ r_v`. The game dimension
and the tracking dimension are decoupled.

## 5. Multi-defender cooperation

- **2v1 `[book 1.4]`**: the attacker must evade *all* defenders ⇒ safe set = **intersection** of
  the single safe sets; add one more constraint `g₂(x) ≤ 0`. Both defenders move to the same
  `x*` ⇒ natural encirclement.
- **mv1 (m pursue 1) `[book 1.4]`**: enumerate all defender combinations `(m,n)` (single and
  pair), evaluate `x₁*(m,n)`, pick the combination minimising `x₁*`; **minimum-headcount rule**:
  if a single-defender subset already attains the minimum, send only one:

$$
(m^*,n^*) = \arg\min_{m\ge n} x_1^*(m,n), \qquad
\text{if } x_1^*(k,k) = x_1^*(m^*,n^*) \text{ then send only } k .
$$

- **mvn task assignment `[book 1.5]`**: build the **feasibility matrix** `xcj_{ij}` (can combo
  `i` alone stop attacker `j`?), then solve a 0-1 ILP:

$$
\max \sum_{i,j} x_{ij} \quad\text{s.t.}\quad
\sum_j x_{ij} \le 1,\ \sum_i x_{ij} \le 1,\ x_{ij} \le xcj_{ij},\
x_{ij}\in\{0,1\},
$$

plus a **conflict constraint** (two combos sharing a defender cannot both sortie). Solve with
`scipy.optimize.milp`. Objective = "stop as many attackers as possible".

## 6. Assumptions & boundaries

- Simple motion only; adding inertia/acceleration limits changes the geometry fundamentally.
- `a > 1` assumed; `a ≤ 1` makes the defender unable to guarantee anything in the open field.
- Perfect information. Under uncertainty see `02-parameter-uncertainty.md`.
- Continuous-time judgement; discrete simulation adds `O(dt)` error.

## 7. Physical interpretation

The Apollonius circle is the set of points the attacker can reach strictly before the defender.
Its radius grows with `a` shrinking… i.e. the *faster* the defender, the *smaller* the
attacker's safe set. `r` gives the defender "free" reach.

## 8. Pitfalls (see `common-pitfalls.md`)

Sign of the SLSQP constraint; initial guess at the defender; integer speed ratio; `a` direction.

## 9. Code

- `examples/pursuit-evasion/apollonius_1v1.py` — judgement, safe set, breakthrough point.
- `examples/multi-agent/assignment_mvn.py` — mv1 selection + mvn ILP.
- `scripts/gtlib/geometry.py` — `apollonius_g`, `solve_breakthrough`, `judge_interception`.
- `scripts/gtlib/assignment.py` — `feasibility_matrix`, `solve_assignment`.

## 10. Research extensions `[ext]`

- Non-zero capture radius ⇒ Cartesian oval (Ch. 3); elliptic/oval safe sets.
- Limited turn rate / Dubins vehicles ⇒ curvature-constrained Apollonius problems.
- Heterogeneous speeds ⇒ weighted Voronoi / multiplicatively-weighted Voronoi partitions.
- Distributed assignment (auction, consensus) instead of centralised ILP.
