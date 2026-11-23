import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HILL_X = 610
XL, XJ, XR = 340, 610, 870     # mocking robber, Jesus, the good thief
H_SIDE, H_MID = 205, 218
S = 0.9


class GoodThief(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    caption_bg = True
    kicker = "LUKE 23  •  THE GOOD THIEF"
    headline = "Two men beside Jesus.\nOnly one asked."
    captions = [
        (cpdv("Luke", 23, 39, "“If you are the Christ, save yourself and us.”"), "Luke 23:39", 3.2),
        (cpdv("Luke", 23, 42, "“Lord, remember me when you come into your kingdom.”"), "Luke 23:42", 6.6),
        (cpdv("Luke", 23, 43, "“Amen I say to you, this day you shall be with me in Paradise.”"), "Luke 23:43", 10.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        dark = 0.42 * prog(t, 0.6, 3.0)
        light = 0.0
        if i == 0:
            dark += 0.22 * prog(t, 9.0, 11.5)
        if i == 2:
            light = prog(t, 9.4, 11.0)

        if light > 0:
            warm_glow(cr, (XJ + XR) / 2, gy - 150, 420, 0.9 * light)
        g = calvary_hill(cr, HILL_X, gy)

        # ---------------- the mocking robber (left, facing Jesus) ----------------
        jeer = 0.0; faceL = 1
        keys = [(0.0, dict(head=24, lean=0)), (2.2, dict(head=24, lean=0)), (2.8, dict(head=-26, lean=-4))]
        if i == 0:
            keys += [(5.2, dict(head=-26, lean=-4)), (5.8, dict(head=10, lean=0)), (6.4, dict(head=-28, lean=-5)),
                     (8.0, dict(head=-28, lean=-5)), (8.6, dict(head=0, lean=0))]
        else:
            keys += [(5.0, dict(head=-26, lean=-4)), (5.6, dict(head=16, lean=0))]
        k = keyed(keys, t)
        if 2.8 < t < 5.0 or (i == 0 and 6.4 < t < 8.0):
            k["head"] += 7 * math.sin(t * 11)        # tossing his head as he jeers
            jeer = 1.0
        if i == 0 and t >= 8.9:                    # turns his face away into the dark
            faceL = -1
            k = keyed([(8.9, dict(head=0, lean=0)), (9.6, dict(head=30, lean=6))], t)
        JL = crucified(cr, XL, g(XL), h=H_SIDE, s=S, head=k["head"], lean=k["lean"], face=faceL)
        if jeer:
            a = prog(t, 2.8, 3.1) * (1 - prog(t, 4.7, 5.0)) if t < 5.2 else prog(t, 6.4, 6.7) * (1 - prog(t, 7.7, 8.0))
            cry_lines(cr, JL["head"][0] + 14, JL["head"][1], face=1, amount=a, size=1.1, t=t)

        # ---------------- Jesus (centre, robed, head bowed) ----------------
        jk = dict(head=26, lean=4)
        if i == 2:
            jk = keyed([(0.0, dict(head=26, lean=4)), (9.0, dict(head=26, lean=4)), (9.8, dict(head=-2, lean=0))], t)
        JJ = crucified(cr, XJ, g(XJ), h=H_MID, s=S, head=jk["head"], lean=jk["lean"], face=1, robe=True)

        # ---------------- the good thief (right) ----------------
        faceR = 1; rk = dict(head=24, lean=0)
        if i >= 1:
            if t < 5.5:
                rk = keyed([(0.0, dict(head=24, lean=0)), (3.2, dict(head=24, lean=0)), (3.8, dict(head=4, lean=0)),
                            (5.0, dict(head=4, lean=0)), (5.4, dict(head=0, lean=0))], t)
            else:                                     # turns toward Jesus and asks
                faceR = -1
                rk = keyed([(5.5, dict(head=0, lean=0)), (6.2, dict(head=-12, lean=-2)), (7.8, dict(head=-12, lean=-2)),
                            (8.6, dict(head=8, lean=2))], t)
                if i == 2:
                    rk = keyed([(5.5, dict(head=0, lean=0)), (6.2, dict(head=-12, lean=-2)), (7.8, dict(head=-12, lean=-2)),
                                (8.6, dict(head=8, lean=2)), (9.6, dict(head=8, lean=2)), (10.4, dict(head=-16, lean=-3))], t)
        JR = crucified(cr, XR, g(XR), h=H_SIDE, s=S, head=rk["head"], lean=rk["lean"], face=faceR)
        if i >= 1 and 6.2 < t < 8.0:
            a = prog(t, 6.2, 6.5) * (1 - prog(t, 7.6, 8.0))
            cry_lines(cr, JR["head"][0] - 14, JR["head"][1], face=-1, amount=0.6 * a, size=0.8, t=t * 0.3)

        lights = []
        if light > 0:
            lights = [((XJ + XR) / 2, gy - 140, 460 * light, light)]
        darkness(cr, y0, PANEL_H, dark, lights)
        if light > 0:
            light_rays(cr, JJ["head"][0], JJ["head"][1], 0.8 * light, r0=40, r1=84, n=16, t=t)


OUTPUT_NAME = "day39a_good_thief_luke23"
