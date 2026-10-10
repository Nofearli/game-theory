# English phrasing for game-theory papers

Reusable, venue-appropriate sentence patterns. **Never invent citations, numbers or results** —
leave a clearly-marked placeholder instead (e.g. `[REF]`, `[VALUE]`).

## 1. Defining the game

- "We consider a pursuit–evasion differential game in which the pursuer `P` and the evader `E`
  evolve under simple motion, `ẋ_i = v_i u_i`, `‖u_i‖ = 1`."
- "The evader wins if it reaches the target set `𝒯` without being captured; the pursuer wins if
  `‖x_P − x_E‖ ≤ r` at some time."
- "Throughout, `α = v_P / v_E > 1` denotes the speed ratio."

## 2. Stating assumptions

- "We assume, without loss of generality, that …"
- "The following assumption is required for tractability and is standard in this literature."
- "Unlike [REF], we do **not** assume perfect state information."

## 3. Definitions

- "**Definition 1 (Barrier).** The barrier `ℬ` is the set of initial evader positions for which
  the game value is zero."
- "We say a strategy is *winning* if it guarantees termination in `𝒯_P` for every admissible
  opponent control."

## 4. Theorems & lemmas

- "**Theorem 1.** Under Assumptions 1–3, the barrier admits the closed-form representation …"
- "**Lemma 2.** The virtual reachable set is strictly convex."
- "**Proof.** The proof is by contradiction. Suppose …"
- "**Corollary 1.** It follows immediately from Theorem 1 that …"

## 5. Optimality statements (be precise)

- "the pair `(u_P*, u_E*)` constitutes a saddle-point (Isaacs) equilibrium" — *not* "the optimal
  strategy" when only one side is optimised.
- "…is optimal in the sense of minimising the worst-case cost over admissible opponent controls."
- "we provide a **numerical** optimal solution; no closed form is claimed."

## 6. Hedging honestly

- "This bound is necessary but not sufficient."
- "The result is established for point capture; the extension to `r > 0` is left open."
- "Numerical evidence suggests … ; a proof is not available."
- "Simulations corroborate the theoretical prediction but do not constitute a proof."

## 7. Simulation section

- "All simulations were run with parameters listed in Table I, using a fixed random seed
  (`seed = [SEED]`); each condition was repeated `N = [N]` times and we report the mean ± 95% CI."
- "As predicted by Theorem 1, the measured capture time agrees with the analytic value to within
  the discretisation error `O(Δt)`."
- "Baselines are given identical information and an equal tuning budget."

## 8. Contributions (Introduction)

- "The main contributions of this paper are threefold. First, we … Second, … Third, …"
- "To the best of our knowledge, this is the first analytical barrier for …"

## 9. Conclusion

- "The results hold under simple motion and full information; relaxing either is left for future
  work."
- "A limitation of the proposed approach is …"

## 10. Phrasing to avoid

| Avoid | Prefer |
|---|---|
| "obviously", "clearly" (for a non-trivial step) | give the argument |
| "optimal" for a heuristic | "near-optimal on the tested distribution" |
| "proves" for a simulation | "supports", "corroborates" |
| "novel" without a diff against prior art | state the concrete difference |
| "significantly better" without a statistic | report the effect size / CI |
