import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HILL = (0.80, 0.77, 0.71)
TIRE_X = 470        # where all three start to flag
STOP_X = 560        # where P1 / P3 stop, spent
TRIP_X = 600        # P2 trips here
GOAL_X = 870        # P3 runs on to here

r_tired = dict(lean=26, head=22, rs=10, re=40, ls=5, le=40)          # arms hanging while staggering
knees = pose("stand", lean=58, head=-6, rs=48, re=-20, ls=40, le=-20, lt=10, lk=24, rt=-6, rk=24)   # hands on knees
k_spent = pose("kneel", lean=34, head=30, rs=20, re=20, ls=15, le=20)
slump = ground_sit_pose(lean=34, head=38, ls=45, le=10, rs=50, re=10)   # sits down in the dust, done
k_hope = pose("kneel", lean=-6, head=-24, rs=140, re=-20, ls=128, le=-20)
wings = pose("stand", lean=-6, head=-18, rs=150, re=-8, ls=128, le=-8)  # arms spread like wings


class WingsLikeEagles(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "ISAIAH 40  •  WINGS LIKE EAGLES"
    headline = "Everyone runs out of strength.\nNot everyone gets up."
    captions = [
        (cpdv("Isaiah", 40, 30, "Servants will struggle and fail…"), "Isaiah 40:30", 5.6),
        (cpdv("Isaiah", 40, 30, "…and young men will fall into infirmity."), "Isaiah 40:30", 4.8),
        (cpdv("Isaiah", 40, 31, "But those who hope in the Lord will renew their strength. They will take up wings like eagles."), "Isaiah 40:31", 8.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        mountain(cr, 700, gy, w=430, h=200, color=HILL)
        for gx in (90, 330, 700):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        hope = prog(t, 6.4, 7.6) if i == 2 else 0.0

        # ---------------- the runner ----------------
        x, wa, _ = track(t, [(0.0, -70), (3.0, TIRE_X)])
        p = run(t, speed=2.4)
        fallen = None
        if i == 1:
            # he digs in and sprints harder ... and goes down
            if t >= 3.0:
                x, wa, _ = track(t, [(3.0, TIRE_X), (4.0, TRIP_X)])
                p = run(t, speed=3.2, amp=48); p["lean"] = 22
            if t >= 4.0:
                fallen = prog(t, 4.0, 4.5)
                x = TRIP_X + 60 * fallen
        elif t >= 3.0:
            x, wa, _ = track(t, [(3.0, TIRE_X), (4.6, STOP_X)])
            if t < 4.6:            # staggering, slowing down
                p = walk(t, speed=1.1, amp=20)
                p.update({k: lerp(run(t)[k] if k in r_tired else 0, v, prog(t, 3.0, 3.6)) for k, v in r_tired.items()})
                p["lean"] += 4 * math.sin(t * 7)
            else:
                keys = [(4.6, pose("stand", **r_tired)), (5.1, knees), (5.9, knees), (6.5, k_spent)]
                if i == 0:
                    keys += [(7.3, k_spent), (8.2, slump)]
                else:
                    keys += [(7.0, k_spent), (7.8, k_hope), (9.2, k_hope), (9.8, pose("stand", head=-10))]
                p = keyed(keys, t)
                if t < 6.5:        # heaving breath
                    p["lean"] += 3 * math.sin(t * 9)
                if i == 2 and t >= 9.9:
                    # renewed: he runs on, light and fast, to the hilltop
                    x, wa, _ = track(t, [(9.9, STOP_X), (11.6, GOAL_X)])
                    if t < 11.6:
                        p = run(t, speed=2.6, amp=44); p["lean"] = 10; p["head"] = -10
                        p["rs"], p["re"], p["ls"], p["le"] = 70, 20, 62, 20     # arms opening out
                    else:
                        p = keyed([(11.6, pose("stand", lean=4, head=-10, rs=70, re=20, ls=62, le=20)), (12.4, wings)], t)

        if hope > 0:
            warm_glow(cr, x, gy - 110, 330, 0.8 * hope)
        if fallen is None:
            J = draw_figure(cr, x, gy, p, s=1.0, face=1)
        else:
            fp = mix(pose("stand", lean=30, head=-10, rs=150, re=20, ls=140, le=20),
                     pose("lie", ls=170, le=0, rs=165, re=0, head=0), fallen)
            J = draw_rotated(cr, x, gy, 90 * fallen, fp, s=1.0, face=1, lift=19 * fallen)

        # ---------------- the eagle (panel 3) ----------------
        if i == 2 and t > 7.0:
            u = prog(t, 7.0, 10.0)
            ex = lerp(1200, 900, u); ey = lerp(y0 + 80, y0 + 140, u)
            if t > 10.0:                      # circling over him
                a = (t - 10.0) * 1.3
                ex = 900 + 60 * math.sin(a) * prog(t, 10.0, 11.0); ey = y0 + 140 + 14 * math.cos(a) * prog(t, 10.0, 11.0)
                ex = lerp(ex, GOAL_X + 60, prog(t, 11.0, 12.5)); ey = lerp(ey, y0 + 105, prog(t, 11.0, 12.5))
            flap = 0.35 * math.sin(t * 4.0) * (1 - prog(t, 8.5, 9.5)) + 0.15 * math.sin(t * 1.6)
            eagle(cr, ex, ey, flap, s=0.62, face=-1)


OUTPUT_NAME = "day38a_wings_like_eagles_isaiah40"
