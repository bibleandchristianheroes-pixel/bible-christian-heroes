import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GRAY = (0.42, 0.40, 0.38)       # bearers and mourners (behind the story figures)
DEAD = (0.74, 0.71, 0.66)       # the dead youth, before he is raised
JX = 740                        # where Jesus stops (facing left)

lying = dict(BASE, lt=90, lk=0, rt=90, rk=0, lean=-90, head=0, ls=90, le=0, rs=90, re=0)
sit_up = dict(BASE, lt=90, lk=0, rt=88, rk=0, lean=0, head=-6, ls=40, le=30, rs=62, re=-14)
dangle = dict(BASE, lt=90, lk=90, rt=84, rk=84, lean=2, head=-4, ls=30, le=30, rs=40, re=20)
hug = pose("stand", rs=75, re=-70, ls=70, le=-70, lean=6, head=4)

weep = pose("head_hands")
calmed = pose("stand", head=-8, rs=40, re=100, ls=35, le=105)


def walking(t, base, wa, speed=0.9, amp=14):
    """Walk cycle on the legs only; arms and torso keep the base pose."""
    if wa <= 0: return dict(base)
    w = walk(t, speed=speed, amp=amp)
    p = dict(base)
    for k in ("lt", "rt", "lk", "rk"):
        p[k] = lerp(base[k], w[k], wa)
    return p


class WidowOfNain(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "LUKE 7  •  THE WIDOW OF NAIN"
    headline = "A funeral left the city gate.\nIt met the Lord of life."
    captions = [
        (cpdv("Luke", 7, 12, "…a deceased person was being carried out, the only son of his mother, and she was a widow."), "Luke 7:12", 3.0),
        (cpdv("Luke", 7, 13, "And when the Lord had seen her, being moved by mercy over her, he said to her, “Do not weep.”"), "Luke 7:13", 7.6),
        (cpdv("Luke", 7, 15, "And the dead youth sat up and began to speak. And he gave him to his mother."), "Luke 7:15", 10.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            warm_glow(cr, 560, gy - 110, 260, prog(t, 9.4, 10.4) * (1 - 0.5 * prog(t, 11.0, 12.0)))
            warm_glow(cr, 390, gy - 100, 280, prog(t, 13.2, 14.6))
        stone_gate(cr, 40, gy, gap=150, h=196, post=34, color=STONE)

        # ---------------- procession offset ----------------
        if i == 0:
            o, wa, _ = track(t, [(0.3, -260), (14.0, 260)])
        else:
            o, wa, _ = track(t, [(0.3, -260), (7.0, 0)])
        wa = max(wa, 0.0)

        # ---------------- mourners ----------------
        for k, cx in enumerate((160, 235)):
            cp = pose("stand", head=14 + 4 * k, lean=4, rs=20, re=40)
            if i == 2 and t > 12.4:
                cp = keyed([(12.4, cp), (13.2, pose("stand", head=-8, rs=40, re=-10, ls=30, le=-5))], t)
            draw_figure(cr, cx + o, gy, walking(t + 0.4 * k, cp, wa), s=0.93, face=1, color=GRAY)

        # ---------------- bearers + bier ----------------
        XB = 525 + o
        bb = pose("stand", rs=30, re=-8, head=4)
        fb = pose("stand", rs=-30, re=8, head=4)
        JB = draw_figure(cr, XB - 75, gy, walking(t + 0.25, bb, wa), s=0.95, face=1, color=GRAY)
        JF = draw_figure(cr, XB + 75, gy, walking(t, fb, wa), s=0.95, face=1, color=GRAY)
        py = (JB["rhand"][1] + JF["rhand"][1]) / 2 - 6
        bier(cr, XB - 95, XB + 95, py, color=GRAY)

        # ---------------- the son ----------------
        alive = prog(t, 10.0, 11.0) if i == 2 else 0.0
        col = tuple(lerp(DEAD[j], INK[j], alive) for j in range(3))
        yx, yg, yp, yface = XB + 12, py, lying, -1
        if i == 2 and t > 10.0:
            s_ = 0.9
            if t < 11.4:
                yp = keyed([(10.0, lying), (11.0, sit_up)], t)
            elif t < 11.9:
                u = prog(t, 11.4, 11.9)
                yp = keyed([(11.4, sit_up), (11.9, dangle)], t); yg = lerp(py, py + 41 * s_, u)
            elif t < 12.4:
                u = prog(t, 11.9, 12.4)
                yp = keyed([(11.9, dangle), (12.4, pose("stand", head=-4))], t); yg = lerp(py + 41 * s_, gy, u)
            else:
                yg = gy
                yx, ywa, _ = track(t, [(12.4, XB + 12), (13.3, 420)])
                yp = walking(t, keyed([(12.4, pose("stand", head=-4)), (13.1, pose("stand")), (13.6, hug)], t), ywa, speed=1.4, amp=22)
        draw_figure(cr, yx, yg, yp, s=0.9, face=yface, color=col)

        # ---------------- the widow ----------------
        wx = 330 + o
        wk = [(0.0, weep)]
        if i >= 1:
            wk += [(7.6, weep), (8.4, calmed)]
        if i == 2:
            wx, wwa, _ = track(t, [(0.3, 70), (7.0, 330), (12.6, 330), (13.3, 352)])
            wk += [(12.6, calmed), (13.3, pose("stand", head=-4)), (13.6, hug)]
            wa_w = wwa if t > 12.0 else wa
        else:
            wa_w = wa
        wp = walking(t + 0.6, keyed(wk, t), wa_w, amp=12)
        WJ = draw_figure(cr, wx, gy, wp, s=0.92, face=1)
        veil_drape(cr, WJ, s=0.92, face=1)
        tamt = 1.0 if i == 0 else 1 - prog(t, 7.4, 8.0)
        tears(cr, WJ["head"][0] + 12, WJ["head"][1] + 12, t, tamt)

        # ---------------- Jesus ----------------
        if i >= 1:
            jx, jwa, _ = track(t, [(3.0, 1150), (7.0, JX)])
            jk = [(7.0, pose("stand")), (7.4, pose("stand", rs=100, re=-30, head=-4)), (8.6, pose("stand", rs=100, re=-30, head=-4)), (9.0, pose("stand", rs=30, re=20))]
            if i == 2:
                jx, jwa, _ = track(t, [(3.0, 1150), (7.0, JX), (8.8, JX), (9.3, JX - 38)])
                jk += [(9.3, pose("stand", rs=30, re=20)), (9.6, pose("reach", rs=78, re=0, lean=8)), (10.6, pose("reach", rs=78, re=0, lean=8)),
                       (11.0, pose("stand")), (12.4, pose("stand")), (13.0, pose("stand", rs=70, re=-20, head=6))]
            jp = body(t, keyed(jk, t), jwa, speed=1.3)
            draw_figure(cr, jx, gy, jp, s=1.05, face=-1, prop="robe")


OUTPUT_NAME = "day33b_widow_of_nain_luke7"
