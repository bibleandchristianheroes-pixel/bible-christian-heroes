import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BCX = 640            # boat centre
JFEET = 862          # Jesus' feet (stern)

class CalmingStorm(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MARK 4  •  CALMING THE STORM"
    headline = "The boat was filling.\nHe was asleep. Then he stood."
    captions = [
        (cpdv("Mark", 4, 37, "And a great wind storm occurred, and the waves broke over the boat, so that the boat was being filled."), "Mark 4:37", 4.0),
        (cpdv("Mark", 4, 38, "…sleeping on a pillow. And they woke him and said to him, “Teacher, does it not concern you that we are perishing?”"), "Mark 4:38", 7.2),
        (cpdv("Mark", 4, 39, "…“Silence. Be stilled.” And the wind ceased. And a great tranquility occurred."), "Mark 4:39", 11.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        gy = gy - 8
        storm = prog(t, 2.0, 3.6)
        if i == 2: storm *= 1 - prog(t, 10.8, 12.4)
        calm_glow = prog(t, 11.2, 13.0) if i == 2 else 0.0
        warm_glow(cr, 760, y0 + 260, 520, calm_glow)
        rough = 0.5 + 3.0 * storm
        tilt = 5 * storm * math.sin(t * 2.3)
        bob = 2 * math.sin(t * 1.7) + 6 * storm * math.sin(t * 2.9)
        gun = gy - 34 + bob

        cr.save(); cr.translate(BCX, gun); cr.rotate(math.radians(tilt)); cr.translate(-BCX, -gun)
        fy = gun + 18     # feet line (hidden by hull)
        # ---------- disciples ----------
        for k, dx in enumerate((470, 560)):
            p = pose("stand")
            x = dx
            if storm > 0.3:
                if k == 0:
                    p = pose("flail") if t < 5.5 or i == 0 else pose("stand", head=-10, ls=150, le=40, rs=60, re=40)
                else:
                    bail = 0.5 + 0.5 * math.sin(t * 5)
                    p = pose("reach", lean=30 - 20 * bail, head=20 - 30 * bail, rs=20 + 140 * bail, re=10, ls=30, le=20)
            if k == 1 and i >= 1 and t > 5.8:
                x, wa, _ = track(t, [(5.8, 560), (6.6, 610)])
                shake = pose("reach", lean=40 + 6 * math.sin(t * 14), head=30, rs=55, re=-10, ls=45, le=0, lt=-10, rt=-30)
                p = body(t, keyed([(5.8, pose("stand")), (6.6, shake)], t), wa) if t < 6.6 else shake
                if i == 2 and t > 9.4:
                    x, wa, _ = track(t, [(9.4, 610), (10.2, 580)])
                    awe = pose("stand", lean=-8, head=-18, rs=70, re=50, ls=60, le=50)
                    p = keyed([(9.4, shake), (10.2, pose("stand", head=-10)), (11.6, awe)], t)
            if k == 0 and i == 2 and t > 10.2:
                p = keyed([(10.2, p), (11.6, pose("stand", lean=-8, head=-18, rs=70, re=50, ls=60, le=50))], t)
            draw_figure(cr, x, fy, p, s=1.02, face=1)
        # ---------- Jesus ----------
        pebble(cr, JFEET - 176, gun - 12, 19, color=STONE)   # the pillow
        rise = prog(t, 9.4, 10.4) if i == 2 else 0.0
        sleep = pose("stand", ls=4, le=0, rs=6, re=0, head=-4, lt=2, rt=-2, lk=0, rk=0)
        if i == 2 and t > 10.0:
            rebuke = pose("stand", rs=150, re=5, ls=120, le=10, head=-12)
            jp = keyed([(10.0, pose("stand")), (10.6, rebuke), (12.6, rebuke), (13.4, pose("stand", rs=60, re=20, ls=40, le=20))], t)
        else:
            jp = mix(sleep, pose("stand"), rise)
        if rise < 0.999:
            draw_rotated(cr, JFEET, gun - 8 * (1 - rise) + 18 * rise, -90 * (1 - rise), jp, s=1.0, face=-1 if rise > 0.5 else 1, prop="robe")
        else:
            draw_figure(cr, JFEET, fy, jp, s=1.05, face=-1, prop="robe")
        fishing_boat(cr, BCX, gun, w=500, mast=0)
        cr.restore()

        splash(cr, BCX - 250, gun + 4, storm * (1 if i == 0 or t < 9 else 1), t, n=12, spread=90)
        splash(cr, BCX + 260, gun + 4, storm, t + 0.5, n=10, spread=70, seed=7)
        water(cr, gy, t, rough=rough, below=90)
        rain(cr, y0, PANEL_H, t, storm)
        wind(cr, y0 + 40, t, storm)
        darkness(cr, y0, PANEL_H, 0.42 * storm)

OUTPUT_NAME = "day14a_calming_the_storm_mark4"
