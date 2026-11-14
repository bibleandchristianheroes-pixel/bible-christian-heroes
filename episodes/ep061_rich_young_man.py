import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX = 760        # Jesus, standing, facing left
KX = 560        # where the young man kneels
BX = 190        # the beggar, sitting on the ground, facing right
BOWL_X = BX + 62

kneel_ask = pose("kneel", head=-14, lean=6, rs=70, re=-20, ls=40, le=30)
clutch = pose("stand", head=26, lean=8, rs=30, re=118, ls=26, le=120)      # bag hugged to the chest
look_bag = pose("stand", head=30, lean=6, rs=40, re=95, ls=30, le=100)
give = pose("reach", rs=78, re=-8, lean=16, head=10)
light = pose("stand", head=-10, rs=20, re=20, ls=14, le=16)


class RichYoungMan(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MARK 10  •  THE RICH YOUNG MAN"
    headline = "Jesus said: come, follow me.\nOnly one let go of the gold."
    captions = [
        (cpdv("Mark", 10, 22, "But he went away grieving, having been greatly saddened by the word. For he had many possessions."), "Mark 10:22", 8.8),
        (cpdv("Matthew", 6, 21, "For where your treasure is, there also is your heart."), "Matthew 6:21", 10.8),
        (cpdv("Mark", 10, 21, "…give to the poor, and then you will have treasure in heaven. And come, follow me.”"), "Mark 10:21", 10.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 1000, gy - 300, r=22, rays=10)

        # ---------------- the beggar ----------------
        beg = ground_sit_pose(head=-6, rs=60, re=20, ls=30, le=40)
        if i == 1 and t > 10.2:
            beg = keyed([(10.2, beg), (10.8, ground_sit_pose(head=-14, rs=60, re=20, ls=30, le=40))], t)
        if i == 2 and t > 10.2:
            beg = keyed([(10.2, beg), (10.6, ground_sit_pose(head=-6, rs=75, re=-10, ls=70, le=-10)),
                         (11.6, ground_sit_pose(head=-24, lean=-10, rs=160, re=5, ls=150, le=10))], t)
        BJ = draw_figure(cr, BX, gy, beg, s=0.92, face=1)
        bowl(cr, BOWL_X, gy - 6, w=30)
        if i == 1 and t > 10.0:   # one coin dropped into the bowl
            u = prog(t, 10.0, 10.5)
            coin(cr, BOWL_X, lerp(gy - 90, gy - 12, u), r=8)

        # ---------------- Jesus ----------------
        love = pose("stand", head=8, rs=30, re=110, ls=20, le=20)            # hand on his heart, gazing down
        point = pose("reach", rs=84, re=-4, lean=4, head=-2)                 # toward the poor man
        jkeys = [(3.6, pose("stand", head=6)), (4.2, love), (5.0, love), (5.6, point), (6.8, point),
                 (7.4, pose("stand", rs=60, re=-10, head=0))]
        jx = JX; jwa = 0; jface = -1
        if i < 2:
            jkeys += [(9.6, pose("stand", rs=60, re=-10, head=0)), (10.4, pose("reach", rs=70, re=-10, head=4)), (14.0, pose("reach", rs=60, re=-10, head=14))]
        else:
            jkeys += [(10.8, pose("stand", rs=60, re=-10)), (11.4, pose("stand", rs=50, re=-30, head=-4))]
            jx, jwa, _ = track(t, [(11.8, JX), (14.6, JX + 210)])
            if t > 11.4: jface = 1
        jp = body(t, keyed(jkeys, t), jwa, speed=1.2)
        draw_figure(cr, jx, gy, jp, s=1.08, face=jface, prop="robe")

        # ---------------- the young man ----------------
        face = 1
        if t < 2.6:
            x, wa, _ = track(t, [(0.4, -70), (2.6, KX)])
            p = mix(pose("stand"), run(t, speed=2.2), wa)
        elif t < 6.2:
            x = KX; wa = 0
            p = keyed([(2.6, pose("stand", lean=10)), (3.1, kneel_ask), (5.6, kneel_ask),
                       (6.2, pose("kneel", head=30, lean=12, rs=30, re=110, ls=26, le=110))], t)
        else:
            x = KX; wa = 0
            p = keyed([(6.2, pose("kneel", head=30, lean=12, rs=30, re=110, ls=26, le=110)), (6.9, look_bag), (8.0, look_bag)], t)
            if i == 0 and t > 8.0:
                x, wa, _ = track(t, [(8.2, KX), (14.0, -90)])
                face = -1
                p = body(t, keyed([(8.0, look_bag), (8.6, clutch)], t), wa, speed=0.9)
            elif i >= 1 and t > 8.0:
                x, wa, _ = track(t, [(8.2, KX), (9.8, BOWL_X + 70)])
                face = -1
                if i == 1:
                    if t < 9.8:
                        p = body(t, look_bag, wa, speed=1.1)
                    else:
                        p = keyed([(9.8, look_bag), (10.0, give), (10.6, give), (11.0, clutch)], t)
                        if t > 11.0:
                            x, wa, _ = track(t, [(11.2, BOWL_X + 70), (15.4, -90)])
                            p = body(t, clutch, wa, speed=0.9)
                else:
                    if t < 9.8:
                        p = body(t, look_bag, wa, speed=1.1)
                    else:
                        p = keyed([(9.8, look_bag), (10.1, give), (10.6, give), (11.0, light)], t)
                        if t > 11.0:
                            x, wa, _ = track(t, [(11.6, BOWL_X + 70), (14.8, JX + 70)])
                            face = 1 if t > 11.2 else -1
                            p = body(t, light, wa, speed=1.3)
                            if t > 14.8:
                                p = keyed([(14.8, light), (15.3, pose("stand", head=-14, rs=30, re=20, ls=20, le=20))], t)
        if i == 2:
            warm_glow(cr, x, gy - 120, 150, prog(t, 10.8, 11.8) * 0.75)
        MJ = draw_figure(cr, x, gy, p, s=1.0, face=face)

        # ---------------- the bag of gold ----------------
        hx, hy = MJ["rhand"]
        bag_given = i == 2 and t > 10.4
        if i == 2 and 10.1 < t < 10.6:      # handed over
            u = prog(t, 10.2, 10.5)
            bx = lerp(hx, BJ["rhand"][0], u); by = lerp(hy, BJ["rhand"][1], u)
            coin_bag(cr, bx, by - 4, s=1.0)
        elif bag_given:
            lx, ly = BJ["rhand"]
            coin_bag(cr, lx, ly - 8, s=1.0)
            coin_glint(cr, lx, ly + 8, prog(t, 11.0, 11.8), t)
        else:
            coin_bag(cr, hx, hy - 8, s=1.0)


OUTPUT_NAME = "day31a_rich_young_man_mark10"
