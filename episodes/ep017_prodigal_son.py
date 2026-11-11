import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX, FX, SX = 150, 300, 380        # house centre, father, son start

class ProdigalSon(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 15  •  THE PRODIGAL SON"
    headline = "He spent it all.\nHis father ran to him anyway."
    captions = [
        (cpdv("Luke", 15, 13, "…set out on a long journey to a distant region. And there, he dissipated his substance, living in luxury."), "Luke 15:13", 7.2),
        (cpdv("Luke", 15, 20, "…while he was still at a distance, his father saw him… and running to him, he fell upon his neck…"), "Luke 15:20", 8.2),
        (cpdv("Luke", 15, 22, "…Quickly! Bring out the best robe, and clothe him with it…"), "Luke 15:22", 10.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            warm_glow(cr, 720, gy - 120, 420, prog(t, 11.4, 12.8))
        small_house(cr, HX, gy)
        # ---------- father ----------
        give = pose("reach", rs=75, re=-5, lean=6)
        fp = keyed([(0.0, give), (1.0, give), (1.5, pose("stand", lean=6))], t)
        fx, fwa, fface = FX, 0.0, 1
        if i == 0:
            if t > 4.5:
                fp = keyed([(4.5, pose("stand", lean=6)), (5.3, pose("stand", lean=10, head=22, rs=-10))], t)
        else:
            watch = pose("stand", lean=6, rs=150, re=115, head=-8)
            fp = keyed([(1.5, pose("stand", lean=6)), (4.6, pose("stand", lean=6)), (5.2, watch), (7.4, watch), (7.6, pose("stand", head=-14))], t) if t < 7.8 else fp
            if t >= 7.8:
                fx, fwa, _ = track(t, [(7.8, FX), (9.1, 735)])
                if t < 9.1:
                    fp = run(t, speed=1.6); fp["lean"] = 18
                else:
                    hug = pose("stand", rs=95, re=-55, ls=95, le=-60, lean=8, head=6)
                    fp = keyed([(9.1, run(9.1, speed=1.6)), (9.4, hug)], t)
                    if i == 2 and t > 10.8:
                        fp = keyed([(10.8, hug), (11.3, pose("stand", rs=60, re=10, ls=60, le=10)), (11.9, pose("joy"))], t)
                        fx = lerp(735, 690, prog(t, 10.8, 11.4))
        # ---------- son ----------
        sp = pose("stand"); sface = -1; swa = 0.0; sx = SX; bag = None; robe = 0.0; scol = INK
        if t < 1.3:
            sp = keyed([(0.0, pose("stand")), (0.6, pose("reach", rs=60, re=-10, lean=0)), (1.0, pose("carry", rs=30, re=10))], t)
            bag = "hand" if t > 0.8 else None
        elif i == 0:
            sx, swa, _ = track(t, [(1.4, SX), (4.0, 760)])
            sface = 1; bag = "hand"
            if t < 4.0:
                sp = body(t, pose("carry", rs=30, re=10), swa)
            elif t < 9.0:
                toss = 0.5 + 0.5 * math.sin((t - 4.2) * 2 * math.pi / 0.5)
                sp = pose("joy", rs=lerp(90, 160, toss), re=lerp(30, 0, toss), ls=150, le=10, head=-18)
                sp["lean"] = -4 + 4 * math.sin(t * 6)
            elif t < 10.0:
                sp = keyed([(9.0, pose("stand", rs=120, re=0, head=10)), (9.5, pose("stand", rs=120, re=0, head=20))], t)
            else:
                sp = keyed([(10.0, pose("stand", rs=60, re=10, head=20)), (11.0, pose("sad_sit")), (13.0, pose("sad_sit")), (13.6, pose("head_hands", lean=30, head=40, lt=128, lk=140, rt=122, rk=134))], t)
                bag = None
        else:
            sface = 1; bag = "hand" if t < 4.5 else None
            if t < 4.6:
                sx, swa, _ = track(t, [(1.4, SX), (4.5, 1160)])
                sp = body(t, pose("carry", rs=30, re=10), swa)
            else:   # comes home: ragged, slow, head down
                sface = -1; scol = SOFT
                sx, swa, _ = track(t, [(6.2, 1150), (9.2, 790)])
                sp = body(t, pose("stand", lean=14, head=24), swa * 0.8, speed=1.1)
                if t >= 9.2:
                    sp = keyed([(9.2, pose("stand", lean=14, head=24)), (9.5, pose("stand", lean=12, head=30, rs=40, re=40, ls=40, le=40))], t)
                    scol = SOFT
                if i == 2:
                    robe = prog(t, 10.3, 11.0)
                    scol = tuple(lerp(SOFT[j], INK[j], robe) for j in range(3))
                    if t > 10.8:
                        sp = keyed([(10.8, pose("stand", lean=12, head=30, rs=40, re=40, ls=40, le=40)), (11.6, pose("stand", head=-10)), (12.4, pose("joy"))], t)
        # draw (father on top while hugging)
        hugging = i > 0 and t >= 9.1
        if not hugging:
            fp = body(t, fp, fwa) if not (i > 0 and 7.8 <= t < 9.1) else fp
            draw_figure(cr, fx, gy, fp, s=1.0, face=fface)
        J = draw_figure(cr, sx, gy, sp, s=0.92, face=sface, color=scol)
        if robe > 0:
            cr.push_group(); draw_figure(cr, sx, gy, sp, s=0.92, face=sface, prop="robe"); cr.pop_group_to_source(); cr.paint_with_alpha(robe)
        if hugging:
            draw_figure(cr, fx, gy, fp, s=1.0, face=fface)
        if t < 0.8:
            coin_bag(cr, FX + 70, gy - 118 + 10 * prog(t, 0.0, 0.6), s=0.9)
        elif bag == "hand":
            fill = 1.0
            if i == 0: fill = 1 - prog(t, 4.2, 8.8)
            coin_bag(cr, J["rhand"][0], J["rhand"][1] - 2, s=0.9, fill=fill)
        if i == 0:
            # coins tossed away into the far country
            for k in range(9):
                t0 = 4.2 + k * 0.5
                u = (t - t0) / 1.4
                if 0 <= u <= 1:
                    hx, hy = 760 + 30, gy - 210
                    coin(cr, hx + 260 * u + 30 * (k % 3), hy - 120 * u + 200 * u * u, r=9, alpha=1 - u)
            # famine: a pig wanders in
            px, pwa, _ = track(t, [(10.4, 1180), (12.0, 960)])
            if t > 10.4:
                pig(cr, px, gy, s=0.85, face=-1, graze=prog(t, 12.0, 12.6))

OUTPUT_NAME = "day09a_prodigal_son_luke15"
