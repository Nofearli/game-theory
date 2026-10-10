# Common pitfalls

Errors that most often invalidate a pursuit–evasion / differential-game result, a proof, or a
simulation. Each entry: **symptom → cause → fix**. `[book]` = drawn from 《博弈书籍.md》,
`[ext]` = general research practice.

## A. Conceptual confusions (most damaging)

1. **Barrier vs reachable set vs winning region.** `[book]`
   - *Symptom*: mixing "who reaches x first" with "which initial positions break through".
   - *Cause*: barrier's independent variable is the **attacker's initial position**; a reachable
     set's is a **spatial point**.
   - *Fix*: state the independent variable before writing any equation.

2. **Game of Kind vs Game of Degree.** `[book]`
   - Kind = *who wins* (set-valued / barrier). Degree = *the value* once a winner is fixed
     (optimisation). Solving a Degree problem does not answer a Kind question.

3. **Open-loop vs feedback (state-feedback) optimality.** `[book]`
   - The 1v1 open-loop optimum is two straight lines to a *fixed* capture point. The closed-loop
     receding-horizon solution re-solves the point each step and curves.
   - A curved trajectory is **not** evidence of sub-optimality. Do not call an open-loop plan a
     feedback law.

4. **Heuristic ≠ optimum.** `[ext]` Never call a proportional-navigation / pursuit / greedy
   assignment "optimal" unless you have a proof or a verified Bellman/HJI certificate.

5. **Simulation ≠ proof.** `[ext]` A passing simulation supports a claim; it does not establish
   it. Label numerical evidence as such.

## B. Coordinate & symbol traps

6. **Speed-ratio definition.** `[book]` `a`, `α`, `ratio = α⁻¹`, `ν = v_E/v_P`, `γ = v_T/v_A`
   all appear; Ch. 6 uses `α = 1.2` with **two different definitions**. Restate before use.

7. **Barrier/winning-region side.** `[book]` "which side of the barrier is the attacker's
   winning region?" is easy to flip. In Ch. 6 the attacker wins *outside* the dome/wedge; the
   defender wins *inside*. Always verify with a single hand-computable test point.

8. **`α` direction in radius formulas.** `[book]` arc radius `‖D − m‖/α` assumes `α = v_P/v_E > 1`.
   Using `v_E/v_P` flips the whole three-branch curve.

9. **Vertical vs horizontal target line (Ch. 6).** `[book]` 90° rotation between papers. Confirm
   which frame you are in before reusing a constant or a figure.

10. **Imaginary vs physical coordinates (Ch. 6, three-stage).** `[book]` The barrier must be
    judged with the **virtual (reflected) evader** `x̃_E`; using physical coordinates gives a
    wrong barrier. See `references/theory/06-reconnaissance-return.md`.

## C. Numerical / implementation traps

11. **Constraint sign.** `[book]` `scipy.optimize` uses `fun(x) ≥ 0`; the Apollonius constraint
    `g(x) ≤ 0` must be passed as `-g(x) ≥ 0`. A "breakthrough point behind the defender" almost
    always means the sign is flipped.

12. **Initial guess at the defender's position.** `[book]` `‖x − p_p‖` has a singular gradient
    there; SLSQP fails. Start from the attacker's position.

13. **Integer speed ratio.** `[book]` `5/3` written as `1` (integer division). Use
    `round(v_p/v_e, 5)`.

14. **Step size too large.** `[book]` A large `dt` lets a step "jump through" the capture disk;
    capture time is then wrong by `O(dt)`. Reduce `dt` and confirm convergence.

15. **Negative `r_eff`.** `[book]` Under large uncertainty `r_eff = r − a·ξ` can go negative; the
    judgement function must handle it (it does, but a plotting routine may not).

16. **Degenerate optimisation / solver failure.** `[ext]` Always check `res.success`, guard
    `Δx = 0` in the perpendicular-bisector formula, and treat "infeasible" separately from
    "unbounded".

17. **RNG not fixed / not reported.** `[ext]` Monte-Carlo results are meaningless without a seed
    and a sample count. Fix the seed, report N, report the CI.

## D. Modelling & claim traps

18. **Mixing continuous-time theory with discrete simulation silently.** `[book]` Barrier
    "ties" become `±r` by one integration step in discrete time; do not report a discrete
    near-tie as a strict theorem.

19. **Unstated assumptions in a proof.** `[ext]` List every assumption (informational symmetry,
    convexity, non-degeneracy, `α > 1`, …). A theorem without its hypotheses is not a theorem.

20. **Over-claiming generality.** `[ext]` A 1v1 result does not automatically extend to `m v n`;
    state the extension's extra requirements.

21. **Unfair baselines.** `[ext]` Comparing a tuned method against an untuned baseline, or
    against a method given less information, is not evidence.

22. **Fabricated support.** `[ext]` Never invent a citation, a numerical value or an experiment.
    If a number is needed and unknown, compute it or mark it as a placeholder.

## E. Writing traps `[ext]`

23. Presenting a *necessary* condition as *sufficient* (or vice-versa).
24. Reporting a single seed as a result.
25. Figures that do not support the text's claim, or axes with unequal aspect ratio that make a
    trajectory look "wrong".
