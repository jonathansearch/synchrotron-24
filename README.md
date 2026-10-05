<p align="center"><img src="images/logo-ratiss-labs.png" width="350" alt="RATISS LABS"/></p>

<h1 align="center">SYNCHROTRON-24</h1>
<p align="center"><i>A complete cosmology, <b>measured</b> — not postulated. Zero ad-hoc equation.</i></p>
<p align="center"><b>2077 Edition</b> — written in 2026 by a lab that saw the future. 🔭</p>

<p align="center">
<a href="PROTOCOLES.md"><img src="https://img.shields.io/badge/Tests-S01%E2%80%93S06-teal.svg" alt="Tests"/></a>
<img src="https://img.shields.io/badge/Targets-5%2F5-brightgreen.svg" alt="Targets"/>
<img src="https://img.shields.io/badge/Laws-13-blue.svg" alt="Laws"/>
<img src="https://img.shields.io/badge/M%C3%A9thode-mesur%C3%A9_pas_postul%C3%A9-purple.svg" alt="Method"/>
<img src="https://img.shields.io/badge/Python-3-yellow.svg" alt="Python"/>
</p>

> *"Information tells space how to remember, and memory curves space."*
> — the chief. (Einstein said: "matter tells space how to curve." We measured better. 😇)

---

## ⚡ In 30 seconds

| 🗝️ | Key | Test | Measured verdict |
|---|---|---|---|
| 1️⃣ | Unitarity (Info > Mass) | S02 + S02b | bits 1→0.05→**0.73**; mass →0.02 **without** recompaction |
| 2️⃣ | Rebound (Topology > Singularity) | S03 + S03b | stop at r=0.77 then **BANG** (H·t=**1.00** exact!) |
| 3️⃣ | Λ (Fragmentation > Constant) | S04 | Λ\* ~ **10⁻³**, sign **+** (pencil 0.1125 refuted ×50) |
| 4️⃣ | Ghost (Memory > Matter) | S05 | at **M=0**: 9/12 retained vs 0/12 in the void |
| 5️⃣ | Confinement (Confining > Leaking) | S06a + S06b | the link ignores the boundary; the field demands the torus (**12 vs 2**, ×6) |

**Status: 5/5 PROGRAM COMPLETE.** Details: [SYNTHESE_PROGRAMME_5_CLES.md](SYNTHESE_PROGRAMME_5_CLES.md).

---

## 🗺️ Table of contents

