import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BX = 720            # the beggar, sitting by the road (facing the travellers)
STOP = 545          # where the traveller stops
KX = 590            # where he kneels (panel 3)
BASKET_X = 505      # where he sets his basket down (panel 3)
OFF = 1200
START = -70

b_sad = ground_sit_pose(lean=16, head=30, rs=40, re=50, ls=30, le=50)
b_ask = ground_sit_pose(lean=6, head=-12, rs=84, re=-14, ls=30, le=50)
b_ask2 = ground_sit_pose(lean=12, head=-6, rs=94, re=-6, ls=30, le=50)
b_watch = ground_sit_pose(lean=6, head=-4, rs=60, re=10, ls=30, le=50)
b_slump = ground_sit_pose(lean=28, head=46, rs=30, re=40, ls=20, le=40)
b_take = ground_sit_pose(lean=10, head=-4, rs=86, re=-6, ls=30, le=50)
b_eat = ground_sit_pose(lean=8, head=14, rs=24, re=136, ls=30, le=50)
b_hand = ground_sit_pose(lean=4, head=-10, rs=96, re=-4, ls=30, le=50)
b_up = pose("stand", rs=76, re=-6, head=0)
b_open = pose("stand", rs=64, re=-14, ls=58, le=-14, head=-4)       # arms opened in welcome

t_base = pose("stand", rs=8, re=10, ls=10, le=12)
t_look = pose("stand", rs=8, re=10, ls=10, le=12, head=26, lean=4)
t_offer = pose("stand", rs=8, re=10, ls=62, le=-8, head=20, lean=4)  # half holds out a loaf
t_keep = pose("stand", rs=8, re=10, ls=26, le=96, head=10)           # pulls it back to his chest
t_set = pose("stand", rs=40, re=0, lean=30, head=24)                  # sets the basket down
t_give = pose("kneel", rs=82, re=-4, ls=30, le=20, head=8, lean=10)
t_hand = pose("kneel", rs=86, re=-6, ls=30, le=20, head=-4, lean=6)
t_pull = pose("stand", rs=74, re=-4, head=-2, lean=-8)
t_awe = pose("kneel", rs=24, re=112, ls=22, le=112, head=34, lean=26)


