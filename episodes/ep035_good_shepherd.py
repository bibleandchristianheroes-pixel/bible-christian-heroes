import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

FLOCK = [470, 565, 660, 750]

class GoodShepherd(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JOHN 10  •  THE GOOD SHEPHERD"
    headline = "The wolf came.\nOne ran. One stood."
    captions = [
        (cpdv("John", 10, 12, "…he sees the wolf approaching, and he departs from the sheep and flees. And the wolf ravages and scatters the sheep."), "John 10:12", 6.4),
        (cpdv("John", 10, 11, "I am the good Shepherd. The good Shepherd gives his life for his sheep."), "John 10:11", 6.6),
        (cpdv("John", 10, 14, "I am the good Shepherd, and I know my own, and my own know me…"), "John 10:14", 10.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            warm_glow(cr, 720, gy - 90, 420, prog(t, 11.0, 12.6))
        # ---------- wolf ----------
        if i == 0:
            wx, wwa, wd = track(t, [(2.4, 1180), (4.4, 960), (6.0, 960), (7.4, 520), (8.6, 330)])
        else:
            wx, wwa, wd = track(t, [(2.4, 1180), (4.4, 1020), (6.4, 1020), (6.7, 1000), (7.3, 1000), (7.7, 1050), (8.0, 1040), (9.0, 1260)])
        wface = -1
        crouch = prog(t, 4.4, 4.9)
        if i == 0 and t > 6.0: crouch = 1 - prog(t, 6.0, 6.3) + prog(t, 8.6, 9.2) * 0.6
        if i >= 1:
            crouch = crouch * (1 - prog(t, 7.3, 7.7) * 0.4)
            if t > 7.8: wface = 1; crouch = 0.0
        wstep = t * (12 if wwa > 0.6 else 8) if wwa > 0.05 else 0.0
        wolf(cr, wx, gy, s=0.95, face=wface, step=wstep, crouch=crouch)

        # ---------- sheep ----------
        for k, fx in enumerate(FLOCK):
            graze = max(0.0, 0.5 + 0.5 * math.sin(t * 1.2 + k * 1.9)) * (1 - prog(t, 4.0, 4.4))
            face, x, step = (1 if k % 2 else -1), fx, 0.0
            if t > 4.4: face = 1
            if i == 0 and t > 6.2:
                t0 = 6.2 + (3 - k) * 0.25
                x, wa, _ = track(t, [(t0, fx), (t0 + 1.6 + k * 0.2, -120 - k * 40)])
                face = -1; step = t * 14 if wa > 0.05 else 0.0
            elif i >= 1 and t > 5.2:
                tx = [470, 535, 600, 665][k]
                x, wa, _ = track(t, [(5.2, fx), (6.2, tx)])
                face = 1 if t < 5.2 or wa < 0.05 else -1
                if i == 2 and t > 9.6:
                    gx = [545, 615, 685, 750][k]
                    x, wa, _ = track(t, [(9.6 + k * 0.2, tx), (10.8 + k * 0.2, gx)])
                    face = 1
                    graze = 0.0
                step = t * 10 if wa > 0.05 else 0.0
            if i == 2 and k == 3 and t > 11.8:
                self.lamb = (x, prog(t, 11.8, 12.6)); continue
            sheep(cr, x, gy, s=0.9 if k != 3 else 0.7, face=face, graze=graze if step == 0 else 0.0, step=step)

        # ---------- the man with the staff ----------
        look = keyed([(3.6, pose("stand")), (4.2, pose("stand", head=-10))], t)
        if i == 0:
            x, wa, d = track(t, [(4.8, 330), (6.2, -120)])
            if t < 4.8:
                p = look; face = 1
                J = draw_figure(cr, x, gy, p, s=1.05, face=face)
                hx, hy = J["lhand"]; staff(cr, hx, hy - 70, gy)
            else:
                p = mix(pose("stand"), run(t), clamp((t - 4.8) / 0.3)); face = -1
                draw_figure(cr, x, gy, p, s=1.05, face=face)
                fl = prog(t, 4.8, 5.2)                       # the dropped staff
                cr.save(); cr.translate(300, gy); cr.rotate(math.radians(-88 * fl)); staff(cr, 0, -150, 0); cr.restore()
            return
        x, wa, d = track(t, [(4.4, 330), (5.6, 830)])
        guard = pose("stand", ls=60, le=-5, rs=-55, re=20, lean=8, lt=12, rt=-18, head=-4)
        p = body(t, look, wa)
        face = 1
        if t >= 5.6:
            p = keyed([(5.6, pose("stand")), (6.0, guard)], t)
            if i == 2 and t >= 9.2:
                kneel = pose("stand", lean=45, head=25, rs=70, re=10, ls=60, le=10, lt=25, lk=35, rt=5, rk=35)
                x, wa, d = track(t, [(9.2, 830), (9.8, 810)])
                face = -1
                p = keyed([(9.2, pose("stand")), (9.8, pose("stand")), (10.4, kneel)], t)
                p = body(t, p, wa)
                if t > 11.8:
                    hold = pose("stand", rs=95, re=-15, ls=88, le=-12, head=-6)
                    p = keyed([(11.8, kneel), (12.6, hold)], t)
            elif i == 1 and t >= 9.2:
                p = keyed([(9.2, guard), (9.8, pose("stand", ls=60, le=-5, rs=-30, re=10, head=-4))], t)
        J = draw_figure(cr, x, gy, p, s=1.08, face=face, prop="robe")
        if i == 2 and t > 11.8:
            lx, u = self.lamb
            shx, shy = J["sh"]
            hx_, hy_ = J["rhand"]
            sheep(cr, lerp(lx, hx_ - 4, u), lerp(gy, hy_ + 4, u) - 20 * math.sin(math.pi * u), s=0.7, face=1)
        hx, hy = J["lhand"]
        if i == 2 and t >= 9.8:
            staff(cr, 900, gy - 150, gy)     # leaned / planted behind him
        else:
            top = hy - 95 if t > 5.6 else hy - 70
            staff(cr, hx, top, min(gy, hy + 120) if t > 5.6 else gy)

OUTPUT_NAME = "day18a_good_shepherd_john10"
