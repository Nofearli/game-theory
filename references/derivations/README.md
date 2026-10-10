# Derivations

Self-contained mathematical derivations that back the theory notes. Each file states its
**status** (rigorous `[new]` vs. reconstruction) and lists the tests that verify it.

| File | Topic | Status |
|---|---|---|
| `barrier-1v1-closed-form.md` | 1v1 analytic barrier: criticality functional, escape-point map, three branches, joint continuity | rigorous |
| `cartesian-oval-parameterisation.md` | `r > 0` barrier as a Cartesian oval; feasibility window; similar-points / barrier-ratio; exact `r→0` degeneration | rigorous |
| `three-stage-pmp.md` | reconnaissance–return: reflection lemma, successful-return condition, SRR = virtual LRR, trajectory structure, `τ_max` scalar reduction; PMP relations quoted | mixed (§2–5,7 rigorous; §6 quoted) |

## Conventions

- `[new]` = derived here from stated assumptions; `[book]` = taken from 《博弈书籍.md》.
- Every derivation ends with a **verification checklist** mapping each claim to a test in
  `tests/`.
- Where a source paper's formula is not reproduced in the book, the derivation **says so** and
  does not present a reconstruction as the original result.

## How to add a derivation

1. Create `references/derivations/<topic>.md` with sections: setup → assumptions → derivation →
   conclusion → verification checklist → open items.
2. Add a row to the table above.
3. Add the corresponding checks to `tests/test_derivations.py` (or a topical test module).
4. If it changes a claim in `references/theory/*.md`, update that file too and re-tag provenance.
