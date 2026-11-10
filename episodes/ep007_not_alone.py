import math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *
from props import *

class NotAlone(Episode):
    dur = 18.0
    kicker = "ECCLESIASTES 4  •  A THREEFOLD CORD"
    headline = "Nobody was made\nto walk alone."
    captions = [
        (cpdv("Ecclesiastes", 4, 10, "…Woe to one who is alone. For when he falls, he has no one to lift him up."), "Ecclesiastes 4:10", 7.4),
        (cpdv("Ecclesiastes", 4, 9, "…it is better for two to be together, than for one to be alone."), "Ecclesiastes 4:9", 9.0),
        (cpdv("Ecclesiastes", 4, 12, "…a threefold cord is broken with difficulty."), "Ecclesiastes 4:12", 7.8),
    ]
    TRIP = 5.6

    def faller(self, cr, t, x, gy, rescue_at=None):
        """Lead walker who trips at TRIP. Returns nothing; draws the right phase."""
        T = self.TRIP
        if t < T:
            draw_figure(cr, x, gy, walk(t), s=1.0); return
        fall = prog(t, T, T + 0.45)
        if rescue_at is None or t < rescue_at:
            if fall < 1:
                draw_rotated(cr, x, gy, 88 * fall, mix(walk(T), pose("flail", lean=10), fall), lift=9 * fall)
            else:
                push = 0.5 + 0.5 * math.sin((t - T) * 3.0) if t < T + 4 else 0
                draw_rotated(cr, x, gy, 88 - 14 * push * (1 if t < T + 4 else 0), pose("lie", ls=150 - 60 * push, le=20, rs=150 - 60 * push, re=20), lift=9)
            return
        u = prog(t, rescue_at, rescue_at + 0.8)
        cr.push_group(); draw_rotated(cr, x, gy, 88, pose("lie"), lift=9); cr.pop_group_to_source(); cr.paint_with_alpha(1 - u)
        sx = x + 60
        p = keyed([(rescue_at, pose("sad_sit", head=-10, lean=10, rs=120, re=0)), (rescue_at + 0.8, pose("sad_sit", head=-10, lean=10, rs=120, re=0)),
                   (rescue_at + 1.8, pose("stand", head=-5))], t)
        cr.push_group(); draw_figure(cr, sx, gy, p, s=1.0); cr.pop_group_to_source(); cr.paint_with_alpha(u)

    def draw_panel(self, cr, i, t, y0, gy):
        rock_path_tufts(cr, gy, [140, 300, 760, 950])
        cr.set_source_rgb(*INK)  # the stone they trip on
        cr.save(); cr.translate(560, gy); cr.scale(16, 10); cr.arc(0, 0, 1, math.pi, 2 * math.pi); cr.restore(); cr.fill()
        T = self.TRIP
        lead_x = lambda tt: lerp(-60, 520, prog(tt, 0.2, T)) if tt < T else 520
        if i == 0:
            self.faller(cr, t, lead_x(t), gy)
            if t > T + 5.5:  # gives up, sits
                pass
        elif i == 1:
            R = T + 3.0
            if t < R + 1.8:
                self.faller(cr, t, lead_x(t), gy, rescue_at=R)
                fx, fwa, _ = track(t, [(0.2, -150), (T, 430), (T + 1.4, 430), (T + 2.2, 520)])
                fp = keyed([(T, pose("stand", head=20)), (T + 2.2, pose("look", head=30)), (R - 0.4, pose("reach", rs=110, re=0, lean=14, head=25)),
                            (R + 1.6, pose("stand", rs=80, re=40))], t)
                draw_figure(cr, fx, gy, body(t, fp, fwa), s=1.0)
            else:
                for k, x0 in enumerate((580, 520)):
                    x, wa, _ = track(t, [(R + 1.8, x0), (17.0, x0 + 620)])
                    draw_figure(cr, x, gy, body(t, pose("stand", head=-6 if k == 0 else 0), wa), s=1.0)
        else:
            # three walkers joined by one cord
            xs = []
            for k in range(3):
                x, wa, _ = track(t, [(0.2, -60 - k * 95), (T, 520 - k * 95), (T + 1.4, 520 - k * 95), (17.0, 1240 - k * 95)])
                xs.append((x, wa))
            stumble = prog(t, T, T + 0.35) * (1 - prog(t, T + 0.5, T + 1.3))
            hold = stumble
            Js = []
            for k, (x, wa) in enumerate(xs):
                if k == 0:
                    p = body(t, pose("flail", lean=10), 0) if 0.05 < stumble else body(t, pose("stand"), wa)
                    J = draw_rotated(cr, x, gy, 38 * stumble, p if stumble > 0.05 else body(t, pose("stand"), wa))
                    J = {kk: (x + (vv[0]) * math.cos(math.radians(38 * stumble)) - vv[1] * math.sin(math.radians(38 * stumble)),
                              gy + vv[0] * math.sin(math.radians(38 * stumble)) + vv[1] * math.cos(math.radians(38 * stumble))) for kk, vv in J.items()}
                else:
                    p = mix(body(t, pose("stand", rs=35, re=25, ls=35, le=25), wa), pose("stand", lean=-16, rs=60, re=0, ls=55, le=0, lt=-14, rt=-24, lk=10, rk=10), hold)
                    J = draw_figure(cr, x, gy, p, s=1.0)
                Js.append(J)
            # the cord: three strands hip to hip
            cr.set_line_width(2.4); cr.set_source_rgb(*INK)
            for a, b in ((Js[2], Js[1]), (Js[1], Js[0])):
                (x1, y1), (x2, y2) = a["rhand"], b["hip"]
                for off in (-3, 0, 3):
                    mx_ = (x1 + x2) / 2; my_ = (y1 + y2) / 2 + 14 * (1 - hold) + off
                    cr.move_to(x1, y1 + off); cr.curve_to(mx_, my_, mx_, my_, x2, y2 - 20 + off); cr.stroke()

OUTPUT_NAME = "day07a_threefold_cord_ecclesiastes4"
