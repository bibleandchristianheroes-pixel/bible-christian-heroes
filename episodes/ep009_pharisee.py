import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class Pharisee(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 18  •  THE PHARISEE AND THE TAX COLLECTOR"
    headline = "Two men prayed.\nOnly one went home justified."
    captions = [
        (cpdv("Luke", 18, 11, "…O God, I give thanks to you that I am not like the rest of men…"), "Luke 18:11", 4.4),
        (cpdv("Luke", 18, 13, "…he struck his chest, saying: ‘O God, be merciful to me, a sinner.’"), "Luke 18:13", 6.4),
        (cpdv("Luke", 18, 14, "…this one descended to his house justified, but not the other."), "Luke 18:14", 11.0),
    ]
    TX = 620

    def draw_panel(self, cr, i, t, y0, gy):
        temple(cr, self.TX, gy)
        # Pharisee: strides to the front of the temple, chest out, arms raised
        px, pwa, _ = track(t, [(0.3, -60), (3.0, 560)])
        pp = keyed([(3.0, pose("stand", head=-15, lean=-8)), (3.6, pose("joy", lean=-12, head=-25)),
                    (6.0, pose("joy", lean=-12, head=-25)), (6.6, pose("stand", lean=-10, head=-20, rs=-20, re=90, ls=-20, le=90))], t)
        pc = SOFT if i == 1 else INK
        pa = 1.0
        if i == 2: pa = 1 - 0.65 * prog(t, 10.4, 11.6)
        cr.push_group(); draw_figure(cr, px, gy, body(t, pp, pwa), s=1.05, color=pc, prop="robe")
        cr.pop_group_to_source(); cr.paint_with_alpha(pa)
        # Tax collector: stays far back, head down, strikes his chest
        if i == 2 and t > 10.0:
            beam = prog(t, 9.4, 10.4)
        else:
            beam = prog(t, 9.4, 10.4) if i == 2 else 0
        if beam > 0:
            g = cairo.LinearGradient(0, y0, 0, gy)
            g.add_color_stop_rgba(0, 1, 0.9, 0.55, 0.0); g.add_color_stop_rgba(1, 1, 0.9, 0.55, 0.45 * beam)
            cr.set_source(g); cr.move_to(150, y0); cr.line_to(250, y0); cr.line_to(290, gy); cr.line_to(110, gy); cr.close_path(); cr.fill()
        tx, twa, td = track(t, [(0.6, -80), (3.6, 200), (11.6, 200), (17.0, -140)])
        beat = abs(math.sin(t * 3.2))
        tp = keyed([(3.6, pose("stand", head=35, lean=10)), (4.2, pose("stand", head=40, lean=12))], t)
        if 4.2 <= t < 10.0:
            tp = pose("stand", head=40, lean=12, rs=55 + 25 * beat, re=130)
        elif t >= 10.0 and i == 2:
            tp = keyed([(10.0, pose("stand", head=40, lean=12, rs=55, re=130)), (11.0, pose("stand", head=-5)), (11.6, pose("stand", head=-8))], t)
        tc = SOFT if i == 0 else INK
        face = -1 if (i == 2 and t > 11.6) else 1
        draw_figure(cr, tx, gy, body(t, tp, twa if (i == 2 or t < 4) else 0), s=1.0, color=tc, face=face)

OUTPUT_NAME = "day02b_pharisee_and_tax_collector_luke18"
