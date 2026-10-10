# Background — what this domain is and how the six directions fit together

Read this first for context. It is the 5-minute orientation that the theory files assume.

## 1. The problem in one sentence

An **attacker (evader)** tries to reach a goal (break a defence line, cross a "gate", complete a
reconnaissance task); a **defender (pursuer)** tries to stop it. Both move under simple motion
(speed fixed, heading free). This is a **differential game** — a game played in continuous time
with continuous state.

## 2. Why it matters

The same mathematical skeleton covers: UAV interception and airspace defence, missile/vehicle
pursuit, perimeter guarding, adversarial drone defence, robot capture-the-flag, and — in
learning form — multi-agent pursuit benchmarks. The theory answers three practical questions:
**can we stop it? where should we stand? and how should we move?**

## 3. The core object: the Apollonius circle

For any point `x`, the attacker reaches it first iff

```
||x - p_defender||  >=  a * ||x - p_attacker||        (a = v_defender / v_attacker > 1)
```

The boundary is the **Apollonius circle** (a **Cartesian oval** when the capture radius `r > 0`).
Everything in the book is built on this one inequality. Everything else is a question about what
you do with it.

## 4. The three questions → the three families of tools

| Question | Independent variable | Tool | Chapter |
|---|---|---|---|
| "Right now, who reaches `x` first?" | a point `x` in space | Apollonius / oval **judgement** | 1, 2 |
| "Given a deployment, how far out can attackers still break through?" | the **attacker's initial position** | **barrier** | 3, 6 |
| "The defender can't see the attacker — where should it stand?" | the **deployment point** | ambiguity region + **optimal deployment** | 4 |

Do not conflate these: **reachable set**, **barrier**, **winning region** and **safety region**
are four different objects (`notation-and-assumptions.md` §4).

## 5. The two classic sub-questions

- **Game of Kind** — *who wins?* Set-valued: a barrier or a winning region answers it.
- **Game of Degree** — *given the winner, what is the value?* An optimisation, solved by PMP /
  HJI / dynamic programming. Always resolve Kind before Degree.

## 6. How the six directions form a progression

The book is a ladder: each chapter relaxes exactly one assumption of the previous one.

```
1. Traditional (perfect information, point capture, single stage)
      |
      +-- relax information accuracy   -> 2. Parameter uncertainty (observation error, Kalman)
      +-- change the question          -> 3. Barrier (deployment feasibility; capture radius)
      +-- relax information structure  -> 4. Partial information (finite sensing; deployment)
      +-- add a third player           -> 5. TAD (target–attacker–defender; equal speed)
      +-- add task structure           -> 6. Reconnaissance–return (round trip; dwell time)
                                             |
                                             +-- replace analysis with learning ->
                                                 7. RL / IL / MARL / safe RL  [extension]
```

Every relaxation is also a **research direction**: "what breaks if I remove this assumption?"

## 7. Vocabulary quick-reference

| Term | Meaning |
|---|---|
| simple motion | `ẋ = u`, `‖u‖ ≤ v` — fixed speed, free heading |
| speed ratio | `a` or `α = v_defender / v_attacker > 1` (Ch. 6 uses `α` with two different definitions) |
| capture radius `r` | capture when `‖p_d − p_a‖ ≤ r`; `r > 0` turns circles into Cartesian ovals |
| reachable set | spatial points the attacker can reach first |
| **barrier** `B` | attacker *initial* positions from which breakthrough is still possible, for a fixed deployment |
| winning region | `W_P` (defender) / `W_E` (attacker), separated by the barrier |
| Game of Kind / Degree | who wins / the value |
| PMP, HJI, Isaacs | optimal-control machinery; Isaacs condition ⇒ saddle point |
| dwell time `τ` | time spent at the reconnaissance boundary (Ch. 6 only) |
| LRR / SRR | long-range / successful-return reachable set (Ch. 6) |

## 8. What the skill adds beyond the book

- **Extension (Ch. 7):** reinforcement learning, imitation learning, MARL, partial observation,
  safe RL and CBF — with the classical strategies used as experts, rewards and safety labels.
- **Research layer:** problem taxonomy, an innovation ladder, a paper-writing guide.
- **Working code:** `scripts/gtlib/` + 7 runnable examples + 37 invariant tests.
- **Derivations:** rigorous derivations of the barrier and oval, and the reconnaissance
  reflection / dwell-time reduction.

## 9. Where to go next

- New to the topic → this file, then `theory/01`, then `theory/03`.
- Want to build something → `theory/01` + `examples/pursuit-evasion/`.
- Writing a paper → `research/research-workflow.md` + `paper-writing/`.
- Extending with learning → `theory/07` + `reinforcement-learning/`.
