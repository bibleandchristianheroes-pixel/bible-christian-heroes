import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GX, GS = 905, 1.42          # Goliath position / scale
STONES = [150, 172, 194, 214, 232]

class DavidGoliath(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "1 SAMUEL 17  •  DAVID AND GOLIATH"
    headline = "A giant in armor.\nA boy with five stones."
    captions = [
        (cpdv("I Samuel", 17, 40, "…he chose for himself five very smooth stones from the torrent… And he took up a sling in his hand."), "1 Samuel 17:40", 3.4),
        (cpdv("I Samuel", 17, 45, "…But I come to you in the name of the Lord of hosts…"), "1 Samuel 17:45", 6.8),
        (cpdv("I Samuel", 17, 49, "…he cast it with the sling and struck the Philistine on the forehead… And he fell on his face, upon the ground."), "1 Samuel 17:49", 10.5),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        brook(cr, 125, 250, gy)
        for k, sx in enumerate(STONES):
            if t < 1.9 + k * 0.32:
                pebble(cr, sx, gy + 6, 6)

        # ---------- Goliath ----------
        idle = pose("stand", rs=25, re=60, ls=40, le=70, head=4)
        gp = idle
        fall = 0.0
        if i >= 1 and t > 4.8:
            laugh = lambda tt: pose("stand", lean=-9 + 3 * math.sin(tt * 18), head=-32 + 6 * math.sin(tt * 18), rs=25, re=60, ls=60, le=90)
            gp = keyed([(4.8, idle), (5.2, laugh(t))], t) if t < 6.6 else keyed([(6.6, laugh(t)), (7.0, pose("stand", rs=60, re=40, ls=40, le=70, head=-4, lean=4))], t)
        if i == 2 and t > 10.3:
            hit = pose("stand", lean=-10, head=-30, rs=40, re=30, ls=60, le=40)
            gp = keyed([(10.3, gp), (10.6, hit), (11.0, pose("stand", lean=10, head=20, rs=90, re=10, ls=90, le=10))], t)
            fall = prog(t, 10.9, 11.7)
        rot = -85 * fall * fall
        cr.save(); cr.rectangle(0, y0, W, gy + 2 - y0); cr.clip(); cr.translate(GX, gy - 20 * fall); cr.rotate(math.radians(rot))
        GJ = draw_figure(cr, 0, 0, gp, s=GS, face=-1)
        giant_gear(cr, GJ, s=GS, face=-1, shield=fall < 0.45, spear=not (i == 2 and t > 10.6))
        cr.restore()
        if i == 2 and t > 10.6:   # the dropped spear
            cr.set_source_rgb(*INK); cr.set_line_width(6); cr.move_to(GX + 20, gy - 3); cr.line_to(GX + 170, gy - 3); cr.stroke()
            if fall > 0.45:
                cr.save(); cr.rectangle(0, y0, W, gy - y0); cr.clip(); cr.arc(GX - 330, gy + 6, 34, math.pi, 2 * math.pi); cr.fill(); cr.restore()
        a = math.radians(rot)
        hx_, hy_ = GJ["head"]
        head = (GX + hx_ * math.cos(a) - hy_ * math.sin(a), gy - 20 * fall + hx_ * math.sin(a) + hy_ * math.cos(a))

        # ---------- David ----------
        dface, dwa = -1, 0
        if t < 1.4:
            dx, dwa, _ = track(t, [(0.2, 330), (1.3, 262)])
            dp = body(t, pose("stand"), dwa)
        elif t < 3.6:
            dx = 262
            dip = abs(math.sin((t - 1.6) * math.pi / 0.32))
            dp = keyed([(1.3, pose("stand")), (1.7, pose("kneel", lean=40, head=35, rs=30 + 25 * dip, re=0, ls=40, le=20))], t)
            if t > 1.7: dp = pose("kneel", lean=40, head=35, rs=30 + 25 * dip, re=0, ls=40, le=20)
        else:
            dface = 1
            dx = 262
            dp = keyed([(3.6, pose("stand", head=-8)), (4.0, pose("stand", rs=12, re=10))], t)
            if i >= 1 and t > 4.2:
                dx, dwa, _ = track(t, [(4.2, 262), (6.2, 470)])
                lord = pose("stand", ls=165, le=5, head=-20, rs=12, re=10)
                dp = body(t, keyed([(6.2, pose("stand", rs=12, re=10)), (6.8, lord)], t), dwa)
                if t > 8.6 and i == 2:
                    swing = pose("stand", rs=165, re=10, ls=30, le=20, head=-4, lean=3)
                    throw = pose("reach", rs=95, re=0, ls=10, le=10, lean=12, lt=12, rt=-14)
                    dp = keyed([(8.6, lord), (9.1, swing), (10.15, swing), (10.35, throw), (11.8, throw), (12.4, pose("joy"))], t)
        DJ = draw_figure(cr, dx, gy, dp, s=0.8, face=dface, prop="bag")
        hx, hy = DJ["rhand"]
        if t > 3.6:
            if i == 2 and 9.1 < t < 10.25:
                sling(cr, hx, hy, (t - 9.1) * 16 + math.pi, L=38)
            elif not (i == 2 and t >= 10.25):
                sling(cr, hx, hy, 0.15 * math.sin(t * 2), L=38)
            else:
                sling(cr, hx, hy, 0.6, L=38, loaded=False)
        if i == 1 or i == 2:
            light_rays(cr, DJ["lhand"][0], DJ["lhand"][1] - 8, 0.6 * prog(t, 6.8, 7.4) * (1 - prog(t, 8.6, 9.0)) if t < 9.0 or i == 1 else 0, r0=14, r1=34, n=10, t=t)
        # the stone in flight
        if i == 2 and 10.25 < t < 10.6:
            u = prog(t, 10.25, 10.55)
            pebble(cr, lerp(hx, head[0] - 10, u), lerp(hy, head[1], u) - 30 * math.sin(math.pi * u), 6)

OUTPUT_NAME = "day15a_david_and_goliath_1samuel17"
