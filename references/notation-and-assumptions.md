# Notation, conventions and assumptions

> **Read this before any derivation.** The source book mixes several conventions across
> chapters. Getting a symbol wrong silently flips a result (see `common-pitfalls.md`).
> Provenance tags: `[book]` = from 《博弈书籍.md》; `[ext]` = added here.

## 1. Global model: simple motion (first-order integrator) `[book]`

$$
\dot{\mathbf p}_i = \mathbf u_i, \qquad \|\mathbf u_i\| \le v_i, \qquad i \in \{p, e\}
$$

- Speed is fixed, heading free (simple motion). This is the atom of *all* six chapters.
- Capture (point capture): `‖p_p − p_e‖ ≤ r`. With capture radius `r > 0` the boundary is a
  **Cartesian oval**, not an Apollonius circle `[book]`.

## 2. Speed ratio — **two different symbols, do not mix** `[book]`

| Symbol | Definition | Where used | Meaning |
|---|---|---|---|
| `a` | `v_p / v_e > 1` | Ch. 1, 2 (defence vs attacker) | defender is faster |
| `α` | `v_P / v_E > 1` | Ch. 3, 4, 6 | same idea, book's barrier notation |
| `ratio` | `α⁻¹ = v_E / v_P < 1` | code in Ch. 3 | the *inverse* used in some scripts |
| `ν` | `v_E / v_P < 1` | Ch. 3.5 (Dorothy) | pursuer normalised to 1 |
| `γ` | `v_T / v_A < 1` | Ch. 5 (TAD) | target speed relative to attacker |
| `α` | `v_d / v_a = 1.2` | Ch. 6.1–6.2 | **different definition, same numeric value** |
| `α` | `v_P / v_E = 1.2` | Ch. 6.3–6.5 | same numeric value again |

⚠️ In Ch. 6 the *numerical value* of `α` is `1.2` in both sub-conventions but the *definition*
differs. **Never copy a speed constant across sections.** Always restate the definition.

## 3. Coordinate conventions `[book]`

**Ch. 1–2, 4, 5** — arena `[-x_max, x_max] × [-y_max, y_max]`, defence line vertical
`x = x_d` (experiment `x_d = 3 m`). Attacker wins if `x ≥ x_d`; defender wins by capture.

**Ch. 3** — target segment `mn` of length `l`; escape point `τ = (τ, 0)` on the target line.
Barrier parameterised by the attacker's *initial* position `z`.

**Ch. 6 — two sub-conventions (⚠️ 90° rotation apart):**

| | Paper 1 (6.1 / 6.2) | Paper 2 (6.3–6.5) |
|---|---|---|
| Goal line | horizontal `y = 0` | vertical `x = 0` |
| Recon point/boundary | point `x_r = (0, 3)` | line `x = l`, `l = 3` |
| Goal region | `{y ≤ 0}` | `{x ≤ 0}` |
| Play region | `{y > 0}` | `{0 < x < l}` |
| Stages | 2 (recon / return) | 3 (recon / loiter / return) |
| Attacker / defender speed | `v_a = 1.0 / v_d = 1.2` | `v_E = 0.5 / v_P = 0.6` |
| Capture radius | `r_j = 0.5` | `r_c = 0.5` |

## 4. Geometry objects — **distinct concepts** `[book]`

| Object | Independent variable | Question answered |
|---|---|---|
| **Apollonius circle / escape set** | a point `x` in space | "given current positions, who reaches `x` first?" |
| **Cartesian oval** | a point `x` in space, `r > 0` | same, with non-zero capture radius |
| **Reachable set** `R_E` | a point `x` | attacker can reach `x` before defender |
| **Barrier** `B` | the **attacker's initial position** | "for a fixed deployment, which initial attacker positions still break through?" |
| **Winning regions** `W_P / W_E` | initial state | split by the barrier: `B` = both can guarantee? neither? |
| **Safety set / CBF** `[ext]` | state | set that must stay invariant |

Do **not** conflate barrier, reachable set, winning region and safety region.

## 5. Time-to-go and the Apollonius inequality `[book]`

$$
t_p(x) = \frac{\|x - p_p\|}{v_p}, \quad t_e(x) = \frac{\|x - p_e\|}{v_e}, \quad
t_e < t_p \iff \|x - p_p\| \ge a\,\|x - p_e\|
$$

With capture radius `r` (and effective radius `r_eff = r − a·ξ` under uncertainty):

$$
g(x) = -\|x - p_p\| + a\,\|x - p_e\| + r_{eff} \le 0 \quad\text{(attacker safe set)}
$$

## 6. Barrier building blocks `[book]`

1v1 analytic barrier (escape point `τ(x) = (α²x − x_D)/(α² − 1)`; middle branch is a
hyperbola, end branches are arcs; joints `δ₁ = x_D/α²`, `δ₂ = δ₁ + (1 − α⁻²)l`).

Cartesian-oval parameterisation by escape point `τ` (Xu 2024, Thm 4.1):

$$
m = \frac{\|\tau - D\| - r}{\alpha}, \qquad
n = \frac{\tau - D_x}{\alpha\,\|\tau - D\|}, \qquad
z(\tau) = \big(\tau - mn,\ m\sqrt{1-n^2}\big)
$$

## 7. Optimal-control / game-theory objects `[book]`

- Hamiltonian `H`, co-states `λ`, transversality conditions, PMP.
- HJI/HJB equation for the value function `V`; Isaacs condition ⇒ saddle point.
- Game of **Kind** = who wins (a *set* / barrier question). Game of **Degree** = the value of
  the game given a winner (an *optimisation* question).
- Optimal strategies in simple-motion games are **full-speed toward the optimal capture point**;
  the closed-loop law re-solves that point every step (receding horizon / MPC-like).

## 8. Standing assumptions `[book]`

- Simple motion, bounded speed, no inertia (unless stated).
- Perfect state information **unless** the chapter is explicitly about partial information
  (Ch. 4) or observation error (Ch. 2).
- Capture = point capture unless `r > 0` is given.
- Continuous-time theory; discrete simulation introduces step-size error `O(dt)` — see
  `common-pitfalls.md`.

## 9. Notation hygiene rules `[ext]`

1. Restate every symbol's definition at first use in a derivation.
2. Keep one symbol per concept within a single answer; if you must switch conventions, show a
   mapping table (like §3 above).
3. Bold upright for vectors `\mathbf{x}`; italic for scalars; `\|\mathbf{x}\|_2` for the norm.
4. Prefer inline `\(...\)` for short expressions, display `$$...$$` only for key equations.
