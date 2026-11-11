import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SHORE = 440
PEOPLE = [(215, 0.82), (285, 0.9), (350, 0.78)]
MX = 420

class CrossingSea(Episode):
    dur = 18.0
    ground = False
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "EXODUS 14  •  CROSSING THE SEA"
    headline = "An army behind. The sea ahead.\nGod made a road."
    captions = [
        (cpdv("Exodus", 14, 13, "And Moses said to the people: “Do not be afraid. Stand firm and see the great wonders of the Lord…"), "Exodus 14:13", 3.6),
        (cpdv("Exodus", 14, 21, "And when Moses had extended his hand over the sea… And the water was divided."), "Exodus 14:21", 7.6),
        (cpdv("Exodus", 14, 22, "And the sons of Israel went in through the midst of the dried sea…"), "Exodus 14:22", 10.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        part = prog(t, 6.4, 8.2) if i >= 1 else 0.0
        sea_wall(cr, SHORE, W + 20, gy, 190 * part, t)
        ground_line(cr, gy, 0, SHORE + 10)
        if part > 0:
            ground_line(cr, gy, SHORE, W)
            sand(cr, SHORE + 40, W - 20, gy, n=40)
        dust_cloud(cr, lerp(-80, 150, prog(t, 0.4, 3.6)), gy, 1.0, t)

        # ---------- the people ----------
        for k, (px, s) in enumerate(PEOPLE):
            x, wa, face = px, 0, -1
            p = pose("look", head=-5)
            p = keyed([(1.0, pose("stand")), (1.6, pose("stand", head=-6)), (2.6, pose("head_hands"))], t)
            if t < 1.6: face = 1
            if t > 4.2:
                p = keyed([(4.2 + 0.2 * k, pose("head_hands")), (4.9 + 0.2 * k, pose("stand", head=-4))], t)
                face = 1 if t > 4.6 + 0.2 * k else -1
            if i == 2 and t > 9.0:
                x, wa, _ = track(t, [(9.2 + 0.3 * k, px), (15.0 + 0.2 * k, px + 500)])
                p = body(t, pose("stand"), wa, speed=1.4); face = 1
                if t > 15.0 + 0.2 * k: p = keyed([(15.0 + 0.2 * k, pose("stand")), (15.6 + 0.2 * k, pose("joy"))], t)
            draw_figure(cr, x, gy, p, s=s, face=face)

        # ---------- Moses ----------
        mx, mwa, mface = MX, 0, -1
        raise_ = pose("stand", rs=128, re=0, head=-8)
        stretch = pose("reach", rs=100, re=-5, lean=6, head=-4)
        mp = keyed([(2.8, pose("stand", rs=20, re=20)), (3.4, raise_)], t)
        staff_mode = "up" if t > 3.2 else "down"
        if i >= 1 and t > 5.4:
            mface = 1
            mp = keyed([(5.4, raise_), (6.0, stretch)], t)
            staff_mode = "fwd"
        if i == 2 and t > 9.0:
            mx, mwa, _ = track(t, [(9.0, MX), (15.0, 960)])
            mp = body(t, pose("stand", rs=40, re=10), mwa, speed=1.4)
            staff_mode = "walk"
            if t > 15.0: mp = keyed([(15.0, pose("stand", rs=40, re=10)), (15.6, pose("stand", rs=128, re=0, head=-10))], t); staff_mode = "up" if t > 15.4 else "walk"
        J = draw_figure(cr, mx, gy, mp, s=1.0, face=mface)
        hx, hy = J["rhand"]
        if staff_mode == "down" or staff_mode == "walk":
            staff(cr, hx, hy - 70, gy)
        elif staff_mode == "up":
            staff(cr, hx, hy - 48, hy + 70)
        else:
            cane(cr, hx + mface * 70, hy - 40, hy + 18, lean=-mface * 80)

        # ---------- the sea ----------
        wind(cr, y0, t, prog(t, 6.0, 6.6) * (1 - prog(t, 8.6, 9.6)) if i >= 1 else 0)
        surface = gy + 120 * part
        if part < 0.99:
            water(cr, surface, t, x0=SHORE - 10, x1=W, rough=1.0, below=PANEL_H)
        if part > 0:
            sea_wall(cr, SHORE, W + 20, y0 + PANEL_H + 6, 46 * part, t + 1.3, color=(0.50, 0.59, 0.64))

OUTPUT_NAME = "day16a_crossing_the_sea_exodus14"
