import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GRAY = (0.42, 0.40, 0.38)      # the disciple following Jesus
SICK = (0.74, 0.71, 0.66)      # the servant, before he is healed
HX = 800                       # the centurion's house (door at HX+40 .. HX+112)
JX = 360                       # where Jesus stops (facing right)
KX = 560                       # where the centurion kneels (facing left)

c_kneel = pose("kneel", lean=22, head=18, rs=110, re=60, ls=30, le=40)          # hand on heart, head bowed
c_plead = pose("kneel", lean=12, head=4, rs=70, re=-10, ls=30, le=40)           # "only say the word"
c_point = pose("kneel", lean=6, head=-8, rs=40, re=20, ls=-60, le=10)           # gestures back to his house
c_bow = pose("kneel", lean=40, head=30, rs=40, re=40, ls=30, le=40)
j_open = pose("stand", rs=55, re=-10, ls=50, le=-10, head=-6, lean=-4)            # wonder
j_go = pose("stand", rs=85, re=-8, head=-4)                                        # "Go"
hug = pose("stand", rs=75, re=-70, ls=70, le=-70, lean=6, head=4)


class CenturionsFaith(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "MATTHEW 8  •  THE CENTURION'S FAITH"
    headline = "He didn't ask Jesus to come.\nHe asked for one word."
    captions = [
        (cpdv("Matthew", 8, 8, "“Lord, I am not worthy that you should enter under my roof, but only say the word, and my servant shall be healed."), "Matthew 8:8", 3.6),
        (cpdv("Matthew", 8, 10, "…Jesus wondered. And he said to those following him: “Amen I say to you, I have not found so great a faith in Israel."), "Matthew 8:10", 7.4),
        (cpdv("Matthew", 8, 13, "…“Go, and just as you have believed, so let it be done for you.” And the servant was healed at that very hour."), "Matthew 8:13", 11.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        door = prog(t, 11.0, 11.8) if i == 2 else 0.0
        if i == 1:
            warm_glow(cr, KX, gy - 70, 200, prog(t, 7.2, 8.4))
        house(cr, HX, gy, w=230, h=215, door_open=door, light=door)

        # ---------------- the servant (P3) ----------------
        if i == 2 and t > 11.6:
            healed = prog(t, 11.8, 12.6)
            col = tuple(lerp(SICK[j], INK[j], healed) for j in range(3))
            sx, swa, _ = track(t, [(11.8, HX + 76), (13.2, HX - 40)])
            sp = keyed([(11.8, pose("stand", lean=8, head=14, rs=20, re=40)), (12.6, pose("stand", head=-6)), (13.2, pose("stand")), (13.6, hug)], t)
            draw_figure(cr, sx, gy, body(t, sp, swa, speed=1.5), s=0.9, face=-1, color=col)

        # ---------------- the disciple ----------------
        dx, dwa, _ = track(t, [(0.6, -160), (3.4, JX - 130)])
        dp = pose("stand", head=4)
        if i >= 1:
            dp = keyed([(0.0, dp), (7.6, dp), (8.2, pose("stand", head=-8, lean=-4, rs=20, re=60, ls=15, le=60))], t)
        draw_figure(cr, dx, gy, body(t, dp, dwa, speed=1.3), s=0.95, face=1, color=GRAY)

        # ---------------- Jesus ----------------
        jx, jwa, _ = track(t, [(0.2, -60), (3.0, JX)])
        jface = 1
        jk = [(3.0, pose("stand")), (3.6, pose("stand", head=6, rs=25, re=30))]
        if i == 0:
            jk += [(8.0, pose("stand", head=6, rs=25, re=30)), (8.6, pose("stand", rs=70, re=30, head=4))]
        else:
            jk += [(6.6, pose("stand", head=6, rs=25, re=30)), (7.0, pose("stand", head=-4)), (7.6, j_open)]
            if 7.0 <= t < (10.0 if i == 2 else 99):
                jface = -1
            if i == 2:
                jk += [(9.4, j_open), (10.0, pose("stand")), (10.4, j_go), (12.4, j_go), (13.0, pose("stand", rs=40, re=20, head=-4))]
        draw_figure(cr, jx, gy, body(t, keyed(jk, t), jwa, speed=1.3), s=1.05, face=jface, prop="robe")

        # ---------------- the centurion ----------------
        cx, cwa, _ = track(t, [(0.4, HX + 20), (2.6, KX)])
        cface = -1
        walkp = pose("stand", head=2)
        ck = [(2.6, walkp), (3.1, c_kneel), (4.2, c_kneel), (4.7, c_plead), (5.6, c_plead), (6.1, c_point), (6.9, c_point), (7.4, c_bow)]
        if i == 2:
            up = pose("stand", head=-6)
            ck += [(10.4, c_bow), (10.9, pose("kneel", lean=4, head=-12, rs=30, re=30, ls=30, le=30)), (11.3, up)]
            if t > 11.3:
                cx, cwa, _ = track(t, [(11.3, KX), (13.0, HX - 120)])
                cface = 1
                ck += [(12.6, up), (13.4, hug)]
        cp = body(t, keyed(ck, t) if t >= 2.6 else walkp, cwa, speed=1.4)
        Jg = ghost_joints(cx, gy, cp, s=1.0, face=cface)
        cr.save(); cr.rectangle(0, y0, W, gy - y0 - 3); cr.clip()
        cape(cr, Jg, face=cface, s=1.0)
        cr.restore()
        J = draw_figure(cr, cx, gy, cp, s=1.0, face=cface)
        soldier_helmet(cr, J, s=1.0, face=cface)


OUTPUT_NAME = "day34b_centurions_faith_matthew8"
