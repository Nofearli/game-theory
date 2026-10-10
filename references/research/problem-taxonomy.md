# Problem taxonomy — how to classify a game

Use this **first** on any request. The classification determines which theory file and which
method apply.

## 1. The seven classification axes

| Axis | Options | Why it matters |
|---|---|---|
| **Players** | 1v1, 2v1, mv1, mvn, three-body (TAD), N-team | determines whether assignment/coupling is needed |
| **Dynamics** | simple motion / inertia / nonholonomic / bounded turn rate | geometry is exact only for simple motion |
| **Information** | perfect / observation error / partial (finite sensing) / adversarial | selects Ch. 1 vs 2 vs 4 |
| **Target set** | half-plane (line `x=x_d`), segment (gate), convex region, moving target | changes the geometry and the barrier shape |
| **Termination** | point capture / capture radius / time-out / dwell | `r>0` ⇒ Cartesian ovals; dwell ⇒ Ch. 6 |
| **Task structure** | single-stage / two-stage / three-stage (recon–return) | Ch. 6 vs Ch. 1–5 |
| **Objective type** | Game of Kind (who wins) / Game of Degree (the value) | different mathematics |

## 2. Quick decision table

| If the request is about… | Load |
|---|---|
| "can the defender stop the attacker, and where" | `theory/01`, `theory/03` |
| "multiple defenders, who chases whom" | `theory/01` (§5) + `coding` + `examples/multi-agent` |
| "observation noise / robustness / filtering" | `theory/02` |
| "barrier / deployment feasibility / capture radius" | `theory/03` |
| "defender can't see the attacker / sensing radius / deployment point" | `theory/04` |
| "target + attacker + defender, equal speed" | `theory/05` |
| "reconnaissance / capture-the-flag / dwell time" | `theory/06` |
| "learn a strategy / RL / imitation" | `theory/07` + `reinforcement-learning/` |
| "derive / prove / check a theorem" | the matching `theory/*` + `common-pitfalls` |
| "design experiments / figures" | `simulation/` |
| "write / review a paper" | `paper-writing/` |

## 3. Game of Kind vs Game of Degree — the first fork

- **Kind**: a *set-valued* question. "Which initial states are winning?" Answer = a barrier or a
  winning region. Tool: barrier construction, reachability, HJ PDE.
- **Degree**: an *optimisation* question, asked only after the winner is fixed. "Given the winner,
  what is the value?" Tool: PMP / HJI / dynamic programming.
- **Rule:** always resolve Kind before Degree. Applying a Degree strategy outside its winning set
  is invalid.

## 4. Reduction ladder (how to grow a research idea) `[ext]`

The book's own progression is the canonical "generalisation ladder" — use it to generate new
research directions by taking one step up:

1v1 → 2v1 → mv1 → mvn;
perfect info → observation error → partial info;
`r = 0` → `r > 0`;
single-stage → two-stage → three-stage;
deterministic → uncertain → adversarial;
analytic game → learning-based game.

Pick a rung, ask what breaks, and that is your research question.

## 5. Output template for a classification

```
Players:         ...
Dynamics:        ...
Information:     ...
Target / goal:   ...
Termination:     ...
Task structure:  ...
Objective type:  Kind / Degree
Applicable theory file: references/theory/0X-*.md
Key formula(s):  ...
Candidate methods: analytic / numeric / learning
```
