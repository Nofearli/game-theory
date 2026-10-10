# 06 · Reconnaissance–return (capture-the-flag) game

`[book]` Ch. 6 (§6.0–6.5). The attacker no longer heads straight for the goal line: it must
**reach a reconnaissance point / boundary first, then return**. The extra round trip turns the
barrier from a hyperbola into a **dome** (2-stage) or a **wedge** (3-stage), and adds a new
concept: **dwell time `τ`**.

## 0. ⚠️ Two coordinate conventions (the single biggest trap)

The source papers differ only by a 90° rotation. **Confirm which frame you are in first.**

| | 6.1 / 6.2 (paper 1) | 6.3–6.5 (paper 2) |
|---|---|---|
| Goal | horizontal `y = 0` | vertical `x = 0` |
| Recon | point `x_r = (0,3)` | boundary `x = l`, `l = 3` |
| Goal / play region | `{y≤0}` / `{y>0}` | `{x≤0}` / `{0<x<l}` |
| Attacker / defender speed | `v_a = 1.0 / v_d = 1.2` | `v_E = 0.5 / v_P = 0.6` |
| `α` | `v_d/v_a = 1.2` | `v_P/v_E = 1.2` |
| Capture radius | `r_j = 0.5` | `r_c = 0.5` |
| Stages | 2 | 3 |

`α = 1.2` numerically in both, **different definitions** — never copy a speed constant across
sections.

## 1. Unified model (three-stage)

State `z = [x_E, y_E, x_P, y_P]ᵀ`, `σ = ±1` dwell direction. Stage variable `ϑ ∈ {1,2,3}`:

| `ϑ` | stage | evader goal | ends when |
|---|---|---|---|
| 1 | recon | reach the entry point `x_I*` on the recon boundary | `x_E = x_I*` |
| 2 | loiter | translate along the boundary by `v_E τ` in direction `σ` | timer `τ` elapses |
| 3 | return | dash to the optimal return / interception point | `x_E ∈ Ω_goal` or captured |

Termination: `T_E = {x_E ≤ 0, ϑ=3}` (evader wins), `T_P = {‖x_E − x_P‖ ≤ r_c}` (captured).
Cost: evader minimises `J = x_E(t_f)`; pursuer maximises it.

## 2. Three core quantities

**(a) Barrier `B`** — the win/lose boundary:

$$
\mathcal B = \{z \mid J_1(z) = 0\},\quad
\mathcal W_E = \{J_1 > 0\}\ (\text{evader wins}),\quad
\mathcal W_P = \{J_1 < 0\}\ (\text{pursuer wins}),
$$

where `J_1` is the optimal value of the **equivalent dwell–return sub-game** (6.3 Eq. 7).
**It must be judged with the virtual (reflected) evader** `x̃_E` (see §4).

**(b) Win-region direction** (easy to flip): 6.1 dome — `W_a` **outside**, `W_d` inside;
6.4 wedge (opening right) — `W_E` **outside**, `W_P` **inside**. Both mean "the further from the
recon point, the safer", but verify with a test point.

**(c) Reachable sets LRR / SRR** (three-stage):

