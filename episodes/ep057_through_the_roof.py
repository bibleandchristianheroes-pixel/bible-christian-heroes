import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CROWD = (0.50, 0.48, 0.45)
FAR = (0.34, 0.32, 0.30)
HX0, HX1, RH = 560, 1040, 190          # house walls and height
HOLE = (795, 965)
JX = 690                               # Jesus inside
SPACING = 200                          # back bearer = front - SPACING
CROWD_X = [(468, 1), (516, 1), (578, 1)]   # packed in and around the doorway


class ThroughTheRoof(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MARK 2  •  THE HEALING THROUGH THE ROOF"
    headline = "The door was blocked.\nThey went through the roof."
    captions = [
        (cpdv("Mark", 2, 4, "And when they were not able to present him to him because of the crowd…"), "Mark 2:4", 5.4),
        (cpdv("Mark", 2, 5, "Then, when Jesus had seen their faith, he said to the paralytic, “Son, your sins are forgiven you.”"), "Mark 2:5", 12.0),
        (cpdv("Mark", 2, 12, "And immediately he got up, and lifting up his stretcher…they all wondered…"), "Mark 2:12", 13.4),
    ]

    # ---------- helpers ----------
    def stair_y(self, x, gy, i):
        """Hidden stairs behind the house (panels 2-3): ground rises from x 600 to 790."""
        if i == 0: return gy
        return gy - RH * smooth((x - 600) / 190.0)

    def front_x(self, t, i):
        if i == 0:
            return track(t, [(0.4, -190), (4.0, 410)])
        return track(t, [(0.4, -190), (4.0, 410), (5.0, 410), (8.2, 985)])

    def draw_panel(self, cr, i, t, y0, gy):
        ry = gy - RH
        fx, fwa, _ = self.front_x(t, i)
        bx = fx - SPACING

        # ---------------- bearers ----------------
        carry_f = pose("stand", rs=-28, re=-8, ls=-20, le=-6)      # front man: hands behind him
        carry_b = pose("stand", rs=52, re=10, ls=45, le=12)        # back man: hands in front
        kneel_f = pose("kneel", rs=40, re=10)
        kneel_b = pose("kneel", rs=40, re=10)
        dig = 0.5 + 0.5 * math.sin(t * 9)
        faces = [1, 1, 1, 1]          # near back, near front, far back, far front
        if i == 0:
            sad = pose("stand", head=32, lean=10, rs=4, re=6, ls=2, le=6)
            kb = [(4.0, carry_b), (4.6, dict(carry_b, head=-14)), (5.0, dict(carry_b, head=-14)), (5.6, kneel_b), (6.8, kneel_b), (7.8, sad)]
            kf = [(4.0, carry_f), (4.6, dict(carry_f, head=-16)), (5.0, dict(carry_f, head=-16)), (5.6, kneel_f), (6.8, kneel_f), (7.8, sad)]
            pb, pf = keyed(kb, t), keyed(kf, t)
            xs = [bx, fx, bx + 16, fx + 16]
            ps = [pb, pf, dict(pb), dict(pf)]
            if t > 7.0:   # the front pair turn back toward the others
                faces[1] = faces[3] = -1
        else:
            xs = [bx, fx, bx + 16, fx + 16]
            pb = keyed([(9.8, carry_b), (10.3, kneel_b)], t)
            pf = keyed([(9.8, carry_f), (10.3, kneel_f)], t)
            if t > 9.85: faces[1] = -1
            # far pair: open the roof
            far_x = keyed([(8.2, {"b": bx + 16, "f": fx + 16}), (8.7, {"b": 818, "f": 942})], t) if t > 8.2 else {"b": bx + 16, "f": fx + 16}
            xs[2], xs[3] = far_x["b"], far_x["f"]
            if t > 8.2:
                faces[3] = -1
                digp = pose("kneel", rs=55 + 35 * dig, re=20, ls=45, le=20, head=25)
                hold = pose("kneel", rs=35, re=10, head=30)
                pk = keyed([(8.2, pose("stand")), (8.7, digp)], t) if t < 8.7 else (digp if t < 9.8 else keyed([(9.8, digp), (10.2, hold)], t))
                ps = [pb, pf, pk, dict(pk)]
            else:
                ps = [pb, pf, dict(pb), dict(pf)]
            if i == 2 and t > 13.8:          # joy on the roof
                j = prog(t, 13.8, 14.5)
                for k in range(4): ps[k] = mix(ps[k], pose("kneel", ls=150, le=10, rs=150, re=10, head=-15, lean=-5), j)

        moving = fwa > 0.05
        Js = [None] * 4
        for k in (2, 3, 0, 1):        # far pair first
            x = xs[k]; g = self.stair_y(x, gy, i)
            p = body(t + 0.27 * k, ps[k], fwa if moving else 0.0, speed=1.1)
            Js[k] = draw_figure(cr, x, g, p, s=0.85, face=faces[k], color=FAR if k >= 2 else INK)

        # ---------------- the stretcher and the paralysed man ----------------
        hb, hf = Js[0]["rhand"], Js[1]["rhand"]
        land = ((812, gy - 12), (952, gy - 12))
        drawn_late = False
        if i == 0:
            u = prog(t, 5.0, 5.8)
            a = (lerp(hb[0] + 6, 300 - 70, u), lerp(hb[1], gy - 10, u)) if t > 5.0 else (hb[0] + 6, hb[1])
            b = (lerp(hf[0] - 6, 300 + 70, u), lerp(hf[1], gy - 10, u)) if t > 5.0 else (hf[0] - 6, hf[1])
            if t > 5.8: a, b = (230, gy - 10), (370, gy - 10)
            self.man(cr, a, b, t, i)
        else:
            if t < 10.0:
                self.man(cr, (hb[0] + 6, hb[1]), (hf[0] - 6, hf[1]), t, i)
            else:
                drawn_late = True

        # ---------------- the house ----------------
        open_ = prog(t, 8.7, 9.8) if i else 0.0
        cutaway_house(cr, HX0, HX1, gy, h=RH, door=(HX0, HX0 + 12), hole=HOLE, open_=open_)
        if i:
            roof_tiles_pile(cr, 1024, ry, 6 * prog(t, 8.8, 9.8))

        # glow on the man once Jesus sees their faith
        if i and t > 11.6:
            warm_glow(cr, 880, gy - 40, 220, prog(t, 11.8, 12.8))

        if drawn_late:
            u = prog(t, 10.0, 11.8)
            # held above the hole, then let down on ropes
            sa = (lerp(808, land[0][0], u), lerp(ry - 52, land[0][1], u))
            sb = (lerp(958, land[1][0], u), lerp(ry - 52, land[1][1], u))
            for k, end in ((0, sa), (2, sa), (1, sb), (3, sb)):
                if not (i == 2 and t > 13.6):
                    hx, hy = Js[k]["rhand"]
                    rope(cr, hx, hy, end[0], end[1] - 4, color=FAR if k >= 2 else INK)
            self.man(cr, sa, sb, t, i)

        # ---------------- Jesus ----------------
        jp = pose("stand", head=6)
        if i:
            jp = keyed([(10.4, pose("stand", head=-14)), (11.2, pose("stand", head=8)), (11.8, pose("stand", head=14)),
                        (12.4, pose("stand", rs=72, re=-12, head=16)), (14.0, pose("stand", rs=72, re=-12, head=16)),
                        (14.8, pose("stand", rs=40, re=10, head=6))], t)
            if i == 1: jp = keyed([(10.4, pose("stand", head=-14)), (11.2, pose("stand", head=8)), (11.8, pose("stand", head=14)),
                                   (12.4, pose("stand", rs=72, re=-12, head=16))], t)
        draw_figure(cr, JX, gy, jp, s=0.92, face=1, prop="robe")

        # ---------------- the crowd at the door ----------------
        for k, (cx, cf) in enumerate(CROWD_X):
            cp = pose("stand", head=(4 if k % 2 else -4), lean=3)
            if i == 2 and t > 13.6:
                cp = mix(cp, pose("joy"), prog(t, 13.8 + 0.15 * k, 14.6 + 0.15 * k))
            draw_figure(cr, cx, gy, cp, s=0.85, face=cf, color=CROWD)

    def man(self, cr, a, b, t, i):
        """Stretcher from a (left) to b (right) with the man lying on it (feet to the right)."""
        if i == 2 and t > 12.6:
            self.man_rises(cr, t); return
        stretcher(cr, a[0] - 6, a[1], b[0] + 6, b[1])
        ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        cr.save(); cr.translate(b[0] - 4, b[1] - 9); cr.rotate(math.radians(-90 + ang))
        draw_figure(cr, 0, 0, pose("lie", ls=4, le=6, rs=8, re=4, head=-4), s=0.8)
        cr.restore()

    def man_rises(self, cr, t):
        gy = HEADER_H + 2 * PANEL_H + GROUND_OFF
        fx = 948
        # the mat stays on the floor until he picks it up
        pick = prog(t, 14.2, 14.8)
        if t < 14.4:
            stretcher(cr, 806, gy - 12, 958, gy - 12)
        rot = lerp(-90, 0, prog(t, 12.6, 13.6))
        lie = pose("lie", ls=4, le=6, rs=8, re=4, head=-4)
        if t < 13.6:
            cr.save(); cr.translate(fx - 4, gy - 21 * (1 - prog(t, 12.6, 13.6))); cr.rotate(math.radians(rot))
            draw_figure(cr, 0, 0, mix(lie, pose("stand"), prog(t, 12.6, 13.6)), s=0.8); cr.restore()
            return
        # standing, turns to Jesus, stoops for the mat, lifts it high
        stoop = pose("stand", lean=34, head=20, rs=60, re=10, ls=55, le=10, lt=20, lk=30, rt=10, rk=30)
        lifted = pose("joy", head=-14)
        p = keyed([(13.6, pose("stand")), (14.0, pose("stand", head=-6)), (14.4, stoop), (15.2, lifted)], t)
        J = draw_figure(cr, fx - 30 * prog(t, 13.6, 14.2), gy, p, s=0.8, face=-1)
        if t >= 14.4:
            u = prog(t, 14.4, 15.2)
            hx = (J["rhand"][0] + J["lhand"][0]) / 2; hy = min(J["rhand"][1], J["lhand"][1])
            rolled_mat(cr, hx, hy - 4 * u, ang=0, L=lerp(120, 64, u))


OUTPUT_NAME = "day29a_through_the_roof_mark2"
