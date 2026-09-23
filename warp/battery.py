"""Batterie W01-W22 v2 : 10 vols (R10-v8 !), 22 examens. 🛸🔋
Fix v2 : R10-v8 (seuil rentabilité, W02 ∝ 1/v ?), W04 détrendé, couverture
exotique %, W21b facteur v8. Échelles SI : 1u=1m, 10u_m=10000kg, 1t=1s.
"""
import json
import sys
import os
import numpy as np
from ripser import ripser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Voyage, alcubierre_f

M_SI = 10000.0
E_J = M_SI
K_SPRING = 0.5


def h1_of(X):
    return max([float(b[1] - b[0])
                for b in ripser(X)['dgms'][1]] or [0.0])


def vol(nom, **kw):
    T = kw.pop('T', 6000)
    fly = kw.pop('fly', {})
    v = Voyage(seed=kw.pop('seed', 26), **kw)
    r = v.vole(T=T, **fly)
    print(f"[vol {nom}] xs={r['xs_fin']:.1f} t_arr={r['t_arr']} W={r['W']:.1f} "
          f"Fbits={r['F_bits']:.2f}")
    return v, r


print('=== MISSION WARP 2026 v4 : 20 vols, 22 examens + suite native ===')
_tmp = Voyage(seed=26)
np.save('/tmp/w22_x0.npy', _tmp.X0.copy())
H1_avant = h1_of(_tmp.Xm[::4])
print(f'[ref] H1_avant milieu = {H1_avant:.3f}')

_, R1 = vol('R1-libre', T=6000, fly={})
_, R2 = vol('R2-class', E_b=0.0, thrust=0.5, T=8000, fly={})
_, R3 = vol('R3-v1', T=5000, fly={'mode': 'impose', 'v_imp': 1.0})
_, R4 = vol('R4-v2', T=3000, fly={'mode': 'impose', 'v_imp': 2.0})
_, R5 = vol('R5-v4', T=2000, fly={'mode': 'impose', 'v_imp': 4.0})
_, R10 = vol('R10-v8', T=1200, fly={'mode': 'impose', 'v_imp': 8.0})
_, R6 = vol('R6-msg', msg_on=True, T=6000, fly={})
_, R6b = vol('R6b-msgdir', msg_on=True, msg_dir=True, T=6000, fly={})
_, R7 = vol('R7-panne', ecut_x=0.0, T=6000, fly={})
_, R8 = vol('R8-lourd', m_s=40.0, T=8000, fly={})
_, R9 = vol('R9-retour', T=4500,
            fly={'mode': 'retour', 'v_imp': 2.0,
                 'schedule': [(20.0, -2.0)]})
_, R11 = vol('R11-natif', E_b=0.0, ghost_on=True, ghost_m=0.1, msg_on=True,
             msg_dir=True, msg_fabcost=0.01, T=8000, fly={})
_, R12 = vol('R12-g005', E_b=0.0, ghost_on=True, ghost_m=0.05, msg_on=True,
             msg_dir=True, msg_fabcost=0.01, T=8000, fly={})
_, R13 = vol('R13-g02', E_b=0.0, ghost_on=True, ghost_m=0.2, msg_on=True,
             msg_dir=True, msg_fabcost=0.01, T=8000, fly={})
_, R14 = vol('R14-D3', E_b=0.0, ghost_on=True, ghost_m=0.1, ghost_D=3.0, msg_on=True,
             msg_dir=True, msg_fabcost=0.01, T=8000, fly={})
_, R15 = vol('R15-ghostonly', E_b=0.0, ghost_on=True, ghost_m=0.1, T=8000,
             fly={})
_, R16 = vol('R16-msgonly', E_b=0.0, msg_on=True, msg_dir=True,
             msg_fabcost=0.01, T=8000, fly={})
_, R17 = vol('R17-lightghost', E_b=0.0, m_s=1.0, ghost_on=True,
             ghost_m=0.01, T=8000, fly={})
_, R18 = vol('R18-lightmsg', E_b=0.0, m_s=1.0, msg_on=True, msg_dir=True,
             msg_fabcost=0.01, T=8000, fly={})
_, R19 = vol('R19-lightnatif', E_b=0.0, m_s=1.0, ghost_on=True,
             ghost_m=0.01, msg_on=True, msg_dir=True,
             msg_fabcost=0.01, T=8000, fly={})

X0 = np.load('/tmp/w22_x0.npy')
W = {}
s1 = R1['serie']
W['W01_vol_libre'] = {'t_arr': R1['t_arr'], 'v_max': max(s['vs'] for s in s1),
                      'W': R1['W'], 'E_J': R1['W'] * E_J}
tc = [(s['t'], s['vs']) for s in s1 if s['t'] > (R1['t_arr'] or 60) / 2]
tt = np.array([t for t, _ in tc])
vv = np.array([v for _, v in tc])
resid = vv - np.polyval(np.polyfit(tt, vv, 1), tt) if len(tt) > 2 else vv
resid2 = vv - np.polyval(np.polyfit(tt, vv, 2), tt) if len(tt) > 3 else vv
W['W04_stabilite'] = {'v_moy': float(vv.mean()), 'v_std': float(vv.std()),
                      'v_std_detrende': float(resid.std()),
                      'v_std_quad': float(resid2.std())}
