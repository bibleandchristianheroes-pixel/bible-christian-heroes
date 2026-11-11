import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX, BOYX, ANX = 150, 262, 380
CROWD = [690, 780, 870, 960, 1050]
PYR = [(5, 0), (4, 1), (3, 2)]     # twelve baskets: (count, row)

class FiveLoaves(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "JOHN 6  •  FIVE LOAVES"
    headline = "A boy gave his small lunch.\nWatch what Jesus did with it."
    captions = [
        (cpdv("John", 6, 9, "“There is a certain boy here, who has five barley loaves and two fish. But what are these among so many?”"), "John 6:9", 3.8),
        (cpdv("John", 6, 11, "…Jesus took the bread, and when he had given thanks, he distributed it to those who were sitting down to eat…"), "John 6:11", 7.4),
        (cpdv("John", 6, 13, "…they filled twelve baskets with the fragments of the five barley loaves, which were left over…"), "John 6:13", 12.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        # ---- Jesus ----
        take = pose("reach", rs=60, re=10, lean=10, head=12)
        hold = pose("stand", rs=40, re=70, ls=35, le=75, head=8)
        thanks = pose("stand", rs=160, re=8, ls=35, le=75, head=-24)
        jp = keyed([(3.0, pose("stand", head=10)), (4.4, pose("stand", head=10)), (4.8, take), (5.2, hold)], t)
        if i >= 1:
            give = pose("reach", rs=75, re=-5, ls=35, le=75)
            jp = keyed([(4.4, pose("stand", head=10)), (4.8, take), (5.2, hold), (5.6, thanks), (6.4, thanks), (6.8, hold), (7.0, give), (7.4, hold)], t) if t >= 4.4 else jp
            if t > 11.2 and i == 2:
                jp = keyed([(11.2, hold), (11.8, pose("stand", rs=95, re=-15, ls=20, le=15, head=-6))], t)
        J = draw_figure(cr, JX, gy, jp, s=1.12, face=1, prop="robe")

        # ---- the boy with his small basket ----
        bx, bwa, _ = track(t, [(2.0, BOYX), (2.6, BOYX - 25)])
        offer = pose("reach", rs=85, re=-15, ls=80, le=-10, head=-14)
        bp = keyed([(1.8, pose("stand", rs=20, re=60)), (2.6, offer), (4.8, offer), (5.3, pose("stand", head=-10))], t)
        if t > 5.3:
            bp = pose("stand", head=-14 if 5.5 < t < 6.6 and i else -4, rs=10, re=10)
        BJ = draw_figure(cr, bx, gy, body(t, bp, bwa), s=0.7, face=-1)
        if t < 4.9:
            hx, hy = BJ["rhand"]; food_basket(cr, hx - 6, hy + 8, w=36, h=22, loaves=3, fishes=0)
        elif i == 0 or t < 5.6:
            hx = (J["rhand"][0] + J["lhand"][0]) / 2; hy = max(J["rhand"][1], J["lhand"][1])
            food_basket(cr, hx + 6, hy + 10, w=36, h=22, loaves=3)
        elif t < 7.0:
            food_basket(cr, JX + 30, gy, w=36, h=22, loaves=2)
            if t < 6.8:
                loaf(cr, J["rhand"][0], J["rhand"][1] - 8)
        else:
            food_basket(cr, JX + 30, gy, w=36, h=22, loaves=2)

        # ---- Andrew ----
        if i == 0:
            shrug = pose("stand", rs=70, re=-50, ls=70, le=-50, head=12)
            ap = keyed([(3.8, pose("stand")), (4.4, shrug), (6.0, shrug), (6.6, pose("stand", head=6))], t)
            ax, awa, aface = ANX, 0, (-1 if t < 4.0 else 1)
            if t > 6.6: aface = -1
            AJ = draw_figure(cr, ax, gy, ap, s=1.0, face=aface)
        else:
            ax, awa, _ = track(t, [(7.3, ANX), (7.6, ANX + 10), (11.2, 1000), (11.5, 1000), (13.6, 615)])
            carry_ = pose("stand", rs=60, re=60, ls=30, le=70)
            ap = keyed([(3.8, pose("stand")), (4.4, pose("stand", rs=70, re=-50, ls=70, le=-50, head=12)), (5.2, pose("stand")),
                        (6.8, pose("stand")), (7.1, pose("reach", rs=70, re=-10)), (7.4, carry_)], t)
            aface = -1 if t < 7.4 else 1
            if t > 11.2: aface = -1; ap = body(t, pose("stand", rs=40, re=60, ls=30, le=70), awa)
            AJ = draw_figure(cr, ax, gy, body(t, ap, awa) if t <= 11.2 else ap, s=1.0, face=aface)
            if t >= 7.4:
                hx, hy = AJ["lhand"]; food_basket(cr, hx + 4, hy + 12, w=40, h=24, loaves=2)

        # ---- the crowd sits on the grass ----
        rock_path_tufts(cr, gy, [560, 640, 740, 830, 920, 1010])
        for k, cx in enumerate(CROWD):
            got = i >= 1 and t >= 7.6 + (cx - ANX - 260) / 640 * 3.6
            looks = -6 if k % 2 else 4
            p = ground_sit_pose(head=looks)
            if i == 0 and 4.0 < t:
                p = ground_sit_pose(head=-4)
            if got:
                tg = 7.6 + (cx - ANX - 260) / 640 * 3.6
                eat = 0.5 + 0.5 * math.sin((t - tg) * 2.2 + k)
                p = keyed([(tg, ground_sit_pose(head=-4)), (tg + 0.4, ground_sit_pose(head=-4, rs=95, re=10))], t)
                if t > tg + 0.8:
                    p = ground_sit_pose(head=6 - 10 * eat, rs=60 + 40 * eat, re=40 + 70 * eat)
            CJ = draw_figure(cr, cx, gy, p, s=0.8, face=-1)
            if got:
                loaf(cr, CJ["rhand"][0] - 2, CJ["rhand"][1] - 6)

        # ---- twelve baskets left over ----
        if i == 2:
            n = 0
            for cnt, row in PYR:
                for j in range(cnt):
                    tk = 11.4 + n * 0.17; n += 1
                    a = prog(t, tk, tk + 0.35)
                    if a <= 0: continue
                    x = 435 + (j - (cnt - 1) / 2) * 58
                    y = gy - row * 36 - (1 - a) * 40
                    food_basket(cr, x, y, w=50, h=30, full=1.0)
            warm_glow(cr, 435, gy - 60, 260, prog(t, 13.4, 14.6))

OUTPUT_NAME = "day22b_five_loaves_john6"
