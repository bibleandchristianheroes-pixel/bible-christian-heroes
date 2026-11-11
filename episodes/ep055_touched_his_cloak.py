import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CROWD = (0.50, 0.48, 0.45)
OFFS = [-78, -40, 52, 96]      # crowd around him (relative x)

class TouchedHisCloak(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MARK 5  •  THE WOMAN WHO TOUCHED HIS CLOAK"
    headline = "A crowd pressed around him.\nOne touch changed everything."
    captions = [
        (cpdv("Mark", 5, 28, "For she said: “Because if I touch even his garment, I will be saved.”"), "Mark 5:28", 6.4),
        (cpdv("Mark", 5, 27, "…she approached through the crowd behind him, and she touched his garment."), "Mark 5:27", 9.0),
        (cpdv("Mark", 5, 34, "…“Daughter, your faith has saved you. Go in peace…"), "Mark 5:34", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        jx = keyed([(0.4, {"x": 360}), (9.0, {"x": 620})], t)["x"]
        moving = 0.4 < t < 9.0
        touch = prog(t, 8.7, 9.2) * (1 - prog(t, 10.2, 11.2)) if i >= 1 else 0.0
        healed = prog(t, 8.8, 9.6) if i >= 1 else 0.0
        warm_glow(cr, jx - 20, gy - 50, 170, touch)
        if i == 2:
            warm_glow(cr, jx - 40, gy - 110, 320, prog(t, 12.0, 13.4))

        # ---------- crowd ----------
        for k, o in enumerate(OFFS):
            ox = o
            if i == 2 and k < 2:
                ox = lerp(o, (-210, 150)[k], prog(t, 9.8 + 0.3 * k, 11.0 + 0.3 * k))
            cx = jx + ox
            stepping = moving or (i == 2 and k < 2 and 9.8 < t < 11.3)
            cf = 1 if not (i == 2 and k == 0 and t > 9.8) else -1
            cp = pose("stand", head=(4 if k % 2 else -4), lean=3)
            if i == 2 and t > 11.2: cp = pose("stand", head=-4)
            draw_figure(cr, cx, gy, body(t + k * 0.31, cp, 1.0 if stepping else 0.0, speed=0.9), s=0.94 + 0.04 * (k % 2), face=cf, color=CROWD)

        # ---------- Jesus ----------
        jface = 1
        jp = pose("stand")
        if i == 2 and t >= 9.4:
            jface = -1 if t >= 9.8 else 1
            jp = keyed([(9.8, pose("stand", head=-6)), (10.4, pose("stand", head=8)), (11.2, pose("stand", head=14)),
                        (11.8, pose("stand", rs=70, re=-10, head=12)), (12.8, pose("stand", rs=70, re=-10, head=12)), (13.6, pose("stand", rs=40, re=20, head=0))], t)
        draw_figure(cr, jx, gy, body(t, jp, 1.0 if moving else 0.0, speed=0.9), s=1.05, face=jface, prop="robe")

        # ---------- the woman ----------
        col = tuple(lerp(SOFT[j], INK[j], healed) for j in range(3))
        gap = keyed([(0.4, {"x": 300}), (6.0, {"x": 125})], t)["x"]
        stoop = pose("stand", lean=16, head=20, rs=20, re=30, ls=15, le=30)
        reach = pose("stand", lean=12, head=-4, rs=88, re=-5, ls=15, le=20)
        crawl = pose("kneel", lean=42, head=10, rs=95, re=-10, ls=60, le=10)
        moving_w = t < 6.0
        keys = [(5.6, stoop), (6.2, reach)]
        if i >= 1:
            gap = keyed([(0.4, {"x": 300}), (6.0, {"x": 125}), (7.4, {"x": 125}), (8.6, {"x": 88 + (jx - keyed([(0.4, {"x": 360}), (9.0, {"x": 620})], 8.6)["x"]) * 0})], t)["x"]
            keys = [(5.6, stoop), (6.2, reach), (7.0, reach), (7.6, crawl)]
            if i == 1:
                stand_up = pose("stand", lean=-4, head=-6, rs=40, re=115, ls=35, le=118)
                keys += [(9.6, crawl), (10.4, stand_up)]
                if t > 9.6: gap = keyed([(9.6, {"x": gap}), (10.4, {"x": 150})], t)["x"]
            else:
                tremble = pose("kneel", lean=30, head=35, rs=40, re=115, ls=35, le=118)
                rise = pose("stand", lean=-4, head=-10, rs=60, re=10, ls=55, le=15)
                keys += [(9.4, crawl), (10.2, tremble), (12.8, tremble), (13.6, rise), (14.4, pose("joy"))]
        p = keyed(keys, t)
        if i == 2 and 10.2 < t < 12.8:
            p["lean"] += 2.5 * math.sin(t * 22)
        wx = jx - gap
        if i == 1 and t > 9.6:
            wx = 620 - gap
        if i == 2 and t >= 9.0:
            wx = 620 - 88
        J = draw_figure(cr, wx, gy, body(t, p, 1.0 if moving_w else 0.0, speed=1.0), s=0.92, face=1, prop="robe", color=col)
        veil_drape(cr, J, s=0.92, face=1, color=col)

OUTPUT_NAME = "day28a_touched_his_cloak_mark5"
