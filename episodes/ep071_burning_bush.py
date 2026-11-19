import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BUSH = 700          # the burning bush
LOOK_X = 330        # where the shepherd first stops and sees it
NEAR_X = 470        # where he stops when he turns aside (P2, P3)
HILL = (0.70, 0.67, 0.62)   # Horeb, the mountain of God

s_look = pose("stand", head=-8, lean=-2, rs=12, re=20)
s_shrug = pose("stand", head=12, lean=4, rs=24, re=8, ls=-10, le=30)        # turns his head away
s_shield = pose("stand", head=6, lean=-6, rs=10, re=20, ls=120, le=40)        # free arm up against the glare
s_here = pose("stand", head=-6, lean=-2, rs=12, re=20, ls=135, le=-10)        # "Here I am": open hand raised
k_down = pose("kneel", lean=10, head=10, rs=12, re=20, ls=30, le=20)
k_unstrap = pose("kneel", lean=46, head=40, rs=8, re=-6, ls=2, le=-4)      # reaching down to his feet
k_hide = pose("kneel", lean=50, head=30, rs=30, re=110, ls=24, le=116)      # hides his face


class BurningBush(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "EXODUS 3  •  THE BURNING BUSH"
    headline = "A bush on fire, yet not burnt.\nWho will turn aside to see?"
    captions = [
        (cpdv("Exodus", 3, 2, "…he saw that the bush was burning and was not burnt."), "Exodus 3:2", 5.0),
        (cpdv("Exodus", 3, 4, "…he said, “Moses, Moses.” And he responded, “Here I am.”"), "Exodus 3:4", 8.6),
        (cpdv("Exodus", 3, 5, "…remove the shoes from your feet. For the place on which you stand is holy ground."), "Exodus 3:5", 11.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        mountain(cr, 760, gy, w=360, h=190, color=HILL)
        for gx in (90, 470, 980):
            grass_tuft(cr, gx, gy, 12)
        fire_amt = prog(t, 1.4, 2.6)
        if i == 2:
            fire_amt *= 1 + 0.35 * prog(t, 10.6, 12.0)
        burning_bush(cr, BUSH, gy, t, fire=fire_amt, s=1.25)
        called = 0.0
        if i >= 1:
            called = prog(t, 7.8, 8.3) * (1 - prog(t, 10.0, 10.8))
        call_rings(cr, BUSH, gy - 80, called, t, t0=7.8, r1=150)

        # ---------------- the shepherd's path ----------------
        keys = [(0.0, -120), (3.0, LOOK_X)]
        if i == 0:
            keys += [(5.0, LOOK_X), (8.2, -140)]
        else:
            keys += [(5.0, LOOK_X), (7.6, NEAR_X)]
        x, wa, d = track(t, keys)
        face = 1
        if i == 0 and t > 4.8:
            face = -1

        # ---------------- the sheep ----------------
        for k, off in enumerate((-95, -170)):
            if i == 0:
                sk = [(0.0, -120 + off), (3.0, LOOK_X + off), (5.3 + 0.2 * k, LOOK_X + off), (8.8 + 0.3 * k, -230)]
            else:
                sk = [(0.0, -120 + off), (3.0, LOOK_X + off), (5.3 + 0.3 * k, LOOK_X + off), (7.4 + 0.3 * k, NEAR_X + off - 170)]
            sx, swa, sd = track(t, sk)
            sface = sd if swa > 0.05 else (-1 if (i == 0 and t > 5) else 1)
            graze = 0.0 if swa > 0.05 else prog(t % 6.0, 0.5, 1.2) * (1 - prog(t % 6.0, 4.0, 4.8))
            sheep(cr, sx, gy, s=0.78, face=sface, step=(t * 7 if swa > 0.05 else 0), graze=graze)

        # ---------------- poses ----------------
        sp = pose("stand")
        staff_down = False
        if t < 3.0:
            sp = pose("stand")
        elif i == 0:
            sp = keyed([(3.0, pose("stand")), (3.6, s_look), (4.4, s_look), (4.9, s_shrug)], t)
        else:
            sp = keyed([(3.0, pose("stand")), (3.6, s_look), (4.6, s_look), (5.0, pose("stand", head=-4))], t)
            if t >= 7.6:
                if i == 1:
                    sp = keyed([(7.6, pose("stand", head=-4)), (8.0, s_shield), (8.5, s_here)], t)
                else:
                    sp = keyed([(7.6, pose("stand", head=-4)), (8.0, s_shield), (8.5, s_here), (9.4, s_here),
                                (9.9, pose("stand", head=14, lean=6)), (10.4, k_down), (10.8, k_unstrap),
                                (11.8, k_unstrap), (12.4, k_down), (13.2, k_hide)], t)
                    staff_down = t > 10.2
        sp = body(t, sp, wa, speed=1.4)
        J = draw_figure(cr, x, gy, sp, s=1.0, face=face, prop="robe")

        # staff: held upright, or laid on the ground once he kneels
        if staff_down:
            cr.set_source_rgb(*INK); cr.set_line_width(5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(x - 200, gy - 3); cr.line_to(x - 105, gy - 3); cr.stroke()
            cr.arc(x - 200, gy - 13, 10, math.pi / 2, 3 * math.pi / 2); cr.stroke()
        else:
            hx, hy = J["rhand"]
            staff(cr, hx + face * 12, hy - 62, gy if hy < gy - 20 else hy + 20)

        # sandals set aside (P3)
        if i == 2 and t > 11.4:
            cr.save(); cr.push_group()
            sandals(cr, x - 72, gy)
            cr.pop_group_to_source(); cr.paint_with_alpha(prog(t, 11.4, 11.8)); cr.restore()


OUTPUT_NAME = "day36a_burning_bush_exodus3"
