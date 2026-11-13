import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

TX = 330        # Thomas, facing right
JX = 560        # where Jesus appears, facing left
D1, D2 = 640, 730   # the other disciples, facing left
DOOR = 930

arms_x = pose("stand", rs=38, re=-132, ls=34, le=-128, head=-8, lean=-4)   # arms crossed, chin up
cheer = pose("stand", rs=150, re=-10, ls=128, le=10, head=-12, lean=-4)
point_up = pose("stand", rs=160, re=0, ls=20, le=20, head=-14)
show_hands = pose("stand", rs=72, re=-14, ls=62, le=-10, head=4)
reach = pose("stand", lean=12, head=6, rs=84, re=-4, ls=20, le=30)
kneel_lord = pose("kneel", lean=8, head=-14, rs=150, re=-20, ls=140, le=-15)


def light_fade(t, t0, t1, col=INK):
    u = prog(t, t0, t1)
    return tuple(lerp(BG[k], col[k], u) for k in range(3)), u


class DoubtingThomas(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "JOHN 20  •  DOUBTING THOMAS"
    headline = "Doubt crossed its arms.\nThen Jesus showed his hands."
    captions = [
        (cpdv("John", 20, 25, "…“Unless I will see in his hands the mark of the nails… I will not believe.”"), "John 20:25", 5.2),
        (cpdv("John", 20, 27, "…“Look at my hands, and place your finger here… do not choose to be unbelieving, but faithful."), "John 20:27", 8.2),
        (cpdv("John", 20, 28, "Thomas responded and said to him, “My Lord and my God.”"), "John 20:28", 10.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        arched_window(cr, 60, gy - 120, w=70, h=110)
        barred_door(cr, DOOR, gy)

        appear = prog(t, 6.0, 7.4) if i >= 1 else 0.0
        if appear > 0:
            warm_glow(cr, JX, gy - 110, 260 * appear, appear * (0.9 if i == 2 and t > 10.6 else 0.7))
            if i == 2:
                warm_glow(cr, JX - 60, gy - 90, 360, prog(t, 10.6, 12.0))

        # ---------------- the other disciples ----------------
        for k, (dx0, base) in enumerate(((D1, cheer), (D2, point_up))):
            keys = [(0.4, pose("stand")), (1.2, base), (3.6, base), (4.4, pose("stand", head=6 + 4 * k))]
            dx = dx0
            if i >= 1:
                keys += [(6.2, pose("stand", head=6)), (6.8, pose("stand", head=-10, lean=-6, rs=30, re=20))]
                dx = lerp(dx0, dx0 + 70, prog(t, 6.2, 7.2))
                if i == 2:
                    keys += [(11.4, pose("stand", head=-10, lean=-6, rs=30, re=20)), (12.4, pose("kneel", head=28, lean=10, rs=20, re=30, ls=15, le=30))]
            else:
                keys += [(6.0, pose("stand", head=14 + 4 * k)), (7.0, pose("stand", head=24, lean=6))]
            p = keyed(keys, t)
            if t < 4.0:
                p["lean"] += 3 * math.sin(t * 9 + k)       # excited
            draw_figure(cr, dx, gy, p, s=0.95 - 0.03 * k, face=-1)

        # ---------------- Jesus (appears in panels 2-3) ----------------
        if appear > 0:
            col, u = light_fade(t, 6.0, 7.4)
            jp = keyed([(7.0, pose("stand", head=-4)), (7.8, show_hands)], t)
            J = draw_figure(cr, JX, gy, jp, s=1.04, face=-1, prop="robe", color=col)
            wound_marks(cr, J, s=1.04, amount=prog(t, 7.6, 8.2), glow=prog(t, 7.6, 8.4) * 0.8)

        # ---------------- Thomas ----------------
        tface = 1; tx = TX
        keys = [(0.4, pose("stand", head=4)), (1.6, pose("stand", head=-2)), (2.4, arms_x)]
        if i == 0:
            keys += [(4.6, arms_x), (5.2, pose("stand", rs=38, re=-132, ls=34, le=-128, head=10, lean=2))]
            if t > 4.8:
                tface = -1
                tx, wa, _ = track(t, [(4.8, TX), (6.8, TX - 140)])
                p = keyed(keys, t)
                p = body(t, p, wa * 0.8, speed=1.2) if wa > 0.05 else p
                if wa > 0.05:      # keep the arms folded while walking
                    for k_ in ("rs", "re", "ls", "le"): p[k_] = arms_x[k_]
                draw_figure(cr, tx, gy, p, s=0.97, face=tface)
                return
        else:
            keys += [(6.0, arms_x), (6.6, pose("stand", rs=38, re=-132, ls=34, le=-128, head=-8, lean=-8)),
                     (8.4, pose("stand", head=-6, lean=-6, rs=10, re=10, ls=10, le=10)),
                     (9.0, pose("stand", head=-4, rs=20, re=10)), (9.8, reach)]
            if i == 2:
                keys += [(10.2, reach), (10.9, kneel_lord)]
            tx = keyed([(9.0, {"x": TX}), (9.8, {"x": TX + 110})], t)["x"]
        p = keyed(keys, t)
        if t < 4.4:
            p["head"] += (4 * math.sin(t * 10)) * prog(t, 3.0, 3.4) * (1 - prog(t, 4.0, 4.4))   # shakes his head
        draw_figure(cr, tx, gy, p, s=0.97, face=tface)


OUTPUT_NAME = "day30b_doubting_thomas_john20"
