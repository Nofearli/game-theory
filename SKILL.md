---
name: game-theory
description: >
  Professional research assistant for differential / pursuit-evasion / reach-avoid / defense
  games. Use when the user wants to (a) formulate or analyse a pursuit-evasion, barrier,
  reach-avoid, TAD (target-attacker-defender) or reconnaissance-return differential game;
  (b) derive or verify a theorem / proof / optimality condition (PMP, HJI, Isaacs, KKT,
  Lyapunov, CBF); (c) compute Apollonius circles, Cartesian ovals, capture sets, barriers,
  reachable sets or max dwell time; (d) write runnable Python (NumPy/SciPy/Matplotlib) for
  interception judgement, multi-pursuer assignment (ILP/matching), Kalman filtering, or
  closed-loop feedback strategies; (e) design simulation experiments and IEEE-style figures;
  (f) draft or review an IEEE Transactions / AAAI paper section; (g) extend classical games
  with reinforcement learning, imitation learning, MARL, partial observation or safe RL.
  Triggers: 追逃博弈, 攻防博弈, 微分博弈, 界栅, 阿波罗尼奥斯圆, 笛卡尔卵形线, 可达域,
  拦截判定, 任务分配, 极大值原理, HJI, 抓捕半径, 局部感知, 侦察博弈, TAD, reach-avoid,
  barrier, pursuit-evasion, differential game, Apollonius, Pontryagin, Isaacs, dwell time.
description_zh: "微分/追逃/攻防博弈科研助手：理论推导、界栅与可达域计算、可运行 Python、仿真设计与 IEEE 论文写作"
description_en: "Research assistant for differential / pursuit-evasion / defense games: theory, barriers, runnable Python, simulation, IEEE writing"
agent_created: true
---

# Game-Theory Research Skill

A knowledge base + research assistant for **differential games** (pursuit–evasion, reach–avoid,
defense) and their learning-based extensions. It is built on the tutorial book
**《博弈书籍.md》** (six chapters, **bundled** at `assets/book/博弈书籍.md` together with its 60
figures) and extended with vetted methods for research, coding, simulation and paper writing.
The skill is fully self-contained — it never needs another folder.

This SKILL.md defines **capabilities, trigger conditions, the operating workflow and how to
load references**. It deliberately does *not* contain the knowledge itself — load only the
reference files relevant to the current request (progressive disclosure).

---

## 1. When to use

Use this skill whenever a request involves any of:

- **Modelling** a pursuit–evasion / reach–avoid / defense / TAD / reconnaissance–return game.
- **Deriving or checking** a theorem, proof, optimality condition (PMP, HJI/HJB, Isaacs, KKT,
  Lyapunov, CBF), or a barrier / reachable-set characterisation.
- **Computing** Apollonius circles, Cartesian ovals, capture/interception judgements, analytic
  or parametric barriers, escape/reachable sets, max dwell time, optimal deployment points.
- **Coding** runnable Python: interception judgement (SLSQP), 1v1/2v1/mv1/mvn assignment
  (ILP / weighted matching), Kalman filtering, Monte-Carlo robustness, closed-loop feedback.
- **Simulating** and designing experiments (theory-validation / comparison / ablation /
  sensitivity / robustness) and producing IEEE-style figures.
- **Writing / reviewing** an IEEE TAC/TAES/TRO/TIE/TMECH/TII or AAAI/IJCAI/NeurIPS paper.
- **Extending** classical games with RL / imitation learning / MARL / partial observation /
  safe RL / CBF-constrained learning.

Do **not** use it for unrelated optimisation or generic RL questions with no game structure.

---

## 2. Core knowledge base (six classical directions + extensions)

| # | Direction | Reference | Source (book chapter) |
|---|---|---|---|
| 1 | Traditional pursuit–evasion & defense (Apollonius, 1v1→mvn, assignment) | `references/theory/01-pursuit-evasion.md` | Ch. 1 |
| 2 | Parameter-uncertainty games (observation error, robust judgement, KF) | `references/theory/02-parameter-uncertainty.md` | Ch. 2 |
| 3 | Barriers & strategies (1v1/2v1 analytic barrier, capture radius, unexpected strategy) | `references/theory/03-barrier.md` | Ch. 3 |
| 4 | Partial-information games (finite sensing, optimal deployment, 3-D target) | `references/theory/04-partial-information.md` | Ch. 4 |
| 5 | TAD three-body game (Game of Kind / Degree, PMP, HJI) | `references/theory/05-tad.md` | Ch. 5 |
| 6 | Reconnaissance–return game (2-stage / 3-stage, barrier, reachable set, dwell time) | `references/theory/06-reconnaissance-return.md` | Ch. 6 |
| 7 | **Extension** — RL / IL / MARL / safe RL / CBF fusion | `references/theory/07-rl-and-learning-games.md` | *new* |

Cross-cutting files (load as needed):

- `references/background.md` — **domain background & orientation**: what differential /
  pursuit–evasion games are, why they matter, the three core questions, how the six directions
  form a progression, and a vocabulary quick-reference. Load this first when context is thin.
- `references/notation-and-assumptions.md` — symbol table, **coordinate conventions**,
  speed-ratio definitions, capture conditions (mandatory before any derivation).
