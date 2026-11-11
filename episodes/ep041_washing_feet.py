import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JX0 = 190                      # Jesus' stool
DISC = [690, 820, 950]         # seated disciples (facing left)
TABLE = (270, 520)
BASIN0 = 600
KNEEL = pose("kneel", lean=50, head=35, rs=22, re=5, ls=16, le=8)
def washp(t):
    return dict(KNEEL, rs=14 + 20 * (0.5 + 0.5 * math.sin(t * 9)), ls=10 + 20 * (0.5 + 0.5 * math.sin(t * 9 + 1.6)))

class WashingFeet(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JOHN 13  •  WASHING FEET"
    headline = "The Teacher got up from the table\nand knelt at their feet."
    captions = [
        (cpdv("John", 13, 4, "he rose up from the meal, and he set aside his vestments, and when he had received a towel, he wrapped it around himself."), "John 13:4", 4.6),
        (cpdv("John", 13, 5, "…he began to wash the feet of the disciples and to wipe them with the towel…"), "John 13:5", 9.0),
        (cpdv("John", 13, 15, "For I have given you an example, so that just as I have done for you, so also should you do."), "John 13:15", 12.4),
    ]

    def jesus(self, cr, i, t, gy):
        """Returns (x, pose, face, mantle_state, towel, holding) for Jesus."""
        stand = pose("stand")
        seated = sit_pose(rs=60, re=60, ls=50, le=60)
        mantle = "on" if t < 3.3 else ("hand" if t < 4.0 else "stool")
        x, wa, d = track(t, [(2.3, JX0), (2.9, 270), (4.4, 270), (5.4, 545)])
        face = 1
        arms_up = pose("stand", rs=165, re=20, ls=160, le=25, head=-8)
        lay = pose("stand", lean=38, head=25, rs=70, re=0, ls=40, le=10, lt=20, lk=25, rt=-5, rk=25)
        wrap_ = pose("stand", rs=35, re=95, ls=30, le=95, head=12)
        p = keyed([(1.4, seated), (2.2, stand), (3.0, stand), (3.3, arms_up), (3.5, pose("stand", rs=60, re=10)),
                   (3.7, lay), (4.0, lay), (4.3, stand), (4.6, wrap_), (5.0, wrap_), (5.3, stand)], t)
        if 2.95 < t < 4.2: face = -1
        holding = None
        if t >= 5.4:
            pour = pose("reach", rs=78, re=-10, ls=20, le=20, head=15)
            p = keyed([(5.4, stand), (5.9, pose("stand", lean=30, head=20, rs=55, re=0)), (6.3, pour), (7.4, pour), (7.8, stand)], t)
            holding = "pitcher" if 5.9 <= t < 7.8 else None
        kneel = KNEEL
        if i == 0 and t >= 7.8:
            hold = pose("stand", rs=40, re=80, ls=35, le=85, head=6)
            p = keyed([(7.8, stand), (8.5, pose("stand", lean=35, head=20, rs=60, re=0, ls=55, le=0)), (9.0, hold)], t)
            x, wa, _ = track(t, [(9.2, 545), (10.4, 590)])
            holding = "basin" if t >= 8.6 else None
        elif i >= 1 and t >= 7.8:
            x, wa, _ = track(t, [(7.8, 545), (8.3, 582)] + ([(11.0, 582), (11.8, 712)] if i == 1 else [(10.5, 582), (11.3, 470)]))
            wash = washp
            if i == 1:
                if t < 11.0:
                    p = keyed([(7.8, stand), (8.5, kneel)], t)
                    if t > 8.6: p = wash(t)
                elif t < 12.2:
                    p = keyed([(11.0, kneel), (11.4, stand), (11.8, stand), (12.2, kneel)], t)
                else:
                    p = wash(t)
            else:
                if t < 10.4:
                    p = keyed([(7.8, stand), (8.5, kneel)], t)
                    if t > 8.6: p = wash(t)
                else:
                    show = pose("stand", rs=95, re=-15, ls=20, le=15, head=-4)
                    p = keyed([(10.4, kneel), (10.9, stand), (11.4, stand), (11.9, show)], t)
            if wa > 0.05: p = body(t, stand, wa)
        else:
            p = body(t, p, wa if t < 5.4 else 0)
        if t < 5.4: p = body(t, p, wa)
        return x, p, face, mantle, prog(t, 4.4, 5.0), holding

    def draw_panel(self, cr, i, t, y0, gy):
        tt = meal_table(cr, *TABLE, gy, h=66)
        loaf(cr, 340, tt - 9); cup(cr, 430, tt)
        bench(cr, 625, 1020, gy, h=48)
        cr.set_source_rgb(*INK); cr.rectangle(JX0 - 26, gy - 50, 52, 9); cr.fill()   # stool
        cr.set_line_width(6); cr.move_to(JX0 - 18, gy - 40); cr.line_to(JX0 - 18, gy); cr.stroke()
        cr.move_to(JX0 + 18, gy - 40); cr.line_to(JX0 + 18, gy); cr.stroke()

        x, p, face, mantle, towel, holding = self.jesus(cr, i, t, gy)
        if mantle == "stool": folded_cloth(cr, JX0, gy - 50, w=64, h=20)

        # basin position / water
        bx = BASIN0
        if i == 1:
            bx = lerp(BASIN0, 648, prog(t, 8.1, 8.6)); bx = lerp(bx, 778, prog(t, 11.3, 12.0))
        elif i == 2:
            bx = lerp(BASIN0, 648, prog(t, 8.1, 8.6)); bx = lerp(bx, 778, prog(t, 12.2, 12.9))
        water_lvl = prog(t, 6.4, 7.4)

        # disciples
        dj = []
        for k, dx in enumerate(DISC):
            dp = sit_pose(ls=-12, le=4, rs=-8, re=6, head=4)
            watch = prog(t, 3.2, 3.8)
            dp["head"] = 4 + 14 * watch
            ddx, dface, dg = dx, -1, gy
            if i == 2 and k == 0 and t > 11.8:
                stand_ = pose("stand")
                kneel_ = KNEEL
                xx, wa, _ = track(t, [(12.0, dx), (12.6, 712)])
                dp = keyed([(11.8, dp), (12.2, stand_), (12.6, stand_), (13.1, kneel_)], t)
                if t > 13.2:
                    dp = washp(t)
                dp = body(t, dp, wa); ddx = xx; dface = 1
            draw_figure(cr, ddx, dg, dp, s=1.1, face=dface)

        if holding != "basin":
            basin(cr, bx, gy, water_lvl=water_lvl)
        # pitcher sits on the table end until lifted, then on the floor
        J = draw_figure(cr, x, gy, p, s=1.15, face=face, prop="robe")
        if mantle == "on":   # outer mantle over the back, then the figure again on top
            cape(cr, J, face=face, s=1.15)
            J = draw_figure(cr, x, gy, p, s=1.15, face=face, prop="robe")
        if mantle == "hand":
            hanging_cloth(cr, J["rhand"][0], J["rhand"][1] - 4, sway=4 * math.sin(t * 6))
        towel_wrap(cr, J, face=face, s=1.15, amount=towel)
        if holding == "pitcher":
            hx, hy = J["rhand"]
            tilt = 70 * prog(t, 6.2, 6.6) * (1 - prog(t, 7.3, 7.7))
            sp = pitcher(cr, hx - 4, hy + 30, tilt=tilt, face=1)
            if 6.5 < t < 7.4:
                cr.set_source_rgba(0.45, 0.62, 0.75, 0.9); cr.set_line_width(4)
                cr.move_to(*sp); cr.curve_to(sp[0] + 6, sp[1] + 10, bx + 4, gy - 40, bx + 4, gy - 18); cr.stroke()
        elif t < 5.9:
            pitcher(cr, 495, tt)
        else:
            pitcher(cr, 520 if i else 500, gy)
        if holding == "basin":
            hx, hy = J["rhand"]
            basin(cr, hx - 14, hy + 16, water_lvl=1.0)
        # water drops while washing
        washing = (i == 1 and (8.6 < t < 11.0 or t > 12.3)) or (i == 2 and (8.6 < t < 10.4)) or (i == 2 and t > 13.2)
        if washing:
            cr.set_source_rgba(0.45, 0.62, 0.75, 0.9)
            for k in range(5):
                u = (t * 2.3 + k / 5.0) % 1.0
                cr.arc(bx - 14 + k * 7 + 6 * math.sin(k * 3), gy - 30 - 22 * math.sin(math.pi * u) + 10 * u, 2.4, 0, 2 * math.pi); cr.fill()

OUTPUT_NAME = "day21a_washing_feet_john13"
