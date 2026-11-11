import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

JS = 450                 # Jesus' stool
SEATS = [770, 880]       # the two disciples at table (facing left)
TABLE = (510, 700)

class RoadToEmmaus(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 24  •  THE ROAD TO EMMAUS"
    headline = "They walked with him for miles.\nThey knew him in the bread."
    captions = [
        (cpdv("Luke", 24, 15, "…while they were speculating and questioning within themselves, Jesus himself, drawing near, traveled with them."), "Luke 24:15", 4.0),
        (cpdv("Luke", 24, 30, "…he took bread, and he blessed and broke it, and he extended it to them."), "Luke 24:30", 8.6),
        (cpdv("Luke", 24, 32, "…“Was not our heart burning within us, while he was speaking on the way…?”"), "Luke 24:32", 12.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sad = pose("stand", head=26, lean=8)
        su = prog(t, 0, 16) if i == 0 else prog(t, 0, 6)
        sun(cr, 1000, lerp(y0 + 230, gy + 30, su), r=26)
        cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 120); cr.fill()
        if i == 0:
            rock_path_tufts(cr, gy, [140, 380, 610, 840, 1010])
        else:
            meal_table(cr, *TABLE, gy)
            bench(cr, 730, 930, gy)
            cr.set_source_rgb(*INK); cr.rectangle(JS - 24, gy - 44, 48, 9); cr.fill()
            cr.set_line_width(6); cr.move_to(JS - 16, gy - 40); cr.line_to(JS - 16, gy); cr.stroke()
            cr.move_to(JS + 16, gy - 40); cr.line_to(JS + 16, gy); cr.stroke()
            lit = prog(t, 5.0, 6.0)
            lp = lamp(cr, 650, gy - 58, lit=lit, flicker=t)

        # ---- the two disciples ----
        DJ = []
        for k in range(2):
            if i == 0:
                x, wa, _ = track(t, [(0, 70 + 95 * k), (9.6, 470 + 95 * k)])
                face = 1
                look = prog(t, 5.0, 6.0)
                p = mix(sad, pose("stand", head=-4), look)
                if t > 10.0:
                    face = -1 if k == 0 else 1
                    turn = pose("stand", head=-10)
                    p = keyed([(10.0, pose("stand")), (10.6, turn)], t)
                    if k == 1: face = -1
                p = body(t, p, wa, speed=1.2)
            else:
                x, wa, _ = track(t, [(0, 70 + 95 * k), (3.6, 230 + 95 * k), (6.0, SEATS[k] + 20), (6.4, SEATS[k])])
                face = 1 if t < 6.0 else -1
                p = body(t, sad, wa, speed=1.2 if t < 3.6 else 1.6)
                seat = sit_pose(head=6, rs=40, re=40, ls=30, le=40)
                recv = sit_pose(head=-6, rs=78, re=-5, ls=30, le=40, lean=8)
                if t >= 6.0:
                    p = keyed([(6.0, pose("stand")), (6.6, seat), (8.9, seat), (9.4, recv if k == 0 else seat)], t)
                if i == 2 and t >= 11.0:
                    wonder = pose("stand", head=-14, rs=30, re=125, ls=20, le=120)
                    p = keyed([(11.0, p), (11.6, pose("stand", head=-10)), (12.1, wonder)], t)
                    face = 1 if k == 0 else -1
                    x = SEATS[k] + (-30 if k == 0 else 25) * prog(t, 11.0, 11.6)
            J = draw_figure(cr, x, gy, p, s=1.0, face=face)
            DJ.append(J)
            if i == 2:
                g = prog(t, 11.9, 13.2)
                if g > 0:
                    cx = lerp(J["sh"][0], J["hip"][0], 0.3); cy = lerp(J["sh"][1], J["hip"][1], 0.25)
                    warm_glow(cr, cx, cy, 120, g)
                    cr.set_source_rgba(1, 0.62, 0.22, 0.95 * g); cr.arc(cx, cy, 6 + 1.5 * math.sin(t * 6), 0, 2 * math.pi); cr.fill()

        # ---- the stranger ----
        if i == 0:
            jx, jwa, _ = track(t, [(1.0, -90), (3.8, 0), (9.6, 320)])
            explain = lambda tt: pose("stand", rs=45 + 15 * math.sin(tt * 3), re=-25, ls=15, le=10)
            jp = body(t, explain(t) if 4.5 < t else pose("stand"), jwa, speed=1.2 if t > 3.8 else 1.7)
            draw_figure(cr, jx, gy, jp, s=1.1, face=1, prop="robe")
        else:
            jx, jwa, _ = track(t, [(1.0, -90), (3.6, 135), (6.0, JS - 20), (6.4, JS)])
            jp = body(t, pose("stand"), jwa, speed=1.2 if t < 3.6 else 1.6)
            bless = sit_pose(head=-14, rs=150, re=10, ls=145, le=12)
            brk = sit_pose(head=-6, rs=115, re=5, ls=70, le=10)
            give = sit_pose(head=0, rs=82, re=-4, ls=40, le=30, lean=6)
            if t >= 6.0:
                jp = keyed([(6.0, pose("stand")), (6.6, sit_pose(rs=55, re=40, ls=50, le=40)), (7.2, sit_pose(rs=55, re=40, ls=50, le=40)),
                            (7.8, bless), (8.3, bless), (8.7, brk), (9.0, brk), (9.5, give)], t)
            fade = prog(t, 10.0, 11.3) if i == 2 else 0.0
            col = tuple(lerp(INK[j], BG[j], fade) for j in range(3))
            if fade < 1:
                J = draw_figure(cr, jx, gy, jp, s=1.1, face=1, prop="robe", color=col)
                if 7.2 <= t < 8.6:
                    hx = (J["rhand"][0] + J["lhand"][0]) / 2; hy = (J["rhand"][1] + J["lhand"][1]) / 2
                    if fade < 0.5: loaf(cr, hx, hy - 8)
                elif t >= 8.6 and fade < 0.6:
                    sp = prog(t, 8.6, 9.0) * 12
                    bread_half(cr, J["rhand"][0] + 4 + sp * 0.3, J["rhand"][1] - 8, face=-1)
                    if t < 9.3:
                        bread_half(cr, J["lhand"][0] - sp, J["lhand"][1] - 8, face=1)
            if t < 7.2:
                loaf(cr, 560, gy - 67)
            if t >= 9.3:   # the second half reaches the disciple
                u = prog(t, 9.3, 9.6)
                hx, hy = DJ[0]["rhand"]
                if i == 2 and t >= 11.0:
                    bread_half(cr, 600, gy - 66, face=-1)   # left on the table
                elif u > 0:
                    bread_half(cr, hx - 6, hy - 8, face=1)
            if i == 2 and t >= 11.0:
                bread_half(cr, 575, gy - 66, face=1)
            darkness(cr, y0, PANEL_H, 0.55 * prog(t, 4.0, 6.5), [(lp[0], lp[1], 420, lit)])

OUTPUT_NAME = "day22a_road_to_emmaus_luke24"
