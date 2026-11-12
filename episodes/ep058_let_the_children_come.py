import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX = 880        # Jesus (seated on a stone, facing left)
DX = 650        # the disciple, between Jesus and the crowd
KID = 0.58      # child scale


def stride(t, base, amt, running=False, speed=1.4):
    if amt <= 0: return base
    return mix(base, run(t, speed=2.2) if running else walk(t, speed=speed), amt)


class LetTheChildrenCome(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MARK 10  •  LET THE CHILDREN COME"
    headline = "The disciples said: go away.\nJesus said: let them come."
    captions = [
        (cpdv("Mark", 10, 13, "…But the disciples admonished those who brought them."), "Mark 10:13", 5.0),
        (cpdv("Mark", 10, 14, "…“Allow the little ones to come to me, and do not prohibit them…"), "Mark 10:14", 6.4),
        (cpdv("Mark", 10, 16, "And embracing them, and laying his hands upon them, he blessed them."), "Mark 10:16", 11.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        bless = prog(t, 11.2, 12.4) if i == 2 else 0.0
        warm_glow(cr, JX - 90, gy - 70, 300, bless)
        stone_seat(cr, JX + 6, gy)

        # ---------------- the disciple ----------------
        stop = pose("stand", rs=100, re=-28, lean=-2, head=-4)
        if i == 0:
            dx, dwa, _ = track(t, [(3.4, DX), (4.4, 560)])
            dface = 1 if t < 3.2 else -1
            dp = keyed([(3.2, pose("stand", head=6)), (3.6, pose("stand")), (4.4, stop), (7.0, stop),
                        (7.6, pose("stand", rs=-10, re=40, ls=-10, le=40, head=-6))], t)
        else:
            dx, dwa, dd = track(t, [(3.4, DX), (4.4, 560), (6.8, 560), (8.8, 1000)])
            dface = 1 if t < 3.2 or t > 6.6 else -1
            dp = keyed([(3.2, pose("stand", head=6)), (3.6, pose("stand")), (4.4, stop), (6.2, stop),
                        (6.6, pose("stand", head=18)), (9.0, pose("stand", head=18)), (9.6, pose("stand", head=6))], t)
            if t > 8.8: dface = -1
        DJ = draw_figure(cr, dx, gy, stride(t, dp, dwa), s=0.98, face=dface)
        if dp["rs"] > 80 and dwa < 0.2:
            stop_hand(cr, DJ, face=dface, s=0.98)

        # ---------------- Jesus ----------------
        seated = sit_pose(lean=4, head=8, rs=40, re=40, ls=35, le=45)
        come = pose("stand", rs=95, re=-12, head=-4)
        open_arms = pose("stand", rs=70, re=-10, ls=60, le=-5, head=14)
        kneel_bless = sit_pose(lean=12, head=26, rs=84, re=-4, ls=112, le=-28)
        if i == 0:
            jp = keyed([(3.6, seated), (4.4, sit_pose(lean=4, head=-2, rs=40, re=40, ls=35, le=45)),
                        (8.6, sit_pose(lean=4, head=-2, rs=40, re=40, ls=35, le=45)), (9.6, sit_pose(lean=14, head=26, rs=50, re=40, ls=45, le=45))], t)
        else:
            keys = [(3.6, seated), (4.4, sit_pose(lean=4, head=-2, rs=40, re=40, ls=35, le=45)),
                    (5.0, sit_pose(lean=4, head=-2, rs=40, re=40, ls=35, le=45)), (5.8, pose("stand", head=-4)),
                    (6.3, come), (8.2, come), (8.8, open_arms)]
            if i == 2:
                keys += [(10.4, open_arms), (11.2, kneel_bless)]
            jp = keyed(keys, t)
        J = draw_figure(cr, JX, gy, jp, s=1.0, face=-1, prop="robe")

        # ---------------- the mother and her child ----------------
        if i == 0:
            mx, mwa, md = track(t, [(0.4, -120), (3.8, 380), (5.6, 380), (5.9, 375), (9.8, -160)])
            cx, cwa, cd = track(t, [(0.4, -60), (3.8, 440), (5.2, 440), (5.8, 400), (9.8, -100)])
        else:
            mx, mwa, md = track(t, [(0.4, -120), (3.8, 380), (8.2, 380), (9.8, 560)])
            cx, cwa, cd = track(t, [(0.4, -60), (3.8, 440), (7.2, 440), (8.6, JX - 62)])
        mface = 1 if (i or t < 5.7) else -1
        cface = 1 if (i or t < 5.5) else -1
        mp = keyed([(3.8, pose("stand", rs=35, re=10)), (4.6, pose("stand", rs=35, re=10, head=-6, lean=-4))], t)
        if i == 0 and t > 5.6: mp = pose("stand", rs=-10, re=20, head=20)
        if i and t > 9.8: mp = keyed([(9.8, pose("stand", head=-6)), (10.4, pose("stand", rs=118, re=-130, ls=110, le=-125, head=-2))], t)
        MJ = draw_figure(cr, mx, gy, stride(t, mp, mwa), s=0.92, face=mface)
        veil_drape(cr, MJ, s=0.92, face=mface)

        # child: walks in holding hands; hides behind mother when stopped; in panels 2-3 runs to Jesus
        cp = keyed([(3.8, pose("stand", rs=-30, re=10, head=-10)), (4.6, pose("stand", rs=-30, re=10, head=-18))], t)
        running = False
        if i == 0 and t > 5.5:
            cp = pose("stand", head=24, rs=10, re=10)
            if t > 8.2: cp = pose("stand", head=-8, rs=10, re=10)   # a last look back
        if i and t > 7.2:
            running = t < 8.6
            cp = keyed([(8.6, pose("stand", head=-20, rs=60, re=10, ls=50, le=10)), (9.2, pose("stand", head=-30, rs=110, re=-10, ls=100, le=-10))], t)
            if i == 2 and t > 11.2: cp = pose("stand", head=-34, rs=20, re=10, ls=15, le=10)
        CJ = draw_figure(cr, cx, gy, stride(t, cp, cwa, running), s=KID, face=cface)
        if (i == 0 and t < 5.3) or (i and t < 7.2):     # holding hands
            cr.set_source_rgb(*INK); cr.set_line_width(5)
            cr.move_to(*MJ["rhand"]); cr.line_to(*CJ["rhand"]); cr.stroke()

        # ---------------- more children (panel 3) ----------------
        if i == 2:
            for k, (x_end, t0) in enumerate(((JX - 104, 9.0), (JX - 146, 9.5))):
                kx, kwa, _ = track(t, [(t0, -60), (t0 + 2.0, x_end)])
                kp = pose("stand", head=-26, rs=15, re=10)
                if kx > -40:
                    draw_figure(cr, kx, gy, stride(t + k, kp, kwa, True), s=KID - 0.04 * k, face=1)


OUTPUT_NAME = "day29b_let_the_children_come_mark10"
