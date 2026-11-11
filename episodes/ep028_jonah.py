import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SHORE = 400          # land ends here; sea to the right
CITY_X, CITY_S = 20, 0.7

class Jonah(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Start your day with Ave Missal"
    kicker = "JONAH 1–3  •  RUNNING FROM GOD"
    headline = "He ran the other way.\nGod brought him back."
    captions = [
        (cpdv("Jonah", 1, 3, "And Jonah rose in order to flee from the face of the Lord to Tarshish…"), "Jonah 1:3", 3.6),
        (cpdv("Jonah", 2, 1, "And the Lord prepared a great fish to swallow Jonah."), "Jonah 2:1", 8.2),
        (cpdv("Jonah", 3, 3, "And Jonah rose, and he went to Nineveh in accordance with the word of the Lord."), "Jonah 3:3", 12.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        g = gy - 70                                   # land / sea level
        storm = 0.0 if i == 0 else prog(t, 5.0, 6.0) * (1 - prog(t, 8.0, 9.2))
        rough = 0.5 + 2.6 * storm
        ground_line(cr, g, 0, SHORE + 10)
        city_skyline(cr, CITY_X, g, s=CITY_S)

        # ---------- ship ----------
        if i == 0: sx, _, _ = track(t, [(3.2, 500), (7.0, 860)])
        else: sx, _, _ = track(t, [(3.2, 500), (6.4, 760), (9.4, 1400)])
        bob = 2 * math.sin(t * 1.8) + 7 * storm * math.sin(t * 3.1)
        gun = g - 18 + bob
        boat(cr, sx, gun)

        # ---------- Jonah ----------
        jy, jface, jcol, under, show = g, -1, INK, False, True
        jp = pose("stand")
        if t < 3.2:
            jx, wa, _ = track(t, [(1.3, 300), (3.1, 570)])
            jface = -1 if t < 1.0 else 1
            if t < 1.0: jp = keyed([(0.2, pose("stand")), (0.8, pose("stand", head=20))], t)
            jp = body(t, jp, wa)
            jy = lerp(g, gun, clamp((jx - SHORE + 10) / 30.0))
        else:
            jx, jy, jface = sx + 70, gun, 1
            jp = pose("stand", head=-4)
            if i >= 1 and t > 5.6:
                jp = pose("stand", head=-20, ls=120, le=30, rs=130, re=30)
            if i >= 1 and t > 6.6:
                u = prog(t, 6.6, 7.4)
                x0 = 830
                jx = lerp(x0, 920, u); jy = lerp(gun, g + 55, u) - 70 * math.sin(math.pi * u)
                jp = pose("flail"); jface = 1
                if t > 7.2:
                    under = True; jcol = SOFT
                    jy = g + 50 + 6 * math.sin(t * 3); jx = 920
                if t > 8.15: show = False
        if i == 2 and t > 11.0:
            show = True; under = False; jcol = INK
            if t < 11.6:
                u = prog(t, 11.0, 11.6)
                jx = lerp(450, 370, u); jy = lerp(g + 30, g, u) - 80 * math.sin(math.pi * u)
                jp = pose("flail"); jface = -1
            else:
                jx, wa, _ = track(t, [(12.4, 370), (14.6, 262)])
                jface = -1
                kneel = pose("kneel", lean=40, head=30, rs=60, re=20, ls=50, le=20)
                if t < 12.4:
                    jp = keyed([(11.6, kneel), (12.0, kneel), (12.4, pose("stand"))], t)
                else:
                    jp = keyed([(14.6, pose("stand")), (15.2, pose("stand", rs=160, re=5, head=-12))], t)
                    jp = body(t, jp, wa)
                jy = g
        if show and not under:
            draw_figure(cr, jx, jy, jp, s=0.92, face=jface)
        if i == 2 and t > 15.2:
            hx, hy = jx - 20, g - 168
            cry_lines(cr, hx, hy, face=-1, amount=prog(t, 15.2, 15.5), t=t)

        water(cr, g, t, x0=SHORE - 10, x1=W, rough=rough, below=140)
        if show and under:
            draw_rotated(cr, jx, jy, -100, jp, s=0.85, face=1, color=jcol)

        # ---------- the great fish (under water, drawn faded) ----------
        if i >= 1 and t > 7.0:
            if i == 1 or t < 9.0:
                fx, _, _ = track(t, [(7.0, 300), (8.2, 790), (17.0, 860)])
                fface = 1; fy = g + 68
                mouth = prog(t, 7.4, 7.8) * (1 - prog(t, 8.1, 8.3))
            else:
                fx, _, _ = track(t, [(9.2, 790), (10.8, 520), (12.0, 520), (14.0, 1300)])
                fface = -1 if t < 11.9 else 1
                fy = g + 70 - 30 * prog(t, 10.6, 11.0) * (1 - prog(t, 11.6, 12.2))
                mouth = prog(t, 10.8, 11.0) * (1 - prog(t, 11.3, 11.6))
            great_fish(cr, fx, fy, s=0.68, face=fface, mouth=mouth, tail=t * 5, color=SOFT)
        rain(cr, y0, PANEL_H, t, storm)
        wind(cr, y0 + 30, t, storm)
        darkness(cr, y0, PANEL_H, 0.4 * storm)

OUTPUT_NAME = "day14b_jonah_jonah1"
