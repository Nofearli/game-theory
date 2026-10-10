# 05 · TAD three-body game (Target–Attacker–Defender)

`[book]` Ch. 5 (§5.1–5.2). Three players: attacker **A** captures target **T** (A has a non-zero
capture radius `r`: `‖x_T − x_A‖ ≤ r`), defender **D** intercepts A (point capture) to escort T
away. A and D are **equal-speed** — the hard regime classical methods do not cover for
"equal speed + non-zero capture radius".

## 1. Model & termination sets

$$
\dot x_A = v_A(\cos\beta,\sin\beta),\quad
\dot x_D = v_D(\cos\delta,\sin\delta),\quad
\dot x_T = v_T(\cos\zeta,\sin\zeta),
$$

`v_A = v_D` (normalise `v_A = 1`), `γ = v_T/v_A < 1`; controls `β, δ, ζ ∈ [−π, π]`. Termination:

$$
\mathcal T_1: \|x_T - x_A\| \le r\ (\text{A hits T}), \qquad
\mathcal T_2: \|x_D - x_A\| = 0\ (\text{D intercepts A}).
$$

## 2. Game of Degree — who wins *how well* (Eq. 5–7)

Initial states where A hits T before D intercepts belong to `Z_c`; there the T–D team
**minimises** the terminal T–D separation and A **maximises** it:

$$
J(\beta,\delta,\zeta;x_0) = \Psi(x_f) = \|x_{Tf} - x_{Df}\|, \qquad
V(x_0) = \max_{\beta(\cdot)}\min_{\delta(\cdot),\zeta(\cdot)} J .
$$

## 3. Solution by two-sided PMP

Hamiltonian `H`, co-states `λ`, transversality ⇒ the optimal controls are constants (heading
angles) and **all three players head straight for the optimal capture point `z*`**, which solves
two algebraic equations (Eq. 14–15):

- Eq. (14): the Apollonius **oval** (boundary of T's escape set) — `z*` lies on it;
- Eq. (15): the optimality curve — its intersection with the oval on the correct branch gives
  `z*`. Which branch is valid is fixed by a **mean-value (intermediate-value) condition**
  (Remark 5).

The value function satisfies the **HJI equation** (Nash equilibrium):

$$
\max_{\beta}\min_{\delta,\zeta} H = 0 .
$$

**Derivation outline `[book 5.1]`:** write `H`; the co-states are constant on the optimal
trajectory; the transversality condition at `T_1` gives the terminal costate; substituting the
constant controls yields the two algebraic equations; the mean-value condition selects the
physical root; verify `HJI` numerically.

## 4. Game of Kind — who wins *at all* (Eq. 50–66)

The optimal strategy of §3 is valid only **inside A's winning set `Z_c`**. Given an initial
state, first answer *whether* it is in `Z_c`:

- Draw the A–T Apollonius oval (Eq. 14) and **A's limit-interception curve** (Eq. 56).
- If the two are **separated or tangent** ⇒ A wins (`Z_c`);
- if they **intersect** ⇒ T–D wins (`Z_t`).
- The barrier divides `Z_c / Z_t`.

**Limit case** (Fig. 5): when T's initial position is *on* the barrier, at the terminal instant A
is exactly at the meeting point — a strict tie.

## 5. Assumptions & boundaries

- Equal speed `v_A = v_D`; `v_T < v_A`. Adding a superior pursuer (`v_D > v_A`) is the
  Neurocomputing 2025 extension (see the book's references).
- Point capture for D; non-zero radius `r` only for A.
- Full information, simple motion.
- Game of Degree presupposes `x_0 ∈ Z_c`; always run the Kind check first.

## 6. Pitfalls

- Solving the Degree problem without first checking `x_0 ∈ Z_c` (the strategy may be invalid).
- Confusing the oval (escape-set boundary) with the limit-interception curve.
- Picking the wrong branch of Eq. (15) (the degenerate symmetric branch passes through A and T;
  the *selected* one is the right-side intersection, justified by the mean-value condition).
- Assuming the TAD result extends to unequal speeds.

## 7. Code

- `examples/tad/tad_optimal.py` — oval + optimality curve, `z*`, closed-loop capture check.
- `scripts/gtlib/tad.py` — `apollonius_oval`, `optimal_capture_point`, `hji_residual`.

## 8. Research extensions `[ext]`

- Superior-pursuer TAD (`v_D > v_A`) and inferior-pursuer regimes.
- Active defence / barrier-function constructions for TAD (Automatica 2026 line).
- Multi-attacker / multi-defender TAD ⇒ team game, assignment coupling.
- TAD with partial observation or communication delay.
- Learning-based TAD when no analytic `z*` exists (see `07-rl-and-learning-games.md`).
