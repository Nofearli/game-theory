# RL ⇄ game-theory fusion guide  `[ext]`

Operational companion to `theory/07-rl-and-learning-games.md`.

## 1. Decision: do you even need learning?

Run this check first:

1. Is the game simple motion with clean geometry? → **use the analytic strategy** (Ch. 1–6).
2. Is there a closed form but an awkward constraint (actuator limits, obstacles)? → analytic
   baseline **+ a learned residual/safety layer**.
3. No analytic optimum, high dimension, coupled decisions? → **learning**, with an analytic
   feasibility/expert signal wherever possible.

Never reach for RL before checking (1).

## 2. Where classical games help learning

| Classical asset | Use in learning |
|---|---|
| Optimal 1v1/2v1 interception law | expert demonstrations for BC / DAgger |
| Barrier sign `F(x_d)`, `J_1` | dense reward shaping / potential |
| Apollonius / oval test | safety labels, shielding, CBF design |
| ILP assignment | expert assignment labels, or a hard constraint layer |
| TAD `z*` | expert terminal target |
| Reachable set | curriculum: sample start states near the boundary |

## 3. Recommended recipe (highest value first)

1. **Expert + reward shaping.** Use the geometric margin as a dense reward; terminal ±1 alone is
   too sparse for multi-pursuer.
2. **BC warm start**, then **PPO/SAC fine-tune** against a stronger opponent.
3. **Safety layer** from the barrier (CBF/shield) so exploration cannot leave the safe set.
4. **Population self-play** (PSRO / fictitious play) for non-stationarity.
5. **Evaluate against the analytic optimum** where it exists — report the sub-optimality gap.

## 4. Formulation checklist

- Observation space: is it partial (Ch. 4-like) or privileged? State it; do not compare a
  privileged policy with a partial-information classical method.
- Action space: velocity (matching simple motion) vs acceleration (changes the game).
- Reward: shape + terminal; document every term.
- Episode termination: capture, goal, time-out — mirror the theory's termination set.
- Multi-agent: shared or individual reward; CTDE (MAPPO/QMIX) for cooperation.

## 5. Evaluation harness

- ≥ 5 seeds; mean ± CI; fixed evaluation seed set separate from training.
- Baselines: analytic optimal, PN/pursuit heuristic, random, BC-only, strongest published method.
- Metrics: win rate, capture time, constraint violations, control effort, sample complexity.
- Generalisation: unseen initial conditions, unseen `α`/`r`, more players than trained.
- Ablation: −BC, −shaping, −safety layer, one at a time.
- Failure analysis: where and why learning loses.

## 6. Honesty

- "Near-optimal on the tested distribution" — not "optimal".
- No Nash claim from self-play win rates.
- Report the simulator and any sim-to-real gap.
- If a CBF/shield guarantees safety, say so *because of the shield*, and state the shield's
  assumptions — the learned policy itself may be unsafe.

## 7. Dependency notes

- The shipped example `examples/learning-games/pursuit_evasion_env.py` uses **NumPy only**
  (Gymnasium-style API) so it runs without heavy dependencies.
- For real training, add `gymnasium` + `torch`/`stable-baselines3` in the user's own environment;
  do not assume they are installed.
