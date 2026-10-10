# Coding conventions

Rules for every script produced by this skill (examples, scripts, generated research code).

## 1. Structure

Split every game implementation into five clearly separated layers:

```
dynamics      # ẋ = f(x, u); simple motion, integrators
strategy      # control laws: optimal, straight, sinusoidal, proportional, learned
optimiser     # SLSQP / MILP / root-finding that produces targets or decisions
termination   # capture / goal / time-out predicates
plotting      # IEEE-style figures (see simulation/plotting-standards.md)
```

Do not let plotting import from the optimiser or vice-versa. A simulation driver composes them.

## 2. Parameters

- Centralise **all** parameters in one `dataclass` (or a `params.py`).
- Never hard-code a speed, radius, `dt`, seed or initial position inside a function body.
- Validate parameters at construction (`α > 1`, `dt > 0`, `r ≥ 0`).

## 3. Numerical hygiene

- Check `res.success` (and `res.status`) for every optimiser call; raise or fall back explicitly.
- Guard degeneracies: `Δx = 0` in the bisector formula, `‖·‖ = 0` in normalisations.
- Treat **infeasible** and **unbounded** separately from "no interception".
- For discrete simulation, report and justify `dt`; show the `O(dt)` convergence on a degenerate
  case where the analytic answer is known.
- Use `np.hypot` / vectorised NumPy; avoid Python loops over time where a vector works.

## 4. Reproducibility

- `np.random.default_rng(seed)` with an explicit seed argument; never the global RNG.
- Save outputs (CSV/JSON + figures) into a directory passed in, defaulting to `./out/`.
- Print a one-line summary (parameters + result) so runs are self-documenting.
- Record library versions when a result is meant to be cited.

## 5. Interface

- Every module has a docstring stating: purpose, inputs, outputs, how to run.
- Every example is runnable as `python <file>.py` with no arguments (sensible defaults).
- Keep an `if __name__ == "__main__":` entry point.
- Public functions are pure where possible (no hidden global state).

## 6. Tests

- Every mathematical invariant gets a test: `r → 0` degeneracy, simultaneous-arrival identity,
  barrier joint continuity, assignment optimality vs brute force on small instances,
  `τ_max` root correctness.
- Tests live in `tests/` and run with `python tests/run_tests.py` (no pytest required).
- A test must be able to fail; assert against an independently-computed value, not against the
  function's own output.

## 7. Naming

- Functions: `verb_noun` (`solve_breakthrough`, `barrier_1v1`, `max_dwell_time`).
- Physical quantities keep their paper symbols as suffixes (`a`, `alpha`, `r`, `tau`).
- Distinguish `pursuer`/`defender` and `evader`/`attacker` consistently with the theory file.

## 8. What not to do

- No silent unit changes (metres vs millimetres).
- No mixing the two Ch. 6 coordinate conventions in one module.
- No plotting inside an optimisation loop.
- No "tuned to look good" constants without a comment and a source.
