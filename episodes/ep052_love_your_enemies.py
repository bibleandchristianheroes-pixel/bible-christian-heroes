import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

NX = 730          # neighbour
HX = 900          # neighbour's house

class LoveYourEnemies(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "MATTHEW 5  •  LOVE YOUR ENEMIES"
    headline = "He turned his back on you.\nWhat do you do next?"
    captions = [
        (cpdv("Matthew", 5, 39, "But I say to you, do not resist one who is evil…"), "Matthew 5:39", 7.4),
        (cpdv("Matthew", 5, 44, "…pray for those who persecute and slander you."), "Matthew 5:44", 9.4),
        (cpdv("Matthew", 5, 44, "But I say to you: Love your enemies. Do good to those who hate you."), "Matthew 5:44", 11.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 1:
            warm_glow(cr, NX + 40, gy - 150, 300, prog(t, 7.6, 9.4))
        if i == 2:
            warm_glow(cr, 710, gy - 120, 380, prog(t, 11.4, 12.6))
        small_house(cr, HX, gy)
        offer = pose("stand", rs=75, re=-5, head=-4)
        carry = pose("stand", rs=35, re=40)
        crossed = pose("stand", lean=-4, head=15, rs=35, re=-125, ls=30, le=-120)
        stop = pose("stand", lean=-6, head=-6, rs=85, re=85)

        # ---------- neighbour: scowls, turns his back ----------
        nx, nwa, _ = track(t, [(4.2, NX), (5.0, NX + 40)])
        nface = -1 if t < 4.2 else 1
        np_ = keyed([(2.4, pose("stand")), (2.9, stop), (3.5, stop), (4.0, crossed)], t)
        if i == 1 and t >= 9.6:   # glances back over his shoulder
            nface = -1
            np_ = keyed([(9.6, crossed), (10.4, pose("stand", head=-4, rs=35, re=-125, ls=30, le=-120)),
                         (13.0, pose("stand", head=-4, rs=35, re=-125, ls=30, le=-120)), (13.8, pose("stand", head=-8))], t)
        if i == 2 and t >= 9.6:
            nface = -1
            np_ = keyed([(9.6, crossed), (10.4, pose("stand", head=6)), (11.0, pose("stand", rs=70, re=-5)),
                         (11.6, pose("stand", rs=45, re=40, head=-6)), (12.6, pose("stand", rs=45, re=40, head=-10, ls=70, le=10))], t)
        NJ = draw_figure(cr, nx, gy, body(t, np_, nwa), s=1.0, face=nface)

        # ---------- the man ----------
        keys = [(0.2, -60), (2.2, 470)]
        if i == 0: keys += [(6.6, 470), (8.4, 260)]
        if i == 2: keys += [(6.0, 470), (7.6, 650)]
        x, wa, _ = track(t, keys)
        face = 1
        p = keyed([(2.2, carry), (2.8, offer), (4.4, offer), (5.0, pose("stand", rs=40, re=40, head=10))], t)
        loaf_at = "hand"
        wall = 0.0
        if i == 0 and t >= 5.0:
            p = keyed([(5.0, pose("stand", rs=40, re=40, head=10)), (5.8, crossed)], t)
            if t >= 6.4: face = -1
            wall = prog(t, 7.0, 8.4)
            loaf_at = None if t >= 5.5 else "hand"
        elif i == 1 and t >= 5.0:
            pray = pose("kneel", lean=6, head=12, rs=45, re=105, ls=40, le=110)
            p = keyed([(5.0, pose("stand", rs=40, re=40, head=10)), (5.6, pose("kneel", lean=40, head=30, rs=70, re=-10)),
                       (6.4, pose("kneel", lean=40, head=30, rs=70, re=-10)), (7.2, pray), (9.0, pray), (9.6, pose("kneel", lean=0, head=-12, rs=45, re=105, ls=40, le=110))], t)
            if t >= 6.0: loaf_at = (x + 70, gy - 9)
        elif i == 2 and t >= 5.0:
            p = keyed([(5.0, pose("stand", rs=40, re=40, head=10)), (6.0, carry), (7.6, carry), (8.2, offer), (11.0, offer),
                       (11.6, pose("stand", rs=20, re=10)), (12.4, pose("stand", rs=55, re=30, ls=30, le=20, head=-6))], t)
            if t >= 11.2: loaf_at = "neighbour"
        J = draw_figure(cr, x, gy, body(t, p, wa), s=1.0, face=face)

        if loaf_at == "hand":
            hx, hy = J["rhand"]; loaf(cr, hx + 8 * face, hy + 2)
        elif loaf_at == "neighbour":
            hx, hy = NJ["rhand"]; loaf(cr, hx - 6, hy + 2)
        elif isinstance(loaf_at, tuple):
            loaf(cr, *loaf_at)
        if i == 0 and 5.0 <= t:   # he sets the gift down and keeps it
            loaf(cr, 420, gy - 9) if t >= 5.5 else None
        rising_wall(cr, 600, gy, wall)

OUTPUT_NAME = "day26b_love_your_enemies_matthew5"
