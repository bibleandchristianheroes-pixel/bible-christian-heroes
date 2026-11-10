import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class Peter(Episode):
    dur = 18.0
    ground = False
    kicker = "MATTHEW 14  •  PETER ON THE WATER"
    headline = "He only started sinking\nwhen he looked away."
    captions = [
        (cpdv("Matthew", 14, 29, "…Peter, descending from the boat, walked over the water, so as to go to Jesus."), "Matthew 14:29", 4.2),
        (cpdv("Matthew", 14, 30, "…seeing that the wind was strong, he was afraid. And as he began to sink, he cried out…"), "Matthew 14:30", 6.6),
        (cpdv("Matthew", 14, 31, "And immediately Jesus extended his hand and took hold of him."), "Matthew 14:31", 9.0),
    ]
    BX = 190

    def draw_panel(self, cr, i, t, y0, gy):
        gy = gy - 10
        windy = 0.0 if i == 0 else prog(t, 4.8, 5.8) * (1 - (prog(t, 10.2, 11.5) if i == 2 else 0))
        rough = 1 + 1.6 * windy
        wind(cr, y0, t, windy)
        # Jesus
        if i == 2:
            jx, jwa, _ = track(t, [(6.6, 860), (8.4, 640)])
        else:
            jx, jwa = 860, 0
        jp = keyed([(0.6, pose("stand")), (1.2, pose("reach", lean=4)), (2.6, pose("reach", lean=4)), (3.4, pose("stand", rs=60, re=10))], t)
        if i == 2:
            jp = keyed([(3.4, pose("stand", rs=60, re=10)), (6.6, pose("stand")), (8.4, pose("reach", rs=95, re=-10)), (10.2, pose("reach", rs=95, re=-10)), (11.0, pose("stand", rs=40, re=40))], t)
        if i == 0:
            jp = keyed([(0.6, pose("stand")), (1.2, pose("reach", lean=4)), (2.6, pose("reach", lean=4)), (3.4, pose("stand", rs=70, re=10)), (7.6, pose("stand", rs=70, re=10)), (8.4, pose("stand", rs=90, re=60, ls=80, le=60))], t)
        draw_figure(cr, jx, surface_y(jx, gy, t, rough=rough) + 2, body(t, jp, jwa, speed=1.2), s=1.08, face=-1, prop="robe")
        # Peter
        out = prog(t, 1.6, 2.6)
        if i == 0:
            px, pwa, _ = track(t, [(1.6, self.BX + 30), (2.6, self.BX + 150), (7.6, 770)])
            sink = 0
        else:
            px, pwa, _ = track(t, [(1.6, self.BX + 30), (2.6, self.BX + 150), (5.6, 530)])
            sink = 130 * prog(t, 6.0, 9.2) if i == 1 else 85 * prog(t, 6.0, 8.6) * (1 - prog(t, 8.9, 10.0))
        base_y = lerp(gy - 8, surface_y(px, gy, t, rough=rough) + 2, out) + sink
        pp = pose("stand")
        if i == 0:
            pp = keyed([(1.6, pose("stand")), (7.6, pose("stand", head=-10)), (8.4, pose("joy"))], t)
        else:
            look = keyed([(4.8, {"h": -6}), (5.6, {"h": 45})], t)["h"]
            pp = keyed([(5.6, pose("stand", head=look)), (6.4, pose("flail")), (9.0, pose("flail"))], t)
            if t < 5.6: pp = pose("stand", head=look)
            if i == 2:
                pp = keyed([(5.6, pose("stand", head=look)), (6.4, pose("flail")), (8.4, pose("flail")), (9.2, pose("reach", rs=150, re=-5, head=-25)),
                            (10.6, pose("stand", head=-10)), (11.6, pose("stand", head=-12))], t) if t >= 5.6 else pose("stand", head=look)
        draw_figure(cr, px, base_y, body(t, pp, pwa), s=1.0)
        boat(cr, self.BX, gy - 26, bob=3 * math.sin(t * 2.2) * rough)
        water(cr, gy, t, rough=rough, below=220)
        if i == 1 and t > 6.6:  # cry
            a = prog(t, 6.6, 7.0) * (0.6 + 0.4 * math.sin(t * 9))
            cr.set_source_rgba(*INK, a); cr.set_line_width(3)
            hy = base_y - 175
            for ang in (-0.9, -0.3, 0.3):
                cr.move_to(px + 22 * math.cos(ang), hy + 22 * math.sin(ang)); cr.line_to(px + 40 * math.cos(ang), hy + 40 * math.sin(ang)); cr.stroke()

OUTPUT_NAME = "day006_peter_on_the_water_matthew14"