class SheepAndGoats(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MATTHEW 25  •  THE SHEEP AND THE GOATS"
    headline = "Three men passed the same beggar.\nOnly one saw who he was."
    captions = [
        (cpdv("Matthew", 25, 42, "For I was hungry, and you did not give me to eat; I was thirsty, and you did not give me to drink…"), "Matthew 25:42", 7.0),
        (cpdv("Matthew", 25, 45, "…whenever you did not do it to one of these least, neither did you do it to me."), "Matthew 25:45", 8.8),
        (cpdv("Matthew", 25, 40, "…whenever you did this for one of these, the least of my brothers, you did it for me."), "Matthew 25:40", 11.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 1000, gy - 300, r=22, rays=10)
        reveal = prog(t, 10.2, 11.6) if i == 2 else 0.0
        warm_glow(cr, BX, gy - 120, 420, 0.9 * reveal)
        olive_tree(cr, 930, gy, h=130)
        for gx in (180, 330, 470, 1040):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))

        # ---------------- the beggar ----------------
        bx = BX
        common = [(0.0, b_sad), (2.8, b_sad), (3.4, b_ask)]
        if i == 0:
            bp = keyed(common + [(5.8, b_ask), (6.4, b_watch), (7.2, b_watch), (8.0, b_slump)], t)
        elif i == 1:
            bp = keyed(common + [(5.6, b_ask), (6.1, b_ask2), (7.2, b_ask2), (7.8, b_watch), (9.4, b_watch), (10.4, b_slump)], t)
        else:
            bp = keyed(common + [(5.8, b_ask), (6.2, b_take), (6.8, b_take), (7.2, b_eat), (8.0, b_eat),
                                 (8.4, b_sad), (8.7, b_hand), (9.0, b_hand)], t)
            if t > 9.0:
                u = prog(t, 9.0, 9.9)
                bp = mix(b_hand, b_up, u) if u < 1 else keyed([(9.9, b_up), (10.6, b_up), (11.6, b_open)], t)
        cr.push_group()
        BJ = draw_figure(cr, bx, gy, bp, s=0.95, face=-1)
        if reveal > 0:
            cr.push_group()
            draw_figure(cr, bx, gy, bp, s=0.95, face=-1, prop="robe")
            cr.pop_group_to_source(); cr.paint_with_alpha(reveal)
        beggar = cr.pop_group()
        if reveal > 0:                                    # light behind him, then the silhouette on top
            light_rays(cr, BJ["head"][0], BJ["head"][1], 0.8 * reveal, r0=24, r1=56, n=14, t=t)
        cr.set_source(beggar); cr.paint()
        if reveal > 0:
            wound_marks(cr, BJ, s=0.95, amount=reveal, glow=0.0)

        # ---------------- the traveller ----------------
        tx, twa, _ = track(t, [(0.2, START), (4.4, STOP)]); tface = 1
        tp = body(t, keyed([(0.0, t_base), (4.4, t_base), (4.9, t_look)], t), twa, speed=1.5)
        basket_at = "hand"; loaf_at = None
        if i == 0:
            tx, twa, _ = track(t, [(0.2, START), (8.6, OFF)])
            tp = body(t, t_base, twa, speed=1.5)
            if 3.6 < t < 8.0:
                tp["head"] = -20 * prog(t, 3.6, 4.0) * (1 - prog(t, 7.4, 8.0))   # eyes up and away
        elif i == 1 and t > 4.9:
            tp = keyed([(4.9, t_look), (5.4, t_look), (5.9, t_offer), (6.8, t_offer), (7.3, t_keep), (7.9, t_keep), (8.3, t_base)], t)
            if 7.2 < t < 7.9:
                tp["head"] += 8 * math.sin(t * 11)
            loaf_at = "lhand" if 5.6 < t < 8.1 else None
            if t > 8.3:
                tx, twa, _ = track(t, [(8.4, STOP), (12.0, OFF)])
                tp = body(t, t_base, twa, speed=1.5)
                tp["head"] = -14 * prog(t, 8.4, 8.8) * (1 - prog(t, 10.2, 10.8))
        elif i == 2 and t > 4.9:
            tp = keyed([(4.9, t_look), (5.0, t_look), (5.3, t_set), (5.5, t_set)], t)
            if t > 5.4:
                basket_at = "ground"
            if t > 5.5:
                tx, twa, _ = track(t, [(5.6, STOP), (5.9, KX)])
                tp = body(t, keyed([(5.9, t_base), (6.1, t_give), (6.7, t_give), (7.0, pose("kneel", head=10, lean=10)),
                                    (8.4, pose("kneel", head=10, lean=10)), (8.7, t_hand), (9.0, t_hand)], t), twa, speed=1.5)
                loaf_at = "give" if 5.6 < t < 6.6 else ("beggar" if 6.6 <= t < 8.0 else None)
            if t > 9.0:
                u = prog(t, 9.0, 9.9)
                tp = mix(t_hand, t_pull, u)
            if t > 10.2:
                tx, twa, _ = track(t, [(10.3, KX), (10.9, KX - 22)])
                tp = keyed([(10.2, t_pull), (10.9, pose("stand", head=-10, lean=-6)), (11.4, pose("stand", head=-10, lean=-6)),
                            (12.0, t_awe)], t)
        TJ = None
        if tx < OFF - 20:
            TJ = draw_figure(cr, tx, gy, tp, s=1.0, face=tface)

        # ---------------- basket and bread ----------------
        if basket_at == "hand" and TJ is not None:
            hx, hy = TJ["rhand"]
            n = 1 if (i == 1 and 5.6 < t < 8.1) else 2
            food_basket(cr, hx + 4, hy + 26, w=40, h=26, loaves=n)
        elif basket_at == "ground":
            n = 1 if t > 5.7 else 2
            food_basket(cr, BASKET_X, gy, w=40, h=26, loaves=n)
        if loaf_at == "lhand" and TJ is not None:
            hx, hy = TJ["lhand"]
            loaf(cr, hx + 2, hy - 6)
        elif loaf_at == "give" and TJ is not None:
            hx, hy = TJ["rhand"]
            u = prog(t, 5.6, 6.0)
            loaf(cr, lerp(BASKET_X, hx, u), lerp(gy - 30, hy - 6, u))
        elif loaf_at == "beggar":
            hx, hy = BJ["rhand"]
            loaf(cr, hx, hy - 6)


OUTPUT_NAME = "day41b_sheep_and_goats_matthew25"
