import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class TenVirgins(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MATTHEW 25  •  THE TEN VIRGINS"
    headline = "Same night. Same wait.\nOnly one was ready."
    captions = [
        (cpdv("Matthew", 25, 3, "For the five foolish, having brought their lamps, did not take oil with them."), "Matthew 25:3", 8.2),
        (cpdv("Matthew", 25, 4, "Yet truly, the prudent ones brought the oil, in their containers, with the lamps."), "Matthew 25:4", 8.6),
        (cpdv("Matthew", 25, 10, "…those who were prepared entered with him to the wedding, and the door was closed."), "Matthew 25:10", 12.4),
    ]
    HX = 640

    def draw_panel(self, cr, i, t, y0, gy):
        night = prog(t, 0.4, 2.4)
        if i == 0:
            door = prog(t, 10.4, 11.0) * (1 - prog(t, 11.8, 12.4))
        elif i == 1:
            door = 0.0
        else:
            door = prog(t, 10.6, 11.4) * (1 - prog(t, 14.6, 15.4))
        house(cr, self.HX, gy, door_open=door, light=door)
        # brightness of her lamp
        dim = prog(t, 4.5, 7.6)
        if i == 0:
            bright = 1 - dim * (1 if t < 8.0 else 1) ; bright = 0 if t > 8.0 else max(0.08, bright)
        else:
            bright = max(0.25, 1 - dim) if t < 8.0 else lerp(0.25, 1, prog(t, 8.0, 8.8))
        x, wa, d = track(t, [(0, 430), (11.6, 430), (13.6, self.HX + 76)] if i == 2 else [(0, 430), (13.0, 430), (14.2, 600)] if i == 0 else [(0, 430)])
        if i == 2:
            p = keyed([(0, pose("sad_sit", head=0, lean=12, rs=75, re=0)), (11.0, pose("sad_sit", head=-10, lean=12, rs=75, re=0)), (11.6, pose("stand", rs=60, re=10))], t)
        elif i == 0:
            p = keyed([(0, pose("sad_sit", head=0, lean=12, rs=75, re=0)), (8.6, pose("sad_sit", head=30, lean=20, rs=75, re=0)), (11.0, pose("sad_sit", head=-10, lean=12, rs=75, re=0)), (12.4, pose("sad_sit", head=-10, lean=12, rs=75, re=0)), (13.0, pose("stand", rs=60, re=10)), (14.2, pose("knock_up")), (14.8, pose("knock_hit")), (15.4, pose("knock_up")), (16.0, pose("stand", head=25))], t)
        else:
            p = keyed([(0, pose("sad_sit", head=0, lean=12, rs=75, re=0)), (7.4, pose("sad_sit", head=0, lean=12, rs=75, re=0)), (8.0, pose("sad_sit", head=15, lean=14, rs=75, re=0, ls=70, le=10))], t)
        alpha = 1 - prog(t, 13.2, 13.8) if i == 2 else 1
        cr.push_group()
        J = draw_figure(cr, x, gy, body(t, p, wa), s=0.98, prop="robe")
        fx, fy = lamp(cr, J["rhand"][0] + 8, J["rhand"][1] + 4, bright if t > 0.3 else 0, t)
        if i >= 1 and 7.4 < t < 8.9:
            flask(cr, J["lhand"][0] + 6, J["lhand"][1] - 6)
        cr.pop_group_to_source(); cr.paint_with_alpha(alpha)
        lights = [(fx, fy, 230 * bright * alpha, 1.0)]
        if door > 0: lights.append((self.HX + 76, gy - 75, 330 * door, 1.0))
        darkness(cr, y0, PANEL_H, night, lights)

OUTPUT_NAME = "day01b_ten_virgins_matthew25"