- `references/common-pitfalls.md` — the mistakes that most often break a proof or a result.
- `references/source-index.md` — precise mapping theory ⇄ 《博弈书籍.md》 section.
- `references/derivations/` — rigorous derivations (barrier closed form, Cartesian oval,
  three-stage PMP / dwell time) with per-claim verification checklists.

---

## 3. The seven operating modes

Select the mode(s) from the request; modes compose (e.g. A → C → D).

**Mode A — Theory research.** Scenario & scientific question → existing methods → their
limitations → candidate innovation → model → derivation → implementation → simulation →
paper contribution. Output a *testable proposition*, not a vague algorithm suggestion.
Classify the contribution as strict theory / algorithm / experimental / engineering.

**Mode B — Theory proof.** State assumptions → analyse mathematical properties → build
lemma/theorem → complete rigorous proof → check boundary & degenerate cases. Label anything
unproven as *conjecture / numerical observation / needs extra assumption*.

**Mode C — Code implementation.** Pick model → numerical method → runnable program → tests →
verification. Follow `references/coding/coding-conventions.md`.

**Mode D — Simulation research.** State the claim → experiment matrix → baselines → metrics →
figures → implement. Follow `references/simulation/experiment-design.md`.

**Mode E — Paper writing.** Build the argument skeleton first, then contributions, theory,
method, experiments. Follow `references/paper-writing/`.

**Mode F — Paper review.** Audit modelling soundness, theorem correctness, novelty,
optimality claims, experimental sufficiency, language.

**Mode G — Reproduction.** Reproduce a paper's theory/algorithm/figures from its stated
assumptions; **strictly separate original-paper results from your recomputation**.

---

## 4. Workflow

1. **Classify** the game: number of players, motion model, information structure, target set,
   termination. Decide Game of Kind vs Game of Degree. (→ `references/research/problem-taxonomy.md`)
2. **Load notation** — `references/notation-and-assumptions.md`. Never reuse a speed-ratio or
   coordinate convention across chapters without checking its definition.
3. **Load the matching theory file(s)** from the table in §2, plus `common-pitfalls.md`. When the
   task is a proof, a formula check or a "is this derivation right?" question, also load the
   matching file in `references/derivations/` (barrier closed form, Cartesian-oval
   parameterisation, three-stage PMP / dwell time).
4. **Do the work** in the selected mode(s), pulling code from `examples/` and utilities from
   `scripts/gtlib/` where relevant.
5. **Verify** — run `tests/` or the example; state explicitly what was run and what passed.
6. **Report** with provenance: mark every claim as `[book]` (from 《博弈书籍.md》),
   `[extension]` (newly added, with its basis), or `[new]` (derived here). Never present a
   heuristic as a differential-game optimum, and never present a simulation as a proof.

---

## 5. Directory map (progressive loading)

```
game-theory/
├── SKILL.md                      ← this file
├── README.md                     ← install / structure / how to extend
├── references/
│   ├── theory/                   ← 01..07, the six directions + RL extension
│   ├── derivations/              ← rigorous derivations (barrier, oval, three-stage PMP)
│   ├── research/                 ← problem taxonomy, research workflow, innovation patterns
│   ├── paper-writing/            ← section structure, reviewer questions, English phrasing
│   ├── simulation/               ← experiment design, IEEE figure standards
│   ├── coding/                   ← code conventions & module layout
│   ├── reinforcement-learning/   ← RL-game fusion guide
│   ├── background.md             ← domain background & orientation (load first if unsure)
│   ├── notation-and-assumptions.md
│   ├── common-pitfalls.md
│   └── source-index.md
├── examples/                     ← runnable, tested examples (7 categories)
├── scripts/gtlib/                ← reusable geometry / barrier / uncertainty / assignment / plot lib
├── tests/                        ← checks of mathematical invariants (37)
└── assets/book/                  ← the bundled source book + its 60 figures
```

**Loading rule:** read `SKILL.md` always; then read *only* the reference file(s) and example(s)
that the task needs. Do not bulk-load the whole `references/` tree.

---

## 6. Code & quality rules (summary)

- Python + NumPy/SciPy/Matplotlib; PyTorch/Gymnasium/NetworkX only when needed.
- Model and code must match; parameters centralised; modules split into
  dynamics / strategy / optimiser / termination / plotting.
- Every example runs standalone, fixes its RNG seed, saves outputs to a directory, and has a
  test. See `references/coding/coding-conventions.md`.
- Default figure style = IEEE-friendly (defender blue, attacker red, helper green;
  correct axis aspect; vector export). See `references/simulation/plotting-standards.md`.
- Never fabricate citations, numerical results or optimality guarantees.

## 7. Acceptance tasks (self-check)

The skill is expected to handle at least: (1) 1v1 interception judgement; (2) non-zero
capture-radius boundary; (3) many-to-many task assignment; (4) partial-information feedback
interception; (5) three-stage reconnaissance–return game; (6) an end-to-end
idea → model → proof-sketch → code → experiment → paper-outline case.
`tests/` and `examples/` cover (1)–(5); `references/research/` covers (6).
