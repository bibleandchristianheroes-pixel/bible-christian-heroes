import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

RX = 300            # the reader's stool
UX = RX + 70        # where he stands once he gets up
NX = 830            # the neighbour, sitting by the road with his load
BX = NX + 46        # his load, on the ground beside him
KX = NX - 150       # where the helper kneels (panel 3)
LIFT_X = NX + 80    # where the helper picks up the load (panel 3)
OFF = 1200

read = sit_pose(lean=12, head=26, rs=64, re=46, ls=56, le=52)         # scroll held open in both hands
roll = sit_pose(lean=8, head=18, rs=52, re=62, ls=46, le=66)
r_stand = pose("stand", rs=30, re=50, head=2)                          # scroll tucked in his hand
r_set = pose("reach", rs=60, re=10, head=24, lean=22)                  # sets the scroll on the stool
r_mirror = pose("stand", rs=40, re=100, ls=150, le=60, head=-6, lean=-4)   # mirror up, other hand at his hair
r_admire = pose("stand", rs=46, re=96, ls=10, le=20, head=-10, lean=-6)
r_look = pose("stand", head=-6)
r_kneel = pose("kneel", rs=80, re=-6, head=6, lean=10)                 # hand held out
r_pull = pose("stand", rs=70, re=-4, head=4, lean=-4)
r_bend = pose("stand", lean=40, head=20, rs=100, re=6, ls=96, le=6)
r_carry = pose("stand", lean=16, head=4, rs=-20, re=110, ls=-16, le=115)

n_sad = ground_sit_pose(lean=16, head=30, rs=40, re=50, ls=30, le=50)
n_try = ground_sit_pose(lean=30, head=14, rs=-40, re=10, ls=-30, le=10)   # pushes off the ground ... and can't
n_ask = ground_sit_pose(lean=6, head=-12, rs=84, re=-14, ls=30, le=50)    # reaches up to a passer-by
n_take = ground_sit_pose(lean=10, head=-4, rs=86, re=-6, ls=30, le=50)
n_up = pose("stand", rs=74, re=-6, head=0)
n_free = pose("stand", head=-8, rs=20, re=20)


