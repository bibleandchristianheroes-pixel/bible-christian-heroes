import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class Knock(Episode):
    dur = 18.0
    kicker = "LUKE 11  •  KEEP KNOCKING"
    headline = "Most people stop\none knock too soon."
    captions = [
        (cpdv("Luke", 18, 1, "…we should continually pray and not cease…"), "Luke 18:1", 6.4),
        (cpdv("Luke", 11, 9, "Knock, and it shall be opened to you."), "Luke 11:9", 9.6),
        (cpdv("Luke", 11, 10, "…whoever knocks, it shall be opened to him."), "Luke 11:10", 11.6),
    ]
    HX = 720  # house left edge

    def knock_pose(self, t, starts):
        for s0 in starts:
            if s0 <= t < s0 + 1.3:
                ph = (t - s0) / 1.3 * 3  # three taps
                u = abs(math.sin(ph * math.pi))
                return mix(pose("knock_up", head=-4), pose("knock_hit", head=-4), u), True
        return None, False

    def draw_panel(self, cr, i, t, y0, gy):
        door_open = prog(t, 11.0, 12.0) if i == 2 else 0.0
        light = prog(t, 11.0, 12.4) if i == 2 else 0.0
        house(cr, self.HX, gy, door_open=door_open, light=light)
        knocks = [[2.3], [2.3, 5.4], [2.3, 5.4, 8.5]][i]
        stand_x = self.HX + 8
        if i == 0:
            x, wa, d = track(t, [(0.3, -60), (2.1, stand_x), (5.9, stand_x), (9.6, -90)])
        elif i == 1:
            x, wa, d = track(t, [(0.3, -60), (2.1, stand_x), (8.2, stand_x), (9.0, stand_x - 70)])
        else:
            x, wa, d = track(t, [(0.3, -60), (2.1, stand_x), (13.6, stand_x), (15.4, self.HX + 76)])
        face = 1 if (i != 0 or t < 5.9) else -1
        if i == 1 and 8.2 <= t < 9.0: face = -1
        kp, knocking = self.knock_pose(t, knocks)
        if knocking:
            p = kp
        elif i == 0:
            p = body(t, keyed([(2.1, pose("stand")), (4.0, pose("look", head=-6)), (5.6, pose("stand", head=30, lean=4))], t), wa)
        elif i == 1:
            if t < 9.0:
                p = body(t, keyed([(2.1, pose("stand")), (4.2, pose("look", head=-6)), (7.4, pose("look", head=-6)), (8.0, pose("stand", head=25))], t), wa)
            else:
                p = keyed([(9.0, pose("stand", head=25)), (9.8, pose("sad_sit"))], t)
                face = 1
        else:
            p = keyed([(2.1, pose("stand")), (4.2, pose("look", head=-6)), (10.0, pose("look")), (11.8, pose("look", head=-10)), (12.6, pose("joy")), (13.5, pose("stand"))], t)
            p = body(t, p, wa)
        alpha_fig = 1.0
        if i == 2 and t > 14.6:  # walks into the light
            alpha_fig = 1 - prog(t, 14.6, 15.4)
        if alpha_fig > 0:
            cr.push_group()
            draw_figure(cr, x, gy, p, s=1.05, face=face)
            cr.pop_group_to_source(); cr.paint_with_alpha(alpha_fig)
        # knock marks
        for s0 in knocks:
            if s0 <= t < s0 + 1.6:
                for k in range(3):
                    tk = s0 + (k + 0.5) * 1.3 / 3
                    if tk <= t < tk + 0.4:
                        a = 1 - (t - tk) / 0.4
                        cr.set_source_rgba(*INK, a); cr.set_line_width(3)
                        for ang in (-0.6, 0, 0.6):
                            cr.move_to(self.HX + 30 + 14 * math.cos(ang) * -1, gy - 110 + 14 * math.sin(ang))
                            cr.line_to(self.HX + 30 - 30 * math.cos(ang), gy - 110 + 30 * math.sin(ang)); cr.stroke()

OUTPUT_NAME = "day02a_keep_knocking_luke11"
