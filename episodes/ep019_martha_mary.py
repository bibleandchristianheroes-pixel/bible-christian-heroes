import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX, POT_X, TABLE_X = 200, 900, 640
STIR_X = 830

def busy_track(t_end):
    """Rushing back and forth between the pot and the table until t_end."""
    keys = [(0.0, STIR_X), (3.0, STIR_X)]
    tt, at_pot = 3.0, True
    while tt < t_end - 0.3:
        tt += 0.9; keys.append((tt, TABLE_X + 50 if at_pot else STIR_X)); at_pot = not at_pot
        tt += 0.3; keys.append((tt, keys[-1][1]))
    return keys

class MarthaMary(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 10  •  MARTHA AND MARY"
    headline = "So busy serving him,\nshe missed sitting with him."
    captions = [
        (cpdv("Luke", 10, 40, "Now Martha was continually busying herself with serving."), "Luke 10:40", 6.4),
        (cpdv("Luke", 10, 39, "…Mary, who, while sitting beside the Lord’s feet, was listening to his word."), "Luke 10:39", 5.4),
        (cpdv("Luke", 10, 42, "And yet only one thing is necessary. Mary has chosen the best portion…"), "Luke 10:42", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            warm_glow(cr, 280, gy - 100, 360, prog(t, 12.0, 13.4))
        stool(cr, JX, gy)
        cook_pot(cr, POT_X, gy, t, fire=1.0, steam=1.0)
        top = low_table(cr, TABLE_X, gy)
        nb = 1 + int(clamp((t - 3.0) / 2.4, 0, 3)) if i != 1 else 1
        for k in range(nb):
            bowl(cr, TABLE_X - 30 + k * 22, top - 10, w=20)
        # ---------- Jesus walks in and sits ----------
        jx, jwa, _ = track(t, [(0.0, -70), (2.0, JX)])
        sit = pose("stand", lt=88, lk=88, rt=80, rk=82, rs=25, re=45, ls=20, le=45, head=-4)
        teach = pose("stand", lt=88, lk=88, rt=80, rk=82, rs=70, re=-20, ls=20, le=45, head=-4)
        jp = keyed([(2.0, pose("stand")), (2.6, sit)], t) if t >= 2.0 else body(t, pose("stand"), jwa)
        if t > 2.6:
            g = 0.5 + 0.5 * math.sin(t * 1.8)
            jp = mix(sit, teach, 0.6 * g)
            if i == 2 and 8.4 < t < 10.6:
                jp = keyed([(8.4, jp), (8.9, pose("stand", lt=88, lk=88, rt=80, rk=82, rs=95, re=-5, ls=20, le=45, head=-8)), (10.2, pose("stand", lt=88, lk=88, rt=80, rk=82, rs=95, re=-5, ls=20, le=45, head=-8)), (10.6, jp)], t)
        draw_figure(cr, jx, gy, jp, s=1.05, face=1, prop="robe")

        # ---------- the woman ----------
        stir = lambda tt: pose("stand", rs=65 + 18 * math.sin(tt * 7), re=-10 + 25 * math.cos(tt * 7), lean=6, head=8)
        x, wa, face, p, carry = STIR_X, 0.0, 1, stir(t), False
        sit_feet = pose("kneel", lean=8, head=-30, rs=35, re=55, ls=35, le=55, lt=95, lk=150, rt=85, rk=150)
        if i == 1 and t >= 2.8:
            if t < 3.6:
                p = keyed([(2.8, stir(2.8)), (3.4, pose("stand", head=-6))], t); face = 1 if t < 3.2 else -1
            else:
                x, wa, _ = track(t, [(3.6, STIR_X), (5.4, JX + 125)]); face = -1
                p = body(t, keyed([(5.4, pose("stand")), (6.0, sit_feet)], t), wa)
                if t > 6.0:
                    p["head"] = -22 - 4 * math.sin(t * 1.5)
        elif i != 1 and t >= 3.0:
            stop = 9.0 if i == 0 else 8.6
            keys = busy_track(stop)
            x, wa, d = track(t, keys)
            face = d if wa > 0.05 else (1 if abs(x - STIR_X) < 5 else -1)
            carry = wa > 0.05 and d < 0
            base = pose("carry", rs=55, re=45, lean=10) if carry else pose("stand", lean=10)
            p = body(t, base, wa, speed=2.2)
            if wa <= 0.05:
                p = stir(t) if abs(x - STIR_X) < 5 else pose("reach", rs=70, re=-10, lean=25, head=20)
            if t > keys[-1][0]:
                if i == 0:
                    hips = pose("stand", ls=35, le=-110, rs=35, re=-110, head=-10)
                    brow = pose("stand", rs=150, re=110, ls=35, le=-110, head=14)
                    p = keyed([(keys[-1][0], p), (keys[-1][0] + 0.5, hips), (11.0, hips), (11.6, brow), (13.0, brow), (13.6, pose("sad_sit", head=20)), (17.2, pose("sad_sit", head=20))], t)
                    face = -1
                else:
                    t0 = keys[-1][0]
                    x, wa, _ = track(t, [(t0 + 0.6, x), (11.6, JX + 125)]); face = -1
                    p = keyed([(t0, p), (t0 + 0.5, pose("stand", head=-8))], t)
                    if wa > 0: p = body(t, pose("stand"), wa)
                    if t > 11.6:
                        p = keyed([(11.6, pose("stand")), (12.2, sit_feet)], t)
                        if t > 12.2: p["head"] = -22 - 4 * math.sin(t * 1.5)
        J = draw_figure(cr, x, gy, p, s=0.92, face=face)
        if carry:
            bowl(cr, J["rhand"][0] + face * 8, J["rhand"][1] - 8, w=22)
        if t < 3.0 or (abs(x - STIR_X) < 5 and wa <= 0.05 and not (i == 0 and t > 9.0)):
            hx, hy = J["rhand"]   # spoon in the pot
            cr.set_source_rgb(*INK); cr.set_line_width(4); cr.move_to(hx, hy); cr.line_to(hx + 34, hy + 34); cr.stroke()

OUTPUT_NAME = "day10a_martha_mary_luke10"
