# 04 · Partial-information games

`[book]` Ch. 4 (§4.0–4.4). The defender has only a **finite sensing radius** `r`; the attacker
is omniscient. Uncertainty is upgraded from *numerical error* (Ch. 2) to **missing information
structure** — filtering cannot recover it.

## 1. Problem class

- Two differences from Ch. 1: (i) the goal is a **segment** `T` (endpoints `m, n`, length
  `l = ‖m−n‖`), the attacker wins by crossing the "gate"; (ii) **asymmetric information** — the
  defender sees the attacker only inside its sensing disk `S` (radius `r`); before the detection
  instant `t_c` it does not know where the attacker is.
- Simple motion; `α = v_P/v_E > 1` (same as Ch. 1's `a`).
- Two phases: **deployment** (before `t_c`, the defender knows nothing → the *deployment point
  itself is the decision variable*) and **capture** (after `t_c`).

## 2. Escape set & Apollonius circle

Escape set `R_E` (attacker reaches before defender) and its boundary:

$$
x_A = \frac{\alpha^2 x_E - x_P}{\alpha^2 - 1}, \qquad
R_A = \frac{\alpha\|x_E - x_P\|}{\alpha^2 - 1},
$$

i.e. the Apollonius circle centred at `x_A` with radius `R_A` (inside = attacker advantage).
Geometrically equivalent to Ch. 1's half-plane view; here the goal is a segment.

## 3. Capture law `Γ_P^δ` (after detection)

At `t_c` (attacker enters the sensing disk) lock the disk `A_δ`: centre `x_A(t_c)`, radius
`R_{A_δ} = R_A(t_c) + δ`. Capture law (paper Eq. 4):

$$
z_P = (R_{A_δ} - R_A)\,\hat d + \alpha^{-1} y, \qquad u_P = \hat z_P,
$$

with `d̂ = (x_E − x_P)/‖·‖` the line-of-sight unit vector and `y = x_A − x_A(t_c)` the current
Apollonius centre offset from the locked centre. Guarantee: after detection the P–E distance is
**monotonically non-increasing**, with finite-time capture inside `A_δ`.

## 4. Full-information optimal deployment: segment midpoint

Split the attacker-winning region into `S_{F1}, S_{F2}, S_{F3}` (projections of the escape set on
the three sub-segments) and minimise `S_{F1} + S_{F3}`:

$$
\min (S_{F1}+S_{F3}) \Rightarrow x_P = x_Q = l/2,
$$

i.e. the full-information optimal deployment is the **midpoint** `(l/2, 0)` (`S_{F2}` is also
minimised at `l/2` by the integral mean-value theorem). Intuition: standing at the midpoint makes
the left/right exposed areas symmetric and minimal.

## 5. Ambiguity region (the key partial-information concept)

$$
W_S^P = W_B^P \cap S \ (\text{sensing win region}), \qquad
F = W_B^P \setminus S \ (\text{ambiguity region}).
$$

- Attacker entering `W_S^P` is detected; the capture law `Γ_P^δ` guarantees a win (Lemma 1).
- Attacker staying in `F` is invisible ⇒ no guarantee.

Optimal deployment minimises the ambiguity region — ideally the sensing disk covers the whole
barrier `B(x_P)`. The required radius varies with the deployment point, and `r` is fixed ⇒ the
central theorem below.

## 6. Theorem 2 — optimal deployment under partial information

Let `d(x_P)` be the max distance from the defender to the barrier (the max is attained at the
barrier endpoints `x_left / x_right`). The minimum sensing radius needed to cover the whole
barrier is smallest at `(l/2, 0)`:

$$
R_\alpha = (1 + \alpha^{-1})\frac{l}{2},
$$

$$
\boxed{\ x_{opt} = \begin{cases}
\left(\dfrac{l}{2},\ 0\right), & r > R_\alpha \ (\text{disk covers the barrier: guard the midpoint})\\[2mm]
\left(\dfrac{l}{2},\ -\dfrac{r}{1-\alpha^{-1}}\right), & r \le R_\alpha \ (\text{sit } \tfrac{r}{1-\alpha^{-1}} \text{ below the goal line})
\end{cases}\ }
$$

Reading: `r > R_\alpha` ⇒ the attacker must be detected before it can reach the barrier ⇒
reduces to full information, midpoint optimal; `r ≤ R_\alpha` ⇒ an ambiguity region exists, the
worst case treats `F` as attacker-winning, so the defender drops below the goal line to "plug"
the attacker's mandatory path — detection then still leaves enough margin to intercept before the
barrier.

## 7. Extensions in the chapter

- **4.3 heterogeneous multi-player**: 2v2 = two independent 1v1 (whoever detects which evader
  claims it; claim-on-detection, no re-assignment). Extra symbol table in 4.0/4.3.
- **4.4 3-D convex target region**: potential-function / Apollonius-ball intersection,
  Theorem 1 Case 2, Corollary 3 Voronoi deployment; cooperative multi-pursuer single-evader.

## 8. Assumptions & boundaries

- Attacker omniscient; defender sensing is a hard disk (no noise) — this is *structural*
  information loss, not Ch. 2's error.
- The capture law needs the attacker inside the disk at some time; if the attacker never enters
  `W_S^P`, no guarantee.
- Deployment is open-loop (a one-off choice) before detection.

## 9. Pitfalls

Do not confuse `W_S^P` (sensing win region) with `W_B^P` (barrier win region) or `F`. `α` here is
`v_P/v_E`. The "optimal deployment" is a *deployment-stage* result, not a feedback law.

## 10. Code

- `examples/partial-observation/partial_info_1v1.py` — P1–P4 scenarios, deployment curve.
- `scripts/gtlib/partial_info.py` — `law_p_optimal_capture`, `optimal_defensive_point`,
  `ambiguity_region`.

## 11. Research extensions `[ext]`

- Multiple defenders with overlapping sensing ⇒ coverage / Voronoi deployment.
- Moving/patrolling deployment (the defender need not stand still).
- Probabilistic detection (detection radius with a detection function `p(d)`).
- Partial information for the attacker too (both sides blind) ⇒ a game of incomplete information.
