import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class RunTheRace(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "HEBREWS 12  •  RUN THE RACE"
    headline = "Same race.\nWhat are you still carrying?"
    captions = [
        (cpdv("Hebrews", 12, 3, "…so that you may not become weary, failing in your souls."), "Hebrews 12:3", 8.6),
        (cpdv("Hebrews", 12, 1, "…let us set aside every burden and sin which may surround us…"), "Hebrews 12:1", 5.0),
        (cpdv("Hebrews", 12, 2, "Let us gaze upon Jesus, as the Author and the completion of our faith…"), "Hebrews 12:2", 9.6),
    ]
    FIN = 930

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 2:
            cross(cr, 1035, gy, glow=0.5 + 0.5 * prog(t, 6.0, 9.0))
        finish_line(cr, self.FIN, gy)
        if i == 0:   # keeps every burden: slows, stops, falls to his knees
            x, wa, _ = track(t, [(0.3, -60), (3.0, 200), (6.0, 380), (7.4, 430)])
            sp = max(0.25, 1 - prog(t, 3.0, 7.4))
            if t < 7.4:
                p = mix(walk(t, speed=1.2), run(t), sp)
                p["lean"] = 14 + 16 * (1 - sp); p["head"] = 10 + 20 * (1 - sp)
            else:
                p = keyed([(7.4, pose("stand", lean=30, head=30)), (8.2, pose("kneel", lean=40, head=45, rs=60, re=0, ls=50, le=0))], t)
            J = draw_figure(cr, x, gy, p, s=1.0)
            bx, by = J["sh"]
            for k in range(3):
                burden(cr, bx - 44 - k * 6, by - 18 + k * 26, 38, 30)
        else:
            drop_t = [3.6, 4.2, 4.8]
            x, wa, _ = track(t, [(0.3, -60), (3.6, 260), (5.0, 360), (11.6 if i == 1 else 10.4, self.FIN + 30)])
            moving = wa > 0.1
            p = run(t, speed=2.4 if t > 5.0 else 1.6) if moving else pose("stand")
            if not moving and t > 10:
                p = keyed([(10.4 if i == 2 else 11.6, pose("stand")), (11.2 if i == 2 else 12.4, pose("joy"))], t)
            if i == 2 and moving and t > 6.0:
                p["head"] = -18
            J = draw_figure(cr, x, gy, p, s=1.0)
            bx, by = J["sh"]
            for k, td in enumerate(drop_t):
                if t < td:
                    burden(cr, bx - 44 - k * 6, by - 18 + k * 26, 38, 30)
                else:
                    u = prog(t, td, td + 0.35)
                    dx = 300 + 100 * (td - 3.6)  # where it fell (x at drop time)
                    burden(cr, dx - 50 - k * 12, lerp(by - 18 + k * 26, gy - 30, u), 38, 30)

OUTPUT_NAME = "day07b_run_the_race_hebrews12"
