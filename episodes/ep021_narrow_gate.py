import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GX = 600                       # gate centre
STONE = (0.47, 0.45, 0.42)
HERO = 1

class NarrowGate(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 7  •  THE NARROW GATE"
    headline = "Many take the easy way.\nFew find the narrow one."
    captions = [
        (cpdv("Matthew", 7, 13, "…wide is the gate, and broad is the way, which leads to perdition, and many there are who enter through it."), "Matthew 7:13", 6.0),
        (cpdv("Matthew", 7, 14, "How narrow is the gate, and how straight is the way…"), "Matthew 7:14", 8.2),
        (cpdv("Matthew", 7, 14, "…which leads to life, and few there are who find it!"), "Matthew 7:14", 11.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            g = prog(t, 10.0, 12.4)
            warm_glow(cr, 900, gy - 110, 460, g)
            if g > 0: sun(cr, 960, lerp(gy + 40, gy - 190, g), r=24)
            cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 80); cr.fill()
        if i == 0:
            stone_gate(cr, GX, gy, gap=230, h=170, post=30, color=STONE)
        else:
            stone_gate(cr, GX, gy, gap=48, h=118, post=26, color=STONE)
        bundle_ground = None
        for k in range(4):
            sx0 = -60 - k * 95
            col = INK if k == HERO else tuple(min(1, c + 0.07 * k) for c in INK)
            face, p = 1, None
            if i == 0:
                x, wa, d = track(t, [(0.0, sx0), (9.5 + k * 0.5, 1180)])
                p = body(t, pose("stand"), wa)
            elif k != HERO:
                stop = 455 - (k if k < HERO else k - 1) * 75
                x, wa, d = track(t, [(0.0, sx0), (4.4, stop), (5.8, stop), (9.6 + k * 0.4, -120)])
                face = 1 if t < 5.6 else -1
                base = pose("stand")
                if 4.4 <= t < 5.8:
                    base = pose("stand", head=-10 + 10 * math.sin(t * 9) * prog(t, 4.8, 5.0))
                p = body(t, base, wa)
            else:
                keys = [(0.0, sx0), (4.4, 505), (7.2, 505), (9.6, 675)]
                if i == 2: keys += [(10.4, 675), (12.6, 870)]
                x, wa, d = track(t, keys)
                crouch = pose("stand", lean=58, head=20, lt=75, lk=105, rt=30, rk=95, rs=70, re=10, ls=50, le=20)
                if t < 4.4:
                    p = body(t, pose("stand"), wa)
                elif t < 7.2:
                    p = keyed([(4.4, pose("stand")), (5.0, pose("stand", head=-12)), (5.9, pose("stand", head=-12)),
                               (6.3, pose("stand", rs=-30, re=120, ls=-20, le=110)), (6.9, pose("stand", lean=30, head=20, rs=40, re=10))], t)
                elif t < 9.6:
                    c = math.sin(t * 7)
                    p = mix(keyed([(7.2, pose("stand")), (7.6, crouch)], t), dict(crouch, lt=75 + 15 * c, rt=30 - 15 * c), 0.5 * prog(t, 7.6, 7.9))
                else:
                    p = keyed([(9.6, crouch), (10.2, pose("stand", head=-14))], t)
                    if i == 2 and t >= 10.4:
                        p = body(t, keyed([(12.6, pose("stand")), (13.3, pose("joy"))], t), wa)
                # the load comes off before the narrow gate
                if t >= 6.3:
                    bundle_ground = (455, gy - 38) if t >= 6.9 else None
            J = draw_figure(cr, x, gy, p, s=1.0, face=face, color=col)
            if k == HERO and (i == 0 or t < 6.3):
                shx, shy = J["sh"]
                burden(cr, shx - 40, shy + 2, w=36, h=42)
            if k == HERO and i > 0 and 6.3 <= t < 6.9:
                u = prog(t, 6.3, 6.9)
                shx, shy = J["sh"]
                burden(cr, lerp(shx - 40, 455 - 18, u), lerp(shy + 2, gy - 42, u), w=36, h=42)
            if bundle_ground:
                burden(cr, 455 - 18, gy - 42, w=36, h=42)
        if i == 0:   # the broad way runs on into darkness
            a = 0.85 * prog(t, 4.5, 8.0)
            if a > 0:
                lg = cairo.LinearGradient(GX + 80, 0, W, 0)
                lg.add_color_stop_rgba(0, 0.06, 0.06, 0.09, 0); lg.add_color_stop_rgba(0.55, 0.06, 0.06, 0.09, a); lg.add_color_stop_rgba(1, 0.06, 0.06, 0.09, a)
                cr.set_source(lg); cr.rectangle(GX, y0, W - GX, PANEL_H); cr.fill()

OUTPUT_NAME = "day11a_narrow_gate_matthew7"
