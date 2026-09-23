"""Moteur Bulle RATISS-Alcubierre (jouet 2D) — Mission Warp 2026. v2.
L'espace = milieu élasto-plastique (ressorts + mémoire). La bulle = vrai
profil Alcubierre tanh (contraction avant, expansion arrière, intérieur plat).
Le vaisseau surfe par réaction (Newton) ou vole imposé. Zéro force cachée :
tout le déclaré est ci-dessous, tout le reste est MESURÉ par battery.py.
v2 : W_thrust compté (R2 W=0 corrigé), messagers actifs (kap 0.03),
Kuramoto partiel (K=0.15, spread 0.2), 64 bits bord (σ=0.06).
"""
import numpy as np


def alcubierre_f(rs, R, sigma):
    """Vrai profil Alcubierre (1994) : 1 dedans, 0 dehors, mur en R."""
    return ((np.tanh(sigma * (rs + R)) - np.tanh(sigma * (rs - R)))
            / (2 * np.tanh(sigma * R)))


class Voyage:
    def __init__(s, seed=26, NX=41, NY=16, XBOX=30.0, YBOX=10.0,
                 k_anchor=0.5, gamma_m=0.2, yield_r=1.0, plast=0.02,
                 R_b=3.0, R_in=1.5, sigma=1.0, E_b=1.0,
                 m_s=10.0, ksurf=0.2, thrust=0.0,
                 msg_on=False, msg_rho=1.5, msg_tau=250, msg_sig=0.3,
                 msg_kap=0.03, msg_r=1.0, msg_dir=False,
                 ghost_on=False, ghost_D=2.0, ghost_m=0.1, ghost_n=12,
                 ghost_r=0.8, msg_fabcost=0.0,
                 K_kura=0.5, kap_c=0.1, kap_w=0.2, nu_wall=0.1,
                 ecut_x=None):
        r = np.random.default_rng(seed)
        s.rng = r
        gx = np.linspace(-XBOX, XBOX, NX)
        gy = np.linspace(-YBOX, YBOX, NY)
        XX, YY = np.meshgrid(gx, gy)
        s.X0 = np.column_stack([XX.ravel(), YY.ravel()])
        s.Xm = s.X0 + r.normal(0, 0.1, s.X0.shape)
        s.Vm = np.zeros_like(s.Xm)
        s.N = len(s.Xm)
        s.th = r.uniform(0, 2 * np.pi, s.N)     # horloges (cumul, pas modulo)
        s.om = r.normal(1.0, 0.2, s.N)          # spread large : sync partielle
        s.xs = np.array([-20.0, 0.0])           # vaisseau : départ X=-20
        s.vs = np.array([0.0, 0.0])
        s.th_s = 0.0                            # horloge de bord (cumul)
        s.bits = np.array([1, 0] * 32)          # motif bord 64 bits (S01 !)
        s.bits0 = s.bits.copy()
        s.Mp = np.zeros((0, 2))                 # messagers Lambda
        s.Mage = np.zeros(0)
        s.n_leaked = 0
        s.W = 0.0                               # travail total (coût)
        s.W_exp = 0.0                           # travail zone expansion
        s.W_msg = 0.0
        s.W_tow = 0.0                           # cout remorquage fantome
        s.W_fab = 0.0                           # cout fabrication messagers
        s.n_msg_fab = 0                           # travail fourni par messagers
        s.P_wall = E_b * sigma * R_b * nu_wall  # maintenance du mur
        s.p = dict(k_anchor=k_anchor, gamma_m=gamma_m, yield_r=yield_r,
                   plast=plast, R_b=R_b, R_in=R_in, sigma=sigma, E_b=E_b,
                   m_s=m_s, ksurf=ksurf, thrust=thrust, msg_on=msg_on,
                   msg_rho=msg_rho, msg_tau=msg_tau, msg_sig=msg_sig,
                   msg_kap=msg_kap, msg_r=msg_r, msg_dir=msg_dir,
                   ghost_on=ghost_on, ghost_D=ghost_D, ghost_m=ghost_m,
                   ghost_n=ghost_n, ghost_r=ghost_r,
                   msg_fabcost=msg_fabcost, K_kura=K_kura,
                   kap_c=kap_c, kap_w=kap_w, XBOX=XBOX, YBOX=YBOX)
        s.ecut_x = ecut_x
        s.E_b_now = E_b
        s.mid_saved = False
        s.Xm_mid = None

    def step(s, dt, mode, v_now):
        p, rng = s.p, s.rng
        if s.ecut_x is not None and s.xs[0] > s.ecut_x:
            s.E_b_now = 0.0                     # PANNE : bulle coupée, on dérive
        d = s.Xm - s.xs
        rs = np.maximum(np.linalg.norm(d, axis=1), 1e-9)
        ahead = s.Xm[:, 0] > s.xs[0]
        f = alcubierre_f(rs, p['R_b'], p['sigma'])
        mask = (rs > p['R_in']).astype(float)
        mag = s.E_b_now * f * mask
        u = d / rs[:, None]
        Fb = np.zeros_like(s.Xm)
        Fb[ahead] = -u[ahead] * mag[ahead, None]    # contraction AVANT
        Fb[~ahead] = u[~ahead] * mag[~ahead, None]  # expansion ARRIÈRE
        Fm = np.zeros_like(s.Xm)
        if p['msg_on']:  # v4 natif : messagers DÉCOUPLÉS du champ (vivent sans le silo)
            n_new = rng.poisson(p['msg_rho'])
            if n_new > 0:
                a = rng.uniform(np.pi / 2, 3 * np.pi / 2, n_new)
                emit = (s.xs + p['R_b']
                        * np.column_stack([np.cos(a), np.sin(a)]))
                s.Mp = np.vstack([s.Mp, emit])
                s.Mage = np.concatenate([s.Mage, np.zeros(n_new)])
                s.W += n_new * p['msg_fabcost']
                s.W_fab += n_new * p['msg_fabcost']
                s.n_msg_fab += n_new
            if len(s.Mp):
                s.Mage += 1
                s.Mp += rng.normal(0, p['msg_sig'], s.Mp.shape)
                out = (np.abs(s.Mp[:, 0]) > p['XBOX'] + 5) | \
                      (np.abs(s.Mp[:, 1]) > p['YBOX'] + 5)
                s.n_leaked += int(out.sum())
                keep = ~out & (s.Mage <= p['msg_tau'])
                s.Mp, s.Mage = s.Mp[keep], s.Mage[keep]
            if len(s.Mp):
                dd = s.Xm[:, None, :] - s.Mp[None, :, :]
                dist = np.sqrt((dd ** 2).sum(-1))
                hits = dist < p['msg_r']
                for i in np.where(hits.any(1))[0]:
                    if p['msg_dir']:
                        uo = s.Xm[i] - s.xs
                        uo /= max(np.linalg.norm(uo), 1e-9)
                        Fm[i] = p['msg_kap'] * hits[i].sum() * uo
                    else:
                        w = dd[i][hits[i]]
                        w /= np.maximum(np.linalg.norm(w, axis=1,
                                                       keepdims=True), 1e-9)
                        Fm[i] = p['msg_kap'] * w.sum(0)
        Fg = np.zeros_like(s.Xm)
        Fgs = np.zeros(2)
        if p['ghost_on']:
            ga = np.linspace(0, 2 * np.pi, p['ghost_n'], endpoint=False)
            G = s.xs + np.array([p['ghost_D'], 0.0]) + p['ghost_r'] * np.column_stack([np.cos(ga), np.sin(ga)])
            dg = s.Xm[:, None, :] - G[None, :, :]
            rg = np.maximum(np.sqrt((dg ** 2).sum(-1)), 0.05)
            Fg = (p['ghost_m'] * (-dg) / rg[..., None] ** 3).sum(1)
            ds = G - s.xs
            rss = np.maximum(np.linalg.norm(ds, axis=1), 0.05)
            Fgs = (p['ghost_m'] * ds / rss[:, None] ** 3).sum(0) / p['m_s']
            F_on_g = (p['ghost_m'] * dg / rg[..., None] ** 3).sum(0)
            tow = -float((F_on_g * s.vs).sum() * dt)
            s.W_tow += tow
            s.W += tow
        F = Fb + Fm + Fg - p['k_anchor'] * (s.Xm - s.X0) - p['gamma_m'] * s.Vm
        s.Vm += F * dt
        dx = s.Vm * dt
        s.Xm += dx
        s.W += float((Fb * dx).sum()) + s.P_wall * dt
        s.W_exp += float((Fb[~ahead] * dx[~ahead]).sum())
        s.W_msg += float((Fm * dx).sum())
        stretch = s.Xm - s.X0
        over = np.linalg.norm(stretch, axis=1) > p['yield_r']
        s.X0[over] += stretch[over] * p['plast']
        if mode == 'libre':
            react = (-(Fb + Fm).sum(0) * p['ksurf']) / p['m_s'] + Fgs
            s.vs += (react + p['thrust'] / p['m_s']
                     * np.array([1.0, 0.0])) * dt
            s.xs += s.vs * dt
            s.W += float(p['thrust'] * s.vs[0] * dt)  # W poussée (fix v2 !)
        else:
            s.vs = np.array([v_now, 0.0])
            s.xs += s.vs * dt
        z = np.exp(1j * s.th)
        Rg = float(np.abs(z.mean()))
        Psi = float(np.angle(z.mean()))
        s.th += (s.om + p['K_kura'] * Rg * np.sin(Psi - s.th)) * dt
        near = rs < 5.0
        th_loc = float(np.angle(np.exp(1j * s.th[near]).mean())) \
            if near.any() else Psi
        s.th_s += (1.0 + p['kap_c'] * np.sin(th_loc - s.th_s)) * dt
        g_wall = s.E_b_now * p['sigma'] / 2
        flips = rng.random(64) < p['kap_w'] * g_wall * dt
        s.bits ^= flips.astype(int)
        if not s.mid_saved and s.xs[0] >= 0.0:
            s.Xm_mid = s.Xm.copy()
            s.mid_saved = True
        return Rg

    def vole(s, T, dt=0.01, mode='libre', v_imp=0.0, schedule=None,
             snap_every=200, X_ARR=20.0, T_relax=1000):
        serie, t_arr, v_now = [], None, v_imp
        step = 0
        while True:
            if schedule:
                for (tsw, vv) in schedule:
                    if step * dt >= tsw:
                        v_now = vv
            Rg = s.step(dt, mode, v_now)
            if step % snap_every == 0:
                serie.append({'t': round(step * dt, 2),
                              'xs': float(s.xs[0]),
                              'vs': float(s.vs[0]),
                              'W': float(s.W),
                              'n_msg': int(len(s.Mp)),
                              'th_s': float(s.th_s),
                              'th_lab': float(s.th.mean()),
                              'R': float(Rg)})
            step += 1
            if t_arr is None and mode != 'retour' and s.xs[0] >= X_ARR:
                t_arr = step * dt
                break
            if step >= T:
                break
        s.E_b_now = 0.0
        s.vs = np.array([0.0, 0.0])
        for _ in range(T_relax):
            F = -s.p['k_anchor'] * (s.Xm - s.X0) - s.p['gamma_m'] * s.Vm
            s.Vm += F * dt
            s.Xm += s.Vm * dt
        serie.append({'t': round(step * dt, 2), 'xs': float(s.xs[0]),
                      'vs': float(s.vs[0]), 'W': float(s.W),
                      'n_msg': int(len(s.Mp)), 'th_s': float(s.th_s),
                      'th_lab': float(s.th.mean()), 'R': 0.0})
        return {'serie': serie, 't_arr': t_arr, 'W': float(s.W),
                'W_exp': float(s.W_exp), 'W_msg': float(s.W_msg),
                'exotic': float(s.W_exp - s.W_msg),
                'W_tow': float(s.W_tow), 'W_fab': float(s.W_fab),
                'n_msg_fab': int(s.n_msg_fab),
                'n_leaked': s.n_leaked, 'Xm_mid': s.Xm_mid,
                'Xm_fin': s.Xm.copy(), 'X0_fin': s.X0.copy(),
                'Vm_fin': s.Vm.copy(),
                'th_fin': s.th.copy(), 'th_s': float(s.th_s),
                'F_bits': float((s.bits == s.bits0).mean()),
                'xs_fin': float(s.xs[0])}
