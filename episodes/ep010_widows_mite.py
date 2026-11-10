import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class WidowsMite(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "MARK 12  •  THE WIDOW'S OFFERING"
    headline = "The smallest gift\nweighed the most."
    captions = [
        (cpdv("Mark", 12, 41, "…many of the wealthy cast in a great deal."), "Mark 12:41", 3.8),
        (cpdv("Mark", 12, 42, "But when one poor widow had arrived, she put in two small coins…"), "Mark 12:42", 8.6),
        (cpdv("Mark", 12, 44, "…she gave from her scarcity, even all that she had, her entire living."), "Mark 12:44", 11.0),
    ]
    BX = 600

    def draw_panel(self, cr, i, t, y0, gy):
        glow = prog(t, 9.6, 12.0) if i == 2 else 0.0
        offertory_box(cr, self.BX, gy, glow)
        # two wealthy men pour in heavy bags (all panels)
        for k, (t0, sx) in enumerate(((0.3, -80), (1.0, -170))):
            stop = self.BX - 95 - k * 70
            x, wa, _ = track(t, [(t0, sx), (t0 + 2.0, stop), (t0 + 3.6, stop), (t0 + 6.2, 1250)])
            pour = prog(t, t0 + 2.2, t0 + 2.8) * (1 - prog(t, t0 + 3.4, t0 + 3.6))
            p = mix(pose("stand", lean=-6, head=-12), pose("stand", rs=110, re=-10, lean=-8, head=-15), pour)
            if t > t0 + 3.6 and k == 0:
                p = pose("stand", lean=-8, head=-15)
            col = SOFT if i == 2 and t > 10 else INK
            J = draw_figure(cr, x, gy, body(t, p, wa), s=1.08, color=col, prop="robe")
            if t < t0 + 3.6:
                hx, hy = J["rhand"]
                cr.set_source_rgb(*col); cr.save(); cr.translate(hx + 6, hy + 10); cr.scale(16, 19); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
            if 0 < pour and t < t0 + 3.6:
                rnd = random.Random(k)
                for c in range(9):
                    u = ((t - t0 - 2.3) * 2.2 + c / 9) % 1
                    coin(cr, lerp(J["rhand"][0] + 10, self.BX, u) + rnd.uniform(-8, 8), lerp(J["rhand"][1] + 20, gy - 100, u), r=6)
        # the widow (panels 2 and 3), bent, slow
        if i >= 1:
            x, wa, _ = track(t, [(5.0, -60), (7.4, self.BX - 80), (13.0, self.BX - 80)])
            drop = prog(t, 7.6, 8.1) * (1 - prog(t, 8.5, 8.9))
            p = mix(pose("stand", lean=16, head=20), pose("stand", lean=18, head=28, rs=85, re=-5), drop)
            if i == 2 and t > 11.6:
                p = keyed([(11.6, pose("stand", lean=16, head=20)), (12.6, pose("stand", lean=6, head=-12))], t)
            J = draw_figure(cr, x, gy, body(t, p, wa, speed=1.1), s=0.95, prop="robe")
            if t < 8.3:
                coin(cr, J["rhand"][0] + 4, J["rhand"][1] + 4, r=5); coin(cr, J["rhand"][0] + 12, J["rhand"][1] + 6, r=5)
            elif t < 8.8:
                u = prog(t, 8.3, 8.8)
                for d in (0, 8):
                    coin(cr, lerp(J["rhand"][0] + 4 + d, self.BX + d - 4, u), lerp(J["rhand"][1] + 4, gy - 100, u), r=5)

OUTPUT_NAME = "day03b_widows_offering_mark12"
