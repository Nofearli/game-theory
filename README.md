# game-theory — a research skill for differential / pursuit-evasion games

A knowledge base **and** a working research assistant for differential games (pursuit–evasion,
reach–avoid, defence, TAD, reconnaissance–return) and their learning-based extensions.

Built on the tutorial book **《博弈书籍.md》** (six chapters) and extended with vetted guidance
for research, coding, simulation and IEEE/AAAI paper writing.

- **Entry point:** `SKILL.md` (capabilities, triggers, 7 modes, workflow, loading rules).
- **Knowledge:** `references/` (theory, research, writing, simulation, coding, RL, notation,
  pitfalls, source index).
- **Working code:** `scripts/gtlib/` (reusable library) + `examples/` (7 runnable examples).
- **Verification:** `tests/` (37 checks of mathematical invariants).

## Install

The repo **is** the skill folder, so cloning it into a skills directory is the whole install.

**Clone (recommended)**

```bash
# macOS / Linux
git clone https://github.com/<your-user>/game-theory.git ~/.workbuddy-ai/skills/game-theory

# Windows PowerShell
git clone https://github.com/<your-user>/game-theory.git "$env:USERPROFILE\.workbuddy-ai\skills\game-theory"
```

**Or use the bundled script** (from a checkout):

```bash
bash ./install.sh              # macOS / Linux
powershell -ExecutionPolicy Bypass -File .\install.ps1   # Windows
```

**Update later**

```bash
cd ~/.workbuddy-ai/skills/game-theory && git pull
```

See `INSTALL.md` for other agents' skill directories, custom destinations and uninstall steps.

The skill is **fully self-contained**: the source book is bundled at `assets/book/博弈书籍.md`
(with its 60 figures in `assets/book/fig/`), so it does not depend on any other folder.

## Requirements

Python 3.9+ with `numpy`, `scipy`, `matplotlib`. The shipped examples use **only** these three
(plus the standard library). `gymnasium` / `torch` are optional and only needed if you want to
train a real RL policy — the shipped RL example deliberately avoids them.

```bash
python examples/pursuit-evasion/apollonius_1v1.py
python tests/run_tests.py
```

## Directory structure

```
game-theory/
├── SKILL.md                       capabilities / triggers / modes / workflow
├── README.md                      this file
├── INSTALL.md                     install / update / uninstall for any agent
├── install.sh, install.ps1        one-line installer scripts
├── .github/workflows/test.yml     CI: runs the invariant tests on push
├── references/
│   ├── theory/                    the six directions + the RL extension
│   │   ├── 01-pursuit-evasion.md
│   │   ├── 02-parameter-uncertainty.md
│   │   ├── 03-barrier.md
│   │   ├── 04-partial-information.md
│   │   ├── 05-tad.md
│   │   ├── 06-reconnaissance-return.md
│   │   └── 07-rl-and-learning-games.md      [extension]
│   ├── research/                  problem-taxonomy.md, research-workflow.md
│   ├── derivations/               barrier-1v1-closed-form.md,
│   │                              cartesian-oval-parameterisation.md,
│   │                              three-stage-pmp.md, README.md
│   ├── paper-writing/             paper-structure.md, english-phrases.md
│   ├── simulation/                experiment-design.md, plotting-standards.md
│   ├── coding/                    coding-conventions.md
│   ├── reinforcement-learning/    rl-game-fusion.md
│   ├── background.md              domain background & orientation
│   ├── notation-and-assumptions.md  symbols, coordinate frames, speed ratios
│   ├── common-pitfalls.md          the mistakes that break results
│   └── source-index.md             theory ⇄ 《博弈书籍.md》 section map
├── examples/
│   ├── pursuit-evasion/           apollonius_1v1.py
│   ├── barrier/                   barrier_1v1.py
│   ├── partial-observation/       partial_info_1v1.py
│   ├── multi-agent/               assignment_mvn.py
│   ├── tad/                       tad_optimal.py
│   ├── reconnaissance-return/     recon_2stage.py
│   └── learning-games/            pursuit_evasion_env.py
├── scripts/gtlib/                 geometry, uncertainty, filters, barrier,
│                                  assignment, partial_info, tad, recon,
│                                  plotting, simulate
├── tests/                         run_tests.py + 5 test modules (37 checks)
└── assets/book/                   博弈书籍.md + fig/ (60 figures) — bundled source
```

