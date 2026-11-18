import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

NX = 600        # Naomi stops here
OX = 470        # Orpah stops here
RX = 320        # Ruth stops here (at the back)
HILL = (0.66, 0.63, 0.58)   # distant Bethlehem

n_walk = pose("stand", lean=6, head=6)
n_send = pose("stand", lean=2, head=-2, rs=85, re=-6, ls=10, le=20)      # "Go back to your mother's house"
n_sad = pose("stand", lean=10, head=20, rs=20, re=60, ls=10, le=40)
weep = pose("head_hands")
bowed = pose("stand", lean=6, head=22, rs=15, re=50, ls=10, le=50)
hug = pose("stand", rs=75, re=-70, ls=70, le=-70, lean=6, head=4)
cling = pose("stand", rs=78, re=-75, ls=72, le=-72, lean=14, head=14)


class RuthsLoyalty(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "RUTH 1  •  RUTH'S LOYALTY"
    headline = "Naomi told them both to go home.\nOnly one turned back."
    captions = [
        (cpdv("Ruth", 1, 14, "…Orpah kissed her mother-in-law, and then turned back."), "Ruth 1:14", 5.6),
        (cpdv("Ruth", 1, 16, "…wherever you will go, I will go… Your people are my people, and your God is my God."), "Ruth 1:16", 8.4),
        (cpdv("Ruth", 1, 19, "And so they set out together, and they came to Bethlehem."), "Ruth 1:19", 11.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        light = prog(t, 12.4, 14.4) if i == 2 else 0.0
        hill_city(cr, 790, gy, w=280, h=105, light=light, color=HILL)
        for gx in (150, 420, 690):
            grass_tuft(cr, gx, gy, 14)

        # ---------------- Orpah ----------------
        ox, owa, _ = track(t, [(0.3, -150), (2.7, OX), (4.5, OX), (5.0, NX - 70), (5.9, NX - 70), (6.1, NX - 80), (9.6, -120)])
        oface = 1 if t < 5.95 else -1
        ok = [(2.7, pose("stand")), (3.6, pose("stand", head=10)), (4.0, weep), (4.6, pose("stand", head=4)),
              (5.0, hug), (5.7, hug), (6.1, bowed)]
        if t >= 7.6:
            ok += [(7.6, bowed)]
        op = keyed(ok, t) if t >= 2.7 else pose("stand")
        Jo = draw_figure(cr, ox, gy, body(t, op, owa, speed=1.3), s=0.93, face=oface)
        veil_drape(cr, Jo, s=0.93, face=oface)
        tears(cr, Jo["head"][0] + oface * 12, Jo["head"][1] + 12, t, prog(t, 3.9, 4.2) * (1 - prog(t, 6.6, 7.4)), face=oface)

        # ---------------- Naomi ----------------
        nx, nwa, _ = track(t, [(0.2, -40), (2.6, NX)])
        nface = 1 if t < 2.9 else -1
        nk = [(2.6, n_walk), (3.0, pose("stand", lean=4, head=4)), (3.3, n_send), (4.2, n_send), (4.6, n_sad),
              (5.0, hug), (5.7, hug), (6.2, n_sad)]
        if i >= 1:
            nk += [(6.8, n_sad), (7.2, n_send), (7.8, n_send), (8.2, hug)]     # "hurry after her"... but Ruth clings
            if i == 2:
                nk += [(10.4, hug), (10.9, pose("stand", head=-6)), (11.2, n_walk)]
                if t >= 10.95:
                    nface = 1
                    nx, nwa, _ = track(t, [(11.2, NX), (14.6, NX + 175)])
        np_ = keyed(nk, t) if t >= 2.6 else n_walk
        Jn = draw_figure(cr, nx, gy, body(t, np_, nwa, speed=1.2), s=0.95, face=nface)
        veil_drape(cr, Jn, s=0.95, face=nface)
        tears(cr, Jn["head"][0] + nface * 12, Jn["head"][1] + 12, t, prog(t, 4.4, 4.8) * (1 - prog(t, 8.6, 9.4)), face=nface)

        # ---------------- Ruth ----------------
        rx, rwa, _ = track(t, [(0.4, -260), (2.8, RX)])
        rface = 1
        rk = [(2.8, pose("stand")), (3.6, pose("stand", head=10)), (4.0, weep), (6.4, weep), (6.9, bowed)]
        if i >= 1:
            rx, rwa2, _ = track(t, [(0.4, -260), (2.8, RX), (7.4, RX), (8.2, NX - 66)])
            rwa = rwa2 if t < 8.3 else rwa
            rk += [(7.4, pose("stand", head=-4)), (8.2, cling)]
            if i == 2:
                rk += [(10.4, cling), (10.9, pose("stand", head=-6)), (11.2, pose("stand", head=-4))]
                if t >= 11.2:
                    rx, rwa, _ = track(t, [(11.2, NX - 66), (14.6, NX + 95)])
        rp = keyed(rk, t) if t >= 2.8 else pose("stand")
        Jr = draw_figure(cr, rx, gy, body(t, rp, rwa, speed=1.3 if t < 6 else 1.5), s=0.93, face=rface)
        veil_drape(cr, Jr, s=0.93, face=rface)
        tears(cr, Jr["head"][0] + 12, Jr["head"][1] + 12, t, prog(t, 3.9, 4.2) * (1 - prog(t, 8.6, 9.4)), face=1)


OUTPUT_NAME = "day35a_ruths_loyalty_ruth1"