W['W02_cout_vitesse'] = {f"v{k}": {'W': R['W'], 'E_J': R['W'] * E_J,
                                   't_arr': R['t_arr']}
                         for k, R in [(1, R3), (2, R4), (4, R5), (8, R10)]}
cov = (R6['W_msg'] / R6['W_exp']) if R6['W_exp'] else 0
covb = (R6b['W_msg'] / R6b['W_exp']) if R6b['W_exp'] else 0
W['W02_exotique'] = {'R1_sans_msg': R1['exotic'],
                     'R6_avec_msg': R6['exotic'],
                     'W_msg_fourni': R6['W_msg'],
                     'couverture_msg_pct': 100 * cov,
                     'R6b_dir_t_arr': R6b['t_arr'],
                     'R6b_W_msg': R6b['W_msg'],
                     'R6b_exotic': R6b['exotic'],
                     'R6b_couverture_pct': 100 * covb}
e_warp = (s1[-2]['vs'] / R1['W']) if R1['W'] else 0
s2 = R2['serie']
e_class = (s2[-2]['vs'] / R2['W']) if R2['W'] else 0
fw = (e_warp / e_class) if e_class else None
s10 = R10['serie']
e_v8 = (8.0 / R10['W']) if R10['W'] else 0
fw8 = (e_v8 / e_class) if e_class else None
W['W03_facteur_warp'] = {'v_par_E_warp': e_warp, 'v_par_E_class': e_class,
                         'facteur': fw, 't_warp': R1['t_arr'],
                         't_class': R2['t_arr']}
W['W05_panne'] = {'xs_fin': R7['xs_fin'], 't_arr': R7['t_arr'],
                  'W': R7['W'], 'F_bits': R7['F_bits']}
s8 = R8['serie']
W['W06_charge'] = {'t_arr': R8['t_arr'], 'v_max': max(s['vs'] for s in s8),
                   'W': R8['W'], 'ratio_t': (R8['t_arr'] / R1['t_arr'])
                   if R1['t_arr'] and R8['t_arr'] else None}
off0 = (s1[0]['th_s'] - s1[0]['th_lab']) / (2 * np.pi)
W['W07_horloge'] = {'drift_cycles': (R1['th_s'] - s1[-1]['th_lab'])
                    / (2 * np.pi) - off0,
                    'offset_initial_soustrait': off0}
