import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX = 500
STARS = [(820, 70), (905, 125), (1000, 60), (960, 210), (850, 260), (1040, 300), (330, 250), (610, 290), (720, 230), (450, 300)]

class MerciesNew(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "LAMENTATIONS 3  •  MERCIES NEW EVERY MORNING"
    headline = "He fell at nightfall.\nThe morning still came."
    captions = [
        (cpdv("Lamentations", 3, 22, "By the mercies of the Lord, we are not consumed. For his compassion has not passed away."), "Lamentations 3:22", 7.4),
        (cpdv("Lamentations", 3, 23, "I know it at first light; great is your faithfulness."), "Lamentations 3:23", 10.8),
        (cpdv("Lamentations", 3, 25, "The Lord is good to those who hope in him, to the soul that seeks him."), "Lamentations 3:25", 12.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        # sunset behind him (left), sunrise ahead of him (right)
        sy = lerp(gy - 165, gy + 50, prog(t, 0.0, 5.0))
        if sy < gy + 45: sun(cr, 150, sy)
        dawn = prog(t, 9.4, 11.8) if i > 0 else 0.0
        if dawn > 0:
            sun(cr, 935, lerp(gy + 50, gy - 160, dawn))
            warm_glow(cr, 935, gy - 120, 520, dawn * 0.9)
        cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 100); cr.fill()

        # the man: walks in tired, stumbles, sinks down
        x, wa, _ = track(t, [(0.2, -60), (3.0, MX)])
        tired = pose("stand", lean=10, head=22, ls=4, le=10, rs=8, re=10)
        fall = pose("kneel", lean=35, head=35, rs=70, re=-10, ls=60, le=-10)
        low = pose("sad_sit", lean=30, head=45, ls=60, le=-30, rs=64, re=-26)
        keys = [(3.0, tired), (3.5, fall), (4.3, fall), (5.2, low)]
        if i == 0:
            keys += [(7.0, low), (7.8, pose("sad_sit", lean=26, head=20, ls=60, le=-30, rs=64, re=-26))]
        elif i == 1:
            keys += [(10.0, low), (11.0, pose("sad_sit", lean=8, head=-22, ls=60, le=-30, rs=64, re=-26))]
        else:
            keys += [(10.0, low), (10.8, pose("sad_sit", lean=8, head=-22, ls=60, le=-30, rs=64, re=-26)),
                     (11.6, pose("kneel", lean=10, head=-15, rs=40, re=20, ls=40, le=20)),
                     (12.4, pose("stand", head=-12)), (13.2, pose("joy"))]
        p = keyed(keys, t) if t >= 3.0 else body(t, tired, wa)
        draw_figure(cr, x, gy, p, s=1.0, face=1)

        # night
        night = prog(t, 4.2, 6.4) * (1 - dawn)
        lights = []
        if i == 0:
            lit = prog(t, 6.0, 6.7)
            appear = prog(t, 5.0, 5.8)
            if appear > 0:
                cr.push_group(); lp = lamp(cr, MX + 120, gy, lit=lit, flicker=t)
                cr.pop_group_to_source(); cr.paint_with_alpha(appear)
                if lit > 0: lights.append((lp[0], lp[1], 260, lit))
        darkness(cr, y0, PANEL_H, 0.95 * night, lights)
        if night > 0:
            for k, (sx_, sy_) in enumerate(STARS):
                tw = 0.75 + 0.25 * math.sin(t * 2.3 + k * 1.9)
                cr.set_source_rgba(1, 0.96, 0.85, 0.9 * night * tw)
                cr.arc(sx_, y0 + sy_, 2.6, 0, 2 * math.pi); cr.fill()

OUTPUT_NAME = "day25b_mercies_new_lamentations3"
