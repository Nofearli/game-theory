# 07 · Reinforcement learning & learning-based games  `[ext]`

> **Provenance: this entire file is an extension.** Nothing here is from 《博弈书籍.md》.
> It exists to let the skill support classical-game + machine-learning research. Claims about
> optimality carry *no* differential-game guarantee unless proven separately.

## 1. Why learning at all?

Classical chapters give analytic strategies **only for simple motion with clean geometry**. When
any of the following holds, an analytic optimum may not exist or be tractable:

- high-dimensional state / many players, coupled constraints;
- non-simple dynamics (inertia, nonholonomic, actuator limits);
- partial observation with complex belief dynamics;
- hybrid/discrete decisions (assignment, mode switching) coupled with continuous control;
- an adversary whose model is unknown or non-stationary.

In these regimes, learning is a *practical* alternative — but you must state its guarantees and
limits explicitly (see §7).

## 2. Problem formulations (choose deliberately)

| Formulation | When | Notes |
|---|---|---|
| Single-agent RL vs fixed opponent | opponent strategy known/frozen | MDP; cleanest guarantees |
| Self-play / best-response | both sides learn | non-stationary; use PSRO / fictitious play |
| Markov game (Nash) | symmetric multi-agent | Nash equilibria hard; report convergence to ε-Nash |
| POSG / POMDP | partial observation | belief or recurrent policy; Ch. 4 is the analytic analogue |
| Robust / adversarial RL | worst-case disturbance | min–max; connect to H∞ / robust control |

## 3. Expert strategies from classical games

The classical chapters provide **free expert data**, which is their most under-used asset:

- 1v1 / 2v1 optimal interception laws → expert trajectories + expert actions;
- barrier / oval geometry → feasibility labels and safety labels;
- assignment (ILP) → expert assignment labels;
- TAD `z*` → expert terminal targets.

Use them for:

- **Behaviour cloning (BC):** supervised `π_θ(a|s) ≈ π_expert`. Cheap, but compounding error
  `O(T²ε)`; mitigate with DAgger (query the expert on the learner's states).
- **Warm start:** initialise PPO/SAC from the BC policy, then fine-tune against a stronger
  opponent. Usually the highest-value combination.
- **Reward shaping:** use the geometric margin (`F(x_d)`, barrier sign, `J_1`) as a dense
  potential, not just the terminal ±1.
- **Safety labels:** label "safe / unsafe" states with the Apollonius / barrier test and use them
  as a constraint signal (see §5).

## 4. Algorithms (practical defaults)

- **PPO** — robust default for continuous control, on-policy, easy to stabilise.
- **SAC** — off-policy, sample-efficient, good for expensive simulators.
- **MAPPO / QMIX** — multi-agent cooperative (centralised training, decentralised execution).
- **PSRO / fictitious self-play** — population-based training against non-stationarity.
- Keep the environment deterministic-given-seed and versioned; log seeds and hyper-parameters.

## 5. Safe RL and CBF

Bridge classical geometry and learning:

- **Shielding:** project/reject actions that violate the Apollonius/barrier safety condition.
- **CBF-constrained RL:** learn a policy subject to a control-barrier-function constraint
  `L_f h + L_g h·u + κ(h) ≥ 0`; if a valid `h` is available analytically (e.g. from the barrier),
  this gives a *provable* safety filter around a learned performance policy.
- **Lagrangian / CPO:** treat safety as a constrained MDP; tune the multiplier, report the
  constraint-violation rate.
- **Certificate check:** where a classical optimum exists, compare the learned policy against it
  to *bound* sub-optimality rather than claiming optimality.

## 6. Evaluation methodology (non-negotiable)

1. **Baselines:** classical optimal (where available), pursuit/PN heuristic, random, BC-only,
   and the strongest published learning method. Fair information for all.
2. **Metrics:** win rate, capture time, distance-to-target, constraint violations, control
   effort, sample complexity (env steps to reach a performance bar).
3. **Statistics:** ≥ 5 seeds, report mean ± CI (bootstrap or t-interval); never a single seed.
4. **Generalisation:** held-out initial conditions, unseen speeds/radii, more players than trained.
5. **Ablations:** remove BC warm start, remove reward shaping, remove safety layer — one at a time.
6. **Failure analysis:** characterise where learning loses to the classical optimum and why.

## 7. Honesty rules

- Never call a learned policy "optimal" without a proof or a certified bound; say
  "near-optimal on the tested distribution".
- State the observation space precisely — a policy with privileged (omniscient) observations is
  not comparable to a partial-information classical method.
- Report the simulator's fidelity and any sim-to-real gap.
- Do not present a self-play win rate as evidence of a Nash equilibrium.

## 8. Code

- `examples/learning-games/pursuit_evasion_env.py` — a dependency-light Gymnasium-style
  environment for the 1v1 pursuit–evasion game with the classical optimal expert exposed, plus a
  BC warm-start sketch and an evaluation harness (no deep-RL dependency required to run).

## 9. Suggested research directions `[ext]`

- Barrier-guided safe RL (CBF from the analytic barrier) for multi-pursuer defence.
- Expert-in-the-loop: classical assignment + learned continuous control.
- Partially-observable pursuit–evasion with a learned belief vs Ch. 4's analytic deployment.
- Robust RL against worst-case evader manoeuvres (connect to Ch. 3.4's unexpected strategy).
- Transfer from 1v1 to mvn via curriculum + population self-play.
