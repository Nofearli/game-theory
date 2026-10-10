# Source index — theory ⇄ 《博弈书籍.md》

The reference book is **bundled with this skill** (self-contained, images included):

```
game-theory/assets/book/博弈书籍.md      ← read this one
game-theory/assets/book/fig/             ← its 60 figures
```

An external working copy may also exist elsewhere on your machine — prefer the **bundled**
copy above, so the skill never depends on another folder.

> Line numbers below are from the book as of **2026-10-10** (6,110 lines). They drift if the
> book is regenerated — **always resolve by section number first**, then jump to the line.
> If the bundled path is missing, search the workspace for `博弈书籍.md`.

## 1. Chapter / section → line map

| Section | Title | Line |
|---|---|---|
| 前言 | 导读与学习路线 | 60 |
| 1.0 | 攻防博弈理论总览 | 92 |
| 1.1 | 拦截判定与阿波罗尼奥斯圆 | 250 |
| 1.2 | 参数与不确定性分析 | 336 |
| 1.3 | 一对一闭环博弈与三维攻防 | 424 |
| 1.4 | 多对一：协同拦截与组合选取 | 558 |
| 1.5 | 多对多：任务分配与三对三综合仿真 | 697 |
| 1.6 | 实验数据后处理（rosbag） | 836 |
| 2.0 | 第二章节理论总览：参数不确定性博弈 | 922 |
| 2.1 | 参数不确定性博弈：一对一 / 二对一 | 1077 |
| 2.2 | 参数不确定性博弈：多对多 | 1155 |
| 2.3 | 参数不确定性博弈：卡尔曼滤波 | 1240 |
| 2.4 | GUI 软件 | 1365 |
| 3.0 | 第三章理论总览：界栅（barrier） | 1475 |
| 3.1 | 一对一界栅 | 1643 |
| 3.2 | 二对一界栅（无重叠） | 1819 |
| 3.3 | 抓捕半径下的界栅（参数化） | 1901 |
| 3.4 | 有抓捕半径下的非预期策略 | 2079 |
| 3.5 | 一个阿波罗尼奥斯圆就够了 | 2220 |
| 4.0 | 第四章节理论总览：局部感知博弈 | 2424 |
| 4.1 | 局部感知理论仿真：部署、探测与捕获 | 2557 |
| 4.2 | 局部感知实验数据与视频 | 2757 |
| 4.3 | 异构多人局部感知博弈 | 2854 |
| 4.4 | 局部感知博弈：三维凸目标区域 | 2994 |
| 5.1 | TAD 最优策略（Game of Degree） | 3209 |
| 5.2 | TAD 界栅（Game of Kind） | 3491 |
| 6.0 | 第六章节理论总览：侦察（夺旗）博弈 | 3612 |
| 6.1 | 侦察博弈：二阶段界栅与策略 | 3826 |
| 6.2 | 侦察博弈：多体任务分配 | 4254 |
| 6.3 | 侦察博弈：极大值原理与三阶段转化 | 4531 |
| 6.4 | 侦察博弈：三阶段界栅与可达域 | 5125 |
| 6.5 | 侦察博弈：最优策略与最大可驻留时间 | 5619 |

## 2. Topic → section

