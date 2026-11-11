import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

RX0 = 380           # where the broken ground begins
MX = 230            # the man with the map
READ = pose("stand", head=22, rs=55, re=75, ls=50, le=80)

class TrustInTheLord(Episode):
    dur = 18.0
    ground = False
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "PROVERBS 3  •  TRUST IN THE LORD"
    headline = "Your own map, or his hand?\nOnly one gets you home."
    captions = [
        (cpdv("Proverbs", 3, 5, "Have confidence in the Lord with all your heart, and do not depend upon your own prudence."), "Proverbs 3:5", 8.0),
        (cpdv("Proverbs", 3, 6, "In all your ways, consider him…"), "Proverbs 3:6", 7.8),
        (cpdv("Proverbs", 3, 6, "…and he himself will direct your steps."), "Proverbs 3:6", 10.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        smooth_ = prog(t, 8.2, 9.8) if i == 2 else 0.0
        rough = 1.0 - smooth_
        su = prog(t, 10.5, 14.0) if i == 2 else 0.0
        if su > 0:
            sun(cr, 1000, lerp(gy + 60, y0 + 230, su), r=26)
            cr.set_source_rgb(*BG); cr.rectangle(0, gy + 3, W, 120); cr.fill()
        ground_line(cr, gy, 0, RX0)
        rough_ground(cr, RX0, W + 10, gy, rough)
        gyx = lambda x: rough_y(x, RX0, gy, rough)

        # ---------------- the man and his map ----------------
        mx, mwa, _ = track(t, [(0, MX)])
        mface = 1
        p = dict(READ)
        if 1.6 < t < 4.2:   # turns the map, looks one way and the other
            p["head"] = 22 - 30 * prog(t, 2.4, 2.7) + 30 * prog(t, 3.5, 3.8)
            if 2.6 < t < 3.6: mface = -1
        map_ang = 0.5 * prog(t, 1.4, 2.0) - 0.5 * prog(t, 3.8, 4.2)
        map_state = "hand"; fold = 0.0
        JJ = None
        if i == 0:
            mx, mwa, _ = track(t, [(4.2, MX), (5.8, 440), (6.4, 440), (7.1, 330)])
            stumble = pose("stand", lean=-14, head=-20, ls=150, le=30, rs=160, re=20)
            if t >= 4.2:
                p = keyed([(4.2, READ), (5.8, READ), (6.1, stumble), (6.6, stumble), (7.2, pose("stand", head=10)),
                           (7.9, pose("sad_sit")), (8.6, pose("sad_sit", ls=150, le=150, rs=150, re=150, lean=10, head=28, lt=120, lk=150, rt=115, rk=145))], t)
                p = body(t, p, mwa)
                mface = 1 if t < 6.4 else -1
                if t > 7.1: mface = 1
                if t >= 6.0: map_state = "fall"
        else:
            # Jesus crosses the broken ground toward him
            jx, jwa, _ = track(t, [(3.6, 1150), (6.6, 362)])
            offer = pose("reach", rs=72, re=-8, head=6)
            jp = body(t, pose("stand"), jwa)
            jface = -1
            if t >= 6.6:
                jp = keyed([(6.6, pose("stand")), (7.0, offer)], t)
            if t >= 4.6:
                p = keyed([(4.6, p), (5.2, pose("stand", head=0, rs=55, re=75, ls=50, le=80)), (6.8, pose("stand", head=-4, rs=55, re=75, ls=50, le=80)),
                           (7.3, pose("stand", head=-4, rs=20, re=10, ls=15, le=10)), (7.8, pose("reach", rs=68, re=-6, head=-6))], t)
                fold = prog(t, 6.8, 7.2)
                if t >= 7.25: map_state = "drop"
            if i == 2 and t >= 9.6:
                jx, jwa, _ = track(t, [(9.6, 362), (10.0, 366), (14.2, 820)])
                mx, mwa, _ = track(t, [(9.6, MX), (10.0, MX + 44), (14.2, 728)])
                jface = 1 if t > 9.7 else -1
                lead = pose("stand", ls=-38, le=-6, rs=10, re=10, head=-4)
                follow = pose("stand", rs=48, re=-6, ls=10, le=10, head=-8)
                jp = body(t, lead, jwa); p = body(t, follow, mwa)
                jp["ls"] = -38; jp["le"] = -6; p["rs"] = 48; p["re"] = -6
                if t > 14.2:
                    jp = keyed([(14.2, lead), (14.8, lead)], t); p = keyed([(14.2, follow), (14.8, pose("stand", rs=48, re=-6, head=-14))], t)
            JJ = draw_figure(cr, jx, gyx(jx), jp, s=1.1, face=jface, prop="robe")

        if i == 0 and t > 7.1:
            MJ = draw_figure(cr, mx, gyx(mx), p, s=1.0, face=mface)
        else:
            MJ = draw_figure(cr, mx, gyx(mx), body(t, p, mwa) if i else p, s=1.0, face=mface)

        # the map
        if map_state == "hand":
            hx = (MJ["rhand"][0] + MJ["lhand"][0]) / 2; hy = (MJ["rhand"][1] + MJ["lhand"][1]) / 2
            held_map(cr, hx + mface * 4, hy - 10, ang=map_ang * mface, fold=fold)
        elif map_state == "fall":
            u = prog(t, 6.0, 6.7)
            held_map(cr, lerp(470, 520, u), lerp(gy - 150, gyx(520) - 6, u * u), ang=lerp(0, 2.4, u), h=lerp(34, 10, u))
        elif map_state == "drop":
            u = prog(t, 7.25, 7.7)
            fx = MX + 30
            held_map(cr, fx, lerp(gy - 110, gy - 6, u * u), ang=lerp(0, 1.57, u), fold=1.0, h=lerp(34, 12, u), alpha=1 - 0.6 * smooth_)

        # clasped hands
        if JJ is not None and t >= 7.8:
            a = MJ["rhand"]; b = JJ["lhand"] if (i == 2 and t > 9.7) else JJ["rhand"]
            if math.hypot(a[0] - b[0], a[1] - b[1]) < 100:
                cr.set_source_rgb(*INK); cr.set_line_width(8); cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.move_to(*a); cr.line_to(*b); cr.stroke()
                cr.arc((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 7, 0, 2 * math.pi); cr.fill()
        if i == 1:
            warm_glow(cr, 300, gy - 110, 240, prog(t, 8.0, 9.5))

OUTPUT_NAME = "day23b_trust_in_the_lord_proverbs3"
