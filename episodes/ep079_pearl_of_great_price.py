import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX = 105            # the merchant's house
GOODS = [(232, "sack", 7.8), (290, "stool", 8.5), (348, "lamp", 9.2)]    # x, kind, time sold (panel 3)
MX = 640            # where the merchant stops to look
TX = 790            # the trader's table
SX = 905            # the trader
OFF = 1190
HOME = 440          # where he goes back to (panel 2)
GOODS_STOP = 420    # where he stands to sell his goods (panel 3)

m_carry = pose("stand", rs=24, re=30, head=4)
m_look = pose("stand", rs=24, re=30, head=24, lean=8)                 # bends to look at the pearl
m_offer = pose("reach", rs=78, re=-6, head=6, lean=8)                 # holds out his purse
m_pull = pose("stand", rs=120, re=20, ls=70, le=-60, head=-12, lean=-6)   # purse held up, other palm out: "this much!"  # draws it back, other palm up: "come on"
m_push = pose("reach", rs=84, re=-4, ls=50, le=-40, head=0, lean=12)   # pushes it at him again
m_reach_after = pose("reach", rs=70, re=-10, head=-4, lean=10)
m_hang = pose("stand", rs=10, re=14, head=28, lean=6)
m_weigh = pose("stand", rs=44, re=66, head=26, lean=4)                 # looks down at the purse in his hand
m_hug = pose("stand", rs=34, re=96, ls=30, le=100, head=18, lean=4)    # purse held to his chest
m_receive = pose("reach", rs=72, re=-6, ls=66, le=-6, head=4, lean=6)
m_raise = pose("stand", rs=162, re=2, ls=152, le=8, head=-16, lean=-4)

t_hold = pose("stand", rs=14, re=20, ls=10, le=16)
t_show = pose("reach", rs=58, re=-24, head=12, lean=4)               # open palm toward the pearl
t_no = pose("reach", rs=88, re=-60, head=0, lean=-2)                  # flat palm up: no
t_lift = pose("reach", rs=60, re=-10, head=14, lean=8)
t_carry = pose("stand", rs=70, re=60, head=4)
t_take = pose("reach", rs=72, re=-6, ls=20, le=30, head=6, lean=6)
t_bless = pose("stand", rs=128, re=-14, ls=-30, le=20, head=-6, lean=-2)


