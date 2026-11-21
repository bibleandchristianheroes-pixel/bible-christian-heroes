import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

DOOR = 640                  # room door (left edge), 80 wide
SEAT = [230, 345, 460]      # disciples on the bench, facing the door
OUT = [480, 690, 805]       # P3: where they end up, in the doorway and out in the street
CROWD = [(895, 0.84), (965, 0.80), (1035, 0.82)]

sit_pray = sit_pose(lean=16, head=28, rs=72, re=88, ls=66, le=92)
sit_look = sit_pose(lean=0, head=-8, rs=50, re=60, ls=45, le=60)
sit_up = sit_pose(lean=-6, head=-22, rs=70, re=40, ls=60, le=40)
s_startle = pose("stand", lean=-10, head=-24, rs=150, re=30, ls=132, le=40)
s_awe = pose("stand", lean=-8, head=-22, rs=160, re=-6, ls=140, le=-6)
s_reach = pose("stand", lean=6, head=-4, rs=88, re=-10, ls=20, le=20)
s_preach = pose("stand", lean=2, head=-8, rs=142, re=-8, ls=68, le=-8)
s_open = pose("stand", lean=4, head=-6, rs=80, re=-14, ls=64, le=-14)
c_idle = pose("stand", head=6)
c_turn = pose("stand", lean=-4, head=-8, rs=60, re=40, ls=40, le=50)
c_wonder = pose("stand", lean=-6, head=-12, rs=140, re=20, ls=30, le=30)


class Pentecost(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    caption_bg = True
    kicker = "ACTS 2  •  PENTECOST"
    headline = "The door was barred.\nThen the wind came."
    captions = [
        (cpdv("Acts", 2, 1, "…they were all together in the same place."), "Acts 2:1", 4.2),
        (cpdv("Acts", 2, 2, "And suddenly, there came a sound from heaven, like that of a wind approaching violently…"), "Acts 2:2", 5.0),
        (cpdv("Acts", 2, 4, "And they were all filled with the Holy Spirit. And they began to speak in various languages…"), "Acts 2:4", 10.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        gust = 0.0
        if i >= 1:
            gust = prog(t, 4.4, 5.0) * (1 - 0.6 * prog(t, 8.0, 10.0))
        spirit = prog(t, 6.8, 8.0) if i == 2 else 0.0

        # ---------------- the city outside ----------------
        city_skyline(cr, 800, gy, s=0.78, color=STONE)
        bar = 1.0; opened = 0.0
        if i == 2:
            bar = 1 - prog(t, 8.6, 9.3); opened = prog(t, 9.3, 9.9)
        if opened > 0:
            warm_glow(cr, DOOR + 40, gy - 90, 260, 0.6 * opened)
        if spirit > 0:
            warm_glow(cr, 360, gy - 150, 420, 0.75 * spirit)
            light_rays(cr, 360, y0 + 20, 0.45 * spirit, r0=40, r1=120, n=14, t=t)

        lit = lampstand(cr, 80, gy, h=120)
        lamp(cr, 80, lit, lit=1.0 - 0.8 * gust, flicker=math.sin(t * 13))
        bench(cr, 180, 510, gy)

        # ---------------- the crowd in the street ----------------
        for k, (cx, cs) in enumerate(CROWD):
            face = 1 if k != 1 else -1
            p = dict(c_idle); p["head"] += 3 * math.sin(t * 0.9 + k)
            if i == 2 and t > 10.0 + 0.25 * k:
                face = -1
                p = keyed([(10.0 + 0.25 * k, c_idle), (10.6 + 0.25 * k, c_turn), (11.6 + 0.3 * k, c_wonder if k == 1 else c_turn)], t)
            draw_figure(cr, cx, gy, p, s=cs, face=face, prop="robe")

        room_door(cr, DOOR, gy, open_=opened, bar=bar)

        # ---------------- the disciples ----------------
        for k in range(3):
            x = SEAT[k]; face = 1; wa = 0.0
            keys = [(0.0, sit_pray)]
            if k == 2:      # the one nearest the door keeps glancing at it
                keys += [(1.4, sit_pray), (1.9, sit_look), (2.9, sit_look), (3.4, sit_pray)]
            else:
                keys += [(3.4, sit_pray)]
            if i == 0:
                if k == 2:
                    keys += [(3.6, sit_look), (4.2, pose("stand", head=-4)), (5.2, pose("stand", head=-4)), (5.6, s_reach), (6.6, s_reach),
                             (7.0, pose("stand", head=10)), (8.2, pose("stand", head=10)), (8.8, sit_pray)]
                    x, wa, dirn = track(t, [(4.2, SEAT[2]), (5.4, DOOR - 55), (7.0, DOOR - 55), (8.4, SEAT[2])])
                    if 6.9 < t < 8.5:
                        face = -1
                else:
                    keys += [(4.6 + k * 0.3, sit_pray), (5.2 + k * 0.3, sit_look), (6.2 + k * 0.3, sit_pray)]
            else:
                d = 0.15 * k
                keys += [(4.5 + d, sit_pray), (5.0 + d, sit_up), (5.6 + d, s_startle)]
                if i == 1:
                    keys += [(7.6 + d, s_startle), (8.4 + d, s_awe)]
                else:
                    keys += [(7.0 + d, s_startle), (7.8 + d, s_awe), (8.4 + d, s_awe)]
                    if k == 2:
                        keys += [(8.6, s_reach), (9.3, s_reach)]
                    keys += [(9.9 + d, pose("stand", head=-4)), (11.0 + d * 2, pose("stand", head=-4)),
                             (11.6 + d * 2, s_preach if k != 1 else s_open)]
                    x, wa, _ = track(t, [(9.8 + 0.2 * (2 - k), SEAT[k] if k != 2 else DOOR - 55), (11.2 + 0.2 * (2 - k), OUT[k])])
                    if k == 2 and t < 9.8:
                        x, wa, _ = track(t, [(7.9, SEAT[2]), (8.6, DOOR - 55)])
            p = keyed(keys, t)
            if wa > 0.05:
                arms = dict(p)
                p = body(t, pose("stand", head=p["head"], rs=p["rs"], re=p["re"], ls=p["ls"], le=p["le"]), wa, speed=1.3)
            if gust > 0 and t < 7.0:
                p["lean"] += 3 * gust * math.sin(t * 17 + k)
            J = draw_figure(cr, x, gy, p, s=0.96, face=face, prop="robe")
            if spirit > 0:
                u = prog(t, 6.8 + 0.25 * k, 7.8 + 0.25 * k)
                hx, hy = J["head"]
                fire_tongue(cr, hx, hy - 18 - 90 * (1 - u), t, amount=u, seed=k * 2.3, s=0.9)

        # ---------------- the wind ----------------
        if gust > 0:
            wind(cr, y0 + 40, t, 1.2 * gust)
            breeze(cr, 120 + 160 * ((t * 0.6) % 1), gy - 250, t, amount=gust * 0.8, length=220)


OUTPUT_NAME = "day38b_pentecost_acts2"
