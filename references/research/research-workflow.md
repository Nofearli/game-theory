# Research workflow — from an idea to a paper contribution

The canonical pipeline the skill follows in **Mode A** (and the checklist for any new result).

## 0. The pipeline

```
scenario & scientific question
      → state of the art
      → limitation of existing methods
      → candidate innovation point
      → mathematical model
      → theoretical derivation
      → algorithm implementation
      → simulation verification
      → paper contribution
```

Each arrow is a *gate*: do not proceed until the previous step is explicit and defensible.

## 1. Scenario & scientific question

- One sentence: *who* must do *what*, under *which* information and dynamics, to *whom*.
- Convert it into a **falsifiable question**: "does the barrier remain a dome when `r > 0`?"
  not "can we improve defence?".
- Classify with `problem-taxonomy.md`.

## 2. State of the art → limitation

- State the *closest* existing result and its exact assumptions.
- Name the assumption you will relax. A contribution almost always = "we remove assumption X".
- Common relaxation targets: equal speed, perfect information, zero capture radius, single stage,
  convex target, known opponent model.

## 3. Candidate innovation point — be specific

Give a **testable proposition**, not a method name. Compare:

- ✗ "We propose a deep RL method for pursuit–evasion."
- ✓ "We conjecture that the two-stage reconnaissance barrier stays a simple closed curve when
  the dwell time is bounded by `τ_max`, and derive the closed form."

Classify the contribution:

| Type | Evidence needed |
|---|---|
| Strict theory | definition + theorem + proof + boundary cases |
| Algorithm | complexity + correctness + empirical advantage over a fair baseline |
| Experimental | a controlled study that isolates the claimed effect |
| Engineering | a system that meets a quantified requirement |

## 4. Modelling

Write down: state, control, information structure, payoff, strategy space, termination. State
every assumption. Use `notation-and-assumptions.md`. Check consistency with the classification.

## 5. Derivation

- Prefer a **closed form**; otherwise a parametric or scalar reduction (e.g. Ch. 6.5's scalar
  root-finding) — a one-dimensional reduction is itself a contribution.
- Necessary vs sufficient conditions must be labelled.
- Verify each step against a degenerate case (e.g. `r → 0`, `α → 1`, single player).

## 6. Implementation

- Reproduce the analytic result numerically first (same numbers to `~1e-10` on degenerate cases).
- Then implement the general case. Follow `../coding/coding-conventions.md`.

## 7. Simulation verification

Design the experiment **before** coding it (`../simulation/experiment-design.md`). The simulation
must be able to *falsify* the proposition. A simulation that can only confirm is not a test.

## 8. Paper contribution

- One paragraph per contribution: *claim → evidence → where in the paper*.
- Every claim must map to a theorem, a table, or a figure.

## 9. Innovation patterns (reusable) `[ext]`

- **Relax an assumption** (the ladder in `problem-taxonomy.md` §4).
- **Combine two chapters**: e.g. barrier (Ch. 3) + partial information (Ch. 4);
  reconnaissance (Ch. 6) + uncertainty (Ch. 2).
- **Analytic + learning**: analytic expert → warm-started RL, with the analytic result as the
  optimality benchmark.
- **Change the target**: segment → convex region (Ch. 4.4 shows this move).
- **Add a constraint**: dwell time (Ch. 6), actuator limits, communication delay, no-fly zones.
- **Decentralise**: replace a central ILP with a distributed auction; prove equivalence.

## 10. Anti-patterns

- A "new algorithm" that is a renamed standard one.
- A "theorem" that restates an assumption.
- A benchmark against an untuned or under-informed baseline.
- A result that holds only for one parameter set.
- Presenting a simulation curve as a proof.