class PearlOfGreatPrice(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 13  •  THE PEARL OF GREAT PRICE"
    headline = "Three men found the same pearl.\nOnly one gave everything."
    captions = [
        (cpdv("Luke", 14, 33, "…every one of you who does not renounce all that he possesses is not able to be my disciple."), "Luke 14:33", 9.4),
        (cpdv("Matthew", 6, 21, "For where your treasure is, there also is your heart."), "Matthew 6:21", 8.2),
        (cpdv("Matthew", 13, 46, "Having found one pearl of great value, he went away and sold all that he had, and he bought it."), "Matthew 13:46", 12.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        small_house(cr, HX, gy)
        sun(cr, 1000, gy - 300, r=22, rays=10)
        for gx in (470, 560, 1040):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))

        # ---------------- the goods by his house ----------------
        sold_amt = 0.0
        for gx, kind, ts in GOODS:
            gone = prog(t, ts, ts + 0.35) if i == 2 else 0.0
            sold_amt += gone
            if gone < 1:
                cr.push_group()
                if kind == "sack": grain_sack(cr, gx, gy, s=1.0)
                elif kind == "stool": plain_stool(cr, gx, gy, h=34, w=40)
                else: lamp(cr, gx, gy)
                cr.pop_group_to_source(); cr.paint_with_alpha(1 - gone)
            if i == 2 and ts - 0.1 < t < ts + 0.9:
                coin_glint(cr, gx, gy - 46, prog(t, ts - 0.1, ts + 0.2) * (1 - prog(t, ts + 0.5, ts + 0.9)), t=t, r=22)

        # ---------------- the trader's table and the pearl ----------------
        low_table(cr, TX, gy, w=120, h=50)
        top = pearl_stand(cr, TX, gy - 50, h=34)
        glow = 0.35 + 0.45 * prog(t, 2.6, 3.6)

        # ---------------- the trader ----------------
        tx, tface, twa = SX, -1, 0.0
        tp = keyed([(0.0, t_hold), (2.8, t_hold), (3.3, t_show), (4.4, t_show), (4.8, t_hold)], t)
        pearl_at = "stand"
        if t > 5.0:
            tp = keyed([(5.0, t_hold), (5.4, t_no), (6.0, t_no), (6.4, t_hold)], t)
        if i == 0 and t > 6.4:
            tp = keyed([(6.4, t_hold), (6.9, t_no), (8.4, t_no), (8.8, t_hold), (9.1, t_lift), (9.5, t_carry)], t)
            if 6.9 < t < 8.4:
                tp["head"] += 9 * math.sin(t * 9)              # shaking his head
            if t > 9.3:
                pearl_at = "trader"
            if t > 9.7:
                tx, twa, _ = track(t, [(9.7, SX), (11.9, OFF)]); tface = 1
                tp = body(t, t_carry, twa, speed=1.4)
        elif i == 2 and t > 11.4:
            tp = keyed([(11.4, t_hold), (11.9, t_take), (12.4, t_take), (12.6, t_lift), (12.9, t_lift),
                        (13.3, t_hold), (14.0, t_bless)], t)
            if 12.75 < t < 13.0:
                pearl_at = "trader"
            elif t >= 13.0:
                pearl_at = "merchant"
        TJ = None
        if tx < OFF - 20:
            TJ = draw_figure(cr, tx, gy, tp, s=1.05, face=tface, prop="robe_hat")
            if TJ is not None and tface == -1 and abs(tp["rs"] - t_no["rs"]) < 4 and tp["re"] < -50:
                stop_hand(cr, TJ, face=-1, s=1.0)

        # ---------------- the merchant ----------------
        mx, mface = MX, 1
        mx, mwa, _ = track(t, [(0.3, 380), (2.6, MX)])
        mp = body(t, keyed([(0.0, m_carry), (2.8, m_carry), (3.4, m_look), (4.4, m_look), (4.9, m_offer)], t), mwa, speed=1.4)
        bag_at, bag_s = "hand", 0.78
        if i == 0 and t > 5.4:
            mp = keyed([(5.4, m_offer), (5.9, m_pull), (6.5, m_push), (7.1, m_pull), (7.7, m_push), (8.3, m_pull),
                        (8.9, m_push), (9.4, m_push), (9.9, m_reach_after), (10.8, m_reach_after), (11.6, m_hang)], t)
        elif i == 1 and t > 5.4:
            mp = keyed([(5.4, m_offer), (5.9, m_weigh), (6.9, m_weigh), (7.3, m_hug)], t)
            if 6.2 < t < 6.9:
                mp["head"] += 8 * math.sin(t * 10)              # "no, too much"
            if t > 7.3:
                bag_at = "chest"
            if t > 7.5:
                mx, mwa, _ = track(t, [(7.6, MX), (9.9, HOME)]); mface = -1
                mp = body(t, keyed([(9.9, m_hug), (10.6, pose("stand", rs=34, re=96, ls=30, le=100, head=30, lean=6))], t),
                          mwa, speed=1.3)
        elif i == 2 and t > 5.4:
            mp = keyed([(5.4, m_offer), (5.8, m_carry), (6.2, pose("stand", rs=24, re=30, head=-10))], t)
            if 6.0 < t < 9.9:
                mx, mwa, _ = track(t, [(6.2, MX), (7.3, GOODS_STOP)]); mface = -1
                if t < 7.3 and t > 6.2:
                    mp = run(t, speed=2.2); mp["rs"], mp["re"] = 24, 30
                else:
                    mp = keyed([(7.3, m_carry), (7.6, pose("stand", rs=24, re=30, head=10))], t)
            elif t >= 9.9:
                mx, mwa, _ = track(t, [(9.9, GOODS_STOP), (11.5, MX + 40)])
                mp = body(t, keyed([(11.5, m_carry), (11.8, m_offer), (12.4, m_offer), (12.6, m_receive),
                                    (13.4, m_receive), (14.0, m_raise)], t), mwa, speed=1.5)
            bag_s = 0.78 + 0.5 * sold_amt / 3
            if t > 12.3:
                bag_at = "trader"
        MJ = draw_figure(cr, mx, gy, mp, s=1.0, face=mface)
        if i == 0 and 5.8 < t < 9.4:                         # haggling back and forth
            a = prog(t, 5.8, 6.1) * (1 - prog(t, 9.0, 9.4))
            cry_lines(cr, MJ["head"][0] + 16, MJ["head"][1], face=1, amount=a, size=0.9, t=t)
            if TJ is not None:
                cry_lines(cr, TJ["head"][0] - 16, TJ["head"][1], face=-1, amount=0.7 * a, size=0.8, t=t + 1.3)

        # ---------------- the purse ----------------
        if bag_at == "hand":
            hx, hy = MJ["rhand"]
            coin_bag(cr, hx, hy + 2, s=bag_s)
        elif bag_at == "chest":
            hx = (MJ["rhand"][0] + MJ["lhand"][0]) / 2; hy = min(MJ["rhand"][1], MJ["lhand"][1])
            coin_bag(cr, hx, hy - 4, s=bag_s)
        elif bag_at == "trader" and TJ is not None:
            u = prog(t, 12.3, 12.6)
            hx = lerp(MJ["rhand"][0], TJ["lhand"][0], u); hy = lerp(MJ["rhand"][1], TJ["lhand"][1], u)
            coin_bag(cr, hx, hy + 2, s=bag_s)

        # ---------------- the pearl ----------------
        if pearl_at == "stand":
            px, py = TX, top
            g = glow
        elif pearl_at == "trader" and TJ is not None:
            if i == 0:
                u = prog(t, 9.1, 9.5)
                px = lerp(TX, TJ["rhand"][0], u); py = lerp(top, TJ["rhand"][1] - 12, u)
            else:
                u = prog(t, 12.75, 13.0)
                px = lerp(TX, TJ["rhand"][0], u); py = lerp(top, TJ["rhand"][1] - 12, u)
            g = glow
        elif pearl_at == "merchant":
            u = prog(t, 13.0, 13.3)
            ax = TJ["rhand"][0] if TJ else TX; ay = (TJ["rhand"][1] - 12) if TJ else top
            hx = (MJ["rhand"][0] + MJ["lhand"][0]) / 2; hy = min(MJ["rhand"][1], MJ["lhand"][1]) - 16
            px, py = lerp(ax, hx, u), lerp(ay, hy, u)
            g = glow + 0.5 * prog(t, 13.6, 14.4)
        else:
            px = None
        if px is not None:
            if i == 1 and t > 8.0:
                g *= 1 - 0.35 * prog(t, 8.0, 10.0)
            pearl(cr, px, py, r=13, glow=g)
            if i == 2 and t > 13.6:
                light_rays(cr, px, py, 0.7 * prog(t, 13.6, 14.4), r0=34, r1=74, n=14, t=t)


OUTPUT_NAME = "day40a_pearl_of_great_price_matthew13"
