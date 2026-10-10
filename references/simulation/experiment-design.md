# Simulation & experiment design

The skill must help decide **what experiment can actually prove the claim**. Five experiment
classes, each with a purpose, controls, metrics and the conclusion it can support.

## 1. Experiment classes

### (a) Theory-validation experiment
- **Purpose:** show the implemented result matches the analytic prediction.
- **Controls:** fix parameters; compare simulation vs closed form on a degenerate case
  (`r→0`, `τ→0`, 1v1) where the analytic value is exact.
- **Metrics:** absolute/relative error vs the analytic value (expect `~1e-10` on degenerate
  cases, `O(Δt)` in general).
- **Supports:** "the implementation is correct".

### (b) Performance-comparison experiment
- **Purpose:** show the proposed method beats baselines.
- **Controls:** identical information and tuning budget; ≥ 5 seeds.
- **Metrics:** win/capture rate, capture time, distance-to-goal, control effort.
- **Supports:** "the method is better on this distribution".

### (c) Ablation experiment
- **Purpose:** attribute the gain to a specific component.
- **Controls:** remove one component at a time.
- **Metrics:** delta in the primary metric.
- **Supports:** "component X contributes Y".

### (d) Sensitivity experiment
- **Purpose:** show robustness to parameter choice.
- **Controls:** sweep one parameter (`α`, `r`, noise level, `dt`).
- **Metrics:** metric vs parameter curve; identify the break point.
- **Supports:** "the result is not an artefact of one parameter set".

### (e) Robustness experiment
- **Purpose:** show behaviour under uncertainty / adversarial input.
- **Controls:** Monte-Carlo over noise; worst-case opponent; unseen initial conditions.
- **Metrics:** success probability with CI; worst-case cost.
- **Supports:** "the guarantee degrades gracefully".

## 2. Design template (fill before coding)

```
Claim under test:      ...
Experiment class:      (a)/(b)/(c)/(d)/(e)
Independent variable:  ...
Controlled variables:  ...
Baselines:             ...
Metrics + CI:          ...
Seeds / N:             ...
Expected observation:  ...
Conclusion it supports: ...
What would falsify it: ...
```

## 3. Standard visualisations for pursuit–evasion

| Figure | Shows | Notes |
|---|---|---|
| Trajectory plot | geometry of the game | defender blue, attacker red, helper green; equal aspect |
| Distance–time curve | capture time, monotonicity | mark the `r` threshold |
| Heading-angle curve | control behaviour | useful for "unexpected strategy" |
| Control-input curve | effort / saturation | mark the speed bound |
| Barrier / reachable set | deployment feasibility | fill winning regions with low-saturation colours |
| Capture-time / success histogram | distribution over seeds | report mean ± CI |
| Assignment diagram | who chases whom | bipartite or annotated arena |

## 4. Reproducibility rules `[ext]`

- Fix and report the seed; report `N`; report the CI method.
- Save raw results (CSV/JSON) **and** the figures; keep a parameter file.
- One script = one experiment; a `run_all.py` reproduces every figure.
- Never edit a figure by hand; regenerate from data.
- Record library versions (`numpy`, `scipy`, …).

## 5. Common mistakes

- A single seed reported as a result.
- A baseline that is under-tuned or under-informed.
- A sweep that changes two parameters at once.
- A figure that cannot be read in greyscale (colour-only encoding).
- A simulation that can only confirm (no falsification condition).
