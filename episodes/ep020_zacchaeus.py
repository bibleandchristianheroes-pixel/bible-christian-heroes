import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CROWD = [370, 435, 500, 565]
TREE_X, TREE_H = 925, 260
ZS = 0.72                      # Zacchaeus is small
ZX = 660

class Zacchaeus(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "LUKE 19  •  ZACCHAEUS"
    headline = "Too small to see Jesus.\nSo he climbed higher."
    captions = [
        (cpdv("Luke", 19, 3, "…he was unable to do so, because of the crowd, for he was small in stature."), "Luke 19:3", 5.0),
        (cpdv("Luke", 19, 4, "And running ahead, he climbed up a sycamore tree, so that he might see him."), "Luke 19:4", 6.4),
        (cpdv("Luke", 19, 5, "…Jesus looked up and saw him, and he said to him: “Zacchaeus, hurry down…”"), "Luke 19:5", 11.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        seat = sycamore_tree(cr, TREE_X, gy, h=TREE_H, sway=2 * math.sin(t * 1.2))
        # ---------- crowd ----------
        block = prog(t, 3.2, 4.0) if i == 0 else 0.0
        for k, cx in enumerate(CROWD):
            x = cx + 40 * block * (1 if k >= 2 else 0.5) + (25 * math.sin(t * 2.5) * prog(t, 4.0, 4.4) * (1 - prog(t, 7.0, 7.4)) if (i == 0 and k == 3) else 0)
            face = -1
            p = pose("stand", head=-4 + 3 * math.sin(t * 1.3 + k))
            if i == 2 and t > 9.6 + k * 0.1:
                face = 1
            draw_figure(cr, x, gy, p, s=1.0 - 0.03 * (k % 2), face=face, color=tuple(min(1, c + 0.06 * (k % 2)) for c in INK))
        # ---------- Jesus walks along the road ----------
        jkeys = [(0.0, -80), (7.0, 230)]
        if i == 2: jkeys += [(10.6, 700)]
        jx, jwa, _ = track(t, jkeys)
        jp = body(t, pose("stand"), jwa, speed=1.2)
        if i == 2 and t >= 10.6:
            up = pose("stand", head=-35, rs=150, re=-10)
            jp = keyed([(10.6, pose("stand")), (11.2, up), (13.0, up), (13.6, pose("stand", head=-20, rs=60, re=10))], t)
            if t > 14.2:
                jp = keyed([(14.2, pose("stand", head=-20, rs=60, re=10)), (14.8, pose("stand", head=0, rs=45, re=15))], t)
        draw_figure(cr, jx, gy, jp, s=1.05, face=1, prop="robe")
        # ---------- Zacchaeus ----------
        hop = 20 * abs(math.sin(t * 5.5)) * prog(t, 0.8, 1.2) * (1 - prog(t, 3.8, 4.0))
        x, face, lift = ZX, -1, hop
        p = pose("stand", rs=150, re=10, head=-15) if hop > 2 else pose("stand", head=-15)
        ground = gy
        sit = pose("stand", lt=88, lk=88, rt=80, rk=82, rs=40, re=-20, ls=40, le=-10, lean=14, head=10)
        if i == 0 and t >= 4.0:
            x, wa, d = track(t, [(4.0, ZX), (4.6, 625), (5.2, 700), (5.8, 625), (6.4, 690), (7.6, 700)])
            face = -1
            hop2 = 18 * abs(math.sin(t * 5.5)) * (1 - prog(t, 7.0, 7.4))
            lift = hop2
            p = pose("stand", rs=150, re=10, head=-15) if hop2 > 2 else pose("stand", head=-15)
            p = body(t, p, wa * 0.5)
            if t > 7.4:
                p = keyed([(7.4, pose("stand")), (8.2, pose("stand", head=30, lean=8)), (9.0, pose("sad_sit"))], t)
                face = 1 if t > 8.4 else -1
        elif i > 0 and t >= 4.0:
            sx, sy = seat
            if t < 5.2:
                x, wa, _ = track(t, [(4.0, ZX), (5.2, TREE_X - 30)]); face = 1
                p = run(t, speed=2.6); lift = 0
            elif t < 6.8:
                u = prog(t, 5.2, 6.8); face = 1
                x = lerp(TREE_X - 30, sx + 18, u)
                ground = lerp(gy, sy + 46.5 * ZS, u)
                c = math.sin(t * 10)
                p = pose("stand", rs=165 + 10 * c, re=0, ls=160 - 10 * c, le=10, lt=60 + 25 * c, lk=90, rt=40 - 25 * c, rk=90, lean=-5)
                lift = 0
            else:
                x = sx + 18; ground = sy + 46.5 * ZS; face = -1; lift = 0
                peer = pose("stand", lt=88, lk=88, rt=80, rk=82, rs=150, re=60, ls=40, le=-10, lean=22, head=6)   # hand shading eyes
                p = keyed([(6.8, sit), (7.4, peer)], t)
                if i == 2 and t > 11.0:
                    p = keyed([(11.0, peer), (11.6, sit)], t)
                    if t > 12.8:   # hurries down, joyfully
                        u = prog(t, 12.8, 13.8); x = lerp(sx + 18, TREE_X - 34, u); ground = lerp(sy + 46.5 * ZS, gy, u)
                        p = pose("stand", rs=160, re=0, ls=150, le=10, lt=40, lk=60, rt=10, rk=40)
                        if t > 13.8:
                            x, wa, _ = track(t, [(13.8, TREE_X - 34), (14.6, 762)])
                            p = keyed([(13.8, pose("stand")), (14.6, pose("stand")), (15.1, pose("joy"))], t)
                            p = body(t, p, wa)
        draw_figure(cr, x, ground - lift, p, s=ZS, face=face)

OUTPUT_NAME = "day10b_zacchaeus_luke19"
