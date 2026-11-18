import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

WALL = (30, 230)        # house wall with the window towards Jerusalem
DX = 345                # where Daniel kneels (facing the window, i.e. left)
DEN = (560, 1060)       # the lions' den
IN_X = 675              # where Daniel ends up inside the den
LA = 825                # lion A's resting spot (facing Daniel)
LB = 940                # lion B, further back
FAR = (0.32, 0.30, 0.28)

pray = pose("kneel", lean=4, head=-14, rs=150, re=10, ls=140, le=12)           # arms lifted towards the window
bow = pose("kneel", lean=36, head=28, rs=25, re=95, ls=20, le=95)
hands = pose("kneel", lean=10, head=6, rs=70, re=-95, ls=65, le=-95)           # hands joined
praise = pose("kneel", lean=-4, head=-18, rs=160, re=8, ls=150, le=10)
s_walk = pose("stand", head=2)
s_grab = pose("stand", rs=82, re=-4, ls=70, le=10, lean=6)
s_push = pose("stand", rs=88, re=-2, ls=80, le=0, lean=16)


def paced_x(t):
    return LA + 60 * math.sin(t * 0.8), (1 if math.cos(t * 0.8) > 0 else -1)


class DanielLionsDen(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "DANIEL 6  •  DANIEL IN THE LIONS' DEN"
    headline = "The king made praying a crime.\nDaniel opened his window."
    captions = [
        (cpdv("Daniel", 6, 10, "…opening the windows in his upper room towards Jerusalem, he knelt down three times a day…"), "Daniel 6:10", 3.0),
        (cpdv("Daniel", 6, 16, "Then the king commanded, and they brought Daniel and cast him into the den of lions."), "Daniel 6:16", 8.4),
        (cpdv("Daniel", 6, 22, "My God has sent his angel, and he has closed the mouths of the lions, and they have not harmed me…"), "Daniel 6:22", 11.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        wl = prog(t, 1.4, 3.0)
        window_wall(cr, WALL[0], WALL[1], gy, h=170, ww=80, wh=110, light=wl * (1 if i == 0 else 1 - 0.7 * prog(t, 6.0, 7.0)))
        gate = 1.0
        if i >= 1:
            gate = 1 - prog(t, 7.4, 8.0) * (1 - prog(t, 8.8, 9.4))
        lions_den(cr, DEN[0], DEN[1], gy, h=160, gate=gate)
        thrown = i >= 1 and t >= 8.6
        calm = prog(t, 11.0, 12.2) if i == 2 else 0.0

        # ---------------- the angel (P3) ----------------
        if i == 2:
            warm_glow(cr, 905, gy - 120, 230, prog(t, 10.2, 11.2))
            angel_figure(cr, 905, gy, pose("stand", rs=80, re=-10, ls=40, le=10, head=-4), s=1.0, face=-1,
                         alpha=prog(t, 10.2, 11.0), spread=prog(t, 10.4, 11.4))

        # ---------------- lions ----------------
        roar = 0.0
        if i >= 1:
            roar = prog(t, 8.8, 9.3) * (0.75 + 0.25 * math.sin(t * 7)) * (1 - prog(t, 10.8, 11.4))
        bx, bface = LB, -1
        if i == 0 or t < 8.4:
            bx = LB + 25 * math.sin(t * 0.6 + 1.0)
        lion(cr, bx, gy, s=0.82, face=bface, step=(t * 5 if (i == 0 or t < 8.4) else 0), roar=roar * 0.8, lie=calm, color=FAR)
        ax, aface = paced_x(t)
        astep = t * 6
        if i >= 1 and t >= 8.4:
            px, _ = paced_x(8.4)
            ax = lerp(px, LA, prog(t, 8.4, 9.0)); aface = -1
            astep = t * 6 if t < 9.0 else 0
        lion(cr, ax, gy, s=1.0, face=aface, step=astep, roar=roar, lie=calm)

        # ---------------- soldiers (P2, P3) ----------------
        if i >= 1 and 4.2 < t < 14.5:
            for k, (sx0, sx1) in enumerate(((-90, 235), (-190, 160))):
                sx, swa, _ = track(t, [(4.4, sx0), (6.0, sx1), (6.6, sx1), (8.2, sx1 + 240), (8.7, sx1 + 255), (10.4, sx1 + 255), (13.8, sx0 - 60)])
                sface = -1 if t > 10.2 else 1
                sk = [(4.4, s_walk), (6.0, s_walk), (6.4, s_grab if k == 0 else s_walk), (8.2, s_grab if k == 0 else s_walk)]
                if k == 0:
                    sk += [(8.4, s_push), (8.9, s_push), (9.4, s_walk)]
                sp = body(t, keyed(sk, t), swa, speed=1.5)
                Jg = ghost_joints(sx, gy, sp, s=0.97, face=sface)
                cr.save(); cr.rectangle(0, y0, W, gy - y0 - 3); cr.clip()
                cape(cr, Jg, face=sface, s=0.97); cr.restore()
                J = draw_figure(cr, sx, gy, sp, s=0.97, face=sface)
                soldier_helmet(cr, J, s=0.97, face=sface)

        # ---------------- Daniel ----------------
        dx, dwa, _ = track(t, [(0.1, -70), (1.8, DX)])
        dface = 1 if t < 1.8 else -1
        dk = [(1.8, pose("stand", head=-4)), (2.3, pose("kneel", head=4)), (2.8, pray)]
        if i == 0:
            dk += [(6.0, pray), (6.8, bow), (9.0, bow), (9.8, pray), (12.4, pray), (13.0, hands)]
        else:
            dk += [(5.0, pray), (5.4, pose("kneel", head=-4, lean=0)), (6.0, pose("stand", head=6)), (6.6, pose("stand", head=10, lean=4))]
            if t >= 5.6:
                dface = 1
            if t >= 6.6:
                dx, dwa, _ = track(t, [(6.6, DX), (8.2, DX + 215), (8.8, IN_X)])
                dk += [(8.2, pose("stand", head=10, lean=4)), (8.6, pose("stand", lean=-14, head=-10, rs=40, re=40, ls=30, le=40)),
                       (9.0, pose("stand", head=-6)), (9.6, hands)]
                if i == 2:
                    dk += [(11.4, hands), (12.2, praise)]
        dp = keyed(dk, t) if t >= 1.8 else pose("stand")
        draw_figure(cr, dx, gy, body(t, dp, dwa, speed=1.5), s=0.95, face=dface)


OUTPUT_NAME = "day35b_daniel_lions_den_daniel6"