class DoersOfTheWord(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "JAMES 1  •  DOERS OF THE WORD"
    headline = "Three people read the same Word.\nOnly one did it."
    captions = [
        (cpdv("James", 1, 22, "So be doers of the Word, and not listeners only, deceiving yourselves."), "James 1:22", 7.6),
        (cpdv("James", 1, 24, "…after considering himself, he went away and promptly forgot what he had seen."), "James 1:24", 9.4),
        (cpdv("James", 1, 25, "…not a forgetful hearer, but instead a doer of the work. He shall be blessed in what he does."), "James 1:25", 9.4),
    ]

    def neighbour(self, cr, i, t, gy, pass_t):
        """The man by the road. pass_t = when someone walks past him (None in panel 3)."""
        keys = [(0.0, n_sad), (2.2, n_sad), (2.7, n_try), (3.3, n_try), (3.8, n_sad)]
        if pass_t is not None:
            keys += [(pass_t - 0.9, n_sad), (pass_t - 0.5, n_ask), (pass_t + 0.6, n_ask), (pass_t + 1.3, n_sad)]
            p = keyed(keys, t)
            return draw_figure(cr, NX, gy, p, s=0.95, face=-1), "ground"
        keys += [(7.0, n_sad), (7.4, ground_sit_pose(lean=6, head=-12, rs=30, re=50, ls=30, le=50)),
                 (7.9, n_take), (8.4, n_take)]
        x = NX; face = -1
        if t < 8.4:
            return draw_figure(cr, x, gy, keyed(keys, t), s=0.95, face=-1), "ground"
        if t < 9.4:
            u = prog(t, 8.4, 9.4)
            p = mix(n_take, n_up, u)
            return draw_figure(cr, x, gy, p, s=0.95, face=-1), "rising"
        p = keyed([(9.4, n_up), (9.9, n_free)], t)
        x, wa, _ = track(t, [(11.3, NX), (14.0, 500)])
        return draw_figure(cr, x, gy, body(t, p, wa, speed=1.3), s=0.95, face=face), "up"

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 990, gy - 300, r=22, rays=10)
        olive_tree(cr, 120, gy, h=130)
        for gx in (200, 470, 590, 1010):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        help_glow = prog(t, 13.4, 14.6) if i == 2 else 0.0
        warm_glow(cr, 600, gy - 110, 380, 0.8 * help_glow)
        stool(cr, RX, gy, h=44, w=56)

        # ---------------- the reader ----------------
        rx, rface, rwa = RX, 1, 0.0
        rp = keyed([(0.0, read), (4.2, read), (4.8, roll)], t)
        rp["head"] += 3 * math.sin(t * 1.4)
        scroll_open = 1 - prog(t, 4.2, 4.8)
        scroll_at = "hands"
        sitting = t < 5.0
        mirror = None
        pass_t = None
        if t >= 5.0:
            rx, rwa, _ = track(t, [(5.0, RX), (5.6, UX)])        # steps off the stool
        if i == 0:
            pass_t = 7.4
            if t >= 5.0:
                rp = keyed([(5.0, roll), (5.5, r_stand)], t)
                rx, rwa, _ = track(t, [(5.6, UX), (9.8, OFF)])
                rp = body(t, rp, rwa)
                scroll_at = "hand"
        elif i == 1:
            pass_t = 10.6
            scroll_open = 1 - prog(t, 4.4, 5.0)
            if t >= 5.0:
                rp = keyed([(5.0, roll), (5.5, r_stand), (5.8, r_set), (6.2, r_set), (6.6, r_look),
                            (7.0, r_mirror), (8.2, r_mirror), (8.5, r_admire), (9.3, r_admire), (9.7, r_look)], t)
                if 5.7 < t < 6.5:
                    rface = -1                                   # turns back to lay it on the stool
                if 7.0 < t < 9.3:
                    rp["head"] += 5 * math.sin(t * 3)               # turning his face this way and that
                scroll_at = "hand" if t < 6.0 else "stool"
                if 6.8 < t < 9.6:
                    mirror = prog(t, 6.8, 7.1) * (1 - prog(t, 9.3, 9.6))
                rx, rwa, _ = track(t, [(9.8, UX), (13.4, OFF)])
                rp = body(t, rp, rwa)
        else:
            if t >= 5.0:
                rp = keyed([(5.0, roll), (5.5, r_stand), (5.8, r_set), (6.1, r_set), (6.4, r_look)], t)
                scroll_at = "hand" if t < 5.95 else "stool"
                if 5.7 < t < 6.3:
                    rface = -1
                if t >= 6.4:
                    rx, rwa, _ = track(t, [(6.4, UX), (7.6, KX)])
                    rp = body(t, keyed([(6.4, r_look), (7.6, r_look), (8.0, r_kneel), (8.5, r_kneel), (9.4, r_pull),
                                        (9.6, pose("stand"))], t), rwa)
                if t >= 9.6:
                    rx, rwa, _ = track(t, [(9.6, KX), (10.4, LIFT_X)])
                    rp = body(t, pose("stand"), rwa)
                    if t >= 10.4:
                        rface = -1
                        rp = keyed([(10.4, pose("stand")), (10.8, r_bend), (11.1, r_bend), (11.5, r_carry)], t)
                    if t >= 11.5:
                        rx, rwa, _ = track(t, [(11.5, LIFT_X), (14.0, 640)])
                        rp = body(t, r_carry, rwa, speed=1.3)
                        for k_ in ("lean", "rs", "re", "ls", "le"): rp[k_] = r_carry[k_]

        # the neighbour and his load (drawn behind the passer-by)
        NJ, nstate = self.neighbour(cr, i, t, gy, pass_t)
        load_on_ground = not (i == 2 and t > 10.9)
        if load_on_ground:
            burden(cr, BX, gy - 46, w=54, h=46)

        if sitting:
            RJ = draw_figure(cr, rx, gy, rp, s=1.0, face=rface)
        else:
            RJ = draw_figure(cr, rx, gy, rp, s=1.0, face=rface)

        # the load on the helper's back
        if i == 2 and t > 10.9:
            sx, sy = RJ["sh"]
            u = prog(t, 10.9, 11.5)
            bx = lerp(BX, sx + 4, u); by = lerp(gy - 46, sy - 18, u)
            burden(cr, bx, by, w=54, h=46)

        # ---------------- the scroll ----------------
        if scroll_at == "hands":
            hx = (RJ["rhand"][0] + RJ["lhand"][0]) / 2; hy = min(RJ["rhand"][1], RJ["lhand"][1])
            reading_scroll(cr, hx + 6, hy - 14, w=70, h=40, open_=scroll_open)
        elif scroll_at == "hand":
            hx, hy = RJ["rhand"]
            reading_scroll(cr, hx + 2, hy - 4, w=70, h=34, open_=0.0, ang=0.3)
        else:
            reading_scroll(cr, RX, gy - 44 - 16, w=70, h=26, open_=0.0, ang=math.pi / 2)

        # ---------------- the mirror ----------------
        if mirror:
            hx, hy = RJ["rhand"]
            hand_mirror(cr, hx, hy, ang=-0.25, s=0.95 * mirror,
                        flash=0.9 * max(0.0, math.sin(t * 2.2)) * mirror)


OUTPUT_NAME = "day40b_doers_of_the_word_james1"
