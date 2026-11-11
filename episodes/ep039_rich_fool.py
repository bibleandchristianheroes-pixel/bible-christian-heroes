import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BXC = 840                 # barns (centre)
SACKS = [(715, 0), (755, 0), (735, -38), (960, 0), (1000, 0), (980, -38)]
SEAT = 470                # where he relaxes
CANDLE = 610

class RichFool(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 12  •  THE RICH FOOL"
    headline = "Bigger barns. Many years.\nHe had one night."
    captions = [
        (cpdv("Luke", 12, 18, "…I will tear down my barns and build larger ones. And into these, I will gather all…"), "Luke 12:18", 5.4),
        (cpdv("Luke", 12, 19, "…Soul, you have many goods, stored up for many years. Relax, eat, drink, and be cheerful."), "Luke 12:19", 9.6),
        (cpdv("Luke", 12, 20, "…Foolish one, this very night they require your soul of you…"), "Luke 12:20", 13.1),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        for k in range(6):
            wheat(cr, 40 + k * 38, gy, 120, sway=math.sin(t * 1.3 + k) * 0.5)
        # ---------- barns ----------
        small = 1 - prog(t, 4.0, 5.0)
        big = prog(t, 5.2, 7.6)
        barn(cr, BXC + 20, gy, w=130, h=90, built=small)
        barn(cr, BXC, gy, w=260, h=150, built=big)
        n = 4 + (1 if t > 1.2 else 0) + (1 if t > 2.7 else 0)
        for k in range(n):
            x, dy = SACKS[k]
            u = prog(t, 7.6 + k * 0.12, 8.1 + k * 0.12)
            if u >= 1: continue
            grain_sack(cr, lerp(x, BXC, u), gy + dy * (1 - u) - 50 * math.sin(math.pi * u), s=0.95 * (1 - 0.5 * u))

        # ---------- the rich man ----------
        hammer = pose("knock_up") if math.sin(t * 18) > 0 else pose("knock_hit")
        carry = pose("stand", rs=150, re=20, ls=150, le=20, head=4)
        face = 1
        if t < 3.0:
            x, wa, d = track(t, [(0.3, 250), (1.2, 660), (1.8, 250), (2.7, 660)])
            loaded = (d > 0)
            p = body(t, carry if loaded else pose("stand"), wa); face = d
            if wa < 0.05: face = 1
        elif t < 3.9:
            x = 660; p = keyed([(3.0, pose("stand")), (3.3, pose("head_hands", lean=-4, head=-10)), (3.7, pose("head_hands", lean=-4, head=-10)), (3.9, pose("stand"))], t)
            loaded = False
        elif t < 7.6:
            x = 660 if t < 5.1 else 640; p = hammer; loaded = False
        elif i == 0 or t < 8.4:
            x = 640; loaded = False
            p = keyed([(7.6, pose("stand")), (8.0, pose("stand", head=-14)), (9.0, pose("stand", head=-14, rs=-20, re=110, ls=-20, le=110))], t)
        else:
            x, wa, d = track(t, [(8.4, 640), (9.2, SEAT)])
            loaded = False
            relax = pose("sad_sit", lean=-14, head=-12, ls=-35, le=0, rs=30, re=90)
            if t < 9.2:
                p = body(t, pose("stand"), wa); face = -1
            else:
                face = 1
                p = keyed([(9.2, pose("stand")), (9.7, relax)], t)
                if t > 9.7:
                    sip = max(0.0, math.sin((t - 9.7) * 2.2))
                    p = mix(relax, pose("sad_sit", lean=-18, head=-25, ls=-35, le=0, rs=100, re=70), sip)
                if i == 2 and t > 12.4:
                    p = keyed([(12.4, p), (13.0, pose("sad_sit", lean=8, head=40, ls=10, le=10, rs=10, re=10))], t)
        J = draw_figure(cr, x, gy, p, s=1.0, face=face)
        if loaded:
            grain_sack(cr, J["head"][0], J["head"][1] - 10, s=0.85)
        if i >= 1 and t > 9.4:
            loaf(cr, SEAT + 75, gy - 9)
            flask(cr, J["rhand"][0] + 6, J["rhand"][1] - 4)

        # ---------- night and the candle (panel 3) ----------
        if i == 2:
            night = prog(t, 10.6, 11.8)
            out = prog(t, 13.0, 13.3)
            if t > 10.4:
                fl = candle(cr, CANDLE, gy, lit=1 - out, t=t, smoke=prog(t, 13.0, 13.4) * (1 - prog(t, 15.5, 16.5)))
                darkness(cr, y0, PANEL_H, 0.92 * night, [(fl[0], fl[1], 260 * (1 - out), 1.0)])
                crescent_moon(cr, 1010, y0 + 110, 22, alpha=night)

OUTPUT_NAME = "day20a_rich_fool_luke12"
