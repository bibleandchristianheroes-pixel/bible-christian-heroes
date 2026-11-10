import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class TenLepers(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "LUKE 17  •  THE TEN LEPERS"
    headline = "Ten were healed.\nOne came back."
    captions = [
        (cpdv("Luke", 17, 14, "…as they were going, they were cleansed."), "Luke 17:14", 4.6),
        (cpdv("Luke", 17, 15, "And one of them, when he saw that he was cleansed, returned, magnifying God with a loud voice."), "Luke 17:15", 7.4),
        (cpdv("Luke", 17, 17, "…Were not ten made clean? And so where are the nine?"), "Luke 17:17", 11.8),
    ]
    JX = 170

    def draw_panel(self, cr, i, t, y0, gy):
        jp = keyed([(0.8, pose("stand")), (1.4, pose("stand", rs=130, re=0)), (3.0, pose("stand", rs=130, re=0)), (3.6, pose("stand"))], t)
        if i == 2:
            jp = keyed([(3.6, pose("stand")), (11.6, pose("stand", head=-6)), (12.3, pose("stand", rs=100, re=-30, head=-12)), (15.0, pose("stand", rs=100, re=-30, head=-12))], t)
        draw_figure(cr, self.JX, gy, jp, s=1.08, prop="robe")
        clean = lambda tt, k: prog(tt, 4.0 + k * 0.12, 4.8 + k * 0.12)
        for k in range(10):
            sx = 330 + k * 62
            ret = (k == 0 and i >= 1)
            if ret:
                x, wa, d = track(t, [(2.6, sx), (5.6, sx + 210), (6.2, sx + 210), (9.4, self.JX + 110)])
            else:
                x, wa, d = track(t, [(2.6, sx), (10.5 + k * 0.15, sx + 900)])
            c = clean(t, k)
            col = tuple(lerp(SOFT[j], INK[j], c) for j in range(3))
            base = mix(pose("stand", lean=18, head=25, rs=30, re=50), pose("stand"), c)
            if ret and t >= 5.6:
                base = keyed([(5.6, pose("stand")), (6.2, pose("look", head=-15)), (6.8, pose("joy")), (8.0, pose("joy")), (8.6, pose("stand"))], t)
                if i == 2:
                    base = keyed([(9.4, pose("stand")), (10.2, pose("kneel", lean=60, head=50, rs=110, re=0, ls=100, le=0))], t) if t >= 9.4 else base
            face = -1 if (ret and t > 6.0) else 1
            if i == 0 and k == 0 and t > 5.6:
                face = 1
            draw_figure(cr, x, gy, body(t, base, wa, speed=1.3 + 0.03 * k), s=0.82, color=col, face=face)

OUTPUT_NAME = "day04b_ten_lepers_luke17"
