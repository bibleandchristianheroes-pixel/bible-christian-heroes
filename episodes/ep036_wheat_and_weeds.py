import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

WHEAT = [360 + 70 * k for k in range(8)]
WEEDS = [395 + 140 * j for j in range(4)]
BARN = 975
FIRE = 200
HOME = 170           # where the farmer sleeps

class WheatAndWeeds(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Start your day with Ave Missal"
    kicker = "MATTHEW 13  •  THE WHEAT AND THE WEEDS"
    headline = "An enemy sowed weeds by night.\nThe Lord waited for the harvest."
    captions = [
        (cpdv("Matthew", 13, 25, "But while the men were sleeping, his enemy came and sowed weeds amid the wheat, and then went away."), "Matthew 13:25", 4.6),
        (cpdv("Matthew", 13, 29, "…No, lest perhaps in gathering the weeds, you might also root out the wheat together with it."), "Matthew 13:29", 11.0),
        (cpdv("Matthew", 13, 30, "…Gather first the weeds, and bind them into bundles to burn, but the wheat gather into my storehouse."), "Matthew 13:30", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        night = prog(t, 2.4, 3.4) * (1 - prog(t, 6.6, 7.6))
        grow = prog(t, 7.6, 10.0)
        if i == 0: grow = prog(t, 7.6, 11.0)
        sway = math.sin(t * 1.4) * 0.5
        door = prog(t, 12.4, 13.0) if i == 2 else 0.0
        if i == 2:
            warm_glow(cr, BARN, gy - 40, 300, door)
        barn(cr, BARN, gy, w=150, h=100)
        if door > 0:
            cr.set_source_rgba(1, 0.86, 0.48, door); cr.rectangle(BARN - 31, gy - 61, 62, 61); cr.fill()

        # ---------- reaper path (panel 3) ----------
        rx = None
        if i == 2:
            rx, rwa, _ = track(t, [(9.9, HOME), (11.6, 850)])

        # ---------- wheat ----------
        for k, x in enumerate(WHEAT):
            cut_t = None
            if rx is not None and t > 9.9:
                cut_t = 9.9 + (x - HOME) / (900 - HOME) * 1.7
            if cut_t is not None and t >= cut_t:
                u = prog(t, 12.2 + k * 0.08, 13.0 + k * 0.08)
                if u >= 1: continue
                sx = lerp(x, BARN, u); sy = gy - 140 * math.sin(math.pi * u) * (0.4 + 0.1 * (k % 3))
                cr.save(); cr.translate(sx, sy); sc = 0.9 * (1 - 0.6 * u); cr.scale(sc, sc)
                sheaf(cr, 0, 0); cr.restore()
                continue
            h0 = 12 + 14 * prog(t, 0.3, 2.4)
            h = lerp(h0, 150, grow)
            if h < 40:
                sprout(cr, x, gy, h)
            else:
                wheat(cr, x, gy, h, sway=sway, grain=prog(t, 9.0, 10.5) if i else prog(t, 9.6, 11.0))

        # ---------- weeds ----------
        bundle = 0
        for j, x in enumerate(WEEDS):
            h = lerp(0, 22, prog(t, 4.6 + j * 0.3, 5.6 + j * 0.3))
            h = lerp(h, 140, grow)
            pulled = None
            if rx is not None:
                pt = 9.9 + (x - HOME) / (900 - HOME) * 1.7
                if t >= pt:
                    u = prog(t, pt, pt + 0.7)
                    if u >= 1:
                        bundle += 1; continue
                    wx = lerp(x, FIRE, u); wy = gy - 160 * math.sin(math.pi * u)
                    cr.save(); cr.translate(wx, wy); cr.rotate(-1.2 * u); tare(cr, 0, 0, 90); cr.restore()
                    continue
            if i == 1 and j == 1 and 10.7 < t < 11.4:   # servant tugs at it
                tare(cr, x + 3 * math.sin(t * 40), gy, h, sway=sway); continue
            tare(cr, x, gy, h, sway=sway)
        if i == 2 and bundle > 0:
            fs = prog(t, 11.9, 12.6)
            sheaf(cr, FIRE, gy, s=0.6 + 0.12 * bundle, weed=True)
            fire(cr, FIRE, gy, fs, t)

        # ---------- the enemy (all panels, at night) ----------
        if 3.4 < t < 6.8:
            ex, ewa, _ = track(t, [(3.4, -60), (6.6, 1150)])
            throw = 0.5 + 0.5 * math.sin(t * 6)
            p = mix(pose("sow_back", lean=18, head=10), pose("sow_fwd", lean=22, head=12), throw)
            J = draw_figure(cr, ex, gy, body(t, p, ewa * 0.8), s=0.98, prop="bag")
            if 360 < ex < 900:
                for k in range(4):
                    u = ((t * 1.7) + k / 4) % 1
                    seed_dot(cr, J["rhand"][0] + 30 * u, J["rhand"][1] + (gy - J["rhand"][1]) * u ** 1.5, r=3)

        # ---------- the farmer / master ----------
        rise = prog(t, 7.4, 8.1) if t > 5 else 1 - prog(t, 2.4, 3.1)
        if rx is not None and t > 9.9:
            reap = pose("stand", lean=30, head=20, rs=60, re=20, ls=40, le=20)
            p = body(t, reap, rwa)
            if t > 11.6:
                p = keyed([(11.6, reap), (12.2, pose("stand", head=-6)), (13.2, pose("joy"))], t)
            draw_figure(cr, rx, gy, p, s=1.05, prop="robe")
        elif rise < 1:
            draw_rotated(cr, HOME + 40, gy - 4, -88 * (1 - rise), pose("stand", ls=2, le=2, rs=4, re=4, lt=2, lk=0, rt=-2, rk=0), s=1.05, prop="robe")
        else:
            p = pose("stand", head=-6)
            if i == 0:
                p = keyed([(8.1, pose("stand")), (10.2, pose("stand", head=-6)), (10.6, pose("stand", head=14, lean=4))], t)
                if 10.6 < t < 11.6: p["head"] = 14 + 9 * math.sin((t - 10.6) * 16)
            elif i == 1:
                stop = pose("stand", rs=95, re=-35, head=-6)
                p = keyed([(10.4, pose("stand", head=-6)), (10.8, stop), (12.4, stop), (12.8, pose("stand", head=-6))], t)
            draw_figure(cr, HOME + 40, gy, p, s=1.05, prop="robe")

        # ---------- servant (panel 2) ----------
        if i == 1 and t > 9.6:
            sx, swa, _ = track(t, [(9.6, -60), (10.5, WEEDS[1] - 45), (11.5, WEEDS[1] - 45), (12.0, WEEDS[1] - 95)])
            bend = pose("stand", lean=50, head=30, rs=60, re=0, ls=50, le=10, lt=20, lk=30, rt=0, rk=30)
            p = body(t, pose("stand"), swa)
            face = 1
            if t >= 10.5:
                p = keyed([(10.5, pose("stand")), (10.8, bend), (11.3, bend), (11.6, pose("stand", head=-8))], t)
                if t > 11.5: face = -1 if t < 12.0 else 1
                p = body(t, p, swa)
                if t >= 12.0: face = -1; p = pose("stand", head=0)
            draw_figure(cr, sx, gy, p, s=0.98, face=face)

        darkness(cr, y0, PANEL_H, 0.72 * night)
        crescent_moon(cr, 960, y0 + 120, 24, alpha=night)

OUTPUT_NAME = "day18b_wheat_and_weeds_matthew13"