## Verified examples

Each example prints a summary, saves an IEEE-style SVG + PNG under its own `out/`, and returns
a result object (so tests can call it).

| Example | Demonstrates | Verified output |
|---|---|---|
| `apollonius_1v1.py` | 1v1 judgement, safe set, breakthrough point | `x* = (-0.6204, -0.9819)` — matches the book exactly |
| `barrier_1v1.py` | 3-branch analytic barrier + Cartesian-oval parameterisation | barrier criticality `~1e-10`; `r→0` degeneracy `~1e-16` |
| `partial_info_1v1.py` | deployment point vs sensing radius; detect → capture | `R_α = 2.0`; capture at `t = 6.5 s` |
| `assignment_mvn.py` | feasibility matrix + 0-1 ILP assignment | ILP optimum; infeasible combo excluded |
| `tad_optimal.py` | escape oval, `z*`, Kind prediction, closed loop | A wins; closed loop confirms capture |
| `recon_2stage.py` | numerical 2-stage barrier + dwell time | Case A ∈ `W_P`, Case B ∈ `W_E` (matches the book) |
| `pursuit_evasion_env.py` | Gym-style env + classical expert + BC baseline | expert win-rate 1.00 vs naive BC 0.50 |

## Tests

```bash
python tests/run_tests.py        # -> "37 passed, 0 failed"
```

They assert on invariants, not on the functions' own outputs: the book's breakthrough value,
barrier joint continuity, `r→0` degeneracy, `ξ→0` at contact, KF error reduction, ILP vs
brute-force optimality, shared-defender exclusion, the virtual-evader transform, the
`W_P`/`W_E` classification of the book's Case A/B, and `τ_max` monotonicity — plus the
**derivation checks** in `tests/test_derivations.py` (reflection lemma, collinearity of the
optimal boundary point, 2v1 joining-arc radius equality, similar-points collinearity in `r`,
three-stage → one-leg reduction).

## Provenance conventions (important)

Every claim in an answer is tagged:

- `[book]` — from 《博弈书籍.md》 (give the section, e.g. `[book 3.3]`).
- `[ext]` — added by this skill (RL, CBF, safe RL, coding / simulation / writing guides).
- `[new]` — derived in the current session; state the assumptions.

Two modules are **independent reconstructions**, not transcriptions of the source papers, and
say so in their docstrings: `scripts/gtlib/tad.py` and `scripts/gtlib/recon.py`. Use the paper's
closed forms for publication numbers; use these for experimentation.

## How to extend

**Add a new theory direction** (e.g. "pursuit–evasion with obstacles"):
1. create `references/theory/08-<topic>.md` with the standard sections (problem class, model &
   assumptions, core formulas, derivation, conclusions, boundaries, pitfalls, code, extensions);
2. add a row to the table in `SKILL.md` §2 and to `references/source-index.md`;
3. if it has a name, add the symbol to `references/notation-and-assumptions.md`.

**Add a new paper**:
1. add a section to the relevant `references/theory/*.md` (mark `[ext]` until verified);
2. add its theorem names to `references/source-index.md` §3;
3. if you reproduce it, add `examples/<category>/<paper>.py` and a test in `tests/`.

**Add a new algorithm / utility**: put reusable math in `scripts/gtlib/<module>.py` (pure
NumPy/SciPy, no plotting imports), and a runnable demo in `examples/`.

**Keep it honest**: never fabricate a citation, a number or an optimality guarantee; label
unproven statements as conjecture / numerical observation; never present a heuristic as a
differential-game optimum or a simulation as a proof.

## License

MIT — see [`LICENSE`](LICENSE). Anyone may download, use, modify and redistribute this skill.

The bundled tutorial book 《博弈书籍.md》 (`assets/book/`) is the author's own writing; the
research papers it summarises remain the property of their respective authors.

## Acceptance tasks

The skill is designed to handle: (1) 1v1 interception judgement; (2) non-zero capture-radius
boundary; (3) many-to-many task assignment; (4) partial-information feedback interception;
(5) three-stage reconnaissance–return game; (6) an end-to-end idea → model → proof-sketch →
code → experiment → paper-outline case. `examples/` covers (1)–(5); `references/research/`
covers (6).
