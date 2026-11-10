import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class FaithWorks(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JAMES 2  •  FAITH AND WORKS"
    headline = "Same cold night.\nThree ways to walk by."
    captions = [
        (cpdv("James", 2, 15, "So if a brother or sister is naked and daily in need of food,"), "James 2:15", 4.4),
        (cpdv("James", 2, 16, "…“Go in peace, keep warm and nourished,” and yet not give them the things that are necessary…"), "James 2:16", 7.6),
        (cpdv("James", 2, 17, "Thus even faith, if it does not have works, is dead…"), "James 2:17", 11.4),
    ]
    MX = 620

    def draw_panel(self, cr, i, t, y0, gy):
        snow(cr, y0, PANEL_H, t, seed=3 + i)
        warm = prog(t, 9.2, 10.4) if i == 2 else 0
        shiver = 2.5 * math.sin(t * 30) * (1 - warm)
        mp = pose("sad_sit", head=25 - 30 * prog(t, 10.4, 11.2) * (i == 2))
        if i == 2 and t > 11.4:
            mp = keyed([(11.4, pose("sad_sit", head=-5)), (12.4, pose("stand", head=-8))], t)
        draw_figure(cr, self.MX + shiver, gy, mp, s=1.0, face=-1, prop="robe" if warm > 0.5 else None)
        if i == 0:
            x, wa, _ = track(t, [(0.6, -80), (9.0, 1200)])
            draw_figure(cr, x, gy, body(t, pose("stand", head=-10), wa), s=1.05, prop="robe")
        elif i == 1:
            x, wa, _ = track(t, [(0.6, -80), (4.6, self.MX - 120), (8.6, self.MX - 120), (13.0, 1200)])
            p = keyed([(4.6, pose("stand", head=15)), (5.4, pose("stand", head=15, rs=135, re=-10)), (7.8, pose("stand", head=15, rs=135, re=-10)), (8.6, pose("stand", head=-5))], t)
            draw_figure(cr, x, gy, body(t, p, wa), s=1.05, prop="robe")
        else:
            x, wa, _ = track(t, [(0.6, -80), (4.6, self.MX - 120), (12.6, self.MX - 120)])
            coat_on = t < 8.4
            p = keyed([(4.6, pose("stand", head=15)), (6.0, pose("kneel", head=20)), (8.4, pose("kneel", rs=80, re=0, head=20)), (9.4, pose("kneel", rs=80, re=0)), (10.4, pose("kneel", rs=60, re=20)), (12.4, pose("stand", rs=40, re=40))], t)
            J = draw_figure(cr, x, gy, body(t, p, wa), s=1.05, prop="robe" if coat_on else None)
            if 8.4 <= t < 9.4:  # coat passing over
                u = prog(t, 8.4, 9.4)
                cr.set_source_rgb(*INK); cx = lerp(x + 20, self.MX - 10, u)
                cr.move_to(cx - 18, gy - 90); cr.line_to(cx + 18, gy - 90); cr.line_to(cx + 26, gy - 30); cr.line_to(cx - 26, gy - 30); cr.close_path(); cr.fill()
            if 9.6 <= t < 10.8:
                loaf(cr, lerp(J["rhand"][0], self.MX - 20, prog(t, 9.6, 10.4)), J["rhand"][1])
            if t > 9.8:
                g = cairo.RadialGradient(self.MX - 60, gy - 60, 0, self.MX - 60, gy - 60, 240 * warm)
                g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.35 * warm); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
                cr.set_source(g); cr.rectangle(0, y0, W, PANEL_H); cr.fill()

OUTPUT_NAME = "day06b_faith_and_works_james2"