| Topic | Section |
|---|---|
| Simple-motion model, defence line `x_d` | 1.0 §1 |
| Time-to-go, Apollonius inequality | 1.0 §2, 1.1 |
| Interception judgement as an NLP (SLSQP) | 1.0 §3, 1.1 |
| Optimal strategy = full speed to `x*`; closed loop | 1.0 §4, 1.3 |
| 3-D layered extension | 1.3 下篇 |
| 2v1 (intersection of safe sets) | 1.4 上篇 |
| mv1 combination selection (minimum-headcount) | 1.4 下篇 |
| mvn task assignment (0-1 ILP, `scipy.optimize.milp`) | 1.0 §6, 1.5 上篇 |
| 3v3 integrated simulation | 1.5 下篇 |
| rosbag experiment post-processing | 1.6 |
| `kesai_ij` distance-dependent uncertainty model | 2.0 §2, 2.1 |
| Effective capture radius `r_eff = r − a ξ` | 2.0 §3, 2.1 |
| Monte-Carlo robust judgement | 2.0 §4, 2.1 |
| Robust assignment (pairwise outcomes under uncertainty) | 2.0 §5, 2.2 |
| Kalman filter (position-state & constant-velocity) | 2.0 §6, 2.3 |
| Closed-loop capture-rate statistics | 2.0 §7, 2.3 |
| Barrier vs reachable set | 3.0 §1 |
| 1v1 analytic barrier (arc–hyperbola–arc) | 3.0 §2, 3.1 |
| 2v1 barrier (bisector split + joining arc) | 3.0 §3, 3.2 |
| Capture radius ⇒ Cartesian oval, parameterisation | 3.0 §4, 3.3 |
| Unexpected (heading-dependent) strategy | 3.0 §5, 3.4 |
| One-Apollonius-circle (Lyapunov) strategy | 3.0 §6, 3.5 |
| Partial-information model, ambiguity region | 4.0 §1, §5 |
| Capture law `Γ_P^δ` | 4.0 §3, 4.1 |
| Optimal deployment point (Theorem 2) | 4.0 §6, 4.1 |
| Heterogeneous 2v2 = two 1v1 | 4.3 |
| 3-D convex target region, potential/Voronoi | 4.4 |
| TAD Game of Degree (PMP, HJI) | 5.1 |
| TAD Game of Kind (barrier) | 5.2 |
| Recon 2-stage barrier + strategy | 6.1 |
| Dynamic weighted matching assignment | 6.2 |
| PMP → three-stage transformation | 6.3 |
| Three-stage barrier + LRR/SRR | 6.4 |
| Optimal three-stage strategy, max dwell time | 6.5 |

## 3. Named results cited in the book

| Result | Where | Note |
|---|---|---|
| Theorem 1 (parametric dome barrier) | 6.1 | includes proof |
| Lemma 1 (SRR = virtual LRR ∩ `{x<l}`) | 6.4 | reflection equivalence |
| Theorem 2 (parametric wedge barrier) | 6.4 | envelope proof |
| Max dwell time `τ_max` existence/uniqueness | 6.5 | scalar reduction lemma |
| Theorem 1 / Corollary 1 / Lemma 1 (one AC) | 3.5 | Lyapunov `V = d_max·d_min` |
| Theorem 4.1 (oval parameterisation) | 3.3 | Xu 2024 |
| Lemma 3.2 (unexpected strategy) | 3.4 | Xu 2024 |
| Theorem 2 (optimal deployment) | 4.0 §6, 4.1 | Ma 2025 |

## 4. Derivations bundled with this skill `[new]`

| File | Covers | Status |
|---|---|---|
| `derivations/barrier-1v1-closed-form.md` | escape-point map, `B₁/B₂/B₃`, joints `δ₁,δ₂` (book 3.0 §2 / 3.1) | rigorous |
| `derivations/cartesian-oval-parameterisation.md` | `r>0` oval, feasibility window, similar points, `r→0` (book 3.3) | rigorous |
| `derivations/three-stage-pmp.md` | reflection lemma, SRR = virtual LRR, trajectory structure, `τ_max` scalar reduction (book 6.0 §4.3 / 6.4 / 6.5); PMP relations quoted (book 6.3) | mixed |

## 5. Errata & cautions found while building this skill `[ext]`

- The book's Ch. 3 / Ch. 4 overview preambles originally mis-numbered each other
  ("第四章…" in the 3.0 preamble); **fixed** in the merged book. If you use an older copy,
  ignore the number in that sentence.
- Ch. 6's two coordinate conventions (§3 of `notation-and-assumptions.md`) are a documented
  source of error, not a typo — do not "unify" them silently.
- The book is a *tutorial*: several derivations are stated as "proof omitted / from the paper".
  Treat such statements as `[book]` summaries, not as verified proofs.

## 6. How to cite inside answers

- `[book]` — content taken from 《博弈书籍.md`; give the section number (e.g. `[book 3.3]`).
- `[ext]` — content added by this skill (RL, CBF, safe RL, coding/simulation/writing guides).
- `[new]` — derived in the current session; state the assumptions used.
