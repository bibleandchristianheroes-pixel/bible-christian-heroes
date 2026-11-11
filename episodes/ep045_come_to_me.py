import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX = 780
BENT = pose("stand", lean=34, head=12, rs=20, re=110, ls=15, le=115)

class ComeToMe(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 11  •  COME TO ME"
    headline = "Still carrying it alone?\nHe said: come."
    captions = [
        (cpdv("Matthew", 11, 28, "Come to me, all you who labor and have been burdened, and I will refresh you."), "Matthew 11:28", 5.6),
        (cpdv("Matthew", 11, 29, "Take my yoke upon you, and learn from me, for I am meek and humble of heart…"), "Matthew 11:29", 7.6),
        (cpdv("Matthew", 11, 30, "For my yoke is sweet and my burden is light."), "Matthew 11:30", 9.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        rock_path_tufts(cr, gy, [120, 330, 520, 930, 1040])
        welcome = pose("stand", rs=105, re=-15, ls=95, le=-15, head=4)
        # ---------- shared start: he trudges in, Jesus opens his arms ----------
        mx, mwa, _ = track(t, [(0.0, -40), (4.4, 560)])
        mp = body(t, BENT, mwa, speed=1.0)
        for k_ in ("lean", "head", "rs", "re", "ls", "le"): mp[k_] = BENT[k_]
        mface = 1
        jx, jface = JX, -1
        jp = keyed([(2.0, pose("stand")), (2.8, welcome)], t)
        bag = "back" if t < 4.6 else "ground"
        bag_x = None
        small = False
        yk = False
        jwa = 0
        if i == 0:   # lays down the load and rests at his feet
            kneel = pose("kneel", lean=10, head=28, rs=10, re=20, ls=8, le=20)
            mx2, mwa2, _ = track(t, [(5.2, 560), (5.8, 650)])
            if t >= 4.4:
                mx = mx2
                mp = keyed([(4.4, BENT), (5.0, pose("stand", lean=6)), (5.8, pose("stand")), (6.4, kneel), (9.0, kneel),
                            (10.0, pose("kneel", lean=4, head=-18, rs=10, re=20, ls=8, le=20))], t)
                mp = body(t, mp, mwa2)
            rest = pose("reach", rs=58, re=20, lean=10, head=14, ls=10, le=10)
            if t >= 5.6:
                jp = keyed([(5.6, welcome), (6.4, pose("stand", head=8)), (7.0, rest)], t)
        elif i == 1:  # shares the yoke and they walk on together
            if t >= 4.4:
                jx, jwa, _ = track(t, [(4.6, JX), (5.6, 690), (8.0, 690), (13.0, 900)])
                mx, mwa, _ = track(t, [(4.4, 560), (5.6, 560), (8.0, 560), (13.0, 770)])
                jface = -1 if t < 5.7 else 1
                up = pose("stand", head=-4)
                mp = keyed([(4.4, BENT), (6.6, BENT), (7.4, pose("stand", lean=6, head=0, rs=20, re=110, ls=15, le=115))], t)
                mp = body(t, mp, mwa)
                jp = keyed([(4.4, welcome), (5.0, pose("stand")), (6.0, pose("stand", rs=160, re=20, ls=150, le=20, head=-6)),
                            (6.6, pose("stand", rs=150, re=60, ls=140, le=60)), (7.2, pose("stand", rs=20, re=110, ls=15, le=115))], t)
                jp = body(t, jp, jwa)
                yk = t >= 6.6
                bag = "back" if t < 6.8 else "yoke"
        else:         # sets down the heavy load, takes a light one, walks on lightly
            if t >= 4.4:
                mx, mwa, _ = track(t, [(4.4, 560), (7.8, 560), (13.2, 840)])
                jx, jwa, _ = track(t, [(4.4, JX), (5.4, 670), (7.8, 670), (13.2, 960)])
                jface = -1 if t < 7.6 else 1
                light = pose("stand", head=-10, rs=150, re=30, ls=15, le=10)
                mp = keyed([(4.4, BENT), (5.0, pose("stand", lean=6)), (5.8, pose("stand")), (6.6, pose("reach", rs=70, re=-10)),
                            (7.2, light)], t)
                if t > 7.8:
                    mp = body(t, light, mwa, speed=1.9)
                    mp["head"] = -12
                give = pose("reach", rs=70, re=-10, head=6)
                jp = keyed([(4.4, welcome), (5.4, pose("stand")), (6.2, give), (6.8, give), (7.2, pose("stand"))], t)
                jp = body(t, jp, jwa)
                small = t >= 6.7
        bounce = 6 * abs(math.sin(t * 6)) if (i == 2 and t > 8.0 and mwa > 0.2) else 0
        MJ = draw_figure(cr, mx, gy - bounce, mp, s=1.0, face=mface)
        JJ = draw_figure(cr, jx, gy, jp, s=1.1, face=jface, prop="robe")

        # the heavy load
        if bag == "back":
            sx, sy = MJ["sh"]
            burden(cr, sx - 72, sy - 26, w=64, h=60)
            draw_figure(cr, mx, gy - bounce, mp, s=1.0, face=mface)
        elif bag == "ground":
            drop = prog(t, 4.4, 4.9)
            bx = lerp(MJ["sh"][0] - 74, 470, drop) if t < 4.9 else 470
            by = lerp(gy - 140, gy - 60, drop * drop) if t < 4.9 else gy - 60
            burden(cr, bx, by, w=64, h=60)
        elif bag == "yoke":
            a, b = MJ["sh"], JJ["sh"]
            cx = (a[0] + b[0]) / 2; cy = (a[1] + b[1]) / 2
            cr.set_source_rgb(*INK); cr.set_line_width(3); cr.move_to(cx, cy - 4); cr.line_to(cx, cy + 34); cr.stroke()
            burden(cr, cx - 32, cy + 32, w=64, h=60)
        if yk:
            a, b = MJ["sh"], JJ["sh"]
            yoke(cr, a[0], a[1], b[0], b[1])
        if small:
            if t < 7.2:
                hx, hy = JJ["rhand"]
            else:
                hx, hy = MJ["rhand"]
            burden(cr, hx - 13, hy - 20, w=26, h=20)
        if i == 0:
            warm_glow(cr, 650, gy - 90, 230, prog(t, 9.4, 11.0))

OUTPUT_NAME = "day23a_come_to_me_matthew11"
