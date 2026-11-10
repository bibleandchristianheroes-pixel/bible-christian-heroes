import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class Talents(Episode):
    dur = 18.0
    kicker = "MATTHEW 25  •  THE TALENTS"
    headline = "Same master. Three servants.\nWhat are you doing with yours?"
    captions = [
        (cpdv("Matthew", 25, 20, "…Behold, I have increased it by another five."), "Matthew 25:20", 12.2),
        (cpdv("Matthew", 25, 22, "…Behold, I have gained another two."), "Matthew 25:22", 12.8),
        (cpdv("Matthew", 25, 25, "And so, being afraid, I went out and hid your talent in the earth."), "Matthew 25:25", 13.4),
    ]
    SX = 230; PILE = 300

    def draw_panel(self, cr, i, t, y0, gy):
        given = [5, 2, 1][i]
        # master: stands right, hands over coins, leaves, returns
        mx, wa, d = track(t, [(0, 860), (3.0, 860), (4.6, 1200), (9.6, 1200), (11.2, 640)])
        mface = -1 if (t < 3.0 or t > 9.6) else 1
        mp = keyed([(0.6, pose("stand")), (1.0, pose("reach")), (2.6, pose("reach")), (3.0, pose("stand")),
                    (11.2, pose("stand")), (11.8, pose("stand", rs=120, re=10) if i < 2 else pose("stand", head=10))], t)
        draw_figure(cr, mx, gy, body(t, mp, wa), s=1.1, face=mface, prop="robe")
        # coins flying from master to pile
        for k in range(given):
            t0 = 1.0 + k * 0.3; t1 = t0 + 0.6
            if t0 <= t < t1:
                u = (t - t0) / 0.6
                coin(cr, lerp(800, self.PILE + 20, u), lerp(gy - 120, gy - 20, u) - 90 * 4 * u * (1 - u))
        n = sum(1 for k in range(given) if t >= 1.6 + k * 0.3)
        sp = pose("stand")
        if i < 2:   # trades: coins multiply
            gained = given * prog(t, 5.0, 9.0)
            tot = n + (gained if t >= 5.0 else 0)
            coin_stack(cr, self.PILE, gy, tot)
            work = 0.5 + 0.5 * math.sin(t * 7)
            sp = keyed([(2.0, pose("stand")), (4.6, pose("look", head=20)), (5.0, pose("kneel", rs=70, re=30)),
                        (9.0, pose("kneel", rs=70, re=30)), (9.6, pose("stand")), (11.6, pose("stand")), (12.2, pose("joy"))], t)
            if 5.0 <= t <= 9.0: sp = pose("kneel", rs=60 + 30 * work, re=20)
            sx = self.SX
        else:       # digs a hole and hides it
            dig = 0.5 + 0.5 * math.sin(t * 8)
            if t < 5.0:
                coin_stack(cr, self.PILE, gy, n)
            sx, wa2, _ = track(t, [(4.4, self.SX), (5.2, self.SX + 180)])
            hx = self.SX + 270
            if 5.4 <= t < 9.0:   # hole / mound
                h = prog(t, 5.6, 7.0)
                cr.set_source_rgb(*BG); cr.rectangle(hx - 26 * h, gy - 2, 52 * h, 26); cr.fill()
                cr.set_source_rgb(*INK); cr.set_line_width(3)
                cr.arc(hx - 50, gy, 18 * h, math.pi, 2 * math.pi); cr.fill()
            if t >= 7.2:
                c = prog(t, 7.2, 7.6)
                if t < 8.2: coin(cr, hx, lerp(gy - 60, gy + 12, c))
            if t >= 8.2:
                cr.set_source_rgb(*INK); m = prog(t, 8.2, 9.0)
                cr.save(); cr.translate(hx, gy); cr.scale(34, 14 * m + 0.01); cr.arc(0, 0, 1, math.pi, 2 * math.pi); cr.restore(); cr.fill()
            if 5.4 <= t <= 9.0: sp = pose("kneel", rs=60 + 50 * dig, re=30)
            else:
                sp = keyed([(2.0, pose("stand")), (4.4, pose("look", head=-10)), (9.0, pose("kneel")), (9.8, pose("stand", head=15)),
                            (11.8, pose("stand", head=15)), (12.8, pose("sad_sit"))], t)
            sp = body(t, sp, wa2)
        draw_figure(cr, sx, gy, sp, s=1.0)

OUTPUT_NAME = "day004_talents_matthew25"