$$
\mathcal R_E^{L} = \{\|x-x_P\| \ge \alpha\|x-x_E'\| + v_P\tau + r_c\}
\quad(\text{safe after dwelling}),
$$

$$
\mathcal R_E^{S} = \{\|x-x_P\| \ge \alpha\, d_S(x) + v_P\tau + r_c\},\quad
d_S(x) = \min_{x_I \in \mathcal L_{recon}} (\|x-x_I'\| + \|x_I-x_E\|).
$$

**Lemma 1 (SRR equivalence):** `R_E^S = R̃_E^L ∩ {x < l}` — the SRR is exactly the virtual LRR
restricted to the physical branch `x < l` (reflect to straighten the two-leg path).
**Successful return is feasible iff `R_E^S ∩ L_goal ≠ ∅`** (Eq. 35).

> **Full derivation:** `../derivations/three-stage-pmp.md` §2–§5 prove the reflection lemma, the
> successful-return condition and the SRR = virtual-LRR equivalence, and derive the trajectory
> symmetry `φ⁽¹⁾* = π − φ⁽³⁾*`; §6 states the paper's PMP relations; §7 gives the `τ_max` scalar
> reduction. Verified by `tests/test_derivations.py` and `tests/test_recon_tad.py`.

## 3. Two-stage barrier (6.1, closed-form dome) + assignment (6.2)

- 6.1: parametric **dome** barrier, Theorem 1 **with proof**; `B̃` circle; triple win-region
  split; AR/PAR + Lemma 1. `F(x_d)` = signed margin; `k_f ∈ {0,1}` = terminal flag.
- 6.2: multi-body **dynamic weighted matching**: Lemma 3 priority ordering + maximum-weight
  matching (Eq. 36/37) + Algorithms 1/2. Paper Case 2: this method captures 4 / escapes 0 vs
  the reference's 3 / 1. Matching weight `w_{ij} = r_i^{-1}` (or `(1+α_i^{-1})r_i^{-1}`);
  re-matching = Algorithm 2. The greedy "whoever detects claims" is the `N_P = N_E` special case
  and does **not** guarantee a maximum total capture.

## 4. PMP → three-stage transformation (6.3)

Use **Pontryagin's maximum principle** to convert the two-stage problem into three stages
(recon / loiter / return): Hamiltonian → constant co-states → transversality ⇒

$$
\nu = 2\alpha\cos\phi^{(3)*}, \qquad \phi^{(1)*} = \pi - \phi^{(3)*}.
$$

Includes the **virtual evader** `x̃_E = (2l − x_E, y_E + σ v_E τ)` (reflect + translate) so the
dwelling phase straightens into a single leg. Remark 1: the virtual (imaginary) evader.

## 5. Three-stage barrier & reachable sets (6.4)

Theorem 2: parametric **wedge** barrier (opening right) with an **envelope proof**. Lemma 1
reflection equivalence; Lemma 2 the virtual LRR is **strictly convex**. The barrier evolves with
`τ`; Case A ∈ `W_P`, Case B ∈ `W_E`.

## 6. Optimal three-stage strategy & max dwell time (6.5)

- Eq. 37: three-stage **state-feedback** optimal strategy — three straight segments
  `E(0) → x_I* → x_I*′ → x̃_L`, and `P(0) → x̃_L` one straight line.
- **Max dwell time `τ_max`**: Theorem (existence + uniqueness) + a scalar-reduction lemma
  (reduce to a scalar root-finding problem in `G_σ(y_r)`).
- Reproduces paper §VI Experiment 1/2 and Fig. 11 (e.g. Case A cumulative times
  `3.39 / 4.39 / 13.12 s`, `τ_max = 2.85 s`).

## 7. Assumptions & boundaries

- Full information (unlike Ch. 4); complexity is in the *task structure* (round trip + dwell).
- Two-player (reconnaissance vs interception); three-player TAD is Ch. 5.
- Simple motion; point capture with radius `r_c`.
- The barrier is judged in **virtual coordinates**.

## 8. Pitfalls

Coordinate convention (§0); virtual vs physical coordinates; copying `α`/speeds across 6.1↔6.3;
win-region side; the discrete `O(dt)` tie error at the barrier.

## 9. Code

- `examples/reconnaissance-return/recon_2stage.py` — 2-stage dome barrier + closed loop.
- `examples/reconnaissance-return/recon_3stage_dwell.py` — dwell time `τ_max` by scalar reduction.
- `scripts/gtlib/recon.py` — `virtual_evader`, `dome_barrier`, `wedge_barrier`, `max_dwell_time`.

## 10. Research extensions `[ext]`

- Two goal lines (the third source paper's TIE line — not yet expanded in the book).
- Multi-evader / multi-pursuer with dwell constraints + dynamic assignment.
- Reconnaissance under partial information (merge with Ch. 4).
- Learning-based reconnaissance-return when the analytic barrier is intractable.
