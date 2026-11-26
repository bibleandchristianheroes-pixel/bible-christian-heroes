import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX = 740            # left edge of the feast house (door at HX+28 .. HX+102)
SX = 500            # where the elder son stops outside
FX0 = HX + 64       # the father, coming out of the door
FX = 600            # where the father stands to plead

s_carry = pose("stand", rs=24, re=8)
s_hear = pose("stand", rs=24, re=8, head=-10)
s_cross = pose("stand", rs=38, re=-132, ls=34, le=-128, head=-8, lean=-4)        # arms crossed, chin up
s_sulk = ground_sit_pose(lean=18, head=28, rs=38, re=-132, ls=34, le=-128)        # sits with his back turned
s_soft = pose("stand", head=24, lean=6, rs=10, re=14, ls=8, le=14)               # arms drop, head down
s_joy = pose("joy", ls=140, le=20, rs=150, re=10)
f_plead = pose("stand", rs=78, re=-12, ls=66, le=-16, lean=10, head=4)
f_reach = pose("reach", rs=84, re=-4, lean=14, head=10)
f_sad = pose("stand", head=34, lean=8, rs=8, re=24, ls=6, le=24)
f_arm = pose("stand", rs=72, re=-8, head=4)                                       # hand on the son's shoulder
f_joy = pose("stand", rs=72, re=-8, ls=150, le=10, head=-12)


class ElderBrother(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 15  •  THE LOST SON'S BROTHER"
    headline = "His brother came home.\nWill he go in to the feast?"
    captions = [
        (cpdv("Luke", 15, 28, "Then he became indignant, and he was unwilling to enter."), "Luke 15:28", 5.6),
        (cpdv("Luke", 15, 31, "…Son, you are with me always, and all that I have is yours."), "Luke 15:31", 7.4),
        (cpdv("Luke", 15, 32, "…this brother of yours was dead, and has revived; he was lost, and is found."), "Luke 15:32", 10.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 980, gy - 330, r=20, rays=10)
        for k, wx in enumerate((24, 54, 84, 114)):
            wheat(cr, wx, gy, 108 + 14 * (k % 2), sway=math.sin(t * 1.3 + k))
        for gx in (220, 380, 1060):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        glow = prog(t, 12.0, 13.4) if i == 2 else 0.0
        warm_glow(cr, HX + 60, gy - 110, 420, 0.8 * glow)
        feast_house(cr, HX, gy, t, light=1.0)

        # ---------------- the elder son ----------------
        sx, swa, _ = track(t, [(0.2, -70), (3.6, SX)])
        sface = 1
        sp = body(t, keyed([(0.0, s_carry), (3.6, s_carry), (4.0, s_hear), (4.8, s_hear), (5.4, s_cross)], t), swa, speed=1.5)
        spade_at = "hand" if t < 4.9 else "ground"
        if i == 0 and t > 6.2:
            sx, swa, _ = track(t, [(6.4, SX), (10.4, -90)])
            sface = -1
            sp = body(t, keyed([(6.2, s_cross), (6.6, pose("stand", rs=38, re=-132, ls=34, le=-128, head=6))], t), swa, speed=1.4)
            for k_ in ("rs", "re", "ls", "le"):
                sp[k_] = s_cross[k_]
        elif i == 1 and t > 7.6:
            sface = -1
            sp = keyed([(7.6, s_cross), (8.0, pose("stand", rs=38, re=-132, ls=34, le=-128, head=4)),
                        (8.6, pose("stand", rs=38, re=-132, ls=34, le=-128, head=4)), (9.4, s_sulk)], t)
        elif i == 2 and t > 9.0:
            sp = keyed([(9.0, s_cross), (9.8, s_soft), (10.4, s_soft), (10.8, pose("stand", head=6, rs=10, re=14, ls=8, le=14))], t)
            if t > 10.8:
                sx, swa, _ = track(t, [(11.0, SX), (12.6, HX + 62)])
                sp = body(t, pose("stand", head=0, rs=10, re=14, ls=8, le=14), swa, speed=1.5)
                if t > 12.6:
                    sp = keyed([(12.6, pose("stand", head=-6)), (13.3, s_joy)], t)
                    sp["lean"] += 3 * math.sin(t * 5)
        SJ = None
        if sx > -80:
            SJ = draw_figure(cr, sx, gy, sp, s=0.92, face=sface)
        if spade_at == "hand" and SJ is not None:
            hx, hy = SJ["rhand"]
            spade(cr, hx, hy - 34, hx + 12, gy - 4, s=0.9)
        elif spade_at == "ground":
            spade(cr, SX + 40, gy - 92, SX + 46, gy + 4, s=0.9)       # planted in the ground

        # ---------------- the father ----------------
        if t > 5.0:
            fx, fwa, _ = track(t, [(5.0, FX0), (6.8, FX)])
            fface = -1
            fp = body(t, keyed([(5.0, pose("stand", head=-4)), (6.8, pose("stand", head=-4)), (7.2, f_plead)], t), fwa, speed=1.5)
            if i == 0:
                fx, fwa, _ = track(t, [(5.0, FX0), (6.8, 640)])
                fp = body(t, keyed([(5.0, pose("stand", head=-4)), (6.8, pose("stand", head=-4)), (7.3, f_reach),
                                    (9.6, f_reach), (10.6, f_sad)], t), fwa, speed=1.5)
            elif i == 1:
                fp = keyed([(6.8, pose("stand", head=-4)), (7.2, f_plead), (8.8, f_plead), (9.6, f_reach),
                            (10.8, f_reach), (11.8, f_sad)], t) if t > 6.8 else fp
            else:
                if t > 6.8:
                    fp = keyed([(6.8, pose("stand", head=-4)), (7.2, f_plead), (9.6, f_plead), (10.2, f_arm)], t)
                if t > 10.8:
                    fface = 1
                    fx, fwa, _ = track(t, [(11.0, FX - 2), (11.2, SX - 58), (12.6, HX - 40)])
                    fp = body(t, f_arm, fwa, speed=1.5)
                    for k_ in ("rs", "re"):
                        fp[k_] = f_arm[k_]
                    if t > 12.6:
                        fp = keyed([(12.6, f_arm), (13.3, f_joy)], t)
                elif t > 10.2:
                    fx, fwa, _ = track(t, [(10.2, FX), (10.8, FX - 2)])
            a = prog(t, 5.0, 5.5)
            cr.push_group()
            draw_figure(cr, fx, gy, fp, s=1.0, face=fface)
            cr.pop_group_to_source(); cr.paint_with_alpha(a)


OUTPUT_NAME = "day42a_elder_brother_luke15"
