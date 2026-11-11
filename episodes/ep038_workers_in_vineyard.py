import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

AX, BX = 180, 250        # idle workers in the marketplace
AWORK, BWORK = 860, 760  # where they work among the vines
PAYX = 520               # where the owner pays

class WorkersInVineyard(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MATTHEW 20  •  THE WORKERS IN THE VINEYARD"
    headline = "One worked all day.\nOne came at the last hour."
    captions = [
        (cpdv("Matthew", 20, 1, "…the father of a family who went out in early morning to lead workers into his vineyard."), "Matthew 20:1", 3.6),
        (cpdv("Matthew", 20, 6, "Yet truly, about the eleventh hour, he went out and found others standing…"), "Matthew 20:6", 9.8),
        (cpdv("Matthew", 20, 9, "…those who had arrived about the eleventh hour came forward, each received a single denarius."), "Matthew 20:9", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        # ---------- the sun crosses the day ----------
        day = 0.1 + 0.25 * prog(t, 3.0, 9.0) if i == 0 else 0.1 + 0.78 * prog(t, 4.6, 9.0)
        a = math.pi * (1 - day)
        sx, sy = 880 + 150 * math.cos(a), gy - 175 - 130 * math.sin(a)
        if i >= 1: warm_glow(cr, sx, sy, 380, 0.6 * prog(t, 7.5, 9.0))
        sun(cr, sx, sy, r=22, rays=8)
        vines(cr, 640, 1010, gy, t)
        work = lambda tt, k: pose("reach", rs=150 + 15 * math.sin(tt * 5 + k), re=-10, ls=130, le=20 + 25 * math.sin(tt * 5 + k), head=-25, lean=0)

        # ---------- owner ----------
        ox, owa, od = track(t, [(0.4, 1150), (2.2, 340), (3.0, 340), (5.0, 1150)])
        if i >= 1 and t > 8.6:
            if i == 1:
                ox, owa, od = track(t, [(8.6, 1150), (9.8, 340), (10.6, 340), (12.0, 1150)])
            else:
                ox, owa, od = track(t, [(8.6, 1150), (9.8, 340), (10.4, 340), (11.0, PAYX)])
        beckon = pose("stand", rs=110 + 25 * math.sin(t * 10), re=-70, head=-4)
        op = body(t, pose("stand"), owa)
        oface = od if owa > 0.05 else -1
        if 2.2 <= t < 3.0 or (i >= 1 and 9.8 <= t < 10.4):
            op = beckon; oface = -1
        if i == 2 and t >= 11.0:
            give = pose("stand", rs=80, re=-10)
            oface = 1
            op = keyed([(11.0, pose("stand")), (11.5, give), (12.0, give), (12.3, pose("stand")), (12.9, give), (13.4, give), (13.8, pose("stand", rs=20, re=10))], t)
        J = draw_figure(cr, ox, gy, op, s=1.08, face=oface, prop="robe")
        ohand = J["rhand"]

        # ---------- worker hired at dawn ----------
        ax, awa, ad = track(t, [(3.0, AX), (5.0, AWORK)])
        ap = body(t, pose("stand"), awa)
        aface = 1
        if t >= 5.0:
            ap = work(t, 0)
        if 2.3 < t < 3.0:
            ap = pose("stand", head=-12)
        acoin = False
        if i == 2 and t > 12.3:
            ax, awa, ad = track(t, [(12.3, AWORK), (13.0, PAYX + 80)])
            aface = -1
            ap = body(t, pose("stand"), awa)
            if t > 13.0:
                ap = keyed([(13.0, pose("stand", rs=60, re=-10)), (13.5, pose("stand", rs=60, re=-10)), (13.9, pose("joy", ls=10, le=10))], t)
                acoin = t > 13.35
        JA = draw_figure(cr, ax, gy, ap, s=1.0, face=aface)
        if acoin: coin(cr, JA["rhand"][0], JA["rhand"][1] - 4, r=10)

        # ---------- worker left standing ----------
        bx, bface, bcoin = BX, 1, False
        bp = pose("stand", rs=-10, re=40, ls=-10, le=40)
        if i >= 1 and t > 6.0:
            bp = keyed([(6.0, bp), (6.6, pose("stand", head=20)), (7.4, pose("sad_sit", head=-5, lean=-4, ls=40, le=60, rs=40, re=60))], t)
            if t > 9.8:
                bp = keyed([(9.8, bp), (10.2, pose("stand", head=-10)), (10.6, pose("joy"))], t)
            if t > 10.8:
                if i == 1:
                    bx, bwa, bd = track(t, [(10.8, BX), (12.2, BWORK)])
                    bp = body(t, pose("stand"), bwa)
                    if t > 12.2: bp = work(t, 2)
                else:
                    bx, bwa, bd = track(t, [(10.8, BX), (11.5, PAYX + 80), (12.2, PAYX + 80), (12.8, PAYX - 110)])
                    bp = body(t, pose("stand"), bwa)
                    bface = -1 if t > 11.5 else 1
                    if 11.5 <= t < 12.2:
                        bp = keyed([(11.5, pose("stand", rs=60, re=-10)), (12.0, pose("stand", rs=60, re=-10))], t)
                    elif t >= 12.2:
                        bface = 1 if t > 12.8 else -1
                        bp = body(t, pose("stand", rs=160, re=5, head=-15), bwa)
                    bcoin = t > 11.85
        JB = draw_figure(cr, bx, gy, bp, s=1.0, face=bface)
        if bcoin: coin(cr, JB["rhand"][0], JB["rhand"][1] - 4, r=10)

        # coins in flight
        if i == 2:
            for t0, tgt in ((11.5, JB), (12.9, JA)):
                u = prog(t, t0, t0 + 0.4)
                if 0 < u < 1:
                    coin(cr, lerp(ohand[0], tgt["rhand"][0], u), lerp(ohand[1], tgt["rhand"][1], u) - 30 * math.sin(math.pi * u), r=9)

OUTPUT_NAME = "day19b_workers_in_vineyard_matthew20"