W['W08_kuramoto'] = {'R_fin': s1[-2]['R'], 'R_mid': s1[len(s1) // 2]['R']}
W['W09_bits'] = {'F_R1': R1['F_bits'], 'F_R5_v4': R5['F_bits'],
                 'F_R7_panne': R7['F_bits'], 'F_R10_v8': R10['F_bits']}
thf = R1['th_fin']
Xf = R1['Xm_fin']
Rf = float(np.abs(np.exp(1j * thf[Xf[:, 0] > 10]).mean()))
Rr = float(np.abs(np.exp(1j * thf[Xf[:, 0] < -10]).mean()))
W['W10_ordre_av_ar'] = {'R_avant': Rf, 'R_arriere': Rr}
for key, R in [('R1', R1), ('R5_v4', R5), ('R9_retour', R9)]:
    dep = np.linalg.norm(R['Xm_fin'] - X0, axis=1)
    W[f'W11_sillage_{key}'] = {'dep_moy': float(dep.mean()),
                               'dep_max': float(dep.max())}
    PE = 0.5 * K_SPRING * float((dep ** 2).sum())
    KE = 0.5 * float((R['Vm_fin'] ** 2).sum())
    W[f'W12_energie_{key}'] = {'PE_ressorts': PE, 'KE_milieu': KE,
                               'E_resid': PE + KE}
W['W13_H1'] = {'avant': H1_avant, 'apres_R1': h1_of(R1['Xm_fin'][::4]),
               'apres_R9': h1_of(R9['Xm_fin'][::4])}
W['W14_stray'] = {'msg_restants': R6['serie'][-1]['n_msg'],
                  'msg_leaked': R6['n_leaked']}
mid = R1['Xm_mid']
if mid is not None:
    rs = np.linalg.norm(mid - np.array([0.0, 0.0]), axis=1)
    dep_mid = np.linalg.norm(mid - X0, axis=1)
    fth = alcubierre_f(rs, 3.0, 1.0)
    cc = float(np.corrcoef(dep_mid, fth)[0, 1])
    W['W15_profil_mur'] = {'correlation_tanh': cc}
    av = (mid[:, 0] > 0) & (rs < 6)
    ar = (mid[:, 0] < 0) & (rs < 6)
    W['W16_contraction'] = {'n_avant': int(av.sum()),
                            'dep_avant': float(dep_mid[av].mean())}
    W['W17_expansion'] = {'n_arriere': int(ar.sum()),
                          'dep_arriere': float(dep_mid[ar].mean())}
    inside = rs < 1.5
    W['W18_plat'] = {'n_dedans': int(inside.sum()),
                     'dep_dedans': float(dep_mid[inside].mean())
                     if inside.any() else 0.0}
else:
    W['W15_profil_mur'] = {'correlation_tanh': None}
    W['W16_contraction'] = {}
    W['W17_expansion'] = {}
    W['W18_plat'] = {}
bord_rel = (R1['th_s'] - s1[0]['th_s']) / (2 * np.pi)
labo_rel = (s1[-1]['th_lab'] - s1[0]['th_lab']) / (2 * np.pi)
W['W19_jumeaux'] = {'bord_cycles': R1['th_s'] / (2 * np.pi),
                    'labo_cycles': s1[-1]['th_lab'] / (2 * np.pi),
                    'bord_relatif': bord_rel, 'labo_relatif': labo_rel,
                    'qui_vieillit': 'bord' if bord_rel > labo_rel else 'labo'}
rng = np.random.default_rng(7)
P = rng.normal(0, 0.1, (200, 2))
esc = 0
for _ in range(2500):
    P += rng.normal(0, 0.3, P.shape)
    dehors = np.linalg.norm(P, axis=1) > 6.0
    esc += int(dehors.sum())
    P = P[~dehors]
    if len(P) == 0:
        break
W['W20_horizon'] = {'echappes_200': esc,
                    'verdict': 'pas de horizon (diffusion libre) — limite'}
e_v4 = (4.0 / R5['W']) if R5['W'] else 0
fw4 = (e_v4 / e_class) if e_class else None
W['W21_causalite'] = {'facteur_warp': fw,
                      'superluminique_energetique': (fw or 0) > 1.0,
                      'facteur_v8': fw8,
                      'v8_rentable': (fw8 or 0) > 1.0,
                      'facteur_v4': fw4,
                      'seuil_rentable': 'entre v2 et v4 (facteur 0.36->1.95)'}
dep9 = np.linalg.norm(R9['Xm_fin'] - X0, axis=1)
W['W22_retour'] = {'xs_fin': R9['xs_fin'], 'W': R9['W'],
                   'dep_moy': float(dep9.mean()),
                   'F_bits': R9['F_bits']}

N = {}
for nom, R in [('R11-natif', R11), ('R12-g005', R12), ('R13-g02', R13),
               ('R14-D3', R14), ('R15-ghostonly', R15),
               ('R16-msgonly', R16), ('R17-lightghost', R17),
               ('R18-lightmsg', R18), ('R19-lightnatif', R19)]:
    sq = R['serie']
    mid = R['Xm_mid']
    if mid is not None:
        rsm = np.linalg.norm(mid - np.array([0.0, 0.0]), axis=1)
        depm = np.linalg.norm(mid - X0, axis=1)
        bins = np.arange(0, 12.5, 0.5)
        prof = [depm[(rsm >= b) & (rsm < b + 0.5)].mean()
                if ((rsm >= b) & (rsm < b + 0.5)).any() else 0.0
                for b in bins]
        hm = max(prof) / 2
        wide = [b for b, pp in zip(bins, prof) if pp > hm]
        width = (max(wide) - min(wide)) if wide else 0.0
        av = (mid[:, 0] > 0) & (rsm < 6)
        ar = (mid[:, 0] < 0) & (rsm < 6)
        dav = float(depm[av].mean()) if av.any() else 0.0
        dar = float(depm[ar].mean()) if ar.any() else 0.0
    else:
        width, dav, dar = 0.0, 0.0, 0.0
    depf = np.linalg.norm(R['Xm_fin'] - X0, axis=1)
    N[nom] = {'t_arr': R['t_arr'], 'v_max': max(x['vs'] for x in sq),
              'W': R['W'], 'W_tow': R['W_tow'], 'W_fab': R['W_fab'],
              'W_msg': R['W_msg'], 'wall_width': float(width),
              'dep_avant': dav, 'dep_arriere': dar,
              'F_bits': R['F_bits'], 'H1_apres': h1_of(R['Xm_fin'][::4]),
              'dep_moy': float(depf.mean())}
    print(f"[natif {nom}] t={R['t_arr']} vmax={N[nom]['v_max']:.2f} "
          f"W={R['W']:.1f} (tow {R['W_tow']:.1f}, fab {R['W_fab']:.1f}) "
          f"mur={width:.1f} H1={N[nom]['H1_apres']:.3f}")
for k in sorted(W):
    print(f'{k} : {W[k]}')
os.makedirs('warp/resultats', exist_ok=True)
json.dump({'params': {'M_SI': M_SI}, 'W': W, 'native': N,
           'series': {'R1': R1['serie'], 'R2': R2['serie'],
                      'R4': R4['serie'], 'R9': R9['serie'],
                      'R10': R10['serie'], 'R11': R11['serie'], 'R15': R15['serie'],
                      'R16': R16['serie'], 'R17': R17['serie'],
                      'R18': R18['serie'], 'R19': R19['serie']}},
          open('warp/resultats/w22.json', 'w'))
print('[w22] 22 examens + suite native (9 vols purs), v4 🛸🎓')
