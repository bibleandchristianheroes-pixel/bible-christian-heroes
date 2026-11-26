import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX = 840            # Jesus, facing left
DX = 520            # the disciple, sitting and listening
KX = 752            # where Peter kneels

j_stand = pose("stand", head=0, rs=10, re=12)
j_lift = pose("stand", rs=150, re=10, head=-8)                    # lifts up the bread
j_offer = pose("reach", rs=78, re=-6, lean=6, head=4)              # holds it out
j_call = pose("reach", rs=88, re=-2, lean=12, head=0, ls=40, le=10) # reaches after him
j_sad = pose("stand", head=30, lean=6, rs=60, re=-10)
j_give = pose("reach", rs=60, re=-4, lean=14, head=18)              # gives the bread to the kneeling man
j_bless = pose("stand", rs=70, re=16, ls=8, le=12, head=20, lean=10) # hand on his head

d_listen = ground_sit_pose(head=-8, rs=30, re=50, ls=24, le=50)
d_lean = ground_sit_pose(head=-12, lean=4, rs=40, re=40, ls=30, le=40)
d_doubt = ground_sit_pose(head=16, lean=-8, rs=30, re=50, ls=24, le=50)
d_up = pose("stand", head=4)
d_walk = pose("stand", head=10, lean=6)
d_look = pose("stand", head=-6)
d_kneel = pose("kneel", rs=60, re=-60, ls=52, le=-62, head=14, lean=10)        # bread held to the chest
d_kneel_up = pose("kneel", rs=60, re=-60, ls=52, le=-62, head=-14, lean=4)


class BreadOfLife(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "JOHN 6  •  THE BREAD OF LIFE"
    headline = "Many walked away from him.\nOne answered: to whom would we go?"
    captions = [
        (cpdv("John", 6, 67, "After this, many of his disciples went back, and they no longer walked with him."), "John 6:67", 6.2),
        (cpdv("John", 6, 68, "Therefore, Jesus said to the twelve, “Do you also want to go away?”"), "John 6:68", 7.6),
        (cpdv("John", 6, 69, "Then Simon Peter answered him: “Lord, to whom would we go? You have the words of eternal life."), "John 6:69", 9.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        glow = prog(t, 9.0, 10.6) if i == 2 else 0.0
        warm_glow(cr, (JX + KX) / 2, gy - 120, 380, 0.85 * glow)
        olive_tree(cr, 1010, gy, h=130)
        for gx in (160, 330, 600, 930):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))

        # ---------------- Jesus ----------------
        jkeys = [(0.0, j_stand), (0.8, j_stand), (1.4, j_lift), (3.4, j_lift), (4.0, j_offer)]
        if i == 0:
            jkeys += [(6.4, j_offer), (7.4, j_sad)]
        elif i == 1:
            jkeys += [(6.6, j_offer), (7.1, j_call), (10.4, j_call), (11.6, j_sad)]
        else:
            jkeys += [(7.0, j_offer), (7.6, j_give), (8.4, j_give), (9.0, j_stand), (9.6, j_bless)]
        jp = keyed(jkeys, t)
        JJ = draw_figure(cr, JX, gy, jp, s=1.05, face=-1, prop="robe")
        if i == 2 and t > 9.6:
            light_rays(cr, JJ["head"][0], JJ["head"][1], 0.6 * prog(t, 9.6, 10.6), r0=22, r1=50, n=12, t=t)

        # ---------------- the disciple ----------------
        dkeys = [(0.0, d_listen), (1.4, d_listen), (2.0, d_lean), (4.2, d_lean)]
        dx, dface = DX, 1
        bread = "jesus"
        if i == 0:
            dp = keyed(dkeys + [(4.8, d_doubt), (5.4, d_doubt), (6.0, d_up)], t)
            if 4.8 < t < 5.6:
                dp["head"] += 10 * math.sin(t * 14)                          # shakes his head
            if t > 6.0:
                dx, dwa, _ = track(t, [(6.2, DX), (10.0, -90)])
                dface = -1
                dp = body(t, d_walk, dwa, speed=1.5)
        elif i == 1:
            dp = keyed(dkeys + [(4.8, d_doubt), (5.4, d_doubt), (6.0, d_up)], t)
            if 4.8 < t < 5.6:
                dp["head"] += 10 * math.sin(t * 14)
            if t > 6.0:
                dx, dwa, _ = track(t, [(6.2, DX), (7.4, 380), (9.8, 380), (13.2, -90)])
                dface = -1 if (t < 7.8 or t > 9.5) else 1                      # stops and looks back
                dp = body(t, d_walk if dface < 0 else d_look, dwa, speed=1.5)
        else:
            dp = keyed(dkeys + [(4.8, d_lean), (5.4, d_lean), (6.0, d_up)], t)
            if t > 6.0:
                dx, dwa, _ = track(t, [(6.2, DX), (7.2, KX)])
                dp = body(t, pose("stand", head=-6), dwa, speed=1.5)
                if t > 7.2:
                    dp = keyed([(7.2, pose("stand", head=-6)), (7.7, pose("kneel", rs=72, re=-10, ls=64, le=-12, head=-10, lean=8)),
                                (8.4, pose("kneel", rs=72, re=-10, ls=64, le=-12, head=-10, lean=8)), (8.9, d_kneel),
                                (9.6, d_kneel_up)], t)
            if t > 8.4:
                bread = "peter"
        DJ = None
        if dx > -80:
            DJ = draw_figure(cr, dx, gy, dp, s=0.95, face=dface)

        # ---------------- the bread ----------------
        if bread == "jesus":
            hx, hy = JJ["rhand"]
            loaf(cr, hx - 6, hy - 6)
        elif DJ is not None:
            hx = (DJ["rhand"][0] + DJ["lhand"][0]) / 2; hy = (DJ["rhand"][1] + DJ["lhand"][1]) / 2
            loaf(cr, hx + 4, hy - 4)


OUTPUT_NAME = "day42b_bread_of_life_john6"
