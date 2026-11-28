import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CROWD = (0.50, 0.48, 0.45)
P0, P1_ = 700, 1060          # temple porch
D1, D2 = 778, 1018           # the two teachers (seated)
BX = 898                     # the boy, seated among them
SUN = (995, -338)            # sun / moon (relative to gy)

open_hands = pose("stand", rs=34, re=78, ls=28, le=84, head=14)        # "not here"
ask = pose("reach", rs=88, re=-6, lean=6, head=0)
seek = pose("stand", head=-10, rs=14, re=16)
grief = pose("head_hands")
hand_face = pose("stand", ls=150, le=150, head=22, lean=6, rs=10, re=14)
comfort = pose("reach", rs=78, re=10, lean=4, head=12)
wonder = pose("stand", rs=120, re=12, ls=110, le=14, head=-8, lean=-4)
embrace = pose("kneel", lean=10, head=6, rs=78, re=40, ls=72, le=44)
point_up = pose("stand", rs=170, re=4, ls=30, le=20, head=-12)


def night(t):
    return 0.55 * (prog(t, 6.2, 6.6) * (1 - prog(t, 7.0, 7.4)) + prog(t, 7.8, 8.2) * (1 - prog(t, 8.6, 9.0)))


class LostChildInTheTemple(Episode):
    dur = 18.0
    caption_bg = (False, True, False)
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 2  •  THE BOY JESUS IN THE TEMPLE"
    headline = "They searched for three days.\nHe was in his Father's house."
    captions = [
        (cpdv("Luke", 2, 44, "…supposing that he was in the company, they went a day’s journey, seeking him among their relatives and acquaintances."), "Luke 2:44", 3.4),
        (cpdv("Luke", 2, 45, "And not finding him, they returned to Jerusalem, seeking him."), "Luke 2:45", 6.0),
        (cpdv("Luke", 2, 49, "…did you not know that it is necessary for me to be in these things which are of my Father?"), "Luke 2:49", 12.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sx, sy = SUN[0], gy + SUN[1]
        nt = night(t) if i >= 1 else 0.0
        if nt < 0.3:
            sun(cr, sx, sy, r=20, rays=10)
        temple_porch(cr, P0, P1_, gy, h=176)
        found = prog(t, 12.0, 13.0) if i == 2 else 0.0
        warm_glow(cr, BX - 60, gy - 120, 300, 0.35 + 0.6 * found)

        # ---------- the teachers and the boy, in the temple the whole time ----------
        bench(cr, D1 - 34, D1 + 34, gy, h=42)
        bench(cr, D2 - 34, D2 + 34, gy, h=42)
        talk = math.sin(t * 2.1)
        draw_figure(cr, D1, gy, sit_pose(lean=8 + 3 * talk, head=10, rs=60 + 14 * max(0, talk), re=30, ls=40, le=40), s=0.95, face=1, prop="robe_hat")
        draw_figure(cr, D2, gy, sit_pose(lean=10 - 3 * talk, head=12, rs=50, re=50, ls=44, le=40), s=0.95, face=-1, prop="robe_hat")

        # ---------- the relatives: no one has seen him; they travel on ----------
        for k, (x0, t_turn, t_shrug) in enumerate([(150, 2.9, 3.3), (240, 2.5, 2.9)]):
            x, wa, d = track(t, [(0, x0), (1.6, x0 - 40), (4.6, x0 - 40), (8.4, x0 - 520)])
            face = -1
            p = body(t, pose("stand"), wa)
            if 1.6 <= t < 4.7:
                face = 1 if t > t_turn else -1
                p = keyed([(t_shrug, pose("stand", head=4)), (t_shrug + 0.4, open_hands), (t_shrug + 1.0, open_hands),
                           (t_shrug + 1.4, pose("stand", head=6))], t)
            if x > -80:
                draw_figure(cr, x, gy, p, s=0.92, face=face, color=CROWD)

        # ---------- Joseph and Mary ----------
        self.parents(cr, i, t, gy)
        self.boy(cr, i, t, gy)

        darkness(cr, gy - GROUND_OFF, PANEL_H, nt)
        crescent_moon(cr, sx, sy, r=20, alpha=clamp(nt / 0.4))

    def boy(self, cr, i, t, gy):
        s = 0.62
        if i < 2 or t < 10.8:
            stool(cr, BX, gy, h=27, w=34)
            q = math.sin(t * 1.7 + 1)
            p = sit_pose(lean=-2, head=-10, rs=80 + 30 * max(0, q), re=-10, ls=30, le=40)
            draw_figure(cr, BX, gy, p, s=s, face=-1 if q > -0.2 else 1, prop="robe")
            return
        stool(cr, BX, gy, h=27, w=34)
        x, wa, _ = track(t, [(11.0, BX - 6), (12.0, 680)])
        p = keyed([(10.8, sit_pose(head=-10)), (11.1, pose("stand", head=-6))], t)
        p = body(t, p, wa, speed=1.8)
        if t > 12.0:
            p = keyed([(12.0, pose("stand", rs=60, re=30, ls=56, le=30, head=6)), (12.5, pose("stand", rs=60, re=30, ls=56, le=30, head=6)),
                       (13.0, point_up)], t)
        if t > 13.0:
            G = ghost_joints(x, gy, p, s=s, face=-1)
            light_rays(cr, G["rhand"][0], G["rhand"][1] - 8, 0.6 * prog(t, 13.0, 13.8), r0=12, r1=34, n=10, t=t)
        draw_figure(cr, x, gy, p, s=s, face=-1, prop="robe")

    def parents(self, cr, i, t, gy):
        jx, jwa, _ = track(t, [(0, 360), (1.6, 320)])
        mx, mwa, _ = track(t, [(0, 440), (1.6, 400)])
        jface, mface = -1, -1
        jp = body(t, pose("stand"), jwa)
        mp = body(t, pose("stand"), mwa)
        if t >= 1.6:
            # she turns: where is the boy?
            mface = 1 if (1.9 < t < 2.5) else -1
            mp = keyed([(1.6, pose("stand")), (1.9, seek), (2.5, seek), (2.8, pose("stand", head=8)), (3.8, pose("stand", head=8)), (4.3, grief)], t)
            jp = keyed([(1.6, pose("stand")), (2.5, pose("stand", head=4)), (2.9, ask), (3.3, ask), (3.6, pose("stand", head=6)),
                        (3.7, ask), (4.3, ask), (4.7, comfort)], t)
            if t > 4.5:
                jface = 1
        if i >= 1 and t >= 5.4:
            jface = mface = 1
            jx, jwa, _ = track(t, [(5.6, 320), (9.4, 420)])
            mx, mwa, _ = track(t, [(5.6, 400), (9.4, 500)])
            look = pose("stand", head=-10 + 14 * math.sin(t * 1.6))
            mp = body(t, keyed([(5.4, grief), (5.8, look)], t) if t < 5.8 else look, mwa, speed=1.2)
            jp = body(t, keyed([(5.4, comfort), (5.8, pose("stand", head=-4))], t), jwa, speed=1.2)
            if t > 9.4:
                mp = keyed([(9.4, look), (9.9, hand_face)], t)
                jp = keyed([(9.4, pose("stand", head=-4)), (9.9, pose("stand", head=-12, rs=20, re=30))], t)
            if i == 2 and t > 10.0:
                # she lifts her head and sees him
                jx, jwa, _ = track(t, [(10.4, 420), (11.4, 506)])
                mx, mwa, _ = track(t, [(10.2, 500), (11.0, 588)])
                mp = body(t, keyed([(10.0, hand_face), (10.3, pose("stand", head=-6, rs=60, re=20))], t), mwa, speed=1.8)
                jp = body(t, keyed([(10.0, pose("stand", head=-12, rs=20, re=30)), (10.4, pose("stand", head=-2))], t), jwa, speed=1.6)
                if t > 11.2:
                    mp = keyed([(11.2, pose("stand", head=-6, rs=60, re=20)), (11.9, embrace)], t)
                if t > 11.4:
                    jp = keyed([(11.4, pose("stand", head=-2)), (12.6, pose("stand", head=-2)), (13.2, wonder)], t)
        draw_figure(cr, jx, gy, jp, s=1.0, face=jface)
        J = draw_figure(cr, mx, gy, mp, s=0.93, face=mface, prop="robe")
        veil_drape(cr, J, s=0.93, face=mface)


OUTPUT_NAME = "day44a_boy_jesus_in_the_temple_luke2"
