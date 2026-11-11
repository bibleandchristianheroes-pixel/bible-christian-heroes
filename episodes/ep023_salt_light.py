import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX = 300
HEAP_X = 540
STAND_X = 420

class SaltLight(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 5  •  SALT AND LIGHT"
    headline = "Salt that lost its taste.\nLight that can't be hidden."
    captions = [
        (cpdv("Matthew", 5, 13, "…if salt loses its saltiness… It is no longer useful at all, except to be cast out and trampled under by men."), "Matthew 5:13", 6.6),
        (cpdv("Matthew", 5, 14, "You are the light of the world. A city set on a mountain cannot be hidden."), "Matthew 5:14", 7.4),
        (cpdv("Matthew", 5, 16, "…let your light shine in the sight of men, so that they may see your good works, and may glorify your Father…"), "Matthew 5:16", 12.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        x, wa, _ = track(t, [(0.0, -60), (2.0, MX)]); face = 1
        p = body(t, pose("stand"), wa)
        night = 0.0
        if i == 0:
            taste = pose("stand", rs=150, re=140, head=6)
            shake = pose("stand", rs=40, re=50, head=8)
            toss = pose("reach", rs=110, re=-10, lean=8)
            if t >= 2.0:
                p = keyed([(2.0, pose("stand")), (2.4, pose("stand", rs=40, re=50)), (2.8, taste), (3.4, taste), (3.8, shake),
                           (4.6, shake), (4.9, pose("stand", rs=-30, re=20, lean=-4)), (5.2, toss), (5.8, toss), (6.4, pose("stand", head=14, lean=6))], t)
                if 3.8 < t < 4.6: p["head"] = 8 + 16 * math.sin((t - 3.8) * 20)
            # salt flies onto the road and is trampled
            flew = prog(t, 5.0, 5.6)
            if 5.0 < t < 5.6:
                for k in range(10):
                    u = (t - 5.0) / 0.6
                    sx = lerp(MX + 60, HEAP_X - 30 + k * 6, u); sy = lerp(gy - 120, gy - 4, u) - 60 * math.sin(math.pi * u) * (1 - k * 0.05)
                    cr.set_source_rgb(0.40, 0.38, 0.35); cr.arc(sx, sy, 3, 0, 2 * math.pi); cr.fill()
            if t >= 5.5:
                tr = prog(t, 7.4, 8.2) * 0.6 + prog(t, 9.6, 10.4) * 0.4
                salt_heap(cr, HEAP_X, gy, 1.0, trampled=tr)
            for k, (t0, t1) in enumerate(((5.6, 10.6), (7.8, 12.8))):
                px, pwa, _ = track(t, [(t0, 1160), (t1, -100)])
                if t0 < t < t1:
                    pp = body(t, pose("stand", head=-4 if k else 4), pwa)
                    draw_figure(cr, px, gy, pp, s=0.98 - 0.04 * k, face=-1, color=tuple(min(1, c + 0.06 * k) for c in INK))
            J = draw_figure(cr, x, gy, p, s=1.0, face=face)
            if 2.2 < t < 5.0:
                salt_pouch(cr, J["rhand"][0] + 2, J["rhand"][1] - 4)
        elif i == 1:
            night = prog(t, 2.6, 5.6)
            light = prog(t, 5.8, 7.4)
            hill_city(cr, 650, gy, w=420, h=140, light=light)
            if t >= 2.0:
                point = pose("stand", rs=125, re=-5, head=-14)
                p = keyed([(2.0, pose("stand")), (6.2, pose("stand", head=-6)), (7.0, point), (9.8, point), (10.4, pose("stand", head=-10))], t)
                if t > 10.4:
                    x, wa, _ = track(t, [(10.4, MX), (13.2, 470)])
                    p = body(t, keyed([(13.2, pose("stand", head=-10)), (13.8, pose("joy", head=-14))], t), wa)
            darkness(cr, y0, PANEL_H, 0.8 * night, [(650 + 420 * 0.55, gy - 190, 360, light)])
            hill_city(cr, 650, gy, w=420, h=140, light=light)
            draw_figure(cr, x, gy, p, s=1.0, face=face)
        else:
            night = prog(t, 2.6, 5.6)
            top = lampstand(cr, STAND_X, gy, h=110)
            lit = prog(t, 6.6, 7.0)
            lamp_pos = None
            if t >= 2.0:
                hold = pose("stand", rs=60, re=40)
                place = pose("reach", rs=110, re=-15, lean=6)
                p = keyed([(2.0, pose("stand")), (2.6, hold), (6.4, hold), (7.0, pose("stand", rs=80, re=20)), (7.6, pose("stand", rs=80, re=20)),
                           (8.2, place), (8.6, place), (9.2, pose("stand"))], t)
                if t > 12.0:
                    p = keyed([(12.0, pose("stand")), (12.8, pose("joy"))], t)
            J = draw_figure(cr, x, gy, p, s=1.0, face=face)
            if 2.4 < t < 8.4:
                lx, ly = J["rhand"][0] + 4, J["rhand"][1] + 12
                if t > 7.6:
                    u = prog(t, 7.6, 8.4); lx, ly = lerp(lx, STAND_X, u), lerp(ly, top, u)
                lamp_pos = lamp(cr, lx, ly, lit=lit, flicker=t)
            elif t >= 8.4:
                lamp_pos = lamp(cr, STAND_X, top, lit=1.0, flicker=t)
            # people are drawn to the light, and give glory to God
            for k, (t0, sx, ex) in enumerate(((8.6, 1160, 640), (9.2, 1240, 760))):
                px, pwa, _ = track(t, [(t0, sx), (t0 + 2.8, ex)])
                if t > t0:
                    pp = body(t, pose("stand", head=-4), pwa)
                    if t > t0 + 2.8:
                        pp = keyed([(t0 + 2.8, pose("stand", head=-6)), (t0 + 3.4, pose("stand", head=-6)), (t0 + 4.0, pose("joy"))], t)
                    draw_figure(cr, px, gy, pp, s=0.96, face=-1, color=tuple(min(1, c + 0.05 * k) for c in INK))
            lights = [(lamp_pos[0], lamp_pos[1], 420 * lit + 200 * prog(t, 8.4, 10.0), lit)] if lamp_pos and lit > 0 else []
            darkness(cr, y0, PANEL_H, 0.85 * night, lights)

OUTPUT_NAME = "day12a_salt_light_matthew5"
