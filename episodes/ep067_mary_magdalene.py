import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CAVE = (600, 430, 205, 0.30, 108, 170)   # x, w, h, mouth frac, mouth w, mouth h  -> mouth centre 689
MX = 540                                   # where Mary stands at the tomb
JX = 300                                   # where Jesus stops behind her

weep = pose("head_hands")
gaze = pose("stand", lean=34, head=24, rs=95, re=105, ls=85, le=110)        # bowed, looking into the tomb
turned = pose("stand", head=-4, rs=20, re=40, ls=15, le=40)
plead = pose("reach", rs=78, re=-12, ls=50, le=30, lean=6, head=-6)
hush = pose("stand", head=14, lean=6, rs=50, re=90, ls=40, le=95)          # turns back to the tomb, downcast
kneel_up = pose("kneel", lean=4, head=-14, rs=120, re=-20, ls=110, le=-15)


class MaryMagdalene(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JOHN 20  •  MARY MAGDALENE AT THE TOMB"
    headline = "She thought he was the gardener.\nThen he said her name."
    captions = [
        (cpdv("John", 20, 11, "But Mary was standing outside the tomb, weeping. Then, while she was weeping, she bowed down and gazed into the tomb."), "John 20:11", 3.2),
        (cpdv("John", 20, 15, "…Considering that it was the gardener, she said to him, “Sir, if you have moved him, tell me where you have placed him…”"), "John 20:15", 7.2),
        (cpdv("John", 20, 16, "Jesus said to her, “Mary!” And turning, she said to him, “Rabboni!”"), "John 20:16", 10.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        cx0, cw, ch, mf, mw, mh = CAVE
        if i == 2:
            warm_glow(cr, JX, gy - 110, 260, prog(t, 10.0, 11.2))
        rock_cave(cr, cx0, gy, w=cw, h=ch, mouth=mf, mw=mw, mh=mh)
        round_stone(cr, 960, gy + 2, r=80, rot=0.9)          # already rolled away: the tomb is empty

        # ---------------- Mary ----------------
        x, wa, _ = track(t, [(0.2, -60), (2.4, MX)])
        face = 1
        keys = [(2.4, pose("stand")), (2.9, weep), (3.4, weep), (4.0, gaze)]
        if i == 0:
            keys += [(8.0, gaze), (8.8, weep), (12.0, weep), (13.0, gaze)]
        else:
            keys += [(5.6, gaze), (6.1, turned), (6.6, turned), (7.1, plead), (8.6, plead), (9.1, turned), (9.4, hush)]
            if 6.0 <= t < 9.2:
                face = -1
            if i == 2:
                keys += [(9.9, hush), (10.2, turned)]
                if t >= 10.2:
                    face = -1
                    joyrun = pose("stand", lean=10, head=-10, rs=70, re=-10, ls=60, le=-5)
                    x, wa2, _ = track(t, [(10.2, MX), (11.0, MX), (12.0, JX + 135)])
                    wa = wa2
                    keys += [(10.6, pose("stand", lean=-8, head=-14, rs=60, re=40, ls=50, le=40)), (11.0, joyrun), (12.0, joyrun), (12.5, kneel_up)]
        p = keyed(keys, t) if t >= 2.4 else pose("stand", head=10)
        p = body(t, p, wa, speed=1.3 if t < 3 else 1.8)
        J = draw_figure(cr, x, gy, p, s=0.92, face=face)
        veil_drape(cr, J, s=0.92, face=face)
        tamt = prog(t, 2.6, 3.0)
        if i == 1:
            tamt *= 1 - 0.6 * prog(t, 6.6, 7.2) * (1 - prog(t, 9.0, 9.5))
        if i == 2:
            tamt *= 1 - prog(t, 10.2, 10.6)
        tears(cr, J["head"][0] + face * 12, J["head"][1] + 12, t, tamt, face=face)

        # ---------------- Jesus (risen) ----------------
        if i >= 1:
            jx, jwa, _ = track(t, [(3.6, -70), (6.0, JX)])
            jk = [(6.0, pose("stand")), (6.6, pose("stand", head=4, rs=20, re=30))]
            if i == 2:
                call = pose("stand", rs=72, re=-6, ls=50, le=10, head=-6, lean=-2)
                jk += [(9.6, pose("stand", head=4, rs=20, re=30)), (9.9, call), (12.0, call),
                       (12.8, pose("stand", rs=55, re=-10, ls=10, le=10, head=10, lean=4))]
            JJ = draw_figure(cr, jx, gy, body(t, keyed(jk, t), jwa, speed=1.3), s=1.05, face=1, prop="robe")
            if i == 2:
                cry_lines(cr, JJ["head"][0] + 8, JJ["head"][1], face=1, amount=prog(t, 9.8, 10.0) * (1 - prog(t, 10.9, 11.3)), t=t)


OUTPUT_NAME = "day34a_mary_magdalene_john20"
