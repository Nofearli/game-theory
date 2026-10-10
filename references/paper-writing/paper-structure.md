# Paper structure (IEEE Transactions / AAAI style)

Target venues: IEEE TAC, TAES, TRO, TIE, TMECH, TII, TCST; AAAI / IJCAI / NeurIPS.
Each section below: **purpose → must-contain → common reviewer complaints**.

## 1. Introduction

- **Purpose:** motivate, position, state contributions.
- **Must contain:** background → related work (grouped, not a list) → the *gap* → the problem →
  a numbered contribution list (3–4 items) → paper organisation.
- **Reviewer complaints:** contribution list is vague ("we study X"); related work misses the
  closest paper; no clear gap; claims not supported later.

## 2. Problem Formulation

- **Purpose:** define the game precisely so the theory is checkable.
- **Must contain:** scenario figure; motion model (equations); information assumptions; state and
  control variables; capture / goal / termination conditions; payoff; the formal problem.
- **Reviewer complaints:** assumptions hidden; `α`/`a` defined inconsistently; capture condition
  changed silently between sections; discrete simulation not distinguished from continuous model.

## 3. Theoretical Analysis

- **Purpose:** the core contribution — definitions, lemmas, theorems, corollaries, proofs.
- **Must contain:** numbered assumptions; a definition for each new object (barrier, reachable
  set, winning region); theorems with complete proofs or a clearly-stated proof location;
  physical interpretation after each theorem; boundary/degenerate cases.
- **Reviewer complaints:** necessary condition claimed as sufficient; proof skips the
  transversality / boundary case; "optimal" claimed for a heuristic; no proof of existence /
  uniqueness for the optimum; theorem hypotheses not used in the proof (⇒ over-specified).

## 4. Method / Strategy Design

- **Purpose:** turn theory into an implementable algorithm.
- **Must contain:** algorithm box with inputs/outputs; complexity; implementation notes;
  theoretical guarantee (or an explicit statement that there is none).
- **Reviewer complaints:** algorithm not reproducible; complexity unstated; no handling of
  solver failure / degeneracy; feedback law presented as open-loop (or vice-versa).

## 5. Numerical Simulations / Experiments

- **Purpose:** verify the theory and show the method's value.
- **Must contain:** parameter table; baseline descriptions (fair information); metrics;
  theory-vs-simulation agreement; ablation; sensitivity; a failure/limiting case.
- **Reviewer complaints:** single seed; no baseline or an unfair one; parameters tuned per method
  without disclosure; figures that do not isolate the claimed effect; no comparison against the
  analytic optimum where one exists.

## 6. Conclusion

- **Purpose:** close the loop.
- **Must contain:** restated contributions; conditions under which the results hold; limitations;
  concrete future work.
- **Reviewer complaints:** over-claiming generality; no limitations; future work is a wish-list.

## 7. Global checklist before submission

- [ ] Every claim in the abstract maps to a theorem / table / figure.
- [ ] One symbol = one concept throughout; a notation table if conventions switch.
- [ ] All figures legible in greyscale; axis aspect ratio correct.
- [ ] Reproducibility: seeds, parameters, code/data availability.
- [ ] No fabricated citation; every reference verified.
- [ ] Optimality claims are either proven or explicitly hedged.

## 8. Reviewer questions to self-answer (pre-empt these)

1. What exactly is new relative to the closest prior work? Cite it and diff.
2. Is the "optimal" strategy a Nash/Isaacs optimum, or a best response? Under what assumptions?
3. Which assumptions are essential and which are for tractability?
4. Does the barrier/reachable-set claim hold in discrete time?
5. Is the baseline given the same information and tuning budget?
6. Do the figures isolate the claimed effect, or are they confounded?
7. What happens at the degenerate limits (`α→1`, `r→0`, `τ→0`)?
8. Could a simpler method achieve the same result?

## 9. Contribution-strength test `[ext]`

A result is a *paper-level* contribution only if it passes all three:

- **Non-trivial:** not a restatement of an assumption or a renamed standard result.
- **General:** holds beyond a single parameter set (state the generality).
- **Checkable:** a reader can verify it from the stated assumptions.
