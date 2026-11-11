import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

FLOCK = [470, 548, 630, 712, 795, 878]   # the ninety-nine
LOST_WORLD = 1830                         # where the lost one is found (panel 2, world x)

class LostSheep(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Start your day with Ave Missal"
    kicker = "LUKE 15  •  THE LOST SHEEP"
    headline = "Ninety-nine were safe.\nHe went after the one."
    captions = [
        (cpdv("Luke", 15, 4, "…would not leave the ninety-nine in the desert and go after the one whom he had lost…"), "Luke 15:4", 8.2),
        (cpdv("Luke", 15, 5, "And when he has found it, he places it on his shoulders, rejoicing."), "Luke 15:5", 11.9),
        (cpdv("Luke", 15, 7, "…there will be so much more joy in heaven over one sinner repenting…"), "Luke 15:7", 13.6),
    ]

    def flock(self, cr, t, gy, S=0.0, look=0.0):
        for k, fx in enumerate(FLOCK):
            counted = prog(t, 3.7 + k * 0.36, 3.9 + k * 0.36) * (1 - prog(t, 4.3 + k * 0.36, 4.6 + k * 0.36))
            g = 0.5 + 0.5 * math.sin(t * 1.3 + k * 1.7)
            graze = max(0.0, g * (1 - counted) * (1 - look))
            sheep(cr, fx - S, gy, s=0.9, face=(1 if k % 2 else -1) if look < 0.5 else 1, graze=graze)

    def draw_panel(self, cr, i, t, y0, gy):
        S = 1100 * prog(t, 6.8, 10.0) if i == 1 else 0.0
        night = prog(t, 7.0, 9.0) if i == 1 else 0.0
        # the lost one wanders off (all panels)
        lx, lwa, _ = track(t, [(1.0, 960), (3.6, 1190)])
        if t < 3.7:
            sheep(cr, lx - S, gy, s=0.9, face=1, graze=0.2 if lwa < 0.1 else 0.0, step=t * 9 if lwa > 0.1 else 0)

        # ---------- shepherd ----------
        point = pose("stand", rs=80, re=0, ls=20, le=10)
        count = keyed([(3.4, pose("stand", ls=20, le=10)), (3.7, point), (6.0, point),
                       (6.4, pose("stand", rs=150, re=115, ls=20, le=10, head=-6)), (6.8, pose("stand", rs=150, re=115, ls=20, le=10, head=-6))], t)
        if 3.7 < t < 6.0:
            count["head"] = 8 * abs(math.sin((t - 3.7) * math.pi / 0.36))
        sx, wa, face, carry, staff_on, bounce = 300, 0, 1, None, True, 0.0
        p = count
        lamp_at = None
        if t >= 6.8:
            if i == 0:
                sx, wa, _ = track(t, [(6.8, 300), (10.2, 1220)])
                p = body(t, pose("stand", ls=20, le=10), wa)
            elif i == 1:
                sx, wa, _ = track(t, [(6.8, 300), (10.0, 420), (10.8, 640)])
                walk_amt = 1.0 if t < 10.8 else 0.0
                hold = pose("stand", rs=55, re=-15, ls=20, le=10)
                if t < 10.8:
                    p = body(t, hold, walk_amt)
                else:
                    kneel = pose("kneel", lean=35, head=30, rs=75, re=-10, ls=70, le=-10)
                    up = pose("stand", rs=150, re=70, ls=150, le=70, head=-6)
                    joy = pose("stand", rs=150, re=70, ls=150, le=70, head=-22)
                    p = keyed([(10.8, hold), (11.3, kneel), (11.6, kneel), (12.2, up), (12.6, joy)], t)
                    staff_on = False
                    u = prog(t, 11.6, 12.2)
                    carry = u
                    if t > 12.6: bounce = 7 * abs(math.sin((t - 12.6) * 4.2))
                lamp_at = (610, gy) if t >= 10.8 else "hand"
            else:
                sx, wa, _ = track(t, [(6.8, 300), (8.8, 1220), (10.2, 1220), (12.6, 1015)])
                if t < 10.2:
                    p = body(t, pose("stand", ls=20, le=10), wa)
                else:
                    staff_on = False; face = -1
                    up = pose("stand", rs=150, re=70, ls=150, le=70, head=-6)
                    kneel = pose("stand", lean=55, head=25, rs=25, re=10, ls=20, le=10, lt=25, lk=35, rt=5, rk=35)
                    p = keyed([(12.6, up), (13.0, kneel), (13.5, kneel), (13.9, pose("stand", head=-10)), (14.3, pose("joy"))], t)
                    p = body(t, p, wa)
                    carry = 1.0 - prog(t, 12.9, 13.3)
        J = draw_figure(cr, sx, gy - bounce, p, s=1.05, face=face)
        if staff_on:
            hx, hy = J["lhand"]; staff(cr, hx, hy - 70, gy)

        # ---------- the found sheep ----------
        if i == 1:
            fx = LOST_WORLD - S
            thornbush(cr, fx - 30, gy, s=1.0)
            if carry is None or carry <= 0:
                sheep(cr, fx, gy, s=0.9, face=-1, graze=0.0)
            else:
                shx, shy = J["sh"]
                x = lerp(fx, shx, carry); y = lerp(gy, shy + 42, carry) - 40 * math.sin(math.pi * carry)
                sheep(cr, x, y, s=0.85, face=-1)
            # lamp
            if lamp_at == "hand":
                lp = lamp(cr, J["rhand"][0] + 8, J["rhand"][1] + 14, lit=1.0, flicker=t)
            elif lamp_at:
                lp = lamp(cr, *lamp_at, lit=1.0, flicker=t)
            else:
                lp = None
            self.flock(cr, t, gy, S)
            lights = [(lp[0], lp[1], 360, 1.0)] if lp else []
            darkness(cr, y0, PANEL_H, 0.85 * night, lights)
        elif i == 2:
            if carry is not None:
                shx, shy = J["sh"]
                x = lerp(950, shx, carry); y = lerp(gy, shy + 42, carry) - 30 * math.sin(math.pi * carry)
                sheep(cr, x, y, s=0.85 if carry > 0.5 else 0.9, face=-1)
            look = prog(t, 13.5, 14.0)
            self.flock(cr, t, gy, look=look)
            warm_glow(cr, 700, y0 + 120, 560, prog(t, 13.6, 14.8))
        else:
            self.flock(cr, t, gy, look=prog(t, 10.4, 11.0) * 0.0)

OUTPUT_NAME = "day08b_lost_sheep_luke15"
