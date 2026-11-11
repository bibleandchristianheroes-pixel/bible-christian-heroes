import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX, AX = 370, 800

class Annunciation(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 1  •  THE ANNUNCIATION"
    headline = "An angel. A greeting.\nAnd one word: yes."
    captions = [
        (cpdv("Luke", 1, 28, "…“Hail, full of grace. The Lord is with you. Blessed are you among women.”"), "Luke 1:28", 4.4),
        (cpdv("Luke", 1, 29, "…she was disturbed by his words, and she considered what kind of greeting this might be."), "Luke 1:29", 7.6),
        (cpdv("Luke", 1, 38, "…“Behold, I am the handmaid of the Lord. Let it be done to me according to your word.”"), "Luke 1:38", 11.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        appear = prog(t, 1.4, 3.0)
        yes = prog(t, 11.0, 13.0) if i == 2 else 0.0
        leave = prog(t, 13.4, 15.0) if i == 2 else 0.0
        # light: behind the angel, then filling the whole room at her yes
        warm_glow(cr, AX + 20, gy - 140, 330, appear * (1 - leave) * (1 - yes * 0.5))
        warm_glow(cr, MX + 120, gy - 150, 900, yes * 1.1)
        arched_window(cr, 560, gy - 70, w=74, h=110, light=0.25 + 0.6 * yes)

        # ---------- angel ----------
        greet = pose("stand", rs=115, re=-25, head=-4)
        speak = pose("stand", rs=70, re=-10, ls=60, le=-5, head=0)
        ap = keyed([(0.0, pose("stand", head=6)), (3.0, pose("stand", head=6)), (3.6, greet)], t)
        if i == 2 and t >= 8.2:
            ap = keyed([(8.2, greet), (9.0, speak), (10.6, speak), (11.4, pose("stand", head=14, rs=20, re=20))], t)
        angel_figure(cr, AX, gy, ap, s=1.05, face=-1, alpha=appear * (1 - leave), spread=0.4 + 0.6 * appear)

        # ---------- Mary ----------
        pray = pose("kneel", lean=8, head=18, rs=45, re=105, ls=40, le=110)
        look = pose("kneel", lean=0, head=-12, rs=45, re=105, ls=40, le=110)
        trouble = pose("stand", lean=-8, head=24, rs=40, re=115, ls=35, le=120)
        x, wa, _ = track(t, [(6.4, MX), (7.3, MX - 40)])
        keys = [(3.2, pray), (4.0, look)]
        if i >= 1:
            keys += [(6.4, look), (7.3, trouble)]
        if i == 2:
            hum = pose("stand", lean=-2, head=-6, rs=40, re=-15, ls=35, le=-15)
            bow = pose("kneel", lean=12, head=26, rs=50, re=-20, ls=45, le=-20)
            keys += [(9.4, trouble), (10.2, hum), (10.9, bow)]
            x, wa, _ = track(t, [(6.4, MX), (7.3, MX - 40), (9.4, MX - 40), (10.2, MX)])
        p = keyed(keys, t)
        face = 1
        J = draw_figure(cr, x, gy, p, s=0.95, face=face, prop="robe")
        veil_drape(cr, J, s=0.95, face=face)

        # panel 3: light rays as she says yes
        if yes > 0:
            cr.set_source_rgba(1, 0.82, 0.4, 0.55 * yes); cr.set_line_width(3)
            hx, hy = J["head"]
            for k in range(11):
                a = math.pi + (k + 0.5) * math.pi / 11
                cr.move_to(hx + math.cos(a) * 40, hy + math.sin(a) * 40)
                cr.line_to(hx + math.cos(a) * (55 + 60 * yes), hy + math.sin(a) * (55 + 60 * yes)); cr.stroke()

OUTPUT_NAME = "day27a_annunciation_luke1"
