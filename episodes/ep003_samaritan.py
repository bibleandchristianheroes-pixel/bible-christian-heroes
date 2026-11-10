import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class Samaritan(Episode):
    dur = 18.0
    kicker = "LUKE 10  •  THE GOOD SAMARITAN"
    headline = "Three people saw him.\nOnly one stopped."
    captions = [
        (cpdv("Luke", 10, 31, "…a certain priest was descending along the same way. And seeing him, he passed by."), "Luke 10:31", 6.0),
        (cpdv("Luke", 10, 32, "And similarly a Levite…also saw him, and he passed by."), "Luke 10:32", 6.8),
        (cpdv("Luke", 10, 33, "But a certain Samaritan…seeing him, he was moved by mercy."), "Luke 10:33", 7.6),
    ]
    VX = 600  # victim's feet

    def draw_panel(self, cr, i, t, y0, gy):
        rock_path_tufts(cr, gy, [160, 330, 880, 990])
        # the wounded man (lying, head to the left), later helped up in panel 3
        rise = prog(t, 9.0, 10.6) if i == 2 else 0.0
        lie = pose("lie")
        if i == 2:
            if t < 9.0:
                draw_rotated(cr, self.VX, gy, -90, lie, lift=9)
            elif t < 9.8:
                u = prog(t, 9.0, 9.8)
                cr.push_group(); draw_rotated(cr, self.VX, gy, -90, lie, lift=9)
                cr.pop_group_to_source(); cr.paint_with_alpha(1 - u)
                cr.push_group(); draw_figure(cr, 540, gy, pose("sad_sit", head=10, lean=15))
                cr.pop_group_to_source(); cr.paint_with_alpha(u)
            else:
                hx, wa, d = track(t, [(10.6, 540), (12.2, 540), (16.8, 1180)])
                p = keyed([(9.8, pose("sad_sit", head=10, lean=15)), (10.8, pose("stand", head=15, lean=6))], t)
                draw_figure(cr, hx, gy, body(t, p, wa * 0.7, speed=1.2))
            if t < 9.4 and t > 7.0:  # bandage
                cr.set_source_rgba(*BG, 1 - prog(t, 9.0, 9.4)); cr.set_line_width(4)
                a = prog(t, 7.0, 8.4)
                cr.move_to(self.VX - 70, gy - 17); cr.line_to(self.VX - 70 + 26 * a, gy - 17); cr.stroke()
        else:
            twitch = 3 * math.sin(t * 1.3) if t > 4 else 0
            draw_rotated(cr, self.VX, gy, -90, pose("lie", ls=170 + twitch), lift=9)
        if i == 0:   # priest: slows, looks, walks on past
            x, wa, d = track(t, [(0.4, -70), (3.6, self.VX - 230), (5.0, self.VX - 200), (9.5, 1200)])
            look = keyed([(3.4, {"h": 0}), (4.0, {"h": 28}), (5.0, {"h": 28}), (5.6, {"h": -10})], t)["h"]
            draw_figure(cr, x, gy, body(t, pose("stand", head=look), wa), s=1.05, prop="robe_hat")
        elif i == 1:  # Levite: glances, hurries past
            x, wa, d = track(t, [(0.4, -70), (3.6, self.VX - 230), (4.6, self.VX - 220), (8.0, 1200)])
            look = keyed([(3.4, {"h": 0}), (4.0, {"h": 25}), (4.6, {"h": -25})], t)["h"]
            draw_figure(cr, x, gy, body(t, pose("stand", head=look, lean=8), wa, speed=2.2), s=1.05, prop="robe")
        else:          # Samaritan: stops, kneels, tends, lifts, walks with him
            x, wa, d = track(t, [(0.4, -70), (3.6, self.VX - 230), (4.4, self.VX - 220), (5.4, self.VX - 120),
                                 (10.6, self.VX - 120), (12.2, self.VX - 120), (16.8, 1100)])
            tend = 0.5 + 0.5 * math.sin(t * 6)
            keys = [(4.4, pose("stand", head=28)), (5.4, pose("look", head=25)), (6.2, pose("kneel")),
                    (6.6, pose("kneel", rs=75, re=20 + 25 * tend)), (8.4, pose("kneel", rs=70, re=30)),
                    (9.0, pose("kneel")), (10.0, pose("stand", head=10)), (11.6, pose("stand")),
                    (12.2, pose("stand", rs=60, re=60))]
            p = keyed(keys, t)
            if 6.6 <= t <= 8.4: p = pose("kneel", rs=75, re=20 + 25 * tend)
            draw_figure(cr, x, gy, body(t, p, wa if t < 5.5 or t > 12.2 else 0, speed=1.2), s=1.05)

OUTPUT_NAME = "day003_good_samaritan_luke10"