1. [The concept](#concept) — 2. [Quick start](#quickstart) — 3. [The 8 rooms of the lab](#salles) — 4. [The tests](#tests) (S01→S06b) — 5. [Key numbers](#chiffres) — 6. [Examples](#exemples) — 7. [The method](#methode) — 8. [Roadmap](#roadmap) — 9. [Tree](#arbo) — 10. [Credits](#credits)

---

<a id="concept"></a>
## 1. 💡 The concept

**The observation (§0 of the PROGRAM)**: we put the same real laws of real life into the universal simulation, and it predicts the true behavior. This is not a copy: **it is the same architecture**. Our universe = focusing + sphere + tori, total shape unknown — and it is IT, coded in the universe, that allows it to exist, to be consistent and to predict reality.

**The architecture (§1, measured)**: the background = torus + sphere **disconnected** (gap 0.892, H1=5.296) → globally NOT round. The torus = the memory (H1 cycles), the sphere = the local roundness. **Without holes, no persistence; without persistence, no world.**

**The chief's visions (§2, sealed then measured)**: 🎈 **balloon** (elastic closed universe) → S03/S04; 🌀 **rebound** (saturated Φ → changes state) → S03; 🍽️ **digestion** (the tides consume the singularity); ⚖️ **weight** (concentration fluctuation — observed spontaneously in S04!); 🕳️ **white hole** = pierced balloon.

📖 Full theory: [PROGRAMME.md](PROGRAMME.md) · [PRINCIPE-ENFERMEMENT.md](PRINCIPE-ENFERMEMENT.md)

---

<a id="quickstart"></a>
## 2. 🚀 Quick start

```bash
git clone https://github.com/jonathansearch/synchrotron-24.git
cd synchrotron-24
pip install numpy matplotlib ripser
python3 experiences/s05_fantome.py   # the ghost that weighs 👻
```

Expected output (2 seconds):
```
[s05] past: 12/12 swallowed, M_fantome=0.12, H1_empreinte=0.677
[s05] VOID   : swallowed= 0/12 bound= 0/12 ...
[s05] GHOST  : swallowed= 0/12 bound= 9/12 ...   # <-- the ghost weighs!
[s05] HOLE   : swallowed=12/12 bound=12/12 ...
```

Then explore: every test writes its JSON into `resultats/` and its figure into `images/`.

---

<a id="salles"></a>
## 3. 🏛️ The 8 rooms of the lab (8 repos in 1!)

| Room | Folder | Content |
|---|---|---|
| 🎯 Missions | `README.md`, `JOURNAL.md`, `images/` | the 5 campaigns, the logbook, the evidence |
| 📐 Theory | `PRINCIPE-ENFERMEMENT.md`, `PROGRAMME.md` | the principle (Φ≥Φc demands confinement) + the program §0-§5 |
| ⚖️ Laws | `LOIS.md`, `SYNTHESE_PROGRAMME_5_CLES.md` | 13 laws + synthesis of the 5 keys and validity |
| 🔬 Bench | `PROTOCOLES.md`, `experiences/` | 9 scripts, all replayable, declared vs measured |
| 📦 Raw facts | `resultats/` | one JSON per test: the numbers, nothing but the numbers |
| 🎫 Questions | `tickets/` | 7 tickets: the questions we measured to the point of confession |
| 🖼️ Gallery | `images/` | 10 figures: every verdict has its portrait |
| 🗺️ Future | `tickets/APPLICATION_PROGRAMME_5_CLES.md` | publication? application? frontier? (chief alone decides) |

---

<a id="tests"></a>
## 4. 🧪 The tests (all of them, in order, with evidence)

### 🌌 Pre-test: the background is NOT round
Torus + sphere: gap 0.892 (disconnected), H1 background = 5.296 (torus 4.271, sphere 1.024 = sampling floor). Non-round branch → the real is round-**concentrated**-shape-unknown. The torus is chosen for memory (H1), not out of bias.

### S01 — Birth: 24 qubits fall into the hole 🕳️
❓ What happens at the horizon? 🔧 M=0.5, r_s=1, exact redshift, κ/r flips, frozen absorbed. 🏆 **24/24 absorbed**, P_sig freezes at 0.9 (saturation, not infinity!), F_info≈0.79, R torn, emergent tide.

<img src="images/plot_S01.png" width="100%" alt="S01: birth"/>
<img src="images/plot_S01_chute.png" width="100%" alt="S01: the fall"/>

### S02 — Page curve: does the info come back? 📄
❓ Slow evaporation → does F_info climb back? 🔧 M 0.5→0.02 (declared), kick 1.5·v_esc. 🏆 bits outside **1→0.05→0.73±0.02**, 24/24 re-emitted, S01 control = 0 → **UNITARITY MEASURED**.

<img src="images/plot_S02.png" width="100%" alt="S02: Page curve"/>

### S02b — Dissociation: mass dies, info migrates ⚖️
❓ Does Hawking confuse two regimes? 🔧 massive qubits m=0.01, measured M_local + PHI probe. 🏆 M_local peak **0.65→0.02** (the frozen ones weigh then leave!), I→**0.73**, PHI 5.1→**0.001** (×5000 below the initial: **no recompaction**). Topology = conserved, energy = dissipated.

<img src="images/plot_S02b.png" width="100%" alt="S02b: dissociation"/>

### S03 — Rebound: KO of the singularity 🥊
❓ Does the universe bounce? 🔧 ring H1~5.7, F=-g/r²+k/r⁴ (k=0 GR / k>0 Planck) + friction (v1 without friction cancelled: orbits!). 🏆 GR **crosses and pulverizes** (H1 5.75→**0.000**, amnesia); Planck **stops at r=0.77** (rho~12.5≈rho_crit/2, mini-tattoo **H1~0.1**). No zero point!

<img src="images/plot_S03.png" width="100%" alt="S03: Planck rebound"/>

### S03b — Resurrection: THE BIG BANG ARRIVES 💥
❓ Everything at the same point, then we let go? 🔧 zero point eps=0.1, S03 micro-law, without friction, bits + flips. 🏆 Planck **EXPLODES**: r 0.1→**343** (×2600!), H1 0→**61**, **H·t=1.00 EXACT** (Hubble emerges!), H1/r=0.178 constant (homothety!), rho in 1/t³, **ROUND 12/12** 🌍, F frozen 0.46, 24/24 bits, 0 fusion. GR: fused core (d_min 0.0015!), H1=0.00, jets.

<img src="images/plot_S03b.png" width="100%" alt="S03b: resurrection"/>

### S04 — Lambda: the ghost captured 👻
❓ What repulsion stabilizes Φ? Sign? Order? 🔧 free ring R0=4, F_Λ=+Λ·r (exact shape of the real Λ!), scan -0.05→+0.2. 🏆 **Zero crunch**, universal fragmentation (= spontaneous WEIGHT!); BOUND/FREE separatrix between 0 and 0.002 → **Λ\* ~10⁻³, SIGN +** (like the real universe!), pencil 0.1125 **refuted ×50** 🥞; t_RIP 8→240 (critical slowdown!), rounding chaos; fast RIPs **freeze the ring** (H1→20-36) — escape saves the memory!

<img src="images/plot_S04.png" width="100%" alt="S04: lambda ghost"/>

### S05 — Ghost: gravity WITHOUT matter 👻🍎
❓ Hole removed, imprint kept → do the next ones fall? 🔧 common past 12/12 swallowed (M_ghost=0.12, **H1=0.677**); VOID (M=0) vs GHOST (M=0+imprint) vs HOLE (M=0.5); **paired** apples (same seed!). 🏆 VOID **0/12** (leak) vs GHOST **9/12 BOUND** (rmin 0.64, they dive!) vs HOLE 12/12. **24% of the mass retains 75% of the apples.** Gravity = topological memory. (The chief's ontological verdict sealed in the ticket: double seal ✅✅.)

<img src="images/plot_S05.png" width="100%" alt="S05: the ghost that weighs"/>

### S06a — Open boundary: the link ignores the wall 🧱
❓ Does the ghost die in an open universe? (chief's order + Qwen suggestion) 🔧 S05-GHOST + absorbing boundary R_OUT=8. 🏆 **8/12 + 1 parabolic** (E=-0.0045) vs 9/12 closed — same regime, **not 0/12**! Newton does not know whether the world is open: naive hypothesis refuted (we don't build on sand 😇).

### S06b — Messengers: the field demands the resonator ✉️
❓ What if gravity travels? 🔧 **zero direct force**: messengers emitted by the imprint (random walk, life TAU); CLOSED = periodic torus (accumulation) vs OPEN = leak; criterion **winding |Δθ|>π** (v1 E_proxy broken → v2). 🏆 msg **909 vs 170** (leak ×5.3); at k=7e-5: **12/12 vs 2/12 (×6!)** — the confined field winds everything, the leaking field evaporates. **Confinement is the condition of carried gravity.** DGP style: gravity-leak! Target 5 FINISHED. **PROGRAM COMPLETE.** 🏁

<img src="images/plot_S06.png" width="100%" alt="S06: closure judged"/>

---

<a id="chiffres"></a>
## 5. 📊 Key numbers (everything, in one table)

| Test | Measurement | Value | Control |
|---|---|---|---|
| Background | H1 (torus+sphere disconnected) | 5.296 (gap 0.892) | sphere 1.024 = floor |
| S01 | absorbed / P_sig / F_info | 24/24, 0.9 (frozen), 0.79 | — |
| S02 | bits outside / re-emitted | 1→0.05→0.73±0.02, 24/24 | S01 control = 0 |
| S02b | M_local / I_rec / PHI | peak 0.65→0.02, 0.73, →0.001 | — |
| S03 | GR: H1 / Planck: r_stop, rho, H1 | 0.000 / 0.77, 12.5, ~0.1 | v1 cancelled (orbits) |
| S03b | Planck: r / H1 / H·t / roundness / F | 343, 60.9, 1.00, 12/12, 0.46 frozen | GR: H1=0, d_min 0.0015 |
| S04 | Λ\* / sign / t_RIP / fast-RIP H1 | ~10⁻³ / + / 8→240 / →20-36 | pencil 0.1125 refuted ×50 |
| S05 | VOID / GHOST / HOLE (bound) | 0/12, **9/12**, 12/12 | H1_imprint = 0.677 |
| S06a | GHOST-OPEN vs closed | 8+1parab. vs 9/12 | naive 0/12 refuted |
| S06b | CLOSED vs OPEN (k=7e-5) / msg | **12 vs 2** (×6) / 909 vs 170 | weak k 0/0, strong k 12/10 |

---

<a id="exemples"></a>
## 6. 💻 Examples

**Ex. 1 — Replay the Big Bang** (2 s):
```bash
python3 experiences/s03b_resurrection.py
# [s03b] Planck: r 0.1 -> 343.21, H1 0.005 -> 60.91, H.t=1.00, ...
```

**Ex. 2 — Verify Hubble yourself**:
```python
import json
s = json.load(open('resultats/s03b.json'))['runs']['Planck']['serie']
for r in s[10::10]:
    print('t =', r['t'], ' H.t =', round(r['H'] * r['t'], 3))
# t = 2.0  H.t = 1.0
# t = 4.0  H.t = 1.0   ... (emergent, coded nowhere!)
```

**Ex. 3 — Plot your own curve**:
```python
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
s = json.load(open('resultats/s02.json'))['serie']
plt.plot([r['t'] for r in s], [r['bits_out'] for r in s])
plt.title('Page curve: 1 -> 0.05 -> 0.73')
plt.savefig('my_page.png')
```

---

<a id="methode"></a>
## 7. ⚖️ The method (the weapon, not the mood)

**Declared vs measured, always.** Every test separates: the DECLARED (micro-laws, parameters, owned choices — in the docstring) and the MEASURED (what emerges and settles it). We do not solve the paradoxes: **we measure them until they confess.**

**3 sealed refutations** (radical honesty):
1. 🥞 S04: pencil Λ\*=0.1125 → measured ~10⁻³ (**refuted ×50**, fragmentation offers escape)
2. 🧱 S06a: naive "open = 0/12" → measured 8~9/12 (**refuted**, Newton ignores the boundary)
3. 🌀 S06b-v1: E_proxy criterion → broken (slow ballistic, heating) → v2 winding (**fixed**)

**Validity conditions**: **closed (H1≠0)** universe + **saturated focusing (Φ≥Φc)**. The NUMBERS are toy (N=24, 2D); the RATIOS (conserved/dissipated, bound/free, closed/open) are the physics. Details: [SYNTHESE_PROGRAMME_5_CLES.md](SYNTHESE_PROGRAMME_5_CLES.md).

---

<a id="roadmap"></a>
## 8. 🗺️ Roadmap (the vault is open — now what?)

🎫 [APPLICATION_PROGRAMME_5_CLES.md](tickets/APPLICATION_PROGRAMME_5_CLES.md) — 3 tracks, **chief alone decides**:
1. 📰 **Publication**: the 5-keys paper?
2. 🔭 **Application**: testable predictions (H1 transfer? ×6 confinement? Λ by fragmentation?)
3. 🌌 **New frontier**: S07+ (NOT ordered — the PROGRAM is sealed, sacred silence 🤫)

---

<a id="arbo"></a>
## 9. 📁 Tree

```
synchrotron-24/
├── README.md                      # ← you are here (2077 edition)
├── SYNTHESE_PROGRAMME_5_CLES.md   # the 5 keys + validity
├── PROGRAMME.md                   # §0-§5: observation, architecture, laws, targets, method
├── PRINCIPE-ENFERMEMENT.md        # Φ≥Φc demands confinement (S06 track)
├── LOIS.md                        # 13 laws (7 foundation + 6 measured... well, 13!)
├── PROTOCOLES.md                  # §S01→§S06b: all protocols
├── JOURNAL.md                     # the complete logbook
├── experiences/                   # 9 replayable scripts (s01→s06b)
├── resultats/                     # one JSON per test (the raw facts)
├── images/                        # logo + 9 figures (the proofs
...[truncated 515 chars]
---

## ⚛️ QPU Campaign 2026 (real measurements + noisy sims)

| Milestone | Done | Verdict |
|---|---|---|
| Batches 1-3 (IBM) | 65 pubs | GHZ/KZ/Grover/Page: sim = hardware |
| Batch 4 collision (kingston) | 29 pubs | contact 5σ, Page +0.2, H echo 0.014 |
| Harvest 1 (kingston, 51 pubs) | brutal>mid 3/3 (3.3σ), Page revival | session drift 0.04 → autocal |
| Harvest 2 (2 backends, 240 pubs) | zz→plateau (K 88%, M 60%), Page bell peak λ0.8 | backend factor 1.4 → calibration/backend |
| Noise-sim RADAR | horizon ≥ 8L, revival 4L→6L | noise model = 87% of the real (kingston) |
| MICROSCOPE 0-12L | MI dies before zz, horizon ~14L | law of the trio (zz, MI, H) — Page alone lies |
| QPU routes | IBM quota dead → qBraid validated (sim=exact) → AWS Braket (pending CB) | radar-lite quote ~$5 |

**Product**: ENTANGLEMENT DOSIMETRY (new problem: nobody doses λ/depth). Index: [qpu-bigbang/README.md](qpu-bigbang/README.md) · synthesis: [qpu-bigbang/SYNTHESE_MOISSONS.md](qpu-bigbang/SYNTHESE_MOISSONS.md) · problem: [qpu-bigbang/moissonneur/PROBLEME.md](qpu-bigbang/moissonneur/PROBLEME.md).

## 📜 License
MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Jonathan.
