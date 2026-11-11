import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BX = 170                                   # where Bartimaeus sits
OFFS = [0, 110, 240, 330]                  # disciple A, Jesus, disciple B, disciple C

class Bartimaeus(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MARK 10  •  BLIND BARTIMAEUS"
    headline = "They told him to be quiet.\nHe only cried louder."
    captions = [
        (cpdv("Mark", 10, 47, "…he began to cry out and to say, “Jesus, Son of David, take pity on me.”"), "Mark 10:47", 3.6),
        (cpdv("Mark", 10, 48, "And many admonished him to be quiet. But he cried out all the more…"), "Mark 10:48", 7.0),
        (cpdv("Mark", 10, 52, "…“Go, your faith has made you whole.” And immediately he saw, and he followed him on the way."), "Mark 10:52", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        rock_path_tufts(cr, gy, [70, 330, 1010])
        # ---------- the procession ----------
        J = None
        for k, off in enumerate(OFFS):
            keys = [(0.5, 1150 + off), (8.0, 560 + off)]
            if i == 2 and k == 0: keys += [(9.0, 560), (10.0, 760)]
            if i == 2 and k == 1: keys += [(13.2, 670), (15.4, 400)]
            x, wa, d = track(t, keys)
            face = -1
            p = pose("stand")
            if k == 0 and i >= 1 and t > 6.0:
                hush = pose("stand", rs=150, re=150, ls=55, le=0, head=8, lean=4)
                p = keyed([(6.0, pose("stand")), (6.5, hush), (8.6, hush), (9.0, pose("stand"))], t)
                if i == 2 and 9.0 < t < 10.0: face = 1
            if k == 2 and i >= 1 and t > 6.4:
                down = pose("reach", rs=65, re=0, ls=10, le=10, lean=4)
                p = keyed([(6.4, pose("stand")), (6.9, down), (8.6, down), (9.0, pose("stand"))], t)
            if k == 1 and i == 2 and t > 8.6:
                call = pose("reach", rs=80, re=10, ls=10, le=10)
                touch = pose("reach", rs=105, re=-10, ls=10, le=10, lean=4)
                p = keyed([(8.6, pose("stand")), (9.1, call), (10.6, call), (11.0, pose("stand")), (11.3, touch), (12.2, touch), (12.7, pose("stand"))], t)
            if k == 1 and i == 1 and t > 7.6:
                p = keyed([(7.6, pose("stand")), (8.4, pose("stand", head=-6))], t)
            out = draw_figure(cr, x, gy, body(t, p, wa, speed=1.3), s=1.05 if k == 1 else 0.98, face=face,
                              prop="robe" if k == 1 else None)
            if k == 1: J = out

        # ---------- Bartimaeus ----------
        sit = pose("sad_sit", head=12, lean=14, rs=70, re=10, ls=50, le=-10)
        listen = pose("sad_sit", head=-12, lean=8, rs=70, re=10, ls=50, le=-10)
        cry = pose("sad_sit", lean=-6, head=-22, rs=150, re=15, ls=140, le=15)
        loud = pose("kneel", lean=-6, head=-28, rs=168, re=4, ls=158, le=4, lt=95, lk=95)
        bx, bwa, face = BX, 0, 1
        cane_on = True; cry_amt, cry_size = 0.0, 1.0
        p = keyed([(2.4, sit), (2.9, listen), (3.5, cry)], t)
        cry_amt = prog(t, 3.5, 3.8)
        if i >= 1 and t > 6.0:
            p = keyed([(6.0, cry), (6.5, listen), (6.9, loud)], t)
            cry_amt = prog(t, 6.9, 7.2) + (1 - prog(t, 6.0, 6.3)) * (1 - prog(t, 6.9, 7.0))
            cry_size = lerp(1.0, 1.6, prog(t, 6.9, 7.2))
        if i == 2 and t > 9.4:
            cry_amt *= 1 - prog(t, 9.4, 9.7)
            feel = pose("stand", rs=75, re=0, ls=60, le=10, head=10)
            see = pose("stand", head=-25, lean=-4, rs=150, re=20, ls=140, le=20)
            if t < 11.6:
                p = keyed([(9.4, loud), (9.9, pose("joy")), (10.3, feel)], t)
                bx, bwa, _ = track(t, [(10.3, BX), (11.5, 570)])
                p = body(t, p, bwa, speed=1.2)
            elif t < 13.2:
                bx = 570; p = keyed([(11.6, feel), (12.0, pose("stand", head=6)), (12.4, see)], t)
            else:
                bx, bwa, _ = track(t, [(13.6, 570), (15.6, 510)])
                p = body(t, keyed([(13.2, see), (13.6, pose("stand"))], t), bwa, speed=1.3); face = -1 if t > 13.4 else 1
            cane_on = t < 11.6
        Jb = draw_figure(cr, bx, gy, p, s=0.95, face=face)
        if cane_on:
            hx, hy = Jb["rhand"]
            if i == 2 and t > 10.3:
                cane(cr, hx + 30, gy, hy, lean=-30)      # sweeping ahead while walking
            else:
                cane(cr, hx + 6, hy - 40, gy, lean=0) if t < 3.5 else None
        if i == 2 and t > 11.6:   # dropped cane lies where he stopped
            cane(cr, 520, gy - 3, gy - 3, lean=-90)
        if not (i == 2 and t > 11.6) and t >= 3.5:
            cane(cr, BX + 70, gy - 3, gy - 3, lean=-90) if not (i == 2 and t > 10.3) else None
        hx, hy = Jb["head"]
        cry_lines(cr, hx + 10, hy, face=1, amount=clamp(cry_amt), size=cry_size, t=t)
        if i == 2:
            light_rays(cr, hx, hy, prog(t, 12.0, 12.6) * (1 - 0.4 * prog(t, 13.4, 14.4)), t=t)

OUTPUT_NAME = "day13b_bartimaeus_mark10"
