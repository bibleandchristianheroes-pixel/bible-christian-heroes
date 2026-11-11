import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

ROW = [500, 570, 640, 710, 780]
CUT = 0                    # index of the stalk he cuts in panel 3

class DoNotGrowWeary(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "GALATIANS 6  •  DO NOT GROW WEARY"
    headline = "Same seed. Same hot sun.\nWho kept watering?"
    captions = [
        (cpdv("Galatians", 6, 9, "And so, let us not be deficient in doing good."), "Galatians 6:9", 8.4),
        (cpdv("Galatians", 6, 9, "…in due time, we shall reap without fail."), "Galatians 6:9", 11.2),
        (cpdv("Galatians", 6, 10, "Therefore, while we have time, we should do good works toward everyone…"), "Galatians 6:10", 13.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        heat = 0.5 + 0.5 * math.sin(t * 3)
        sun(cr, 960, y0 + 110, r=30 + 3 * heat)

        # ---------- crops ----------
        early = 26 * prog(t, 2.2, 5.0)
        for k, px in enumerate(ROW):
            if i == 0:
                sprout(cr, px, gy, early, wither=prog(t, 7.0 + 0.2 * k, 9.0 + 0.2 * k))
                continue
            if i == 2 and k == CUT and t >= 12.3:
                cr.set_source_rgb(*INK); cr.set_line_width(3); cr.move_to(px, gy); cr.line_to(px, gy - 10); cr.stroke()
                continue
            if t < 9.0:
                sprout(cr, px, gy, early + 19 * prog(t, 6.0 + 0.3 * (4 - k), 8.4 + 0.3 * (4 - k)))
            else:
                h = lerp(45, 130 + 6 * math.sin(k * 2.1), prog(t, 9.0, 11.0))
                wheat(cr, px, gy, h, sway=0.25 * math.sin(t * 1.4 + k), grain=prog(t, 9.8, 11.2))

        # ---------- farmer ----------
        keys = [(0.2, -60), (1.8, 430), (2.0, 430), (5.0, 720)]
        if i == 0:
            keys += [(6.0, 720), (7.4, 300)]
        else:
            keys += [(6.0, 720), (9.0, 430)]
            if i == 2: keys += [(11.0, 430), (11.6, 470), (12.6, 470), (13.2, 425)]
        x, wa, d = track(t, keys)
        face = 1 if t < 5.6 else -1
        hold = pose("stand", rs=55, re=-20)
        pour = 2.0 < t < 5.0 or (i > 0 and 6.0 < t < 9.0)
        p = body(t, hold, wa)
        p["rs"], p["re"] = hold["rs"], hold["re"]
        jug = "hand"
        sheaf = None
        if 5.0 <= t < 6.0:
            p = keyed([(5.0, hold), (5.3, pose("stand", rs=150, re=140, head=14, ls=10)), (5.7, pose("stand", rs=150, re=140, head=14)), (6.0, hold)], t)
        if i == 0 and t >= 7.4:
            p = keyed([(7.4, pose("stand", head=10)), (8.0, pose("sad_sit", lean=20, head=30, ls=40, le=40, rs=50, re=40))], t)
            jug = (x - 70, gy)
        elif i == 1 and t >= 9.0:
            p = keyed([(9.0, hold), (9.4, pose("stand", rs=20, re=10)), (10.6, pose("stand", head=-12, rs=20, re=10)), (11.4, pose("joy"))], t)
            face = 1 if t > 9.3 else -1
            if t >= 9.3: jug = (x - 70, gy)
        elif i == 2 and t >= 9.0:
            face = 1 if 9.3 < t < 12.4 else -1
            jug = (385, gy) if t >= 11.0 else "hand"
            reach = pose("stand", lean=30, head=20, rs=70, re=-10, ls=60, le=0, lt=20, lk=10)
            give = pose("stand", rs=80, re=-10, head=-4, lean=6)
            p = keyed([(9.0, hold), (9.4, pose("stand", rs=20, re=10)), (10.6, pose("stand", head=-12)),
                       (11.0, pose("stand")), (11.7, pose("stand")), (12.0, reach), (12.3, reach), (12.7, pose("stand", rs=50, re=20)),
                       (13.2, give), (13.9, give), (14.4, pose("joy", rs=40, re=20))], t)
            p = body(t, p, wa)
            if 12.3 <= t < 13.9: sheaf = "farmer"
            elif t >= 13.9: sheaf = "neighbour"
        J = draw_figure(cr, x, gy, p, s=1.0, face=face)
        if jug == "hand":
            hx, hy = J["rhand"]
            tip = watering_jug(cr, hx, hy - 6, tilt=40 if pour else 0, face=face)
            if pour: pour_drops(cr, tip[0], tip[1], gy, t, drift=6 * face)
        else:
            watering_jug(cr, jug[0], jug[1] - 38, tilt=0, face=-1)

        # ---------- neighbour (panel 3) ----------
        if i == 2:
            nx, nwa, _ = track(t, [(11.2, -70), (13.1, 300)])
            np_ = keyed([(13.1, pose("stand")), (13.6, pose("stand", rs=70, re=-10)), (13.9, pose("stand", rs=70, re=-10)),
                         (14.6, pose("stand", rs=160, re=5, ls=150, le=10, head=-14))], t) if t >= 13.1 else pose("stand")
            NJ = draw_figure(cr, nx, gy, body(t, np_, nwa), s=0.96, face=1)
            hand = J["rhand"] if sheaf == "farmer" else NJ["rhand"] if sheaf == "neighbour" else None
            if hand:
                for dx in (-5, 0, 5):
                    wheat(cr, hand[0] + dx, hand[1] + 22, 62, sway=dx * 0.06, grain=1.0)
            warm_glow(cr, 400, gy - 110, 330, prog(t, 14.0, 15.0))

OUTPUT_NAME = "day26a_do_not_grow_weary_galatians6"
