import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

KX = 170          # throne / king
SX = 330          # servant kneels here
FX = 840          # fellow servant
GRAB_X = 735

class UnforgivingServant(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "MATTHEW 18  •  THE UNFORGIVING SERVANT"
    headline = "Forgiven a fortune.\nHe wouldn't forgive a little."
    captions = [
        (cpdv("Matthew", 18, 27, "Then the lord of that servant, being moved with pity, released him, and he forgave his debt."), "Matthew 18:27", 2.8),
        (cpdv("Matthew", 18, 28, "…he found one of his fellow servants who owed him one hundred denarius… ‘Repay what you owe.’"), "Matthew 18:28", 7.6),
        (cpdv("Matthew", 18, 33, "…should you not also have had compassion on your fellow servant, just as I also had compassion on you?"), "Matthew 18:33", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        throne(cr, KX, gy, face=1)
        # ---------- the king ----------
        sit = dict(lt=88, lk=88, rt=80, rk=82)
        hold = pose("stand", rs=75, re=-10, ls=60, le=10, **sit)
        tear = pose("stand", rs=85, re=-40, ls=85, le=-40, head=6, **sit)
        open_ = pose("stand", rs=60, re=-20, ls=50, le=0, head=-4, **sit)
        kp = keyed([(0.0, hold), (2.0, hold), (2.4, tear), (2.8, open_)], t)
        kx = KX
        if i == 2 and t > 9.2:
            call = pose("stand", rs=150, re=20, head=-6)
            point = pose("reach", rs=88, re=0, lean=4, head=0)
            toward = pose("stand", rs=60, re=-30, ls=70, le=-10, head=-6)
            kp = keyed([(9.2, open_), (9.8, pose("stand")), (10.2, call), (11.4, call), (11.9, point), (14.2, point), (14.8, toward)], t)
            kx = KX + 30 * prog(t, 9.2, 9.8)
        KJ = draw_figure(cr, kx, gy, kp, s=1.05, face=1)
        crown(cr, KJ["head"], s=1.05, face=1)
        # the debt, torn up
        if t < 2.4:
            hx, hy = KJ["rhand"]; debt_scroll(cr, hx + 22, hy - 4)
        else:
            debt_scroll(cr, 275, gy - 112, tear=prog(t, 2.2, 2.6), fall=prog(t, 2.8, 3.6), gy=gy)

        # ---------- fellow servant ----------
        if i > 0:
            fp = pose("stand")
            fx = FX
            if t > 7.0:
                lean_back = pose("stand", lean=-10, head=-10, rs=100, re=40, ls=100, le=40)
                beg = pose("kneel", lean=20, head=-10, rs=110, re=-20, ls=100, le=-10)
                fp = keyed([(7.0, pose("stand")), (7.4, lean_back), (8.4, lean_back), (9.0, beg)], t)
                if i == 2 and t > 11.0:
                    fp = keyed([(11.0, beg), (11.8, pose("stand", head=-4)), (13.0, pose("stand", head=-4))], t)
            draw_figure(cr, fx, gy, fp, s=0.96, face=-1, color=(0.24, 0.23, 0.22))

        # ---------- the forgiven servant ----------
        kneel = pose("kneel", lean=45, head=30, rs=100, re=-10, ls=90, le=-10)
        p, x, face, wa = kneel, SX, -1, 0.0
        if t < 2.6:
            p = keyed([(0.0, kneel), (0.6, pose("kneel", lean=30, head=10, rs=100, re=-10, ls=90, le=-10)), (1.2, kneel)], t) if t < 1.2 else kneel
        elif t < 4.0:
            p = keyed([(2.6, kneel), (3.2, pose("kneel", lean=10, head=-10, rs=40, re=40, ls=40, le=40))], t)
        elif i == 0:
            p = keyed([(4.0, pose("kneel", lean=10, head=-10, rs=40, re=40, ls=40, le=40)), (4.8, pose("stand")), (5.4, pose("joy"))], t)
            if t > 5.4: p["lean"] = -6 + 3 * math.sin(t * 5)
        else:
            p = keyed([(4.0, pose("kneel", lean=10, head=-10, rs=40, re=40, ls=40, le=40)), (4.8, pose("stand"))], t)
            if t >= 4.8:
                keys = [(4.8, SX), (7.0, GRAB_X)]
                if i == 2: keys += [(9.8, GRAB_X), (11.6, SX + 30)]
                x, wa, d = track(t, keys)
                face = 1 if t < 9.8 else -1
                grab = pose("reach", rs=100, re=-20, lean=14, head=-4, ls=20, le=60)
                demand = pose("stand", rs=60, re=0, lean=6, head=8, ls=20, le=60)
                if t < 7.0:
                    p = body(t, pose("stand"), wa)
                elif t < 9.8 or i == 1:
                    p = keyed([(7.0, pose("stand")), (7.4, grab), (8.4, grab), (9.0, demand)], t)
                    if 7.4 < t < 8.4: p["lean"] = 14 + 4 * math.sin(t * 14)
                else:
                    if t < 11.6:
                        p = body(t, pose("stand", head=10), wa)
                        if t < 10.2: p = keyed([(9.8, demand), (10.2, pose("stand", head=0))], t)
                    else:
                        shame = pose("kneel", lean=40, head=45, rs=20, re=10, ls=20, le=10)
                        p = keyed([(11.6, pose("stand", head=10)), (12.0, pose("stand", head=10)), (12.8, shame)], t)
        draw_figure(cr, x, gy, p, s=1.0, face=face)

OUTPUT_NAME = "day12b_unforgiving_servant_matthew18"
