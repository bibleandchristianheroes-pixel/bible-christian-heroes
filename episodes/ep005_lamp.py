import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class Lamp(Episode):
    dur = 18.0
    caption_bg = True
    kicker = "MATTHEW 5  •  LET YOUR LIGHT SHINE"
    headline = "Same light.\nThree choices."
    captions = [
        (cpdv("Matthew", 5, 15, "And they do not light a lamp and put it under a basket…"), "Matthew 5:15", 7.0),
        (cpdv("Matthew", 5, 15, "…on a lampstand, so that it may shine to all who are in the house."), "Matthew 5:15", 9.0),
        (cpdv("Matthew", 5, 16, "So then, let your light shine in the sight of men…"), "Matthew 5:16", 11.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        night = prog(t, 0.6, 3.0)
        x, wa, d = track(t, [(0.3, -60), (2.6, 300)] + ([(9.0, 300), (13.0, 520)] if i == 2 else []))
        lit = prog(t, 3.6, 4.2)
        lights = []
        J = None
        # lamp placement
        if i == 0:
            p = keyed([(2.6, pose("carry")), (3.4, pose("carry")), (4.6, pose("carry")), (5.4, pose("kneel", rs=70, re=10)),
                       (6.6, pose("kneel", rs=70, re=10)), (7.4, pose("sad_sit", head=20))], t)
            J = draw_figure(cr, x, gy, body(t, p, wa), s=1.0)
            if t < 5.4:
                fx, fy = lamp(cr, J["rhand"][0] + 4, J["rhand"][1] + 6, lit, t)
            else:
                fx, fy = lamp(cr, 380, gy, lit, t)
            cover = prog(t, 5.8, 6.6)
            if cover > 0:
                basket(cr, 392, lerp(gy - 140, gy, cover))
            lights.append((fx, fy, 260 * lit * (1 - cover * 0.92), 1.0))
        elif i == 1:
            sty = None
            stand_in = prog(t, 5.0, 5.6)
            if stand_in > 0:
                cr.push_group(); sty = lampstand(cr, 420, gy); cr.pop_group_to_source(); cr.paint_with_alpha(stand_in)
            sty = gy - 153
            p = keyed([(2.6, pose("carry")), (4.6, pose("carry")), (5.8, pose("reach", rs=120, re=0)), (6.4, pose("reach", rs=120, re=0)),
                       (7.2, pose("stand", head=-12)), (8.4, pose("joy"))], t)
            J = draw_figure(cr, x, gy, body(t, p, wa), s=1.0)
            if t < 6.4:
                fx, fy = lamp(cr, J["rhand"][0] + 4, J["rhand"][1] + 6, lit, t)
            else:
                fx, fy = lamp(cr, 412, sty, lit, t)
            grow = prog(t, 6.4, 8.4)
            lights.append((fx, fy, 260 * lit + 420 * grow, 1.0))
        else:
            p = keyed([(2.6, pose("carry")), (4.6, pose("carry")), (5.4, pose("hold_high")), (16, pose("hold_high"))], t)
            J = draw_figure(cr, x, gy, body(t, p, wa), s=1.0)
            fx, fy = lamp(cr, J["rhand"][0] + 2, J["rhand"][1] + 4, lit, t)
            lights.append((fx, fy, 260 * lit + 220 * prog(t, 5.0, 6.4), 1.0))
            # others come toward the light from the dark
            for k, (sx, ex, t0) in enumerate(((1150, 720, 8.0), (1250, 820, 9.0), (-120, 380, 10.0))):
                px, pwa, pd = track(t, [(t0, sx), (t0 + 3.2, ex)])
                if t > t0:
                    pp = keyed([(t0 + 3.2, pose("stand")), (t0 + 3.8, pose("stand", head=-12))], t)
                    draw_figure(cr, px, gy, body(t, pp, pwa), s=0.95, face=-1 if sx > ex else 1)
        darkness(cr, y0, PANEL_H, night, lights)

OUTPUT_NAME = "day05a_let_your_light_shine_matthew5"
