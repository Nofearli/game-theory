"""Example: pursuit-evasion RL environment + classical expert + BC sketch
[extension: book Ch. 7 / references/theory/07-rl-and-learning-games.md]

Run:  python pursuit_evasion_env.py
Outputs: out/learning_games_1.{svg,png}, out/expert_data.npz

Uses ONLY NumPy (no gymnasium/torch needed) so it runs anywhere.  Provides:
  * `PursuitEvasionEnv` - a Gymnasium-style environment (reset/step)
  * `expert_action`     - the classical optimal pursuer action (book Ch. 1)
  * `collect_expert`    - demonstration dataset
  * `fit_bc`            - a ridge-regression behaviour-cloning baseline
  * `evaluate`          - win-rate evaluation harness
"""
from __future__ import annotations

import pathlib
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)  # SLSQP bound clipping

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
from gtlib import geometry as G          # noqa: E402
from gtlib import plotting as P          # noqa: E402

V_P, V_E = 0.5, 0.3
R_CAP = 0.4
X_D = 3.0
LIM = 5.0
DT = 0.1
T_MAX = 60.0


class PursuitEvasionEnv:
    """1v1 pursuit-evasion, simple motion, capture radius, defence line x = x_d.

    Observation (5): [p_p - p_e (2), p_e (2), normalised time (1)]
    Action (2): pursuer velocity command (clipped to v_p); the evader runs straight.
    """

    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)
        self.a = V_P / V_E
        self.reset()

    def reset(self, p_p=None, p_e=None):
        self.p_p = np.asarray(p_p if p_p is not None else (3.0, 2.0), float)
        self.p_e = np.asarray(p_e if p_e is not None else (-3.0, 0.0), float)
        self.t = 0.0
        return self._obs()

    def _obs(self):
        return np.concatenate([self.p_p - self.p_e, self.p_e, [self.t / T_MAX]])

    def expert_action(self):
        """Classical optimal pursuer action: full speed toward the breakthrough point."""
        bt = G.solve_breakthrough([(self.p_p, self.a)], self.p_e, R_CAP,
                                  bounds=(-LIM, LIM, -LIM, LIM))
        d = bt["x"] - self.p_p
        n = float(np.linalg.norm(d))
        return V_P * d / n if n > 1e-9 else np.zeros(2)

    def step(self, action):
        u = np.asarray(action, float)
        n = float(np.linalg.norm(u))
        if n > V_P:
            u = u * (V_P / n)
        self.p_p = self.p_p + u * DT
        self.p_e = self.p_e + np.array([V_E, 0.0]) * DT      # evader runs straight
        self.t += DT
        dist = float(np.linalg.norm(self.p_p - self.p_e))
        terminated = False
        reward = -0.01
        if dist <= R_CAP:
            reward, terminated = +10.0, True
        elif self.p_e[0] >= X_D:
            reward, terminated = -10.0, True
        else:
            reward += -0.05 * dist                            # dense shaping
        truncated = self.t >= T_MAX
        return self._obs(), reward, terminated, truncated, {"dist": dist}


def collect_expert(n_episodes=60, seed=0):
    env = PursuitEvasionEnv(seed=seed)
    rng = np.random.default_rng(seed)
    X, Y = [], []
    for _ in range(n_episodes):
        env.reset(p_p=(rng.uniform(2, 4), rng.uniform(-3, 3)),
                  p_e=(rng.uniform(-4, -1), rng.uniform(-3, 3)))
        done = False
        while not done:
            obs = env._obs()
            a = env.expert_action()
            X.append(obs)
            Y.append(a)
            _, _, term, trunc, _ = env.step(a)
            done = term or trunc
    return np.array(X), np.array(Y)


def fit_bc(X, Y, ridge=1e-3):
    """Ridge-regression behaviour cloning: action ~ W [obs; 1]."""
    Xa = np.hstack([X, np.ones((len(X), 1))])
    W = np.linalg.solve(Xa.T @ Xa + ridge * np.eye(Xa.shape[1]), Xa.T @ Y)
    return W


def bc_action(W, obs):
    return np.hstack([obs, [1.0]]) @ W


def evaluate(policy, n_episodes=50, seed=1):
    env = PursuitEvasionEnv(seed=seed)
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(n_episodes):
        env.reset(p_p=(rng.uniform(2, 4), rng.uniform(-3, 3)),
                  p_e=(rng.uniform(-4, -1), rng.uniform(-3, 3)))
        done = False
        while not done:
            a = policy(env)
            _, _, term, trunc, info = env.step(a)
            done = term or trunc
        if info["dist"] <= R_CAP:
            wins += 1
    return wins / n_episodes


def run(make_figure=True):
    out_dir = pathlib.Path(__file__).resolve().parent / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("collecting expert demonstrations ...")
    X, Y = collect_expert(n_episodes=60, seed=0)
    print(f"expert dataset: {X.shape[0]} transitions")
    W = fit_bc(X, Y)
    np.savez(out_dir / "expert_data.npz", X=X, Y=Y, W=W)

    expert_wr = evaluate(lambda env: env.expert_action())
    bc_wr = evaluate(lambda env: bc_action(W, env._obs()))
    straight_wr = evaluate(lambda env: V_P * np.array([1.0, 0.0]))
    print(f"win rate (50 episodes): expert={expert_wr:.2f}  BC={bc_wr:.2f}  "
          f"straight={straight_wr:.2f}")

    if make_figure:
        P.ieee_style()
        fig, ax = P.new_axes(89, 65)
        names = ["expert\n(classical)", "BC\n(ridge)", "straight"]
        vals = [expert_wr, bc_wr, straight_wr]
        ax.bar(names, vals, color=[P.C_ACCENT, P.C_DEFENDER, P.C_NEUTRAL], alpha=0.8)
        ax.set_ylabel("pursuer win rate")
        ax.set_ylim(0, 1.05)
        ax.set_title("Classical expert vs behaviour cloning")
        for i, v in enumerate(vals):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=6)
        P.save_figs(fig, out_dir / "learning_games_1")
        print("figures saved to", out_dir)
    return {"expert": expert_wr, "bc": bc_wr, "straight": straight_wr}


if __name__ == "__main__":
    run()
